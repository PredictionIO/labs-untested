#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_predict
import models


def plot_cross_val_preds(X, y, estimator):

    plt.title('Cross-Validated Predictions - %s' % estimator.name)
    predicted = cross_val_predict(estimator, X, y, cv=5)

    plt.scatter(y, predicted)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    plt.xlabel('Measured')
    plt.ylabel('Predicted')

    plt.show()


if __name__ == '__main__':
    x_file = sys.argv[1]
    y_file = sys.argv[2]

    print("Reading data ...")
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    plot_cross_val_preds(x_array, y_array, models.clustering_lin_regr)

