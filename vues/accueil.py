import streamlit as st

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
st.caption("Application développée avec Streamlit — ENSAE Dakar, 2026.")
