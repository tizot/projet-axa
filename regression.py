# -*- coding: utf-8 -*-
import csv
import numpy as np
from datetime import datetime
from sklearn.linear_model import SGDRegressor

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

NB_ASS = len(assignments)
COL_1 = np.ones(NB_ASS)
ID_ASS = np.identity(NB_ASS)
NB_SLOTS = 41900

X = np.zeros((NB_SLOTS * NB_ASS, 5 + 7 + NB_ASS))
y = np.zeros(NB_SLOTS * NB_ASS)

with open('sums.csv') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        d = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.000")
        X[idx:idx+NB_ASS, 0] = d.year * COL_1
        X[idx:idx+NB_ASS, 1] = d.month * COL_1
        X[idx:idx+NB_ASS, 2] = d.day * COL_1
        X[idx:idx+NB_ASS, 3] = d.hour * COL_1
        X[idx:idx+NB_ASS, 4] = d.minute * COL_1
        for i in range(7): # day of week booleans
            X[idx:idx+NB_ASS, 5+i] = int(row[2+i]) * COL_1
        X[idx:idx+NB_ASS, 12:12+NB_ASS] = ID_ASS

        for i in range(NB_ASS):
            y[idx+i] = row[9+i]


clf = SGDRegressor(loss='squared_loss', shuffle=True, n_iter=5, alpha=0.0001)
clf.fit(X, y)
