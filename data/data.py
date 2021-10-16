import pandas as pd

def get_dataframe():
    df = pd.read_csv('data/admitidos.csv')
    return df