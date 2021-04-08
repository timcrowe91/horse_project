import pandas as pd

x_test = pd.read_csv('raw_data/test_data_X.csv')
y_test = pd.read_csv('raw_data/test_data_y.csv')


from tensorflow.keras.models import load_model

new_model  = load_model('https://console.cloud.google.com/storage/browser/horseracingproject/base_model')


print(new_model.predict(x_test[0]))