# -*- coding: utf-8 -*-

import csv
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


with open('train_data.csv') as f:
    reader = pd.read_csv(f, sep=';', iterator=True,engine='c',nrows=100)
    values = reader.iloc[1]
    cols = [i for i in range(len(values))]
    # Remove non numeric columns
    for i, v in enumerate(values):
        try:
            val = float(v)
        except ValueError:
            cols[i] = -1
    while -1 in cols:
        cols.remove(-1)

beginning = datetime.now()

with open('train_data.csv') as f:
    reader = pd.read_csv(f, sep=';', usecols=cols,engine='c',nrows=100)
    pca = PCA(10).fit(reader)

with open('train_data.csv') as f:
    reader = pd.read_csv(f, sep=';', usecols=cols,engine='c')
    data = pca.transform(reader)


ending = datetime.now()

print("")
print "Début : " + beginning.strftime("%H:%M")
print "Fin : " + ending.strftime("%H:%M")
print "Durée totale : " + str(ending - beginning)
