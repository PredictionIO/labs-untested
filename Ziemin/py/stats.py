#!/usr/bin/python
import numpy as np
import sys
from matplotlib import pyplot as plt
from data import column_names, curr_cols

labels = [column_names[i] for i in curr_cols] + ["y"]

# returns correlation coefficients matrix
def correlations(x_array):
    return np.corrcoef(x_array, rowvar=0)

if __name__ == "__main__":
    x_file = sys.argv[1]
    y_file = sys.argv[2]
    x_array = np.load(x_file)
    y_array = np.load(y_file)
    cors = correlations(np.c_[x_array, y_array])

    # print correlation matrix between used features
    plt.matshow(cors, cmap=plt.cm.Blues)
    plt.title("Features correlations (with result also)")
    plt.xticks(np.arange(len(curr_cols)+1), labels)
    plt.yticks(np.arange(len(curr_cols)+1), labels)
    plt.show()
