from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import tensorflow as tf
from data_model.data import get_model


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


@app.get("/predict_odds")
def predict(X):
    model = get_model()
    numpy_2d_arrays = np.array(dict["X"])
    prediction_list = []
    for i in X:
        prediction = model.predict(X)[i]
        prediction_list.append(prediction)
    return {'predicitons': prediction_list}