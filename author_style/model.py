from tensorflow.python.framework import config
from author_style.utils import *
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Dropout, Input, Lambda, LSTM, Dropout, Bidirectional
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from transformers import TFCamembertModel
import matplotlib.pyplot as plt


def create_model():
    LONGUEUR_MAX_PARAGRAPH = 512
    #Instanciation du modèle
    transformer_model = TFCamembertModel.from_pretrained(
        'jplu/tf-camembert-base')
    #Définition des formats d'entrée
    entrees_ids = tf.keras.layers.Input(shape=(LONGUEUR_MAX_PARAGRAPH, ),
                                        name='input_token',
                                        dtype='int32')
    entrees_masks = tf.keras.layers.Input(shape=(LONGUEUR_MAX_PARAGRAPH, ),
                                          name='masked_token',
                                          dtype='int32')
    #Création de la sortie du modèle
    sortie_camemBERT = transformer_model([entrees_ids, entrees_masks])[0]
    print(sortie_camemBERT.shape)
    print(sortie_camemBERT)
    l1 = Lambda(lambda seq: seq[:, 0, :])(
        sortie_camemBERT)  #pour ne récupérer que les vecteurs CLS
    dense3 = Dense(128, activation='relu')(l1)
    output = Dense(21, activation='softmax')(dense3)
    print(output.shape)
    model = tf.keras.Model(inputs=[entrees_ids, entrees_masks], outputs=output)
    model.layers[2].trainable = False  #Désactive l'entraînement de camemBERT
    return model
