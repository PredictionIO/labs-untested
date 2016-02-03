import numpy as np
from sklearn.preprocessing import scale
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import KFold
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge, \
        LassoLars, Lars, ElasticNet, ARDRegression, SGDRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, \
        RandomForestRegressor, BaggingRegressor
from sklearn.isotonic import IsotonicRegression

from estimators import XGBRegressor, ClusteringEnsemble, FirstWeek0Ensemble, \
        AverageModel, FirstWeekCopyModel, ModelCombinator, \
        LogisticRegressionSeparator, NoveltySeparator
from data import column_indexes, shuffle

xgb_params = {
        'nthread': 4,
        "alpha": 0.004,
        'gamma': 0.005,
        'max_depth': 7,
        # 'subsample': 0.98,
        'eta': 0.3,
        # 'min_child_weight': 1.02
        }

models = [
        ("LinearRegression", LinearRegression(n_jobs=-1)),
        ("RidgeRegression", Ridge(alpha=0.1, normalize=True)),
        # the below one causes MemoryError! ????
        ("KernelRidge", KernelRidge(kernel='rbf', alpha=0.1)), 
        # watch out - O(n^3) - data has to be reduced!!!
        ("SVR", SVR(cache_size=1500, tol=1e-1)),
        ("DecisionTree", DecisionTreeRegressor()),
        ("AdaBoost", AdaBoostRegressor(n_estimators=100)),
        ("GradientBoostingRegressor",
          GradientBoostingRegressor(loss='quantile', min_samples_leaf=4, n_estimators=100)),
        ("RandomForestRegressor", RandomForestRegressor(n_estimators=50)),
        ("Lasso", Lasso(alpha=0.1, normalize=True)),
        ("BayesianRidge", BayesianRidge(normalize=True)),
        ("Avarage", AverageModel()),
        ("FirstWeekCopyModel", FirstWeekCopyModel(column_indexes["first_week"])),
        ("LassoLars", LassoLars(alpha=0.0005, normalize=True)),
        ("Lars", Lars()),
        ("ElasticNet", ElasticNet(alpha=0.1)),
        # this one also has MemoryError ????
        ("ARDRegressor", ARDRegression()),
        ("SGDRegressor", SGDRegressor()),
        ("SGDRegressor2", SGDRegressor(
            penalty='elasticnet', l1_ratio=0.08, alpha=0.0001)),
        ("BaggingLinearRegr", BaggingRegressor(
            LinearRegression(), n_estimators=18, max_samples=0.8, max_features=0.9)),
        ("BaggingRidge", BaggingRegressor(
            Ridge(alpha=0.05), n_estimators=25, max_samples=0.85, max_features=0.9)),
        ("BaggingDecisionTree", BaggingRegressor(DecisionTreeRegressor())),
        ("ClusteringLinRegr", ClusteringEnsemble()),
        ("FirstWeekEnsemble", FirstWeek0Ensemble()),
        ("Combiner", ModelCombinator(
                        [
                            Ridge(alpha=0.05),
                            GradientBoostingRegressor(n_estimators=25)
                        ],
                        LinearRegression(n_jobs=-1))),
        ("LogisticRegrSep", LogisticRegressionSeparator()),
        ("NoveltySeparator", NoveltySeparator()),
        ("XGBRegressor", XGBRegressor(n_rounds=50, **xgb_params))
        ]

metrics = [
        ("MSE", mean_squared_error),
        ]

def prepare_data(X, y):
    X, y = shuffle(X, y)
    X = scale(X)

    return X, y, KFold(y.size, n_folds=5)
