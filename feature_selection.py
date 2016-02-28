# -*- coding: utf-8 -*-

import csv
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA


### Compute variances
labels = []

with open('train_2011_2012.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';', quotechar='"')

    for idx, row in enumerate(reader):
        if idx == 0:
            means = np.zeros(row.shape[1])
            variances = np.zeros(row.shape[1])
        else:
            for i, value in enumerate(row):
                try:
                    value = float(value)
                    variances[i] = (idx-1)/float(idx)*variances[i] + value*value/float(idx)
                    means[i] = (idx-1)/float(idx)*means[i] + value/float(idx)
                except:
                    variances[i] = (idx-1)/float(idx)*variances[i]
                    means[i] = (idx-1)/float(idx)*means[i]

    means = means * means
    for i, m in enumerate(variances):
        if (means[i] != 0):
            variances[i] = (variances[i] - means[i])/means[i]


### PCA
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

beginning_pca = datetime.now()

with open('train_data.csv') as f:
    reader = pd.read_csv(f, sep=';', usecols=cols)

    pca = PCA(10)
    data = pca.fit_transform(reader)
    print(data)

ending_pca = datetime.now()

print("")
print "Début PCA : " + beginning_pca.strftime("%H:%M")
print "Fin PCA : " + ending_pca.strftime("%H:%M")
print "Durée totale PCA : " + str(ending_pca - beginning_pca)
