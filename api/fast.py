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
    return {'prediction': pred[0].item(0)}
