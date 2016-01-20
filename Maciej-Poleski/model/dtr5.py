#!/usr/bin/env python3

import numpy;
from sklearn import tree

# size of utmSources = 108
data = numpy.loadtxt('input_data_reduced5_shuffled_unpacked.csv',delimiter=',')
size = len(data)
testSize = size*80/100

selection = [i for i in range(123)]
selection.remove(2)

data_X = data[:, selection]
data_X_train = data_X[:-testSize]
data_X_test = data_X[-testSize:]

data_Y = data[:,2]
data_Y_train = data_Y[:-testSize]
data_Y_test = data_Y[-testSize:]

regr = tree.DecisionTreeRegressor(max_depth=5)

regr.fit(data_X_train, data_Y_train)

print('Variance score: %.2f' % regr.score(data_X_test, data_Y_test))
