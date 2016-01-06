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
from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.mllib.linalg import Vectors
import pyspark as pyspark

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
	# print(user_number_of_purchases.size)
	return user_number_of_purchases

##########################
# running SVD on the sparse data
def run_svd(X=None):
	svd = decomposition.TruncatedSVD(algorithm='randomized', n_components=2, n_iter=5, tol=0.0001)
	if X is None:
		X = users_as_real_vectors(users)
	p = svd.fit_transform(X)
	plt.figure()
	plt.scatter(p[:,0], p[:,1])
	plt.show()

##########################
# running LDA on the sparse data
def run_latent_dirichlet_allocation(X=None):
	lda = decomposition.LatentDirichletAllocation()
	if X is None:
		X = users_as_real_vectors(users)
	p = lda.fit_transform(X)
	plt.figure()
	plt.scatter(p[:,0], p[:,1])
	plt.show()

##########################
# using spark to run LDA
def lda_spark(X=None):
	if X is None:
		X = users_as_real_vectors(users)
	ldaModel = LDA.train(X, k=3)
	for topic in range(3):
	    print("Topic " + str(topic) + ":")
	    for word in range(0, ldaModel.vocabSize()):
	        print(" " + str(topics[word][topic]))

sc = pyspark.SparkContext("local", "Simple App")

usr = users_as_real_vectors(users)
# run_svd(usr)
# run_latent_dirichlet_allocation(usr)
lda_spark(usr)