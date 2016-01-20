#!/usr/bin/env python3

import numpy;
import xgboost as xgb

# size of utmSources = 108
data = numpy.loadtxt('input_data_reduced4_shuffled_unpacked.csv',delimiter=',')
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

label=[1 if i==2 else 0 for i in range(123)]

dtrain = xgb.DMatrix(data[:-testSize], label=label)
dtest = xgb.DMatrix(data[-testSize:], label=label)

param = {'objective':'reg:linear' }
param['nthread'] = 1
param['eval_metric'] = 'auc'

evallist = [(dtest,'eval'), (dtrain,'train')]

bst = xgb.train(param, dtrain, 10, evallist)

