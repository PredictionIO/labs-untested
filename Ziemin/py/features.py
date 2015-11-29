#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFECV, SelectFromModel, SelectKBest, \
        f_regression
from sklearn.ensemble import RandomForestRegressor
import sklearn.preprocessing as preprocessing
import data
import models
import sys

min_max_scaler = preprocessing.MinMaxScaler()
max_abs_scaler = preprocessing.MaxAbsScaler()

# ---- feature selection ------------------------------

# len(columns) = len(mask)
def print_chosen_features(mask, columns):
    names = [data.column_names[i] for (isTrue, i) in zip(mask, columns) if isTrue]
    print("Selected columns: ")
    for n in names:
        print("* ", n);


class SelectionModel:

    def __init__(self, x_array, y_array, estimator, columns):
        self.x_array = x_array
        self.y_array = y_array
        self.estimator = estimator
        self.columns = columns


class RFECVSelection(SelectionModel):
    name = "RFECV"

    def __init__(self, *args):
        SelectionModel.__init__(self, *args)
        self.selector = RFECV(self.estimator, step=1, cv=5, scoring='mean_squared_error')
        self.selector.fit(self.x_array, self.y_array)
        self.support_ = self.selector.support_

    def print_rankings(self):
        print("Rankings for: ", RFECVSelection.name)
        for (i, rank) in zip(self.columns, self.selector.ranking_):
            print("{0}: {1}".format(data.column_names[i], rank))

    # number of features vs. cv scores
    def plot_num_of_feat_vs_cv_score(self):
        plt.figure()
        plt.xlabel("Number of features selected")
        plt.ylabel("Cross validation scores (mse)")
        plt.plot(range(1, len(self.selector.grid_scores_) + 1),
                self.selector.grid_scores_)
        plt.show()

    def plot_rankings(self):
        plt.figure()
        plt.title("Ranking of features in RFECV")
        plt.bar(range(self.x_array.shape[1]), self.selector.ranking_, align="center", color="r")
        plt.xticks(range(self.x_array.shape[1]), [data.column_names[i] for i in self.columns])
        plt.show()


class SelectFromModelSelection(SelectionModel):
    name = "SelectFromModel"

    def __init__(self, *args):
        SelectionModel.__init__(self, *args)
        self.selector = SelectFromModel(self.estimator)
        self.selector.fit(self.x_array, self.y_array)
        self.support_ = self.selector.get_support()

class SelectBestSelection(SelectionModel):
    name = "SelectKBest"

    def __init__(self, *args):
        SelectionModel.__init__(self, *args)
        self.selector = SelectKBest(f_regression, k='all')
        self.selector.fit(self.x_array, self.y_array)
        self.support_ = self.selector.get_support()
        self.scores_ = self.selector.scores_

    def print_scores(self):
        print("SelectKBest scores:")
        for (score, i) in sorted(zip(self.scores_, self.columns)):
            print("{0}:    {1:.3f}".format(data.column_names[i], score))

    def plot_scores(self):
        plt.figure()
        plt.title("SelectKBest scores")
        sort =  sorted(zip(self.scores_, self.columns))[::-1]
        names = [data.column_names[i] for (score, i) in sort]
        plt.bar(range(self.x_array.shape[1]), [s for (s,i) in sort], align="center", color="r")
        plt.xticks(range(x_array.shape[1]), names)
        plt.show()


# uses ExtraTreesClassifier
def plot_feature_importances(x_array, y_array):
    estimators = 20
    forest = RandomForestRegressor(n_estimators=estimators, max_features=None)
    print("Feature ranking (random tree regressor - %d estimators):" % estimators)
    forest.fit(x_array, y_array)

    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
    indices = np.argsort(importances)[::-1]
    names = [data.column_names[data.curr_cols[i]] for i in indices]

    # Print the feature ranking

    for f in range(x_array.shape[1]):
        print("{0} feature {1} ({2})".format(f + 1, names[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances - random forest regressor - % est." % 20)
    plt.bar(range(x_array.shape[1]), importances[indices],
	   color="r", yerr=std[indices], align="center")
    plt.xticks(range(x_array.shape[1]), names)
    plt.xlim([-1, x_array.shape[1]])
    plt.show()


def plot_feature_variances(x_array, y_array):
    array = np.c_[x_array, y_array]
    array = preprocessing.normalize(array, axis=0, norm='l1')
    variances = np.var(array, axis=0)
    names = [data.column_names[i] for i in data.curr_cols] + ["y"]

    plt.figure()
    plt.title("Features variances (l1 normalization)")
    plt.bar(range(len(variances)), variances, color="r", align="center")
    plt.xticks(range(len(variances)), names)
    plt.show()


def plot_feature_correlations(x_array, y_array):
    cors = np.corrcoef(np.c_[x_array, y_array], rowvar=0)
    # print correlation matrix between used features
    labels = [data.column_names[i] for i in data.curr_cols] + ["y"]
    plt.matshow(cors, cmap=plt.cm.Blues)
    plt.title("Features correlations (with result also)")
    plt.xticks(np.arange(len(data.curr_cols)+1), labels)
    plt.yticks(np.arange(len(data.curr_cols)+1), labels)
    plt.show()


# Usage: ./features.py <x_array.npy> <y_array.npy>
# x_array.npy - features array
# y_array.npy - results array
if __name__ == "__main__":
    x_file = sys.argv[1]
    y_file = sys.argv[2]

    print("Reading data ...")
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    print("Used features: ", [data.column_names[i] for i in data.curr_cols])

    # plot_feature_importances(x_array, y_array)
    # plot_feature_variances(x_array, y_array)
    plot_feature_correlations(x_array, y_array)

    # print("Executing selector: ", RFECVSelection.name)
    # rfecv = RFECVSelection(x_array, y_array, models.linear_regr, data.curr_cols)
    # print_chosen_features(rfecv.support_, data.curr_cols)
    # rfecv.print_rankings()
    # rfecv.plot_num_of_feat_vs_cv_score()
    # rfecv.plot_rankings()

    #print("Executing selector: ", SelectFromModelSelection.name)
    #sfm = SelectFromModelSelection(x_array, y_array, models.linear_regr, data.curr_cols)
    #print_chosen_features(sfm.support_, data.curr_cols)

    # print("Executing selector: ", SelectBestSelection.name)
    # skb = SelectBestSelection(x_array, y_array, models.linear_regr, data.curr_cols)
    # skb.print_scores()
    # skb.plot_scores()
