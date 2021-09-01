from typing import ValuesView
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import requests


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
    text_input = '%20'.join(text_input.split(" "))
    response = requests.get(
        f'https://apiamd64-ywkwoqtfqq-ew.a.run.app/predict?paragraph={text_input}',
    ).json()
    auteurs = response['prediction']
    keys = list(auteurs.keys())
    values = list(auteurs.values())

    index_max = values.index(max(values))
    max_auteur = keys[index_max]


    root_path = os.path.dirname(__file__)
    path_folder = os.path.join(root_path, 'Auteurs_photos')
    images = [image for image in os.listdir(path_folder)]
    max = max(auteurs.values())

    imag1 = Image.open(os.path.join(path_folder, ''.join([max_auteur,'.png'])))
    st.image(imag1, width=400)



    fig = plt.figure(figsize=(5, 5))

    plt.barh(keys, values, color='skyblue')

    plt.xlabel("Probabilité que le texte saisi appartienne à cet auteur")
    plt.ylabel("Nom des auteurs")
    plt.title("Prédiction du style de l'auteur")
    st.pyplot(fig)




#st.header("""C'est Simone de Beauvoire""")
#image = Image.open('Simone_de_Beauvoir.png')
#st.image(image, caption='Simone de Beauvoir', width=200)
