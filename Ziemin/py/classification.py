#!/usr/bin/python
import sys
import os
import numpy as np
from data import curr_index
from sklearn.cross_validation import cross_val_score, StratifiedKFold, train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, SGDClassifier, PassiveAggressiveClassifier, \
        RidgeClassifier
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, StandardScaler, scale
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestRegressor, AdaBoostClassifier, \
        GradientBoostingClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import roc_auc_score
import xgboost as xgb

# classification for the problem:
# choose users who will probably buy something more in the next three weeks

# S - random variable telling whether user is going spend anything in the next three weeks
# A - user spent something in the first week
# P(S = 1) = P(S = 1| A = 1)P(A = 1) + P(S = 1 | A = 0)P(A = 0)
class InterestingUsersClassifier(BaseEstimator):

    def get_params(self, deep=True):
        return {}

    def fit(self, X, y):

        first_week = (X[:, 1] > 0).reshape(X.shape[0])
        not_first_week = np.logical_not(first_week)

        self.yes_est = LogisticRegression(class_weight='balanced')
        self.not_est = LogisticRegression(class_weight='balanced')

        # remove first_week column
        X = np.delete(X, 1, 1)
        X = scale(X)

        self.yes_est.fit(X[first_week], y[first_week])
        self.not_est.fit(X[not_first_week], y[not_first_week])

    def predict(self, X):
        y = np.zeros(X.shape[0])

        first_week = (X[:, 1] > 0).reshape(X.shape[0])
        not_first_week = np.logical_not(first_week)

        # remove first_week column
        X = np.delete(X, 1, 1)
        X = scale(X)

        y[first_week] = self.yes_est.predict(X[first_week])
        y[not_first_week] = self.not_est.predict(X[not_first_week])

        return y

def add_scaler(cls):
    return Pipeline([
        ("scaler", StandardScaler()),
        ("cls", cls)])

class PrepareForBayes(TransformerMixin):

    def fit_transform(self, X, y=None, **fit_params):
        return X[:, [
            curr_index['conv_count'],
            curr_index['views_count'],
            curr_index['viewed_bought_count'],
            curr_index['has_seen_ad']
            ]]

    def fit(self, X, y):
        pass

    def transform(self, X):
        return self.fit_transform(X)


def prepare_bayes(cls):
    return Pipeline([
        ("prepare_bayes", PrepareForBayes()),
        ("cls", cls)])


classifiers = [
        # ("Two LogisticRegressions", InterestingUsersClassifier()),
        # ("Simple Logistic regression", add_scaler(LogisticRegression(class_weight='balanced'))),
        # ("RandomForestRegressor", RandomForestRegressor()),
        # ("AdaBoostClassifier", add_scaler(AdaBoostClassifier())),
        # ("GradientBoostingClassifier", add_scaler(GradientBoostingClassifier())),
        # ("ExtraTreesClassifier", ExtraTreesClassifier(class_weight='balanced')),
        # ("GaussianNB", prepare_bayes(GaussianNB())),
        # ("MultinomialNB", prepare_bayes(MultinomialNB(class_prior=[0.3, 0.7]))),
        # ("SGDClassifier1", add_scaler(SGDClassifier(loss='log', penalty='elasticnet', l1_ratio=0.2, class_weight='balanced'))),
        # ("SGDClassifier2", add_scaler(SGDClassifier(loss='log', alpha=0.01, penalty='elasticnet', l1_ratio=0.2, class_weight='balanced'))),
        # ("Baggin Logistic Classifier", add_scaler(BaggingClassifier(base_estimator=LogisticRegression(class_weight='balanced')))),
        # ("Baggin Logistic SGDC", add_scaler(BaggingClassifier(base_estimator=SGDClassifier(loss='log', penalty='elasticnet', l1_ratio=0.2, class_weight='balanced')))),
        # ('XGBoost classifier', add_scaler(xgb.XGBClassifier( objective='binary:logistic', n_estimators=120, scale_pos_weight=0.1, max_delta_step=1, reg_alpha=0.0020, gamma=0.002))),
        ('XGBoost classifier', add_scaler(xgb.XGBClassifier( objective='binary:logistic', n_estimators=220, scale_pos_weight=209, max_delta_step=1, reg_alpha=0.03, gamma=0.003))),
        # ('XGBoost classifier', add_scaler(xgb.XGBClassifier( objective='binary:logistic', n_estimators=4, max_delta_step=1,))),
        # ('XGBoost classifier', add_scaler(xgb.XGBClassifier( objective='binary:logistic', n_estimators=5,))),
        ]


