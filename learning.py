# -*- coding: utf-8 -*-
import csv
import numpy as np
from datetime import datetime, date

from sklearn import cross_validation
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor, Lasso, ElasticNet
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from data_filler import raw_train_data, test_data


X_raw = raw_train_data(phone_datafile='sums2.csv', weather_datafile='meteo_cleaned.csv')


# Estimator
# clf = SGDRegressor(loss='squared_loss', shuffle=True, n_iter=5, alpha=0.0001)
# clf = Lasso(alpha=1.0)
# clf = ElasticNet()
# clf = LinearSVC(C=1.0)
# clf = DecisionTreeClassifier()
clf = RandomForestClassifier()
scaler = StandardScaler()

# scores = cross_validation.cross_val_score(clf, X_raw[:, :-1], X_raw[:, -1], cv=5)
# print scores

# Predictions
results = test_data(X_raw, clf, submission_file='submission.txt', scaler=scaler, output_file='clf-tree')
