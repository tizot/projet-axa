# -*- coding: utf-8 -*-
import csv
import numpy as np
from datetime import datetime
from sklearn.linear_model import SGDRegressor, Lasso
from sklearn.preprocessing import StandardScaler

# pour chaque ligne, la première colonne est la date, puis si c'est un weekend,
# puis les bool qui correspondent aux jours de la semaine
# pour chaque ASS_ASSIGNEMNT (cf. data_preprocessing), le nombre d'appels

assignments = ['T\xc3\xa9l\xc3\xa9phonie', 'Finances PCX', 'RTC', 'Gestion Renault', 'Nuit', 'Gestion - Accueil Telephonique',
        'Regulation Medicale', 'Services', 'Tech. Total', 'Gestion Relation Clienteles', 'Crises', 'Japon', 'M\xc3\xa9dical',
        'Gestion Assurances', 'Domicile', 'Gestion', 'SAP', 'Medicine', 'LifeStyle', 'Technical', 'TAI - RISQUE SERVICES',
        'RENAULT', 'TAI - CARTES', 'TAI - SERVICE', 'TAI - RISQUE', 'TAI - PNEUMATIQUES', 'Gestion Amex',
        'Maroc - G\xc3\xa9n\xc3\xa9riques', 'TPA', 'Tech. Inter', 'A DEFINIR', 'Technique Belgique', 'Technique International',
        'Gestion Clients', 'Manager', 'Tech. Axa', 'DOMISERVE', 'Truck Assistance', 'NL Technique', 'R\xc3\xa9ception', 'CAT',
        'Gestion DZ', 'NL M\xc3\xa9dical', 'M\xc3\xa9canicien', 'TAI - PANNE MECANIQUE', 'FO Remboursement', 'CMS',
        'Maroc - Renault', 'Divers', 'Prestataires', 'AEVA', 'Evenements', 'KPT', 'IPA Belgique - E/A MAJ', 'Juridique']

DAYS_OF_WEEK_IDX = ['0', '1', '6', '2', '3', '4', '5']
DAYS_OF_WEEK = ['Dimanche', 'Lundi', 'Samedi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

NB_ASS = len(assignments)
COL_1 = np.ones(NB_ASS)
ID_ASS = np.identity(NB_ASS)
NB_SLOTS = 41900

# Construct X and y
X = np.zeros((NB_SLOTS * NB_ASS, 5 + 7 + NB_ASS))
y = np.zeros(NB_SLOTS * NB_ASS)

with open('sums.csv') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        # Date
        d = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.000")
        X[idx:idx+NB_ASS, 0] = d.year * COL_1
        X[idx:idx+NB_ASS, 1] = d.month * COL_1
        X[idx:idx+NB_ASS, 2] = d.day * COL_1
        X[idx:idx+NB_ASS, 3] = d.hour * COL_1
        X[idx:idx+NB_ASS, 4] = d.minute * COL_1

        # Day of week (booleans)
        for i in range(7):
            X[idx:idx+NB_ASS, 5+i] = int(row[2+i]) * COL_1

        # Which assignment?
        X[idx:idx+NB_ASS, 12:12+NB_ASS] = ID_ASS

        # How many calls for this (date, assignment)?
        for i in range(NB_ASS):
            y[idx+i] = row[9+i]

# Sort X and y
indexes = np.argsort(X, axis=1, kind='mergesort')
X = X[indexes]
y = y[indexes]

# Train the estimator
# clf = Lasso(alpha=0.1)
clf = SGDRegressor(loss='squared_loss', shuffle=True, n_iter=100, alpha=0.0001)
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)
clf.fit(X, y)

with open('submission.txt') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    current_line = reader.next()
    initial_date_str = current_line[0]
    initial_date = datetime.strptime(initial_date_str, "%Y-%m-%d %H:%M:%S.000")
    current_date_str = initial_date_str
    current_date = initial_date
    # Iterate while there is a line
    # finished = False
    # while not finished:
        # Iterate until date changes
    X_test = np.zeros((2*24 * NB_ASS, 5 + 7 + NB_ASS))
    idx = 0
    while initial_date.date() == current_date.date():
        # Date
        X_test[idx, 0] = current_date.year
        X_test[idx, 1] = current_date.month
        X_test[idx, 2] = current_date.day
        X_test[idx, 3] = current_date.hour
        X_test[idx, 4] = current_date.minute
        # Day of week
        for i in range(7):
            X_test[idx, 5+i] = 1 if i == DAYS_OF_WEEK_IDX[int(current_date.strftime("%w"))] else 0
        # Assignment
        for i in range(NB_ASS):
            X_test[idx, 12+i] = 1 if assignments[i] == current_line[1] else 0

        idx += 1
        try:
            current_line = reader.next()
            current_date_str = current_line[0]
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d %H:%M:%S.000")
        except StopIteration:
            finished = True
            break

    X_test = scaler.transform(X_test)
    y_test = clf.predict(X_test)
    print (y_test)
