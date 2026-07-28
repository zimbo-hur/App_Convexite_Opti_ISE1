import streamlit as st

st.set_page_config(
    page_title="Optimisation Accès aux Soins - Sénégal",
    page_icon="🏥",
    layout="wide"
)

# --- En-tête ---
st.title("🏥 Optimisation de l'accès aux soins de santé au Sénégal")
st.markdown("### Projet ENSAE Dakar — Cycle ISE, Maths & Éco")

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
    st.subheader("👥 Membres du groupe")
    st.info(
        """
        - Membre 1
        - Membre 2
        - Membre 3
        - Membre 4
        """
    )
    st.caption("✏️ À compléter avec les vrais noms.")

    st.subheader("📚 Références")
    st.write(
        """
        - EHCVM 2018-2019, Sénégal
        - ANSD — Agence Nationale de la Statistique et de la Démographie
        - ENSAE Dakar, 2026
        """
    )

st.markdown("---")
st.caption("Application développée avec Streamlit — ENSAE Dakar, 2026.")
