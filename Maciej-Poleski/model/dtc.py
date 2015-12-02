#!/usr/bin/env python3

import numpy;
from sklearn import tree

data = numpy.loadtxt('input_data_reduced_shuffled.csv',delimiter=',')
size = len(data)
testSize = int(size*80/100)

data_X = data[:, [0, 1, 3, 4, 5]]
data_X_train = data_X[:-testSize]
data_X_test = data_X[-testSize:]

data_Y = [ (1 if y>=5000 else 0) for y in data[:,2]]
data_Y_train = data_Y[:-testSize]
data_Y_test = data_Y[-testSize:]

regr = tree.DecisionTreeClassifier(max_depth=5)

regr.fit(data_X_train, data_Y_train)

print('Variance score: %.2f' % regr.score(data_X_test, data_Y_test))
