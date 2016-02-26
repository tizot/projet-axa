import csv

instances_number = 100
data = []
labels = []


with open('train_2011_2012.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';',quotechar='"')

    for idx,row in enumerate(reader):
        if (idx==0):
            labels = row
        else:
            data.append(row)
            if (idx==100):
                break

    print labels
