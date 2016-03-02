# -*- coding: utf-8 -*-
import csv
import numpy as np
from datetime import datetime, date
from sklearn.linear_model import SGDRegressor, Lasso
from sklearn.preprocessing import StandardScaler

from data_filler import raw_train_data, test_data

X_raw, X_weather = raw_train_data(phone_datafile='sums.csv', weather_datafile='meteo_cleaned.csv')

# Estimator
clf = SGDRegressor(loss='squared_loss', shuffle=True, n_iter=100, alpha=0.0001)
scaler = StandardScaler()

# Predictions
results = test_data(X_raw, X_weather, clf, submission_file='submission.txt', scaler=scaler)
