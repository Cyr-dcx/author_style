from typing import ValuesView
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

image_header = Image.open('Author_style.png')
st.header('''Projet Style d'un auteur''')
st.image(image_header, width=800)


st.markdown("""# Qui est l'auteur qui aurait pu écrire ce paragraphe ?
## Découvrons-le grâce à notre modèle !
# """)

text_input = st.text_input("""Copiez un paragraphe d'auteur ici""")
length = st.write('Nombre de caractères dans le paragraphe:', len(text_input))

prediction = st.button('Prédire')

if prediction == True:
    auteurs = {'BASTIDE Francois-Regis': 0.02,
    'Albert Camus': 0.0,
    'Louis-Ferdinand Celine': 0.67,
    'COHEN Albert': 0.0,
    'DEBEAUVOIR Simone': 0.0,
    'Marguerite Duras': 0.23,
    'Jean Echenoz': 0.0,
    'Romain Gary': 0.06,
    'Pierre Guth': 0.0,
    'Jean Giono': 0.0,
    'Paul Guth': 0.0,
    'Joseph Joffo': 0.01,
    'Joseph Kessel': 0.0,
    'Patrick Modiano': 0.0,
    'Georges Perec': 0.0,
    'QUEFFELEC Henri': 0.0,
    'QUEFFELEC Yann': 0.0,
    'Françoise Sagan': 0.0,
    'Nathalie Sarraute': 0.0,
    'SCHOENDOERFFER Pierre': 0.0,
    'Boris Vian': 0.01,
    'YOURCENAR Marguerite': 0.0}



    root_path = os.path.dirname(__file__)
    path_folder = os.path.join(root_path, 'Auteurs_photos')
    images = [image for image in os.listdir(path_folder)]

    imag1 = Image.open(os.path.join(path_folder, images[0]))
    st.image(imag1, width=200)

    keys = list(auteurs.keys())
    values = list(auteurs.values())

    fig = plt.figure(figsize=(5, 5))

    plt.barh(keys, values, color='skyblue')

    plt.xlabel("Probabilité que le texte saisi appartienne à cet auteur")
    plt.ylabel("Nom des auteurs")
    plt.title("Prédiction du style de l'auteur")
    st.pyplot(fig)

#st.header("""C'est Simone de Beauvoire""")
#image = Image.open('Simone_de_Beauvoir.png')
#st.image(image, caption='Simone de Beauvoir', width=200)
