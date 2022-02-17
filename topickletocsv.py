import pandas as pd 

df = pd.read_csv("data/datacsv.csv")
df.to_pickle("data/datapkl.zip")