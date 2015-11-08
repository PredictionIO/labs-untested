#!/usr/bin/python
import numpy as np
import sys
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

def shuffle(x_array, y_array):
    c = np.c_[x_array.reshape(len(x_array), -1), y_array.reshape(len(y_array), -1)]
    x_array2 = c[:, :x_array.size//len(x_array)].reshape(x_array.shape)
    y_array2 = c[:, x_array.size//len(x_array):].reshape(y_array.shape)

    np.random.shuffle(c)

    return x_array2, y_array2

# Usage: ./regression_models.py <x_array.npy> <y_array.npy>
# x_array.npy - features array
# y_array.npy - results array
if __name__ == "__main__":
    x_file = sys.argv[1]
    y_file = sys.argv[2]

    print("Reading the data")
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    x_array, y_array = shuffle(x_array, y_array)

    # Polynomial features
    poly = PolynomialFeatures(degree=2)
    x_array_poly = poly.fit_transform(x_array)

    print("Checking models")

    rows = len(x_array)
    train_rows = int(0.75 * rows)

    x_train = x_array[:-train_rows]
    y_train = y_array[:-train_rows]
    x_test = x_array[train_rows:]
    y_test = y_array[train_rows:]
    x_train_poly = x_array_poly[:-train_rows]
    x_test_poly = x_array_poly[train_rows:]

    # Linear regression
    clf = linear_model.LinearRegression(normalize=True, n_jobs=-1)
    clf.fit(x_train, y_train)
    mse_lin = np.mean((clf.predict(x_test) - y_test) ** 2)
    print("MSE of linear regression: ", mse_lin)

    clf.fit(x_train_poly, y_train)
    mse_lin = np.mean((clf.predict(x_test_poly) - y_test) ** 2)
    print("MSE of linear regression (polynomial features): ", mse_lin)

    # Ridge
    clf = linear_model.Ridge(alpha=0.1, normalize=True)
    clf.fit(x_train, y_train)
    mse_ridge = np.mean((clf.predict(x_test) - y_test) ** 2)
    print("MSE of ridge regression: ", mse_ridge)

    clf.fit(x_train_poly, y_train)
    mse_ridge = np.mean((clf.predict(x_test_poly) - y_test) ** 2)
    print("MSE of ridge regression (polynomial features): ", mse_ridge)

    # Lasso
    clf = linear_model.Lasso(alpha=0.1, normalize=True)
    clf.fit(x_train, y_train)
    mse_lasso = np.mean((clf.predict(x_test) - y_test) ** 2)
    print("MSE of lasso: ", mse_lasso)

    # Bayesian ridge
    clf = linear_model.BayesianRidge(normalize=True)
    clf.fit(x_train, y_train)
    mse_bayes_ridge = np.mean((clf.predict(x_test) - y_test) ** 2)
    print("MSE of bayesian ridge regression: ", mse_bayes_ridge)

    clf.fit(x_train_poly, y_train)
    mse_bayes_ridge = np.mean((clf.predict(x_test_poly) - y_test) ** 2)
    print("MSE of bayesian ridge regression (polynomial features): ", mse_bayes_ridge)

    # average
    m_array = np.empty(len(y_test))
    m_array.fill(np.mean(y_train))
    mse_avg = np.mean((m_array - y_test) ** 2)
    print("MSE of average model: ", mse_avg)

    # first week copied
    m_array = x_test[:, 2]
    mse_first_week = np.mean((m_array - y_test) ** 2)
    print("MSE of first week copy model: ", mse_first_week)

    # first week day average scaled to 30 days
    m_array = x_test[:, 2] * (30/7)
    mse_first_week_ave = np.mean((m_array - y_test) ** 2)
    print("MSE of first week day average scaled to 30: ", mse_first_week_ave)
