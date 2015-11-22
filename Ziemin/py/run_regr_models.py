#!/usr/bin/python
import numpy as np
import models
import data
from data import column_names
import sys

ms = [ models.linear_regr,
       models.ridge_regr,
       models.lasso,
       models.bayes_regr,
       models.average,
       models.first_week ]

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
