# -*- coding: utf-8 -*-

import csv
from datetime import datetime

import numpy as np

###
# This functions takes pre-processed data, keeps only the relevant columns
# and sums for each 30 min chunk all CSPL__RECEIVED_CALLS sorted by ASS_ASIGMENT
###

FILE_PATH = 'train_data.csv'
WRITE_PATH = 'sums.csv'

assignments = ['T\xc3\xa9l\xc3\xa9phonie', 'Finances PCX', 'RTC', 'Gestion Renault', 'Nuit', 'Gestion - Accueil Telephonique',
        'Regulation Medicale', 'Services', 'Tech. Total', 'Gestion Relation Clienteles', 'Crises', 'Japon', 'M\xc3\xa9dical',
        'Gestion Assurances', 'Domicile', 'Gestion', 'SAP', 'Medicine', 'LifeStyle', 'Technical', 'TAI - RISQUE SERVICES',
        'RENAULT', 'TAI - CARTES', 'TAI - SERVICE', 'TAI - RISQUE', 'TAI - PNEUMATIQUES', 'Gestion Amex',
        'Maroc - G\xc3\xa9n\xc3\xa9riques', 'TPA', 'Tech. Inter', 'A DEFINIR', 'Technique Belgique', 'Technique International',
        'Gestion Clients', 'Manager', 'Tech. Axa', 'DOMISERVE', 'Truck Assistance', 'NL Technique', 'R\xc3\xa9ception', 'CAT',
        'Gestion DZ', 'NL M\xc3\xa9dical', 'M\xc3\xa9canicien', 'TAI - PANNE MECANIQUE', 'FO Remboursement', 'CMS',
        'Maroc - Renault', 'Divers', 'Prestataires', 'AEVA', 'Evenements', 'KPT', 'IPA Belgique - E/A MAJ', 'Juridique']
#0 : Date, 3 : Week-end, 4-10 : days of the week, 11 : night or day, 18 : ASS_ASIGMENT, 125 : CSPL_RECEIVED_CALLS
cols_to_keep = [0,3]+range(4,11)

### Select numeric columns
with open(FILE_PATH) as f:
    reader = csv.reader(f,delimiter=';')
    reader.next()
    current_slot = reader.next()[0]
    current_slot_sums = [0.0 for i in range(len(assignments))]
    counter = 0
    for row in reader:
        counter += 1
        if (counter % 100000 == 0):
            print "Ligne n°%d" % counter
        if (row[0] == current_slot):
            current_slot_sums[assignments.index(row[18])] += float(row[125])
        else:
            with open(WRITE_PATH,'a') as g:
                writer = csv.writer(g)
                writer.writerow([row[x] for x in cols_to_keep]+current_slot_sums)
                current_slot_sums = [0.0 for i in range(len(assignments))]
                current_slot = row[0]
