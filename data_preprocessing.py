# -*- coding: utf-8 -*-
import csv
import datetime
import pandas as pd
import numpy as np

# Useful map between columns and numbers in the csv
#DAY_DS : 2
#DAY_WE_DS : 4
#TPER_TEAM : 5
#ACD_LIB : 9
#ASS_ASSIGNEMNT : 12
#ASS_PARTNER : 13
#ASS_POLE : 14
#ASS_COMENT : 17


#Possible values for string features
string_features = {
    'DAY_WE_DS': ['Dimanche', 'Lundi', 'Samedi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'],
    'ASS_ASSIGNEMNT': ['T\xc3\xa9l\xc3\xa9phonie', 'Finances PCX', 'RTC', 'Gestion Renault', 'Nuit', 'Gestion - Accueil Telephonique',
            'Regulation Medicale', 'Services', 'Tech. Total', 'Gestion Relation Clienteles', 'Crises', 'Japon', 'M\xc3\xa9dical',
            'Gestion Assurances', 'Domicile', 'Gestion', 'SAP', 'Medicine', 'LifeStyle', 'Technical', 'TAI - RISQUE SERVICES',
            'RENAULT', 'TAI - CARTES', 'TAI - SERVICE', 'TAI - RISQUE', 'TAI - PNEUMATIQUES', 'Gestion Amex',
            'Maroc - G\xc3\xa9n\xc3\xa9riques', 'TPA', 'Tech. Inter', 'A DEFINIR', 'Technique Belgique', 'Technique International',
            'Gestion Clients', 'Manager', 'Tech. Axa', 'DOMISERVE', 'Truck Assistance', 'NL Technique', 'R\xc3\xa9ception', 'CAT',
            'Gestion DZ', 'NL M\xc3\xa9dical', 'M\xc3\xa9canicien', 'TAI - PANNE MECANIQUE', 'FO Remboursement', 'CMS',
            'Maroc - Renault', 'Divers', 'Prestataires', 'AEVA', 'Evenements', 'KPT', 'IPA Belgique - E/A MAJ', 'Juridique'],
    'ASS_PARTNER': ['T\xc3\xa9l\xc3\xa9phonie', 'A D\xc3\xa9finir', 'Relation T\xc3\xa9l\xc3\xa9phonique Client\xc3\xa8le',
    'Gestion', 'Nuit', 'R\xc3\xa9gulation', 'HABITATION', 'L.I.E.F', 'Crises', 'M\xc3\xa9dical', 'Sant\xc3\xa9', '', 'Grand Compte',
    'G\xc3\xa9n\xc3\xa9riques', 'Encadrement', 'Cellule Accueil T\xc3\xa9l\xc3\xa9phonique', 'M\xc3\xa9canicien',
    'R\xc3\xa9seaux Prestataires', 'Implant', 'Ressources Humaines', 'A DEFINIR'],
    'ASS_POLE': ['SUPPORT', 'A DEFINIR', 'CLIENTS', 'ADMINISTRATIF', 'PERMANENCE', 'SANTE', 'HABITATION', 'AUTOMOBILE', 'CRISES',
    'MEDICAL', 'LIFESTYLE', 'TRUCK', 'GENERIQUES', 'MECANICIEN', 'DIVERS', 'KPT', 'E/A MAJ', 'JURIDIQUE'],
    'ASS_COMENT': ['', 'Rattachement au P\xc3\xb4le Grand Compte'],
}

# Numeric features
numeric_features = ['CSPL_', ]
data = [[] for i in range(87)]
labels = []
CHUNK_SIZE = 10000

print "Heure de debut : "+datetime.datetime.now().strftime("%I:%M")

# Récupérer les labels initiaux
with open('train_2011_2012.csv') as f:
    reader = csv.reader(f, delimiter=';', quotechar='"')
    labels = reader.next()

# Créer un nouveau fichier et y placer les labels "expansés"
expansed_labels = []
for l in labels:
    if l in string_features.keys():
        expansed_labels.append(";".join(string_features[l]))
    else:
        expansed_labels.append(l)

with open('train_tmp.csv', 'w') as f:
    f.write(";".join(expansed_labels))
    f.write("\n")

    # Parcourir le fichier train_2011_2012.csv et recopier les données dans le nouveau fichier
    with open('train_2011_2012.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')

        for idx, row in enumerate(reader, 1):
            if idx % CHUNK_SIZE == 0:
                print("Ligne %d" % idx)
            r = []
            for i, l in enumerate(row):
                if labels[i] in string_features.keys():
                    for k in string_features[labels[i]]:
                        r.append("1" if k == l else "0")
                else:
                    r.append(l)
            f.write(";".join(r))
            f.write("\n")

# Nettoyage des données : remplacer les NULL par la moyenne de la colonne (pour les données numériques)
with open('train_tmp.csv') as f:
    # Calcul des moyennes des features numériques
    reader = pd.read_csv(f, sep=";", quotechar='"', iterator=True, chunksize=CHUNK_SIZE)
    means = pd.Series(np.zeros(reader.get_chunk(1).shape[1]))
    lines = 0
    for chunk in reader:
        old_lines = lines
        lines += chunk.shape[0]
        print("Moyenne : bloc l. %d - %d" % (old_lines, lines))
        means += chunk.mean(numeric_only=True)

    means = means / lines

with open('train_tmp.csv') as f:
    # Affectation des moyennes aux valeurs NaN
    reader = pd.read_csv(f, sep=";", quotechar='"', iterator=True, chunksize=CHUNK_SIZE)
    idx = 0
    for c in reader:
        print("Ecriture : bloc no. %d" % (idx))
        idx += 1
        c.fillna(value=means)
        c.to_csv('train_data.csv', sep=';', header=(idx==0), mode='a') # write header only for first chunk, and append results


print "Heure de fin : "+datetime.datetime.now().strftime("%I:%M")
