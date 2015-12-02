#!/usr/bin/python
import sys
import numpy as np
import data
from sklearn.cross_validation import cross_val_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle

# Usage: ./classification.py <x_array.npy> <y_array.npy>
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

    # classify if user is going to spent more money in next three weeks
    y_array -= x_array[:, 0]
    y = np.where(y_array > 0.1, 1, 0)

    x_array, y = shuffle(x_array, y)

    clf = Pipeline([('scaler', StandardScaler()), ('clf', SVC(class_weight='balanced', cache_size=1500))])
    # scores = cross_val_score(clf, x_array, y, scoring='recall', cv=5, n_jobs=-1)
    # print(scores.mean())

    # clf = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression(class_weight='balanced'))])
    scores = cross_val_score(clf, x_array, y, scoring='recall', cv=5, n_jobs=-1)
    print("Recall: {0:.2f} (+/-) {0:.3f}".format(scores.mean(), scores.std()))

