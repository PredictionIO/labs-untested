import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import matplotlib
import seaborn as sns
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
from scipy.sparse import lil_matrix, kron,identity
from scipy.sparse.linalg import lsqr

users = pandas.read_csv("data/users.csv", header=None)
conversions = pandas.read_csv("data/conversions.csv", header=None)
items = pandas.read_csv("data/items.csv", header=None)
users_ads = pandas.read_csv("data/users_ads.csv", header=None)

users.columns = ['userId', 'registerCountry', 'signupTime']
conversions.columns = ['userId', 'itemId', 'price', 'quantity', 'timestamp']
items.columns = ['itemId', 'style', 'personality', 'color', 'theme', 'price', 'category']
users_ads.columns = ['userId', 'utmSource', 'utmCampaign', 'utmMedium', 'utmTerm', 'utmContent']

users.signupTime = pandas.to_datetime(users.signupTime)
conversions.timestamp = pandas.to_datetime(conversions.timestamp)

item_indices = items.itemId.value_counts().index
item_indices = pandas.Series(range(len(item_indices)), index = item_indices)

user_indices = users.userId.value_counts().index
user_indices = pandas.Series(range(len(user_indices)), index = user_indices)

##########################
# expressing users as R^d item convesrion count vectors
def users_as_real_vectors(users_df):
	user_number_of_purchases = lil_matrix((user_indices.size, item_indices.size))
	for index, row in conversions.iterrows():
		if not (row.itemId in item_indices.index) or not (row.userId in user_indices.index):
			continue
		item_index = item_indices[row.itemId]
		user_index = user_indices[row.userId]
		user_number_of_purchases[user_index, item_index] += row.quantity
	print(user_number_of_purchases.size)
	return user_number_of_purchases

##########################
# running SVM on the sparse data
def run_svm():
	svd = decomposition.TruncatedSVD(algorithm='randomized', n_components=2, n_iter=5, tol=0.0001)
	X = users_as_real_vectors(users)
	p = svd.fit_transform(X)
	plt.figure()
	plt.scatter(p[:,0], p[:,1])
	plt.show()

run_svm()