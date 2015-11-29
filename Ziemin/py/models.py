import numpy as np
from data import shuffle, devide, column_indexes
from sklearn import linear_model, pipeline, cross_validation, kernel_ridge, \
        svm, tree, ensemble, isotonic
from sklearn.base import BaseEstimator, TransformerMixin


# Trains model on the train set
# @return mean squared error from prediction on the test set
def try_regr_model(model, x_train, y_train, x_test, y_test, metric):
    model.fit(x_train, y_train)
    return metric(model.predict(x_test), y_test)


# given input data instance of this class runs different models
class RegressionModelTester:

    def __init__(self, x_array, y_array, metric, cv_iter_provider):
        self.x_array = x_array
        self.y_array = y_array
        self.metric = metric
        self.cv_iter_provider = cv_iter_provider

    # trains models on some training subset and then tries to predict
    # results on the testing subset
    # @return a dictionary (model_name, (average score, score std))
    def run_models(self, models):
        errors = { }

        for m in models:
            print("Checking model: ", m.name)
            scores = cross_validation.cross_val_score(
                    m, self.x_array, self.y_array,
                    scoring=self.metric, cv=self.cv_iter_provider())
            errors[m.name] = (scores.mean(), scores.std()*2)

        return errors

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


# --- models instances -------------------------
linear_regr = linear_model.LinearRegression(n_jobs=-1)
linear_regr.name = "Linear regression"

ridge_regr = linear_model.Ridge(alpha=0.1, normalize=True)
ridge_regr.name = "Ridge regression"

ridge_regr_cv = linear_model.RidgeCV(
        alphas=[0.005, 0.01, 0.03, 0.08],
        scoring='mean_squared_error',
        fit_intercept=True,
        cv=5,
        normalize=True)
ridge_regr_cv.name = "Ridge regression - cv"

kernel_ridge_regr = kernel_ridge.KernelRidge(kernel='rbf', alpha=0.1)
kernel_ridge_regr.name = "Kernel ridge regression"

svm_svr_regr = svm.SVR(cache_size=1500, tol=1e-1)
svm_svr_regr.name = "svm - SVR"

decision_tree_regr = tree.DecisionTreeRegressor()
decision_tree_regr.name = "Decision Tree Regressor"

ada_boost_regr = ensemble.AdaBoostRegressor(n_estimators=100)
ada_boost_regr.name = "Ada Boost regressor"

gradient_boosting_regr = ensemble.GradientBoostingRegressor(
        loss='quantile', min_samples_leaf=4, n_estimators=100)
gradient_boosting_regr.name = "Gradient boosting regressor"

random_forest_regressor = ensemble.RandomForestRegressor(n_estimators=50)
random_forest_regressor.name = "Random Forest Regressor"

lasso = linear_model.Lasso(alpha=0.1, normalize=True)
lasso.name = "Lasso"

bayes_regr = linear_model.BayesianRidge(normalize=True)
bayes_regr.name = "Bayesian regression"

average = AverageModel()
first_week = FirstWeekCopyModel(column_indexes["first_week"])

lasso_lars_regr = linear_model.LassoLars(alpha=0.0005, normalize=True)
lasso_lars_regr.name = "Lasso lars regr"

only_lars_regr = linear_model.Lars()
only_lars_regr.name = "Only LARS"

elastic_net_regr = linear_model.ElasticNet(alpha=0.1)
elastic_net_regr.name = "Elastic Net"

ard_regr = linear_model.ARDRegression()
ard_regr.name = "ARD regr"

sgd_regr = linear_model.SGDRegressor()
sgd_regr.name = "SGD regr"

isotonic_regr = isotonic.IsotonicRegression()
isotonic_regr.name = "Isotonic regression"

bagging_lin_regr = ensemble.BaggingRegressor(linear_model.LinearRegression())
bagging_lin_regr.name = "Bagging linear regression"

bagging_decision_tree = ensemble.BaggingRegressor(tree.DecisionTreeRegressor())
bagging_decision_tree.name = "Bagging dec tree regressor"

combiner_regr = ModelCombinator(
        [
            linear_model.Ridge(alpha=0.05),
            ensemble.GradientBoostingRegressor(n_estimators=25)
        ],
        linear_regr)
combiner_regr.name = "Combiner"
