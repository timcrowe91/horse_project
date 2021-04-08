import pandas as pd
import numpy as np
X = pd.read_csv('raw_data/test_data_X.csv')
y_test = pd.read_csv('raw_data/test_data_y.csv')

X = X.drop(columns='Unnamed: 0')

X = np.array(X)
X = X.reshape(1413,24,5)
X
from tensorflow.keras.models import load_model
new_model  = load_model('gs://horseracingproject/base_model')


print(new_model.predict(x_test[0]))