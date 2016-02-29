# -*- coding: utf-8 -*-

import csv
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

FILE_PATH = 'train_data.csv'

### Select numeric columns
with open(FILE_PATH) as f:
    reader = pd.read_csv(f, sep=';', nrows=1)
    values = reader.iloc[0]
    cols = [i for i in range(len(values))]
    # Remove non numeric columns
    for i, v in enumerate(values):
        try:
            val = float(v)
        except ValueError:
            cols[i] = -1
    while -1 in cols:
        cols.remove(-1)


### Compute variances
beginning_var = datetime.now()

labels = []
means = np.zeros((1, len(cols)))
variances = np.zeros((1, len(cols)))

with open(FILE_PATH) as f:
    reader = pd.read_csv(f, delimiter=';', quotechar='"', usecols=cols, iterator=True, chunksize=1)

    l = 0 # count lines
    for r in reader:
        if l % 1000 == 0:
            print("Ligne %d" % l)
        variances += r.values[0] * r.values[0]
        means += r.values[0]
        l += 1

    variances = 1.0 / l * variances - means * means

    idx_features = np.argsort(variances)[0]
    print(idx_features)

ending_var = datetime.now()

print("")
print "Début Variances : " + beginning_var.strftime("%H:%M")
print "Fin Variances : " + ending_var.strftime("%H:%M")
print "Durée totale Variances : " + str(ending_var - beginning_var)

### PCA
beginning_pca = datetime.now()

with open(FILE_PATH) as f:
    reader = pd.read_csv(f, sep=';', usecols=cols, engine='c', nrows=100)
    pca = PCA(10).fit(reader)

with open(FILE_PATH) as f:
    reader = pd.read_csv(f, sep=';', usecols=cols, engine='c')
    data = pca.transform(reader)


ending_pca = datetime.now()

print("")
print "Début PCA : " + beginning_pca.strftime("%H:%M")
print "Fin PCA : " + ending_pca.strftime("%H:%M")
print "Durée totale PCA : " + str(ending_pca - beginning_pca)
