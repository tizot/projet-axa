# -*- coding: utf-8 -*-
import csv
import numpy as np
from datetime import datetime, date
from pandas import read_csv

assignments = ['T\xc3\xa9l\xc3\xa9phonie', 'Finances PCX', 'RTC', 'Gestion Renault', 'Nuit', 'Gestion - Accueil Telephonique',
        'Regulation Medicale', 'Services', 'Tech. Total', 'Gestion Relation Clienteles', 'Crises', 'Japon', 'M\xc3\xa9dical',
        'Gestion Assurances', 'Domicile', 'Gestion', 'SAP', 'Medicine', 'LifeStyle', 'Technical', 'TAI - RISQUE SERVICES',
        'RENAULT', 'TAI - CARTES', 'TAI - SERVICE', 'TAI - RISQUE', 'TAI - PNEUMATIQUES', 'Gestion Amex',
        'Maroc - G\xc3\xa9n\xc3\xa9riques', 'TPA', 'Tech. Inter', 'A DEFINIR', 'Technique Belgique', 'Technique International',
        'Gestion Clients', 'Manager', 'Tech. Axa', 'DOMISERVE', 'Truck Assistance', 'NL Technique', 'R\xc3\xa9ception', 'CAT',
        'Gestion DZ', 'NL M\xc3\xa9dical', 'M\xc3\xa9canicien', 'TAI - PANNE MECANIQUE', 'FO Remboursement', 'CMS',
        'Maroc - Renault', 'Divers', 'Prestataires', 'AEVA', 'Evenements', 'KPT', 'IPA Belgique - E/A MAJ', 'Juridique']

DAYS_OF_WEEK_IDX = [0, 1, 3, 4, 5, 6, 2]
DAYS_OF_WEEK = ['Dimanche', 'Lundi', 'Samedi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

NB_ASS = len(assignments)
COL_1 = np.ones(NB_ASS)
ID_ASS = np.identity(NB_ASS)
NB_SLOTS = 41901

# Construct X_raw
def raw_train_data(phone_datafile='sums.csv', weather_datafile='meteo_cleaned.csv'):
    beginning = datetime.now()
    X_raw = np.zeros((NB_SLOTS * NB_ASS, 5 + 7 + NB_ASS + 282 + 1))
    # cols : year, month, day, hour, minute, day of week (7 booleans), assignments (NB_ASS booleans), 282 weather data, nb calls

    print("Taille de X_raw : " + str(X_raw.shape))

    # Fill X_raw
    with open(phone_datafile) as f:
        reader = csv.reader(f)
        print("Lecture du fichier CSV de données téléphoniques")

        l = 0
        for idx, row in enumerate(reader):
            l += 1
            # Date
            d = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.000")
            X_raw[idx*NB_ASS:(idx+1)*NB_ASS, 0] = d.year * COL_1
            X_raw[idx*NB_ASS:(idx+1)*NB_ASS, 1] = d.month * COL_1
            X_raw[idx*NB_ASS:(idx+1)*NB_ASS, 2] = d.day * COL_1
            X_raw[idx*NB_ASS:(idx+1)*NB_ASS, 3] = d.hour * COL_1
            X_raw[idx*NB_ASS:(idx+1)*NB_ASS, 4] = d.minute * COL_1

             # Day of week (booleans)
            for i in range(7):
                X_raw[idx*NB_ASS:(idx+1)*NB_ASS, 5+i] = int(row[2+i]) * COL_1

            # Which assignment?
            X_raw[idx*NB_ASS:(idx+1)*NB_ASS, 12:12+NB_ASS] = ID_ASS

            # How many calls for this (date, assignment)?
            for i in range(NB_ASS):
                X_raw[idx*NB_ASS+i, -1] = row[9+i]

        print("Nombre de lignes lues : %d" % l)

    print("")

    # Fill weather data
    with open(weather_datafile) as f:
        print("Lecture du fichier CSV de données météo")
        X_weather = read_csv(f, sep=",", index_col=0, header=None, parse_dates=True)

        for r in X_raw:
            d = datetime(int(r[0]), int(r[1]), int(r[2]), int(r[3]))
            if len(X_weather[d.strftime("%Y-%m-%d %H:%M:%S")].values) > 0:
                r[12+NB_ASS:12+NB_ASS+282] = X_weather[d.strftime("%Y-%m-%d %H:%M:%S")].values[0]

    print("")

    ending = datetime.now()
    print("Durée de chargement des données d'entrainement : " + str(ending-beginning))
    print("")

    return X_raw, X_weather


# Construct X_test
def test_data(X_raw, X_weather, estimator, submission_file='submission.txt', scaler=None):
    results = []

    with open(submission_file) as f:
        reader = csv.reader(f, delimiter='\t')
        print("Lecture du fichier " + submission_file)

        reader.next()
        current_line = reader.next()
        initial_date_str = current_line[0]
        initial_date = datetime.strptime(initial_date_str, "%Y-%m-%d %H:%M:%S.000")
        current_date_str = initial_date_str
        current_date = initial_date

        # Iterate while there is a line
        finished = False
        while not finished:
            # Iterate until date changes
            print("Date : " + current_date_str)

            X_test = np.zeros((2*24 * NB_ASS, 5 + 7 + NB_ASS + 282))
            # cols : year, month, day, hour, minute, day of week (7 booleans), assignments (NB_ASS booleans), 282 weather data

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

            # Extract filled cells from X_test
            X_test = X_test[:idx, :]
            print("Taille de X_test : " + str(X_test.shape))

            # Add weather data
            for r in X_test:
                d = datetime(int(r[0]), int(r[1]), int(r[2]), int(r[3]))
                if len(X_weather[d.strftime("%Y-%m-%d %H:%M:%S")].values) > 0:
                    r[12+NB_ASS:12+NB_ASS+282] = X_weather[d.strftime("%Y-%m-%d %H:%M:%S")].values[0]

            # Select training data from X_raw
            X_train = np.zeros(X_raw.shape)
            rr = 0
            for r in X_raw:
                if date(int(r[0]), int(r[1]), int(r[2])) < current_date.date():
                    X_train[rr, :] = r
                    rr += 1

            X_train = X_train[:rr, :]
            X_train, y_train = X_train[:, :-1], X_train[:, -1]

            # Train clf with good data
            if scaler is not None:
                scaler.fit(X_train)
                X_train = scaler.transform(X_train)
                X_test = scaler.transform(X_test)

            estimator.fit(X_train, y_train)
            y_test = estimator.predict(X_test)
            results.append(y_test)

            print("Taille de y_test : " + str(y_test.shape))

            for i in range(y_test.shape[0]):
                print(y_test[i])

            print("")
            initial_date = current_date

        return results
