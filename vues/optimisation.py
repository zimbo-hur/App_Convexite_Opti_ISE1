import streamlit as st
import pandas as pd
import numpy as np
import cvxpy as cp
import plotly.express as px
from pathlib import Path

from theme import carte_metrique, appliquer_theme_plotly, sequence_couleurs, COULEURS

st.title("⚙️ Optimisation de l'allocation des ressources")

st.markdown(
    r"""
    $$
    \max Z = \sum_{l} \text{score}_l \times \sum_{k} \ln(1 + x_{kl})
    $$

    où $\text{score}_l = \left(\dfrac{\text{poids}_l \times \text{non\_consultés}_l
    \times \text{coût}_l \times \text{distance}_l}{\text{qualité}_l}\right)^{1/3}$
    et $x_{kl}$ est la quantité de ressource $k$ allouée au département $l$,
    pour 4 types de ressources : médecins, infirmiers, sages-femmes, lits.
    """
)

# --------------------------------------------------------------------------
# Chargement de la table des facteurs par département (auto, depuis le repo)
# --------------------------------------------------------------------------
fichier = Path(__file__).resolve().parent.parent / "data" / "table_departements.xlsx"

if not fichier.exists():
    st.error(
        f"Fichier introuvable : `{fichier}`. Génère-le avec "
        "`calculs_table_departements.py` et place-le dans `data/table_departements.xlsx` "
        "à la racine du repo."
    )
    st.stop()

table = pd.read_excel(fichier)
departements = table["departement"].tolist()
scores = table["score"].to_numpy()
n = len(departements)

st.caption(f"📁 {n} départements chargés depuis `data/table_departements.xlsx`.")

with st.expander("🔍 Voir la table des facteurs par département"):
    st.dataframe(table, width="stretch")

st.markdown("---")

# --------------------------------------------------------------------------
# 1. Contrainte budgétaire et disponibilité des ressources
# --------------------------------------------------------------------------
st.subheader("1️⃣ Budget et disponibilité nationale des ressources")

