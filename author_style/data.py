import joblib
from author_style.params import *
import pandas as pd

def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    X = joblib.load(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH_X}")
    y = joblib.load(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH_y}")
    X=pd.DataFrame(X)
    y=pd.Series(y)
    return X, y
