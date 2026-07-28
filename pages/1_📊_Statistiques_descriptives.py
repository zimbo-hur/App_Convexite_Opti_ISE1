import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Statistiques descriptives", page_icon="📊", layout="wide")

st.title("📊 Statistiques descriptives")
st.caption(
    "Source : EHCVM 2018-2019 (Sénégal). Cette page ne contient aucun chiffre "
    "en dur : elle lit le fichier Excel produit par `calculs_stats_desc.py` "
    "(recalcul pandas des données brutes) et construit les graphiques "
    "dynamiquement à partir de son contenu."
)

fichier = st.file_uploader(
    "📂 Dépose le fichier `stats_desc_sante.xlsx` (généré par calculs_stats_desc.py)",
    type=["xlsx"],
)

if fichier is None:
    st.info(
        """
        **Aucun fichier chargé pour l'instant.**

        1. Récupère `calculs_stats_desc.py` (à la racine du repo).
        2. Lance-le en local, à côté d'un dossier `Donnees/` contenant tes
           3 fichiers EHCVM (`s00_me_SEN2018.dta`, `s03_me_SEN2018.dta`,
           `ehcvm_ponderations_SEN2018.dta`).
        3. Il produit `stats_desc_sante.xlsx` — dépose-le ci-dessus.

        Les données individuelles des ménages ne quittent jamais ton
        ordinateur : seuls les agrégats (pourcentages, moyennes) sont
        dans ce fichier Excel.
        """
    )
    st.stop()

# --- Chargement de toutes les feuilles du classeur ---
try:
    feuilles = pd.read_excel(fichier, sheet_name=None)
except Exception as e:
    st.error(f"Impossible de lire le fichier : {e}")
    st.stop()

st.success(f"Fichier chargé : {len(feuilles)} feuilles détectées.")


def afficher_national(df, titre):
    """Affiche un tableau national (colonnes: indicateur?, modalite, pct)."""
    if "indicateur" in df.columns:
        for indic in df["indicateur"].unique():
            sous = df[df["indicateur"] == indic]
            c1, c2 = st.columns([1, 2])
            with c1:
                for _, row in sous.iterrows():
                    st.metric(f"{indic} — {row['modalite']}", f"{row['pct']} %")
            with c2:
                fig = px.bar(sous, x="modalite", y="pct", title=indic, text="pct")
                st.plotly_chart(fig, width='stretch')
    else:
        st.dataframe(df, width='stretch')


def afficher_regional(df, titre):
    """Affiche un tableau régional (colonnes: indicateur?, region, modalite, pct)."""
    if "indicateur" in df.columns:
        indicateurs = df["indicateur"].unique()
        choix = st.selectbox(f"Indicateur — {titre}", indicateurs, key=f"sel_{titre}")
        sous = df[df["indicateur"] == choix]
    else:
        sous = df
        choix = titre

    if "modalite" in sous.columns:
        fig = px.bar(sous, x="region", y="pct", color="modalite", barmode="stack",
                     title=f"{choix} — par région")
    else:
        # cas d'une feuille au format large (une colonne par variable)
        value_cols = [c for c in sous.columns if c != "region"]
        fig = px.bar(sous, x="region", y=value_cols, barmode="group",
                     title=f"{choix} — par région")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, width='stretch')


# ----------------------------------------------------------------------
# Organisation des onglets — un onglet par grande partie du rapport
# ----------------------------------------------------------------------
onglets_disponibles = []
mapping = {
    "Partie A — Morbidité & recours": ("PartieA_national", "PartieA_regional"),
    "Partie B — Accès & qualité perçue": ("PartieB_national", "PartieB_regional"),
    "Partie C — Couverture & prévention": ("PartieC_national", "PartieC_regional"),
}

# Ne garder que les onglets pour lesquels au moins une feuille existe réellement
for nom_onglet, (nat, reg) in mapping.items():
    if (nat and nat in feuilles) or (reg and reg in feuilles):
        onglets_disponibles.append(nom_onglet)

if not onglets_disponibles:
    st.warning("Aucune feuille reconnue dans ce fichier. Vérifie qu'il a bien été généré par `calculs_stats_desc.py`.")
    st.stop()

tabs = st.tabs(onglets_disponibles)

for tab, nom_onglet in zip(tabs, onglets_disponibles):
    nat, reg = mapping[nom_onglet]
    with tab:
        st.subheader(nom_onglet)
        if nat and nat in feuilles:
            st.markdown("**Niveau national**")
            afficher_national(feuilles[nat], nom_onglet)
        if reg and reg in feuilles:
            st.markdown("**Niveau régional**")
            afficher_regional(feuilles[reg], nom_onglet)

with st.expander("🔍 Voir les feuilles brutes du fichier Excel"):
    for nom, df in feuilles.items():
        st.markdown(f"**{nom}**")
        st.dataframe(df, width='stretch')
