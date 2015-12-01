#!/usr/bin/env python3

import numpy;
from sklearn import linear_model

data = numpy.loadtxt('input_data_reduced_shuffled.csv',delimiter=',')
size = len(data)
testSize = size*80/100

data_X = data[:, [0, 1]]
data_X_train = data_X[:-testSize]
data_X_test = data_X[-testSize:]

data_Y = data[:,2]
data_Y_train = data_Y[:-testSize]
data_Y_test = data_Y[-testSize:]

regr = linear_model.LinearRegression()

regr.fit(data_X_train, data_Y_train)

print('Coefficients: \n', regr.coef_)
print("Residual sum of squares: %.2f" % numpy.mean((regr.predict(data_X_test) - data_Y_test) ** 2))
print('Variance score: %.2f' % regr.score(data_X_test, data_Y_test))
