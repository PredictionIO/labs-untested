#!/usr/bin/python
import numpy as np
import models
import data
from data import column_names
from sklearn.cross_validation import ShuffleSplit, KFold
from sklearn.feature_selection import RFECV, SelectKBest, \
        SelectFromModel, f_regression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, StandardScaler
from sklearn.decomposition import PCA
import sys

ms = [
       # models.linear_regr,
       # models.ridge_regr,
       # models.ridge_regr_cv,
       # models.kernel_ridge_regr,
       # models.svm_svr_regr,
       # models.decision_tree_regr,
       # models.gradient_boosting_regr,
       # models.ada_boost_regr,
       # models.random_forest_regressor,
       # models.lasso,
       # models.bayes_regr,
       # models.average,
       # models.first_week,
       # models.lasso_lars_regr,
       # models.only_lars_regr,
       # models.combiner_regr,
       # models.ard_regr,
       # models.elastic_net_regr,
       # models.sgd_regr,
       # models.isotonic_regr,
       # models.bagging_lin_regr,
       # models.bagging_decision_tree,
       # models.clustering_lin_regr,
       # models.first_week_ensemble_regr,
       # models.logistic_separator_regr,
       models.novelty_separator_regr,
       ]

def get_cv_iterators(n):
    return  {
            "KFold": KFold(n, n_folds=5, shuffle=False),
            "KFold_shuffle": KFold(n, n_folds=5, shuffle=True),
            "ShuffleSplit": ShuffleSplit(n, n_iter=10, test_size=0.25),
            }

# returns a pipeline starting with selecting the best features
def add_feature_selection(model, selection):
    p = Pipeline([
        ("feature_selection", selection),
        (model.name, model)
        ])
    p.name = model.name + " - feature selection"
    return p

def add_feature_scaling(model, scaler):
    p = Pipeline([
        ("scaler", scaler),
        (model.name, model)
        ])
    p.name = model.name + " - feature scaling"
    return p

def add_polynomial_features(model, deg):
    p = Pipeline([
        ("poly_features", PolynomialFeatures(deg)),
        (model.name, model)
        ])
    p.name = model.name + " - poly features {0}".format(deg)
    return p

def add_pca(model, n_components):
    p = Pipeline([
        ("pca", PCA(n_components=n_components)),
        (model.name, model)
        ])
    p.name = model.name + " - pca {0}".format(n_components)
    return p

def create_pipeline(chain, model):
    p = Pipeline(chain + [(model.name, model)])
    p.name = model.name
    return p


# Usage: ./run_regr_models.py <x_array.npy> <y_array.npy>
# x_array.npy - features array
# y_array.npy - results array
if __name__ == "__main__":
    x_file = sys.argv[1]
    y_file = sys.argv[2]
    iters = 1
    if len(sys.argv) > 3:
        iters = int(sys.argv[3])

    print("Reading data ...")
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    # check models only on some subsets
    #cond = (x_array[:,4] != 0).reshape(x_array.shape[0])
    #x_array = x_array[cond]
    #y_array = y_array[cond]


    chain = [
                # ("minmaxscaler", MinMaxScaler()),
                ("standardizer", StandardScaler()),
                # ("feature selection", SelectKBest(f_regression, k=4)),
                # ("pca", PCA(1)),
                # ("poly features", PolynomialFeatures(2))
            ]
    ms = list(map(lambda m: create_pipeline(chain, m), ms))

    print("Testing models ...")
    tester = models.RegressionModelTester(
            x_array, y_array,
            'mean_squared_error',
            lambda: get_cv_iterators(x_array.shape[0])["KFold_shuffle"])
    errors = tester.run_models(ms)

    print("Errors:")
    for name, err in errors.items():
        print("Score of {0} = {1:.3f} (+/- {2:.3f})".format(name, err[0], err[1]))
