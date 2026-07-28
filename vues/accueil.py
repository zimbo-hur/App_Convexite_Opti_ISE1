import streamlit as st
from pathlib import Path


def trouver_dossier_assets():
    """Cherche le dossier 'assets/' en remontant depuis ce fichier (robuste, que
    ce script soit à la racine du repo ou dans un sous-dossier)."""
    ici = Path(__file__).resolve().parent
    for candidat in [ici, ici.parent, ici.parent.parent]:
        if (candidat / "assets").is_dir():
            return candidat / "assets"
    return ici / "assets"  # par défaut, pour un message d'erreur clair si absent


DOSSIER_ASSETS = trouver_dossier_assets()

# --- Logos (ANSD à gauche, ENSAE à droite) ---
logo_gauche, logo_centre, logo_droite = st.columns([1, 2, 1])

chemin_ansd = DOSSIER_ASSETS / "logo_ansd.jpeg"
chemin_ensae = DOSSIER_ASSETS / "logo_ensae.jpeg"

if chemin_ansd.exists() and chemin_ensae.exists():
    with logo_gauche:
        st.image(str(chemin_ansd), width=140)
    with logo_droite:
        st.image(str(chemin_ensae), width=140)
else:
    st.warning(
        f"⚠️ Logos introuvables dans `{DOSSIER_ASSETS}`. Vérifie que le dossier "
        "`assets/` (avec `logo_ansd.jpeg` et `logo_ensae.jpeg`) a bien été "
        "poussé sur GitHub, à la racine du repo."
    )

# --- En-tête ---
st.title("🏥 Optimisation de l'accès aux centres de santé au Sénégal")
st.markdown("### Dans le cadre du cours de Convexité et optimisation, ISE1")
st.markdown("##### Cours dispensé par M. Oumar DIOP")
st.markdown("###### Année académique 2025-2026")
st.markdown("---")

# --- Colonnes : présentation / navigation ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Contexte et objectif du projet")
    st.write(
        """
        Ce projet s'inscrit dans une problématique d'**allocation optimale des
        ressources de santé** au Sénégal (personnel médical, capacité d'accueil,
        budget médicaments, infrastructures), en tenant compte des **barrières
        géographiques et financières** (distance, coût) qui limitent l'accès
        aux soins pour les ménages.

        À partir des données de l'**Enquête Harmonisée sur les Conditions de Vie
        des Ménages (EHCVM 2018-2019)**, nous construisons :

        - un **diagnostic** de la situation sanitaire actuelle (morbidité, recours
          aux soins, qualité perçue, couverture) ;
        - un **modèle d'optimisation** (programmation convexe) permettant de
          proposer une allocation des ressources qui maximise le bien-être
          sanitaire sous contrainte budgétaire et de disponibilité.
        """
    )

    st.subheader("🧭 Comment naviguer dans l'app")
    st.write(
        """
        Utilisez le menu à gauche pour accéder aux différentes pages :

        - **📊 Statistiques descriptives** — état des lieux de l'accès et de la
          qualité des soins au Sénégal (données EHCVM 2018).
        - **⚙️ Optimisation** — sélection des paramètres et lancement du modèle
          d'allocation des ressources.
        """
    )

with col2:
    st.subheader(" Membres du groupe :")
    st.info(
        """
        - Ahmed Firhoun OUMAROU SOULEYE (ISE1-Eco)
        - Andjiboudine ANDIL BEN (ISE1-Math)
        - Hamadou DICKO (ISE1-Math)
        """
    )

st.markdown("---")