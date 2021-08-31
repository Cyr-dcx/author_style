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
    'BAZIN Herve': 0.0,
    'BAZIN Hervé': 0.0,
    'CAMUS Albert': 0.0,
    'CELINE Louis-Ferdinand': 0.67,
    'COHEN Albert': 0.0,
    'DEBEAUVOIR SIMONE': 0.0,
    'DEBEAUVOIR Simone': 0.0,
    'DURAS Marguerite': 0.23,
    'ECHENOZ Jean': 0.0,
    'GARY Romain': 0.06,
    'GASCAR Pierre': 0.0,
    'GIONO Jean': 0.0,
    'GRAINVILLE Patrick': 0.0,
    'GUTH Paul': 0.0,
    'JOFFO Joseph': 0.01,
    'KESSEL Joseph': 0.0,
    'MODIANO Patrick': 0.0,
    'PEREC Georges': 0.0,
    'QUEFFELEC Henri': 0.0,
    'QUEFFELEC Yann': 0.0,
    'SAGAN Fraçoise': 0.0,
    'SARRAUTE Nathalie': 0.0,
    'SCHOENDOERFFER Pierre': 0.0,
    'VIAN Boris': 0.01,
    'YOURCENAR Marguerite': 0.0}

    root_path = os.path.dirname(__file__)
    path_folder = os.path.join(root_path, 'Auteurs_photos')
    images = [images for images in os.listdir(path_folder)]

    image = Image.open(os.path.join(path_folder, images[0]))
    st.image(images[0], width=200)

#   keys = auteurs.keys()
#  values = auteurs.values()

# st.bar_chart(data=auteurs)


#st.header("""C'est Simone de Beauvoire""")
#image = Image.open('Simone_de_Beauvoir.png')
#st.image(image, caption='Simone de Beauvoir', width=200)
