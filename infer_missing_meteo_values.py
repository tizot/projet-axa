# -*- coding: utf-8 -*-#

import csv

###
#This script takes a csv where each row is composed of :
#- a date
#- a table composed of
#    - 100 entries, one for each departement from 0 to 99, each one composed of
#        - either a 0 if there is no data for this departement
#        - either a table of three entries composed of :
#             - temperature
#             - precipitations
#             - pressure
# If there is a 0 that means the value is missing

#It outputs a dict where the keys are time slots and the values are table of 300
# entries, of for each feature of the meteo in each departemnt

FILE_PATH = "meteo/meteo_means.csv"
WRITE_PATH = "meteo/meteo_cleaned.csv"
meteo_dict = {}
means = [[0,0] for i in range(288)]

with open(FILE_PATH) as f:
    reader = csv.reader(f)
    counter = 0
    for row in reader:
        counter += 1
        if (counter % 100 == 0):
            print "Ligne n°%d" % counter
        current_meteo = []
        for i in range(1,97):
            if row[i] != '0':
                if isinstance(eval(row[i])[0],int):
                    current_meteo += ['undef']
                else:
                    current_meteo += [eval(row[i])[0]]
                    means[3*(i-1)][0] += 1
                    means[3*(i-1)][1] += eval(row[i])[0]
                if  isinstance(eval(row[i])[1],int):
                    current_meteo += ['undef']
                else:
                    means[3*(i-1)+1][0] += 1
                    means[3*(i-1)+1][1] += eval(row[i])[1]
                    current_meteo += [eval(row[i])[1]]
                if isinstance(eval(row[i])[2],int):
                    current_meteo += ['undef']
                else:
                    means[3*(i-1)+2][0] += 1
                    means[3*(i-1)+2][1] += eval(row[i])[2]
                    current_meteo += [eval(row[i])[2]]
            else:
                current_meteo = current_meteo + ['undef','undef','undef']
            meteo_dict[row[0]] = current_meteo

for idx,tbl in enumerate(means):
    if tbl[0] == 0:
        means[idx] = 'undef'
    else:
        means[idx] = tbl[1]/tbl[0]

for key in meteo_dict.keys():
    for idx,val in enumerate(meteo_dict[key]):
        if val=='undef':
            meteo_dict[key][idx] = means[idx]
    meteo_dict[key] = filter(lambda a: a != 'undef', meteo_dict[key])

with open(WRITE_PATH,'a') as g:
    writer = csv.writer(g)
    for key in meteo_dict.keys():
        writer.writerow([key]+meteo_dict[key])
