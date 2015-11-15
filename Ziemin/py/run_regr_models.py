#!/usr/bin/python
import numpy as np
import models
import data
from sklearn import linear_model
from data import column_names
import sys

linear_regr = linear_model.LinearRegression(normalize=True, n_jobs=-1)
linear_regr.name = "Linear regression"

ridge_regr = linear_model.Ridge(alpha=0.1, normalize=True)
ridge_regr.name = "Ridge regression"

lasso = linear_model.Lasso(alpha=0.1, normalize=True)
lasso.name = "Lasso"

bayes_regr = linear_model.BayesianRidge(normalize=True)
bayes_regr.name = "Bayesian regression"

average = models.AverageModel()
first_week = models.FirstWeekCopyModel(data.column_indexes["first_week"])

ms = [ linear_regr,
       ridge_regr,
       lasso,
       bayes_regr,
       average,
       first_week ]

# Usage: ./run_regr_models.py <x_array.npy> <y_array.npy> <?iterations>
# x_array.npy - features array
# y_array.npy - results array
# iterations  - (optional) number of iterations for RegressionModelTester
if __name__ == "__main__":
    x_file = sys.argv[1]
    y_file = sys.argv[2]
    iters = 1
    if len(sys.argv) > 3:
        iters = int(sys.argv[3])

    print("Reading data ...")
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    print("Testing models ...")
    tester = models.RegressionModelTester(x_array, y_array, models.mse_metric)
    errors = tester.run_models(ms, iters)

    print("Errors:")
    for name, err in errors.items():
        print("MSE of {0} = {1}".format(name, err))
