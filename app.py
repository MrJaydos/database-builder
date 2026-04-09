import pandas as pd

df = pd.read_csv('name_gender_dataset.csv')
print(df.columns.tolist())
print(df.head())