import csv

instances_number = 100
data = []
labels = []
variances = []
means = []


with open('train_2011_2012.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';',quotechar='"')

    for idx,row in enumerate(reader):
        if (idx==0):
            labels = row
            for i,value in enumerate(row):
                variances.append(0)
                means.append(0)
        else:
            for i,value in enumerate(row):
                try:
                    value = float(value)
                    variances[i] = (idx-1)/float(idx)*variances[i] + value*value/float(idx)
                    means[i] = (idx-1)/float(idx)*means[i] + value/float(idx)
                except:
                    variances[i] = (idx-1)/float(idx)*variances[i]
                    means[i] = (idx-1)/float(idx)*means[i]
            if (idx==10001):
                break

    for i,m in enumerate(variances):
        means[i] = means[i]*means[i]
        if (means[i] != 0):
            variances[i] = (variances[i] - means[i])/means[i]


    print means
    print variances
    # print labels
