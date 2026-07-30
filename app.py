import streamlit as st
from theme import injecter_css

# --- Configuration et thème, centralisés ici (une seule fois pour toute l'app) ---
st.set_page_config(
    page_title="Optimisation Accès aux Soins - Sénégal",
    layout="wide",
)
injecter_css()

# --- Navigation ---
# Les titres et icônes ci-dessous sont ceux affichés dans le menu — totalement
# indépendants du nom des fichiers. Pour renommer une page dans le menu,
# change juste `title=` ici, aucun autre fichier à toucher.
pg = st.navigation([
    st.Page("vues/accueil.py", title="Page d'accueil", icon="🏠", default=True),
    st.Page("vues/stats_desc.py", title="Statistiques descriptives", icon="📊"),
    st.Page("vues/optimisation.py", title="Optimisation", icon="⚙️"),
])
pg.run()
