import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from theme import carte_metrique, appliquer_theme_plotly, COULEURS
from libelles import libelle, LIBELLES_PARTIES

st.title("📊 Statistiques descriptives")
st.caption(
    "Source : EHCVM 2018-2019 (Sénégal). Cette page ne contient aucun chiffre "
    "en dur : elle lit le fichier Excel produit par `calculs_stats_desc.py` "
    "(recalcul pandas des données brutes) et construit les graphiques "
    "dynamiquement à partir de son contenu."
)

# Chemin du fichier agrégé committé dans le repo (aucune donnée individuelle,
# donc pas de souci à le versionner sur GitHub). Place ton export ici :
# data/stats_desc_sante.xlsx à la racine du repo.
CHEMIN_PAR_DEFAUT = Path(__file__).resolve().parent.parent / "data" / "stats_desc_sante.xlsx"

fichier = None
if CHEMIN_PAR_DEFAUT.exists():
    fichier = CHEMIN_PAR_DEFAUT
    st.caption(f"📁 Données chargées automatiquement depuis `{CHEMIN_PAR_DEFAUT.name}` (repo).")

with st.expander("🔄 Charger un autre fichier (écrase les données par défaut pour cette session)"):
    upload = st.file_uploader(
        "Dépose un fichier `stats_desc_sante.xlsx` (généré par calculs_stats_desc.py)",
        type=["xlsx"],
    )
    if upload is not None:
        fichier = upload

if fichier is None:
    st.info(
        """
        **Aucune donnée disponible.**

        1. Récupère `calculs_stats_desc.py` (à la racine du repo).
        2. Lance-le en local, à côté d'un dossier `Donnees/` contenant tes
           3 fichiers EHCVM (`s00_me_SEN2018.dta`, `s03_me_SEN2018.dta`,
           `ehcvm_ponderations_SEN2018.dta`).
        3. Il produit `stats_desc_sante.xlsx`.
        4. **Pour que ce soit permanent** : place ce fichier dans
           `data/stats_desc_sante.xlsx` à la racine de ton repo GitHub et
           commit-le (c'est juste des agrégats, aucune donnée individuelle).
           La page le rechargera automatiquement à chaque visite.
        5. **Ou temporairement** : dépose-le via le menu ci-dessus.
        """
    )
    st.stop()

# --- Chargement de toutes les feuilles du classeur ---
try:
    feuilles = pd.read_excel(fichier, sheet_name=None)
except Exception as e:
    st.error(f"Impossible de lire le fichier : {e}")
    st.stop()

# Arrondi systématique des colonnes numériques (évite les artefacts
# d'imprecision flottante à la relecture du xlsx, ex: 10.6999998092)
for nom, df in feuilles.items():
    for col in df.select_dtypes(include="number").columns:
        feuilles[nom][col] = df[col].round(1)

st.success(f"Données chargées : {len(feuilles)} feuilles détectées.")


def afficher_national(df, accent):
    """Affiche un tableau national (colonnes: indicateur?, modalite, pct)."""
    if "indicateur" in df.columns:
        for indic in df["indicateur"].unique():
            sous = df[df["indicateur"] == indic].copy()
            titre = libelle(indic)
            st.markdown(f"**{titre}**")
            c1, c2 = st.columns([1, 2])
            with c1:
                for _, row in sous.iterrows():
                    carte_metrique(row["modalite"], f"{row['pct']:.1f} %", accent=accent)
            with c2:
                sous["pct_txt"] = sous["pct"].map(lambda v: f"{v:.1f}")
                fig = px.bar(sous, x="modalite", y="pct", title=titre, text="pct_txt")
                appliquer_theme_plotly(fig)
                st.plotly_chart(fig, width='stretch')
    else:
        st.dataframe(df, width='stretch')


def afficher_regional(df, accent):
    """Affiche un tableau régional (colonnes: indicateur?, region, modalite, pct)."""
    if "indicateur" in df.columns:
        indicateurs = list(df["indicateur"].unique())
        choix = st.selectbox(
            "Indicateur", indicateurs, format_func=libelle, key=f"sel_{id(df)}"
        )
        sous = df[df["indicateur"] == choix]
        titre = libelle(choix)
    else:
        sous = df
        titre = "Répartition régionale"

    if "modalite" in sous.columns:
        fig = px.bar(sous, x="region", y="pct", color="modalite", barmode="stack",
                     title=f"{titre} — par région")
    else:
        # cas d'une feuille au format large (une colonne par variable)
        value_cols = [c for c in sous.columns if c != "region"]
        fig = px.bar(sous, x="region", y=value_cols, barmode="group",
                     title=f"{titre} — par région")
    fig.update_layout(xaxis_tickangle=-45)
    appliquer_theme_plotly(fig)
    st.plotly_chart(fig, width='stretch')


# ----------------------------------------------------------------------
# Organisation des onglets — un onglet par grande partie du rapport
# ----------------------------------------------------------------------
onglets_disponibles = []
mapping = {
    "Partie A — Morbidité & recours": ("PartieA_national", "PartieA_regional", COULEURS["teal"]),
    "Partie B — Accès & qualité perçue": ("PartieB_national", "PartieB_regional", COULEURS["ocre"]),
    "Partie C — Couverture & prévention": ("PartieC_national", "PartieC_regional", COULEURS["sauge"]),
}

# Ne garder que les onglets pour lesquels au moins une feuille existe réellement
for nom_onglet, (nat, reg, _) in mapping.items():
    if (nat and nat in feuilles) or (reg and reg in feuilles):
        onglets_disponibles.append(nom_onglet)

if not onglets_disponibles:
    st.warning("Aucune feuille reconnue dans ce fichier. Vérifie qu'il a bien été généré par `calculs_stats_desc.py`.")
    st.stop()

tabs = st.tabs(onglets_disponibles)

for tab, nom_onglet in zip(tabs, onglets_disponibles):
    nat, reg, accent = mapping[nom_onglet]
    with tab:
        st.subheader(LIBELLES_PARTIES.get(nom_onglet, nom_onglet))
        if nat and nat in feuilles:
            st.markdown("##### Niveau national")
            afficher_national(feuilles[nat], accent)
        if reg and reg in feuilles:
            st.markdown("##### Niveau régional")
            afficher_regional(feuilles[reg], accent)

with st.expander("🔍 Voir les feuilles brutes du fichier Excel"):
    for nom, df in feuilles.items():
        st.markdown(f"**{nom}**")
        st.dataframe(df, width='stretch')
