import csv
import datetime

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
DAY_WE_DS_values = ['Dimanche', 'Lundi', 'Samedi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
ASS_ASSIGNMENT_values = ['T\xc3\xa9l\xc3\xa9phonie', 'Finances PCX', 'RTC', 'Gestion Renault', 'Nuit', 'Gestion - Accueil Telephonique', 'Regulation Medicale', 'Services', 'Tech. Total', 'Gestion Relation Clienteles', 'Crises', 'Japon', 'M\xc3\xa9dical', 'Gestion Assurances', 'Domicile', 'Gestion', 'SAP', 'Medicine', 'LifeStyle', 'Technical', 'TAI - RISQUE SERVICES', 'RENAULT', 'TAI - CARTES', 'TAI - SERVICE', 'TAI - RISQUE', 'TAI - PNEUMATIQUES', 'Gestion Amex', 'Maroc - G\xc3\xa9n\xc3\xa9riques', 'TPA', 'Tech. Inter', 'A DEFINIR', 'Technique Belgique', 'Technique International', 'Gestion Clients', 'Manager', 'Tech. Axa', 'DOMISERVE', 'Truck Assistance', 'NL Technique', 'R\xc3\xa9ception', 'CAT', 'Gestion DZ', 'NL M\xc3\xa9dical', 'M\xc3\xa9canicien', 'TAI - PANNE MECANIQUE', 'FO Remboursement', 'CMS', 'Maroc - Renault', 'Divers', 'Prestataires', 'AEVA', 'Evenements', 'KPT', 'IPA Belgique - E/A MAJ', 'Juridique']
ASS_PARTNER_values = ['T\xc3\xa9l\xc3\xa9phonie', 'A D\xc3\xa9finir', 'Relation T\xc3\xa9l\xc3\xa9phonique Client\xc3\xa8le', 'Gestion', 'Nuit', 'R\xc3\xa9gulation', 'HABITATION', 'L.I.E.F', 'Crises', 'M\xc3\xa9dical', 'Sant\xc3\xa9', '', 'Grand Compte', 'G\xc3\xa9n\xc3\xa9riques', 'Encadrement', 'Cellule Accueil T\xc3\xa9l\xc3\xa9phonique', 'M\xc3\xa9canicien', 'R\xc3\xa9seaux Prestataires', 'Implant', 'Ressources Humaines', 'A DEFINIR']
ASS_POLE_values = ['SUPPORT', 'A DEFINIR', 'CLIENTS', 'ADMINISTRATIF', 'PERMANENCE', 'SANTE', 'HABITATION', 'AUTOMOBILE', 'CRISES', 'MEDICAL', 'LIFESTYLE', 'TRUCK', 'GENERIQUES', 'MECANICIEN', 'DIVERS', 'KPT', 'E/A MAJ', 'JURIDIQUE']
ASS_COMENT = ['', 'Rattachement au P\xc3\xb4le Grand Compte']

data = [[] for i in range(87)]
labels = []

print "Heure de debut : "+datetime.datetime.now().strftime("%I:%M")

days_ds_possible_strings = []

with open('train_2011_2012.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';',quotechar='"')

    for idx,row in enumerate(reader):
        if (idx % 1000 == 0):
            print idx
        if (idx==0):
            labels = row
        else:
            for number,feature in enumerate(row):
                if (not (feature in data[number])):
                    data[number].append(feature)


for idx,feature in enumerate(data):
    if (feature.length==1):
        print labels[idx]

print "Heure de fin : "+datetime.datetime.now().strftime("%I:%M")