# Usage: ./classification.py <x_array.npy> <y_array.npy>
# x_array.npy - features array
# y_array.npy - results array
if __name__ == "__main__":
    x_file = sys.argv[1]
    y_file = sys.argv[2]

    print("Reading data ...")
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    # classify if user is going to spent more money in next three weeks
    y_array -= x_array[:, 0]
    y = np.where(y_array > 0.1, 1, 0)

    x_array, y = shuffle(x_array, y)
    x_array = scale(x_array)
    ratio = float(np.sum(y==0) / np.sum(y==1))
    print(ratio)

    print("Testing classifiers")
    # set number of threads for XGBoost
    os.environ["OMP_NUM_THREADS"] = "4"

    for name, cls in classifiers:
        scores = cross_val_score(cls, x_array, y, scoring='roc_auc', cv=5)
        print("---- Scores of %s ----" % name)
        print("Auc: {0:.2f} (+/-) {1:.3f}".format(scores.mean(), scores.std()))
        print("Min: {0:.2f} Max {1:.3f}".format(scores.min(), scores.max()))
        cls.fit(x_array, y, eval_metric='auc')
        classes = cls.predict(x_array)
        print("Size of true on the whole set: %d" % (np.where(classes == 1)[0].shape[0]))
        print()

    for name, cls in classifiers:
        scores = cross_val_score(cls, x_array, y, scoring='recall', cv=5)
        print("---- Scores of %s ----" % name)
        print("Recall: {0:.2f} (+/-) {1:.3f}".format(scores.mean(), scores.std()))
        print("Min: {0:.2f} Max {1:.3f}".format(scores.min(), scores.max()))
        # classes = cls.fit(x_array, y).predict(x_array)
        # print("Size of true on the whole set: %d" % (np.where(classes == 1)[0].shape[0]))
        print()

    X_train, X_test, Y_train, Y_test = train_test_split(x_array, y, stratify=y)
    darray = xgb.DMatrix(x_array, label=y)

    cls = xgb.XGBClassifier(
            objective='binary:logistic',
            n_estimators=50,
            # scale_pos_weight=0.1,
            # max_delta_step=1,
            # reg_alpha=0.0030,
            # gamma=0.003
            )

    cls.fit(X_train, Y_train,
            eval_set=[(X_train, Y_train), (X_test, Y_test)],
            eval_metric='auc',
            verbose=True)

    print()
    bst = cls.booster()
    xgb.plot_importance(bst)
    xgb.plot_tree(bst, num_trees=2)
    matrix = xgb.DMatrix(scale(x_array))
    classes_probs = bst.predict(matrix)
    print(classes_probs.shape)
    print(classes_probs[classes_probs >= 0.5].size)

    
    params = {'eval_metric': 'auc', 'objective':'binary:logistic', 'nthread':4, 'scale_pos_weight':ratio, "alpha": 0.03, 'gamama': 0.003, 'max_delta_step': 1}
    dtrain = xgb.DMatrix(X_train, label=Y_train)
    dtest = xgb.DMatrix(X_test, label=Y_test)
    evals = [(dtrain, 'train'), (dtest, 'test')]
    bst = xgb.train(params, dtrain, 220, evals=evals, verbose_eval=True)
    class_prob = bst.predict(darray)
    print(class_prob[class_prob > 0.5].size)
    y_2 = np.zeros(class_prob.shape[0])
    y_2[class_prob > 0.5] = 1
    print(roc_auc_score(y, y_2))
