from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from tensorflow.python.ops.math_ops import argmax
import numpy as np
from author_style.model import create_model
from transformers import AutoTokenizer
import os
import numpy as np

root_path=__file__
model_path = os.path.join(os.path.dirname(os.path.dirname(root_path)),
                          'model_camembert', 'my_weights')

LONGUEUR_MAX_PARAGRAPH = 512
model=create_model()
model.load_weights(model_path)

#instancier le tokenizeur
tokenizer = AutoTokenizer.from_pretrained('jplu/tf-camembert-base')

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
    X_pred=paragraph
    X_pred_token = tokenizer(X_pred,
                                       max_length=LONGUEUR_MAX_PARAGRAPH,
                                       padding="max_length",
                                       truncation=True,
                                       return_tensors='tf',
                                       add_special_tokens=True)
    inputs_ids = np.array(X_pred_token['input_ids'])
    attention_mask = np.array(X_pred_token['attention_mask'])
    pred = model.predict([inputs_ids, attention_mask])
    return {
        'prediction': {
            'BAZIN Herve': round(pred[0].item(0),4),
            'CAMUS Albert': round(pred[0].item(1),4),
            'CELINE Louis-Ferdinand': round(pred[0].item(2),4),
            'COHEN Albert': round(pred[0].item(3),4),
            'DEBEAUVOIR Simone': round(pred[0].item(4),4),
            'DURAS Marguerite': round(pred[0].item(5),4),
            'ECHENOZ Jean': round(pred[0].item(6),4),
            'GARY Romain': round(pred[0].item(7),4),
            'GIONO Jean': round(pred[0].item(8),4),
            'GUTH Paul': round(pred[0].item(9),4),
            'JOFFO Joseph': round(pred[0].item(10),4),
            'KESSEL Joseph': round(pred[0].item(11),4),
            'MODIANO Patrick': round(pred[0].item(12),4),
            'PEREC Georges': round(pred[0].item(13),4),
            'QUEFFELEC Henri': round(pred[0].item(14),4),
            'QUEFFELEC Yann': round(pred[0].item(15),4),
            'SARRAUTE Nathalie': round(pred[0].item(16),4),
            'SCHOENDOERFFER Pierre': round(pred[0].item(17),4),
            'VIAN Boris':round(pred[0].item(18),4),
            'YOURCENAR Marguerite': round(pred[0].item(19),4),
        }}
