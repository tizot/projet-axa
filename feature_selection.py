import csv
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

with open('train_data.csv') as f:
    reader = pd.read_csv(f, sep=';', iterator=True)
    values = reader.get_chunk(1).values[0]
    cols = [i for i in range(len(values))]
    # Remove non numeric columns
    for i, v in enumerate(values):
        try:
            val = float(v)
        except ValueError:
            cols[i] = -1
    while -1 in cols:
        cols.remove(-1)

with open('train_data.csv') as f:
    reader = pd.read_csv(f, sep=';', usecols=cols)

    pca = PCA(10)
    print(reader)
    data = pca.fit_transform(reader)
    print(data.columns)
