"""
Thème visuel partagé de l'app — palette, typographie et composants,
pensés pour le sujet (accès aux soins de santé au Sénégal), pas les
couleurs par défaut de Streamlit.

Import dans chaque page :
    from theme import injecter_css, carte_metrique, COULEURS, sequence_couleurs
"""

import streamlit as st

# --------------------------------------------------------------------------
# PALETTE — inspirée de la terre ocre du Sahel et des teintes des zones
# humides du fleuve Sénégal, plutôt que le bleu/rouge par défaut de Streamlit.
# --------------------------------------------------------------------------
COULEURS = {
    "fond": "#FAF6F0",        # sable clair
    "surface": "#EFE6D8",     # sable plus soutenu (cartes, fonds de section)
    "encre": "#232323",       # texte principal
    "teal": "#1B4B43",        # bleu-vert profond — structure, Partie A
    "ocre": "#BF5B04",        # terre cuite — accent principal, Partie B
    "sauge": "#6B8F71",       # vert doux — positif, Partie C
    "brique": "#A23E32",      # rouge brique — alertes / valeurs faibles
    "or": "#C9A227",          # accent secondaire
}

# Séquence de couleurs discrètes pour les graphiques (mêmes tons, cohérents
# avec le reste de l'app plutôt que le bleu/rouge/vert par défaut de Plotly)
def sequence_couleurs():
    return [COULEURS["teal"], COULEURS["ocre"], COULEURS["sauge"],
            COULEURS["or"], COULEURS["brique"], "#4A6670"]


def appliquer_theme_plotly(fig):
    """Applique la palette et la typographie du projet à une figure Plotly."""
    fig.update_layout(
        template="plotly_white",
        colorway=sequence_couleurs(),
        font=dict(family="IBM Plex Sans, sans-serif", color=COULEURS["encre"], size=13),
        title_font=dict(family="Spectral, serif", size=18, color=COULEURS["teal"]),
        plot_bgcolor=COULEURS["fond"],
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, l=10, r=10, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=COULEURS["surface"])
    fig.update_yaxes(gridcolor=COULEURS["surface"])
    return fig


def injecter_css():
    """Injecte les polices et styles custom. À appeler une fois en haut de chaque page."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Spectral:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'IBM Plex Sans', sans-serif;
        }}

        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            font-family: 'Spectral', serif !important;
            color: {COULEURS["teal"]} !important;
            font-weight: 600 !important;
        }}

        /* Onglets */
        button[data-baseweb="tab"] {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 500;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {COULEURS["ocre"]} !important;
            border-bottom-color: {COULEURS["ocre"]} !important;
        }}

        /* Cartes métriques custom (voir carte_metrique ci-dessous) */
        .carte-metrique {{
            background: {COULEURS["surface"]};
            border-left: 4px solid var(--accent, {COULEURS["ocre"]});
            border-radius: 6px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.6rem;
        }}
        .carte-metrique .libelle {{
            font-size: 0.82rem;
            color: {COULEURS["encre"]};
            opacity: 0.75;
            margin-bottom: 0.15rem;
        }}
        .carte-metrique .valeur {{
            font-family: 'Spectral', serif;
            font-size: 1.6rem;
            font-weight: 600;
            color: {COULEURS["teal"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def carte_metrique(libelle, valeur, accent=None):
    """Affiche une carte métrique custom (remplace st.metric avec la charte du projet)."""
    accent = accent or COULEURS["ocre"]
    st.markdown(
        f"""
        <div class="carte-metrique" style="--accent: {accent};">
            <div class="libelle">{libelle}</div>
            <div class="valeur">{valeur}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
