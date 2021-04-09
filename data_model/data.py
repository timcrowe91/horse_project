import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
X = pd.read_csv('raw_data/test_data_X.csv')
y_test = pd.read_csv('raw_data/test_data_y.csv')

X = X.drop(columns='Unnamed: 0')
X = np.array(X)
X = X.reshape(1413,24,5)



def get_model():
    X = pd.read_csv('raw_data/test_data_X.csv')
    y_test = pd.read_csv('raw_data/test_data_y.csv')
    X = X.drop(columns='Unnamed: 0')
    X = np.array(X)
    X = X.reshape(1413,24,5)
    new_model  = load_model('gs://horseracingproject/base_model')
    return X, y_test, new_model


if __name__ == '__main__':
    X,y_test,new_model= get_model()