budget_total = st.number_input(
    "Budget total disponible (rémunération médecins/infirmiers/sages-femmes, FCFA)",
    min_value=0, value=5_000_000_000, step=100_000_000, format="%d",
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    dispo_medecins = st.number_input("Médecins disponibles (national)", min_value=0, value=800)
with col2:
    dispo_infirmiers = st.number_input("Infirmiers disponibles (national)", min_value=0, value=3000)
with col3:
    dispo_sagesfemmes = st.number_input("Sages-femmes disponibles (national)", min_value=0, value=1500)
with col4:
    dispo_lits = st.number_input("Lits disponibles (national)", min_value=0, value=10000)

st.markdown("---")

# --------------------------------------------------------------------------
# 2. Coûts unitaires (uniquement médecins/infirmiers/sages-femmes -> budget)
# --------------------------------------------------------------------------
st.subheader("2️⃣ Coûts unitaires (rémunération annuelle, FCFA)")
st.caption("Les lits ne sont pas inclus dans la contrainte budgétaire (coût d'investissement, pas de rémunération).")

c1, c2, c3 = st.columns(3)
with c1:
    prix_medecin = st.number_input("Coût unitaire — médecin", min_value=0, value=6_000_000, step=100_000)
with c2:
    prix_infirmier = st.number_input("Coût unitaire — infirmier", min_value=0, value=2_500_000, step=100_000)
with c3:
    prix_sagefemme = st.number_input("Coût unitaire — sage-femme", min_value=0, value=2_200_000, step=100_000)

st.markdown("---")

# --------------------------------------------------------------------------
# 3. Lancement de l'optimisation
# --------------------------------------------------------------------------
st.subheader("3️⃣ Lancer l'optimisation")

if st.button("🚀 Lancer l'optimisation", type="primary"):
    # x[l, k] : k = 0 médecins, 1 infirmiers, 2 sages-femmes, 3 lits
    x = cp.Variable((n, 4), nonneg=True)

    objectif = cp.Maximize(cp.sum(cp.multiply(scores, cp.sum(cp.log(1 + x), axis=1))))

    dispo = [dispo_medecins, dispo_infirmiers, dispo_sagesfemmes, dispo_lits]
    contraintes = [cp.sum(x[:, k]) <= dispo[k] for k in range(4)]

    prix = np.array([prix_medecin, prix_infirmier, prix_sagefemme])
    contraintes.append(cp.sum(cp.multiply(x[:, :3], prix)) <= budget_total)

    probleme = cp.Problem(objectif, contraintes)

    with st.spinner("Résolution du problème d'optimisation..."):
        try:
            probleme.solve()
        except cp.error.SolverError as e:
            st.error(f"Le solveur a échoué : {e}")
            st.stop()

    if probleme.status not in ("optimal", "optimal_inaccurate"):
        st.error(
            f"Le problème est **{probleme.status}** — vérifie que le budget et les "
            "disponibilités sont cohérents entre eux (souvent : budget trop faible "
            "par rapport aux effectifs disponibles, ou l'inverse)."
        )
        st.stop()

    st.success(f"✅ Optimisation terminée — valeur optimale Z = {probleme.value:,.1f}")

    resultat = pd.DataFrame(
        x.value, columns=["Médecins", "Infirmiers", "Sages-femmes", "Lits"]
    )
    resultat.insert(0, "Département", departements)
    resultat.insert(1, "Score (priorité)", scores)
    for col in ["Médecins", "Infirmiers", "Sages-femmes", "Lits"]:
        resultat[col] = resultat[col].round(1)

    # --- Métriques globales ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        carte_metrique("Médecins alloués", f"{resultat['Médecins'].sum():,.0f}", COULEURS["teal"])
    with m2:
        carte_metrique("Infirmiers alloués", f"{resultat['Infirmiers'].sum():,.0f}", COULEURS["ocre"])
    with m3:
        carte_metrique("Sages-femmes allouées", f"{resultat['Sages-femmes'].sum():,.0f}", COULEURS["sauge"])
    with m4:
        carte_metrique("Lits alloués", f"{resultat['Lits'].sum():,.0f}", COULEURS["brique"])

    budget_utilise = (
        resultat["Médecins"].sum() * prix_medecin
        + resultat["Infirmiers"].sum() * prix_infirmier
        + resultat["Sages-femmes"].sum() * prix_sagefemme
    )
    if budget_total > 0:
        st.caption(f"💰 Budget utilisé : {budget_utilise:,.0f} / {budget_total:,.0f} FCFA "
                   f"({budget_utilise / budget_total * 100:.1f} %)")
    else:
        st.caption(f"💰 Budget utilisé : {budget_utilise:,.0f} FCFA (budget disponible : 0)")

    st.markdown("#### Allocation détaillée par département")
    st.dataframe(
        resultat.sort_values("Score (priorité)", ascending=False),
        width="stretch",
    )

    st.markdown("#### Top 10 départements par ressource allouée")
    top10 = resultat.sort_values("Score (priorité)", ascending=False).head(10)
    top10_long = top10.melt(
        id_vars="Département",
        value_vars=["Médecins", "Infirmiers", "Sages-femmes", "Lits"],
        var_name="Ressource", value_name="Quantité",
    )
    fig = px.bar(top10_long, x="Département", y="Quantité", color="Ressource",
                 barmode="group", title="Allocation optimale — top 10 départements prioritaires")
    fig.update_layout(xaxis_tickangle=-45)
    appliquer_theme_plotly(fig)
    st.plotly_chart(fig, width="stretch")

    st.download_button(
        "📥 Télécharger l'allocation complète (CSV)",
        resultat.to_csv(index=False).encode("utf-8"),
        file_name="allocation_optimale.csv",
        mime="text/csv",
    )
