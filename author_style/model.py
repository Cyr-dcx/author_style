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
from transformers import CamembertConfig
from transformers import TFCamembertForMultipleChoice
from transformers import TFCamembertModel
from transformers import AutoTokenizer
import matplotlib.pyplot as plt


def create_model():
    LONGUEUR_MAX_PARAGRAPH=512
    #Instanciation du modèle
    transformer_model = TFCamembertModel.from_pretrained('jplu/tf-camembert-base')
    #Définition des formats d'entrée
    entrees_ids = tf.keras.layers.Input(shape=(LONGUEUR_MAX_PARAGRAPH,), name='input_token', dtype='int32')
    entrees_masks = tf.keras.layers.Input(shape=(LONGUEUR_MAX_PARAGRAPH,), name='masked_token', dtype='int32')
    #Création de la sortie du modèle
    sortie_camemBERT = transformer_model([entrees_ids, entrees_masks])
    #print(sortie_camemBERT.shape)

    #>>TFBaseModelOutputWithPooling(
    #last_hidden_state=<KerasTensor: shape=(None, 300, 768) dtype=float32 (created by layer 'tf_camembert_model_5')>,
    #pooler_output=<KerasTensor: shape=(None, 768) dtype=float32 (created by layer 'tf_camembert_model_5')>,
    #hidden_states=None, attentions=None)
    #Instanciation du modèle avec Keras
    model_camemBERT = tf.keras.Model(inputs=[entrees_ids, entrees_masks], outputs = sortie_camemBERT, trainable=False)
    #Définition du format d'entrée du modèle
    entrees_ids = tf.keras.layers.Input(shape=(LONGUEUR_MAX_PARAGRAPH,), name='input_token', dtype='int32')
    entrees_masks = tf.keras.layers.Input(shape=(LONGUEUR_MAX_PARAGRAPH,), name='masked_token', dtype='int32')
    #?
    #   Création de la sortie du modèle
    sortie_camemBERT = transformer_model([entrees_ids, entrees_masks])[0]
    l1 = Lambda(lambda seq: seq[:,0,:])(sortie_camemBERT) #pour ne récupérer que les vecteurs CLS
    #print(l1.shape)
    #lstm = LSTM(20, activation='tanh')(l1)
    #dense1 = Dense(512, activation='relu')(l1)
    #dense2 = Dense(256, activation='relu')(l1)
    #bidir1 = Bidirectional(LSTM(units=128, activation='tanh', return_sequences=True))(sortie_camemBERT)
    #bidir2 = Bidirectional(LSTM(units=256, activation='tanh', return_sequences=True))(bidir1)
    #bidir3 = Bidirectional(LSTM(units=256, activation='tanh'))(bidir2)
    #dropout = Dropout(.2)(dense1)
    dense3 = Dense(128, activation='relu')(l1)
    dropout = Dropout(0.1)(dense3)
    dense4 = Dense(64, activation='relu')(dropout)
    output = Dense(26, activation='softmax')(dense4)
    model1 = tf.keras.Model(inputs=[entrees_ids, entrees_masks], outputs = output)
    model1.layers[2].trainable = False   #Désactive l'entraînement de camemBERT
    es = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy', patience=5, verbose=0,
        mode='auto',restore_best_weights=True
    )
    model1.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
    return model1
