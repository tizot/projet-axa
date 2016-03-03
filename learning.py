# -*- coding: utf-8 -*-
import csv
import numpy as np
from datetime import datetime, date

from sklearn import cross_validation
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor, Lasso
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from data_filler import raw_train_data, test_data


X_raw, X_weather = raw_train_data(phone_datafile='sums.csv', weather_datafile='meteo_cleaned.csv')


# Estimator
# clf = SGDRegressor(loss='squared_loss', shuffle=True, n_iter=100, alpha=0.0001)
# clf = Lasso(alpha=1.0)
# clf = LinearSVC(C=1.0)
clf = DecisionTreeClassifier()
scaler = StandardScaler()

scores = cross_validation.cross_val_score(clf, X_raw[:, :-1], X_raw[:, -1], cv=5)

# Predictions
# results = test_data(X_raw, X_weather, clf, submission_file='submission.txt', scaler=scaler, output_file='clf-tree')
