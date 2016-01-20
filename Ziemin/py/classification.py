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
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from sklearn.ensemble import RandomForestRegressor, AdaBoostClassifier, \
        GradientBoostingClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import roc_auc_score, recall_score, precision_score, f1_score, \
        fbeta_score
from sklearn.grid_search import GridSearchCV
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

# class wrapping xgboost classifier to work correctly
# with sklearn
class XGBWrapper(BaseEstimator, ClassifierMixin):

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
        params["scale_pos_weight"] = ratio
        params['objective'] = "binary:logistic"
        params['silent'] = 1
        params['lambda'] = params['lam']
        del params['lam']

        dtrain = xgb.DMatrix(X, label=y)
        self.bst = xgb.train(params, dtrain, self.params["n_rounds"], verbose_eval=False)

    def predict(self, X):
        class_prob = self.predict_proba(X)[:,1]
        y = np.zeros(X.shape[0])
        y[class_prob >= 0.5] = 1
        return y

    def predict_proba(self, X):
        dtest = xgb.DMatrix(X)
        class_prob = self.bst.predict(dtest)
        y0 = np.repeat(1.0, class_prob.size)
        y0 -= class_prob

        return np.c_[y0, class_prob]

    def decision_function(self, X):
        return self.predict_proba(X)


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
        # ('XGBoost classifier', add_scaler(xgb.XGBClassifier( objective='binary:logistic', n_estimators=100, scale_pos_weight=71773, max_delta_step=1, reg_alpha=0.03, gamma=0.003))),
        # ('XGBoost classifier', add_scaler(xgb.XGBClassifier( objective='binary:logistic', n_estimators=4, max_delta_step=1,))),
        # ('XGBoost classifier', add_scaler(xgb.XGBClassifier( objective='binary:logistic', n_estimators=5,))),
        ('XGBoost wrapper', XGBWrapper(n_rounds=3, max_delta_step=1, alpha=0.04, gamma=0.005)),
        ]


# ---------------------------------------------
# y - creation functions
# ---------------------------------------------

def get_y_three_weeks(x_array, y_array):
    # classify if user is going to spent more money in next three weeks
    y_array -= x_array[:, 0]
    y = np.where(y_array > 0.1, 1, 0)
    return y

def get_y_more_than_5000(x_array, y_array):
    y = np.where(y_array >= 5000, 1, 0)
    return y

# --------------------------------------------
# grid search
# --------------------------------------------

def xgb_wrapper_gc(x_array, y):
    from sklearn.metrics import make_scorer
    scorer = make_scorer(fbeta_score, beta=10)
    parameters = {
            'n_rounds': [70, 80],
            'alpha': [.01, .05],
            'gamma': [0.007, 0.01, 0.03, 0.06, 0.1],
            # 'max_delta_step': [1, 2],
            # 'lam': [.5, 1]
            'max_depth': [8],
            'min_child_weight': [1]
            }
    cls = XGBWrapper()
    gc = GridSearchCV(cls, parameters, cv=5, verbose=10, scoring='roc_auc')
    gc.fit(x_array, y)
    print(gc.best_params_)

# ---------------------------------------------
# testing functions
# ---------------------------------------------

# manual cross validation with xgboost regular python API
def cv_xgboost_cl_regular(x_array, y):
    print("-- CV for XGBoost classifier (> 5000 problem) - regular --")

    skf = StratifiedKFold(y, n_folds=5)
    params = {
            'eval_metric': 'auc',
            'objective':'binary:logistic',
            'nthread': 4,
            "alpha": 0.04,
            'gamma': 0.005,
            'max_delta_step': 1,
            'silent': 1,
            'max_depth': 7,
            # 'subsample': 0.99,
            'eta': 0.08,
            # 'min_child_weight': 1.005
            }
    rocs = []
    recs = []
    precs = []
    f1s = []
    scores_dict = { "Recall": [], "Roc_Auc": [], "Precision": [], "F-beta": [] }
    for train_index, test_index in skf:
        # update ratio for training set
        ratio = float(np.sum(y[train_index]==0) / np.sum(y[train_index]==1))
        params["scale_pos_weight"] = ratio
        # training and prediction
        dtrain = xgb.DMatrix(x_array[train_index], label=y[train_index])
        dtest = xgb.DMatrix(x_array[test_index], label=y[test_index])
        bst = xgb.train(params, dtrain, 100, verbose_eval=True)
        class_prob = bst.predict(dtest)
        # scores evaluation
        y_2 = np.zeros(y[test_index].size)
        y_2[class_prob >= 0.5] = 1
        roc_sc = roc_auc_score(y[test_index], y_2)
        rec_sc = recall_score(y[test_index], y_2)
        prec_sc = precision_score(y[test_index], y_2)
        fb_sc = fbeta_score(y[test_index], y_2, beta=10)
        print("Roc auc score: ", roc_sc)
        print("Recall score: ", rec_sc)
        print("Precision score: ", prec_sc)
        print("F-beta score: ", fb_sc)
        print("Number of qualified as true: ", class_prob[class_prob >= 0.5].size)
        print("Number of real true: ", np.sum(y[test_index]))
        scores_dict["Roc_Auc"].append(roc_sc)
        scores_dict["Recall"].append(rec_sc)
        scores_dict["Precision"].append(prec_sc)
        scores_dict["F-beta"].append(fb_sc)

    print()
    for name, scores in scores_dict.items():
        scores = np.array(scores)
        print("{2}: {0:.2f} (+/-) {1:.3f}".format(scores.mean(), scores.std(), name))
        print("Min: {0:.2f} Max {1:.3f}".format(scores.min(), scores.max()))


