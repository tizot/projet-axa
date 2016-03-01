# -*- coding: utf-8 -*-#

import csv
###
#This script reads the meteo data from 2011 to 2012,
#calculates per hour and departement the mean of
# - temperature
# - pressure
# - precipitation
###

FILE_PATH = 'meteo/meteo_2012.csv'
WRITE_PATH = 'meteo/meteo_means.csv'

#Means are stored in this table. Every value is a table where :
#0 is number of instances, 1 the cumulated sum of temperature,
#2 the cumulated sum of precipitations, 3 the cumulated sum of pressures
meteo_means = {}

with open(FILE_PATH) as f:
    reader = csv.reader(f,delimiter=',')
    counter = 0
    for row in reader:
        counter += 1
        if (counter % 100000 == 0):
            print "Ligne n°%d" % counter
        try:
            float(row[1])
            dpt = int(row[1])
            key = row[0]
            if not (key in meteo_means.keys()):
                meteo_means[key] = [0 for i in range(100)]
            meteo_means[key][dpt] = [0 for i in range(4)]
            meteo_means[key][dpt][0] += 1
            meteo_means[key][dpt][1] += (float(row[3])+float(row[4]))/2
            meteo_means[key][dpt][2] += float(row[6])
            meteo_means[key][dpt][3] += float(row[7])
        except ValueError:
            a = 0

with open(WRITE_PATH,'a') as g:
    for key in meteo_means.keys():
        for idx,dpt in enumerate(meteo_means[key]):
            if (meteo_means[key][idx] != 0):
                number_of_instances = meteo_means[key][idx][0]
                meteo_means[key][idx] = [meteo_means[key][idx][1]/number_of_instances,
                meteo_means[key][idx][2]/number_of_instances,
                meteo_means[key][idx][3]/number_of_instances]
        writer = csv.writer(g)
        writer.writerow([key]+meteo_means[key])
