#!/usr/bin/python
import numpy as np
import sys
from matplotlib import pyplot as plt
from data import column_names, curr_cols
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, MeanShift, DBSCAN

def plot_two_dim_features(X):
    p = PCA(n_components=2)
    X_new = p.fit_transform(X)
    plt.figure()
    plt.title("Features distribution after PCA 2")
    plt.scatter(X_new[: ,0], X_new[: ,1])

    plt.show()

def plot_histogram(y, cumulative=False):
    plt.figure()
    plt.title("Histogram - y" + " cumulative" if cumulative else "")
    plt.hist(y, bins=1000, cumulative=cumulative)
    plt.show()

def plot_clusters_kmeans(X):
    print("Calculating clusters")
    y_pred = KMeans(n_clusters=3).fit_predict(X)

    print("PCA reduction")
    p = PCA(n_components=2)
    X_new = p.fit_transform(X)

    print("Printing plots")
    plt.figure()
    plt.title("KMeans clusters - 3")
    plt.scatter(X_new[:, 0], X_new[:, 1], c=y_pred)
    plt.show()


if __name__ == "__main__":
    x_file = sys.argv[1]
    y_file = sys.argv[2]
    x_array = np.load(x_file)
    y_array = np.load(y_file)

    # plot_two_dim_features(x_array)
    # plot_histogram(y_array, False)
    # plot_histogram(y_array, True)
    plot_clusters_kmeans(x_array)
