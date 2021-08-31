from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from numpy.lib.index_tricks import AxisConcatenator
import pandas as pd
from author_style.utils import tokenizer_word2vec
import numpy as np
from author_style.utils import embed_sentence
from author_style.preprocessing import preprocess
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from gensim.models import Word2Vec

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict(paragraph):
    paragraph=preprocess(paragraph)
    X_pred = tokenizer_word2vec(paragraph)
    embedd = Word2Vec(X_pred, min_count=6, size=40)
    X_pred=embed_sentence(embedd, X_pred)
    X_pred = pad_sequences(X_pred,
                           dtype='float32',
                           padding='post',
                           maxlen=300)
    model = load_model('model')
    y_pred = model.predict(X_pred)
    return {'prediction': y_pred[0]}


    #inputs_ids = np.array(X_pred['input_ids'])
    #attention_mask = np.array(X_pred['attention_mask'])
