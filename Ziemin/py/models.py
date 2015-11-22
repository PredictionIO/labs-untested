import numpy as np
from data import shuffle, devide, column_indexes
from sklearn import linear_model

# minimum squared error metric
def mse_metric(out, y):
    return np.mean((out - y) ** 2)


# Trains model on the train set
# @return mean squared error from prediction on the test set
def try_regr_model(model, x_train, y_train, x_test, y_test, metric):
    model.fit(x_train, y_train)
    return metric(model.predict(x_test), y_test)


# given input data instance of this class runs different models
class RegressionModelTester:

    def __init__(self, x_array, y_array, metric):
        self.x_array = x_array
        self.y_array = y_array
        self.metric = metric

    # @param iter is the number of iterations
    # trains models on some training subset and then tries to predict
    # results on the testing subset
    # @return a dictionary (model_name, average MSE)
    def run_models(self, models, iters=1):
        errors = { m.name:0.0 for m in models }

        for i in range(iters):
            arr_x, arr_y = shuffle(self.x_array, self.y_array)
            x_train, y_train, x_test, y_test = devide(arr_x, arr_y, 0.75)

            for m in models:
                errors[m.name] += try_regr_model(
                            m, x_train, y_train, x_test, y_test, self.metric)

        for m in models:
            errors[m.name] /= iters

        return errors

# Basic model returning always an average from the train set
class AverageModel:

    def __init__(self):
        self.name = "Average"

    def fit(self, x_train, y_train):
        self.mean = np.mean(y_train)

    def predict(self, x_test):
        m_array = np.empty(len(x_test))
        m_array.fill(self.mean)
        return m_array

# Basic model returning always the result of the first week
class FirstWeekCopyModel:

    # takes the number of the column representing the first week
    def __init__(self, fw_col_num):
        self.name = "First Week Copy"
        self.fw_col_num = fw_col_num

    def fit(self, x_train, y_train):
        pass

    def predict(self, x_test):
        m_array = x_test[:, self.fw_col_num]
        return m_array

# --- models instances -------------------------
linear_regr = linear_model.LinearRegression(normalize=True, n_jobs=-1)
linear_regr.name = "Linear regression"

ridge_regr = linear_model.Ridge(alpha=0.1, normalize=True)
ridge_regr.name = "Ridge regression"

lasso = linear_model.Lasso(alpha=0.1, normalize=True)
lasso.name = "Lasso"

bayes_regr = linear_model.BayesianRidge(normalize=True)
bayes_regr.name = "Bayesian regression"

average = AverageModel()
first_week = FirstWeekCopyModel(column_indexes["first_week"])
