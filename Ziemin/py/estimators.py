import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge, LinearRegression
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import scale, MinMaxScaler
from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN
from sklearn.svm import OneClassSVM
from data import curr_index
import xgboost as xgb

def prepare_bayes(cls):
    return Pipeline([
        ("prepare_bayes", MinMaxScaler()),
        ("cls", cls)])


# Basic model returning always an average from the train set
class AverageModel(BaseEstimator):

    def __init__(self):
        self.name = "Average"

    def fit(self, x_train, y_train):
        self.mean = np.mean(y_train)

    def predict(self, x_test):
        m_array = np.empty(len(x_test))
        m_array.fill(self.mean)
        return m_array

# Basic model returning always the result of the first week
class FirstWeekCopyModel(BaseEstimator):

    # takes the number of the column representing the first week
    def __init__(self, fw_col_num):
        self.name = "First Week Copy"
        self.fw_col_num = fw_col_num

    def fit(self, x_train, y_train):
        pass

    def predict(self, x_test):
        m_array = x_test[:, self.fw_col_num]
        return m_array

# combines results from different models and then returns them as features
class ModelCombinator(BaseEstimator):

    def __init__(self, estimators, reducer):
        self.estimators_ = estimators
        self.reducer_ = reducer

    def fit(self, X, y):
        preds = []
        for e in self.estimators_:
            e.fit(X, y)
            preds.append(e.predict(X))
            preds[-1] = preds[-1].reshape(preds[-1].shape[0], 1)
        new_features = np.concatenate(preds, axis=1)
        self.reducer_.fit(new_features, y)
        print(self.reducer_.coef_)

    def predict(self, X):
        results = []
        for e in self.estimators_:
            results.append(e.predict(X))
            results[-1] = results[-1].reshape(results[-1].shape[0], 1)
        new_features = np.concatenate(results, axis=1)
        return self.reducer_.predict(new_features)

    def get_params(self, deep=True):
        return { "estimators": self.estimators_, "reducer": self.reducer_ }


# runs KMeans clustering on features and then trains separately reducers for every cluster
class ClusteringEnsemble(BaseEstimator):

    def __init__(self, estimator_const=LinearRegression, n_clusters=2):
        self.estimator_const_ = estimator_const
        self.n_clusters_ = n_clusters
        self.clustering = MiniBatchKMeans(n_clusters=self.n_clusters_)

    def get_params(self, deep=True):
        return { "n_clusters": self.n_clusters_}

    def fit(self, X, y):
        print("Training KMeans")
        colors = self.clustering.fit_predict(X).reshape(X.shape[0])

        print("Training Estimators")
        # each estimator is assigned to one cluster
        self.estimators = [self.estimator_const_() for i in range(self.n_clusters_)]
        for i in range(self.n_clusters_):
            rows = colors == i
            self.estimators[i].fit(X[rows], y[rows])

    def predict(self, X):
        y = np.zeros(X.shape[0])
        print("Predicting clusters")
        colors = self.clustering.predict(X)

        print("Estimating results")
        for i in range(self.n_clusters_):
            rows = colors == i
            y[rows] = self.estimators[i].predict(X[rows])

        return y


# trains only on positive views_count
class FirstWeek0Ensemble(BaseEstimator):

    def __init__(self, estimator_const=LinearRegression):
        self.estimator_const_ = estimator_const

    def get_params(self, deep=True):
        return {}

    def fit(self, X, y):
        bad = X[:, 4] == 0
        good = X[:, 4] > 0

        print("Training Estimators")
        self.good_estimator = self.estimator_const_()
        self.bad_estimator = self.estimator_const_()
        if(y[good].size > 0):
            self.good_estimator.fit(X[good], y[good])
        if(y[bad].size > 0):
            self.bad_estimator.fit(X[bad], y[bad])


    def predict(self, X):
        y = X[:, 0].reshape(X.shape[0])
        bad = X[:, 4] == 0
        good = X[:, 4] > 0

        print("Estimating results")
        if(y[good].size > 0):
            y[good] = self.good_estimator.predict(X[good])

        return y


# trains model only for samples classified as users who will spend anything in 
# the rest of the month after the first week
# those are classified using LogisticRegression
class LogisticRegressionSeparator(BaseEstimator):

    def get_params(self, deep=True):
        return {}

    def fit(self, X, y):
        # lets predict which users will spend anything later
        classes = y - X[:, 0]
        classes = np.where(classes > 0.1, 1, 0)

        self.classifier = LogisticRegression(
                class_weight='balanced')

        self.classifier.fit(X, classes)
        results = self.classifier.predict(X)
        results = results == 1

        self.estimator = Ridge(alpha=0.05)
        self.estimator.fit(X[results], y[results])

    def predict(self, X):
        y = X[:,0].reshape(X.shape[0])
        labels = (self.classifier.predict(X) == 1)
        y[labels] = self.estimator.predict(X[labels])
        return y


# Trains two linear models separately for two categories:
# a) users who were classified as those who will spend anything after a week,
#    these users are found by SVM novely separator
# b) inliers - those who will not spend anything more
class NoveltySeparator(BaseEstimator):

    def get_params(self, deep=True):
        return {}

    def fit(self, X, y):
        # lets treat users spending something in the rest of the month as outliers
        inliers = y - X[:, 0]
        inliers = np.where(inliers < 0.1, True, False)

        self.detector = OneClassSVM(nu=0.05, cache_size=2000, verbose=True)

        # training only on inliers
        print("Training detector")
        self.detector.fit(X[inliers])
        results = self.detector.predict(X).reshape(X.shape[0])
        # predicted
        inliers = results == 1
        outliers = results == -1

        print("Training estimators")
        self.est_inliers = Ridge(alpha=0.05)
        self.est_outliers = Ridge(alpha=0.05)
        self.est_inliers.fit(X[inliers], y[inliers])
        self.est_inliers.fit(X[outliers], y[outliers])

    def predict(self, X):

        y = np.zeros(X.shape[0])

        labels = self.detector.predict(X).reshape(X.shape[0])
        inliers = lables == 1
        outliers = lables == -1

        y[inliers] = self.est_inliers.predict(X[inliers])
        y[outliers] = self.est_outliers.predict(X[outliers])

        return y


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
class XGBClassifierWrapper(BaseEstimator, ClassifierMixin):

    def __init__(self, n_rounds=50, gamma=0.03, alpha=0.005, scale_pos_weight=None,
            lam=1, max_delta_step=1, nthread=4, max_depth=6, silent=1, subsample=1,
            eta=0.1, min_child_weight=1, eval_metric='auc'):

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
                "min_child_weight": min_child_weight,
                "eval_metric": eval_metric,
                "silent": silent,
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


# class wrapping xgboost regressor to work correctly
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

