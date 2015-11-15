#!/usr/bin/python
import numpy as np
import sys
from matplotlib import pyplot as plt
from prepare_files import usecols
from data import column_names

labels = [column_names[i] for i in usecols]

# returns correlation coefficients matrix
def correlations(x_array):
    return np.corrcoef(x_array, rowvar=0)

if __name__ == "__main__":
    x_file = sys.argv[1]
    x_array = np.load(x_file)
    cors = correlations(x_array)

    # print correlation matrix between used features
    plt.matshow(cors, cmap=plt.cm.Blues)
    plt.title("Features correlations")
    plt.xticks(np.arange(len(usecols)), labels)
    plt.yticks(np.arange(len(usecols)), labels)
    plt.show()
