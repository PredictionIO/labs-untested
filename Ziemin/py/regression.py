#!/usr/bin/python
import sys
import os
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils import shuffle
from sklearn.preprocessing import scale
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import KFold
import xgboost as xgb


# class wrapping xgboost classifier to work correctly
# with sklearn
class XGBRegressor(BaseEstimator):

    def __init__(self, n_rounds=50, gamma=0.03, alpha=0.005, scale_pos_weight=None,
            lam=1, max_delta_step=1, nthread=4, max_depth=6, silent=1, subsample=1,
            eta=0.1, min_child_weight=1):

        self.classes_ = [0, 1]
        self.params = {
                "n_rounds": n_rounds,
                "gamma": gamma,
                "alpha": alpha,
                "max_delta_step": max_delta_step,
                "max_depth": max_depth,
                "nthread": nthread,
                "lam": lam,
                "subsample": subsample,
                "eta": eta,
                "min_child_weight": min_child_weight
                }

    def get_params(self, deep=True):
        return self.params

    def set_params(self, **params):
        for key, val in params.items():
            self.params[key] = val
        return self

    def fit(self, X, y, **fit_params):
        params = { key:val for key, val in self.params.items() if key != "n_rounds" }
        ratio = float(np.sum(y==0) / np.sum(y==1))
        # params["scale_pos_weight"] = ratio
        params['objective'] = "reg:linear"
        params['silent'] = 1
        params['lambda'] = params['lam']
        del params['lam']

        dtrain = xgb.DMatrix(X, label=y)
        self.bst = xgb.train(params, dtrain, self.params["n_rounds"], verbose_eval=False)

    def predict(self, X):
        dtest = xgb.DMatrix(X)
        return self.bst.predict(dtest)

    def decision_function(self, X):
        return self.predict_proba(X)

xgb_params = {
        'n_rounds': 100,
        'nthread': 4,
        "alpha": 0.004,
        # 'gamma': 0.005,
        # 'max_delta_step': 1,
        'max_depth': 7,
        # 'subsample': 0.98,
        'eta': 0.3,
        # 'min_child_weight': 1.02
        }


# ---------------------------------------------
# testing functions
# ---------------------------------------------
def cv_xgboost_regressor(regressors, x_array, y):


    for name, model in regressors:
        print("-- Testing: {0} --".format(name))

        mses = []
        scores_dict = { "Recall": [], "Roc_Auc": [], "Precision": [], "F-beta": [] }
        skf = KFold(n=y.size, n_folds=5, shuffle=True)

        fold = 1
        for train_index, test_index in skf:
            model.fit(x_array[train_index], y[train_index])
            results = model.predict(x_array[test_index])
            # scores evaluation
            mse = mean_squared_error(y[test_index], results)
            print("MSE {0}: {1:.4f}".format(fold, mse))
            mses.append(mse)

        print()
        print("MSE: {0:.2f} (+/-) {1:.3f}".format(mses.mean(), mses.std()))
        print("Min: {0:.2f} Max {1:.3f}".format(mses.min(), mses.max()))

regressors = [
        ("XGBRegressor", XGBRegressor(**xgb_params)),
        ]

# Usage: ./classification.py <x_array.npy> <y_array.npy>
# x_array.npy - features array
# y_array.npy - results array
if __name__ == "__main__":
    # set number of threads for XGBoost
    os.environ["OMP_NUM_THREADS"] = "4"
    x_file = sys.argv[1]
    y_file = sys.argv[2]

    print("Reading data ...")
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    print("Preparing data ...")
    # y = get_arrays_three_weeks(x_array, y_array)

    x_array, y = shuffle(x_array, y_array)
    x_array = scale(x_array)

    print("Testing regressors ...")
    cv_xgboost_regressor(regressors, x_array, y)
