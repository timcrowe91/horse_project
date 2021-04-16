import pandas as pd
import numpy as np

def get_data():
    df1 = pd.read_csv("raw_data/20-01.csv")
    df2 = pd.read_csv("raw_data/20-02.csv")
    df3 = pd.read_csv("raw_data/20-03.csv")
    df4 = pd.read_csv("raw_data/20-03b.csv")
    return pd.concat([df1, df2, df3, df4])

def filter_df(df):
    return None