import streamlit as st
import pandas as pd
import numpy as np

# --- Titre et texte ---
st.title("Ma première app Streamlit")
st.write("Bienvenue ! Ceci est une app de test toute simple.")

# --- Un widget interactif ---
nom = st.text_input("Comment tu t'appelles ?")
if nom:
    st.write(f"Salut {nom} 👋")

# --- Un slider ---
n = st.slider("Choisis un nombre", 0, 100, 50)
st.write(f"Tu as choisi : {n}")

# --- Un petit graphique avec des données random ---
st.subheader("Exemple de graphique")
data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)
st.line_chart(data)

# --- Un bouton ---
if st.button("Clique ici"):
    st.success("Tu as cliqué sur le bouton !")