def cv_xgboost_cl_ensemble(x_array, y):
    print("-- CV for XGBoost classifier (> 5000 problem) - sklearn --")

    skf = StratifiedKFold(y, n_folds=5)
    params = {
            'eval_metric': 'auc',
            'nthread': 4,
            "alpha": 0.04,
            'gamma': 0.005,
            'max_delta_step': 1,
            'max_depth': 8,
            'subsample': 0.99,
            'eta': 0.1,
            # 'min_child_weight': 1.02
            }

    rocs = []
    recs = []
    precs = []
    f1s = []
    scores_dict = { "Recall": [], "Roc_Auc": [], "Precision": [], "F-beta": [] }

    for train_index, test_index in skf:
        cls = XGBWrapper(n_rounds=80, **params)
        cls = BaggingClassifier(cls, 8, max_samples=0.9, n_jobs=1)
        # training and prediction
        cls.fit(x_array[train_index], y[train_index])
        class_prob = cls.predict_proba(x_array[test_index])[:,1]
        # scores evaluation
        y_2 = np.zeros(y[test_index].size)
        y_2[class_prob >= 0.5] = 1

        roc_sc = roc_auc_score(y[test_index], y_2)
        rec_sc = recall_score(y[test_index], y_2)
        prec_sc = precision_score(y[test_index], y_2)
        fb_sc = fbeta_score(y[test_index], y_2, beta=10)
        print("Roc auc score: ", roc_sc)
        print("Recall score: ", rec_sc)
        print("Precision score: ", prec_sc)
        print("F-beta score: ", fb_sc)
        print("Number of qualified as true: ", class_prob[class_prob >= 0.5].size)
        print("Number of real true: ", np.sum(y[test_index]))
        scores_dict["Roc_Auc"].append(roc_sc)
        scores_dict["Recall"].append(rec_sc)
        scores_dict["Precision"].append(prec_sc)
        scores_dict["F-beta"].append(fb_sc)

    print()
    for name, scores in scores_dict.items():
        scores = np.array(scores)
        print("{2}: {0:.2f} (+/-) {1:.3f}".format(scores.mean(), scores.std(), name))
        print("Min: {0:.2f} Max {1:.3f}".format(scores.min(), scores.max()))


def run_once_xgboost(x_array, y):
    # stratified xfold for xboost
    X_train, X_test, Y_train, Y_test = train_test_split(x_array, y, stratify=y)
    darray = xgb.DMatrix(x_array, label=y)

    ratio = float(np.sum(y==0) / np.sum(y==1))
    print("Ratio false/true = ", ratio)

    params = {'eval_metric': 'auc', 'objective':'binary:logistic', 'nthread':4, 'scale_pos_weight':ratio, "alpha": 0.03, 'gamama': 0.003, 'max_delta_step': 1}
    dtrain = xgb.DMatrix(X_train, label=Y_train)
    dtest = xgb.DMatrix(X_test, label=Y_test)
    evals = [(dtrain, 'train'), (dtest, 'test')]
    bst = xgb.train(params, dtrain, 50, evals=evals, verbose_eval=True)
    class_prob = bst.predict(darray)
    print("Number of qualified as true: ", class_prob[class_prob > 0.5].size)
    print("Number of real true: ", np.sum(y))
    y_2 = np.zeros(class_prob.shape[0])
    y_2[class_prob > 0.5] = 1
    print("Roc auc score: ", roc_auc_score(y, y_2))
    print("Recall score: ", recall_score(y, y_2))


def test_models_in_loop(x_array, y):
    for name, cls in classifiers:
        scores = cross_val_score(cls, x_array, y, scoring='roc_auc', cv=5)
        print("---- Scores of %s ----" % name)
        print("Auc: {0:.2f} (+/-) {1:.3f}".format(scores.mean(), scores.std()))
        print("Min: {0:.2f} Max {1:.3f}".format(scores.min(), scores.max()))
        # cls.fit(x_array, y, eval_metric='auc')
        # classes = cls.predict(x_array)
        # print("Size of true on the whole set: %d" % (np.where(classes == 1)[0].shape[0]))
        print()

    for name, cls in classifiers:
        scores = cross_val_score(cls, x_array, y, scoring='recall', cv=5)
        print("---- Scores of %s ----" % name)
        print("Recall: {0:.2f} (+/-) {1:.3f}".format(scores.mean(), scores.std()))
        print("Min: {0:.2f} Max {1:.3f}".format(scores.min(), scores.max()))
        # classes = cls.fit(x_array, y).predict(x_array)
        # print("Size of true on the whole set: %d" % (np.where(classes == 1)[0].shape[0]))
        print()


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
    y = get_y_more_than_5000(x_array, y_array)

    x_array, y = shuffle(x_array, y)
    x_array = scale(x_array)

    print("Testing classifiers ...")
    cv_xgboost_cl_regular(x_array, y)
    # cv_xgboost_cl_ensemble(x_array, y)
    # test_models_in_loop(x_array, y)
    # xgb_wrapper_gc(x_array, y)
