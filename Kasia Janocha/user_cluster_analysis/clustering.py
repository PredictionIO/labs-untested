what_to_run = "SPARK_LDA" # "SPARK_LDA", "LDA", "SVN", "SPARK_GMM", "" 

import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import time
import datetime
import matplotlib
import seaborn as sns
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
from scipy.sparse import lil_matrix, kron,identity
from scipy.sparse.linalg import lsqr

from pyspark.mllib.clustering import LDA, LDAModel, GaussianMixture
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.stat.distribution import MultivariateGaussian
from pyspark.mllib.linalg import SparseVector, _convert_to_vector, DenseVector
from pyspark.mllib.feature import PCA as sparkPCA
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
# 
# def users_as_real_vectors_no_outstanders(users_df):
# 	user_number_of_purchases = users_as_real_vectors(users_df)
# 	for x in xrange(1,10):
# 		pass
# 	return user_number_of_purchases


##########################
# expressing users as sparse data passable to pyspark.mllib.clustering
def users_as_parallelizable_sparse_data(initial_sparse_data):
	user_number_of_purchases = []
	cnv = conversions.sort(["userId"])
	prev_user_id = "Initializing"
	current_dict = {}
	for index, row in cnv.iterrows():
		current_user_id = row.userId
		if not (row.itemId in item_indices.index) or not (row.userId in user_indices.index):
			continue
		item_index = item_indices[row.itemId]
		user_index = user_indices[row.userId]
		# transactions are sorted by userId
		if current_user_id == prev_user_id:	
			if item_index in current_dict:
				current_dict[item_index] += row.quantity
			else:
				current_dict[item_index] = row.quantity
			continue
		user_number_of_purchases.append(SparseVector(item_indices.size, current_dict))
		current_dict = {}
		prev_user_id = current_user_id
	return user_number_of_purchases

##########################
# running SVD on the sparse data
def run_svd(X=None, show=True):
	svd = decomposition.TruncatedSVD(algorithm='randomized', n_components=2, n_iter=5, tol=0.0001)
	if X is None:
		X = users_as_real_vectors(users)
	p = svd.fit_transform(X)
	mask = (p[:,0]*p[:,0]+p[:,1]*p[:,1] < 18)
	if show:
		p = p[mask]
		plt.figure()
		plt.scatter(p[:,0], p[:,1])
		plt.show()
	return mask

##########################
# running LDA on the sparse data
def run_latent_dirichlet_allocation(X=None):
	lda = decomposition.LatentDirichletAllocation()
	if X is None:
		X = users_as_real_vectors(users)
	p = lda.fit_transform(X)
	mask = (p[:,0]*p[:,0]+p[:,1]*p[:,1] < 12)
	p = p[mask]
	plt.figure()
	plt.scatter(p[:,0], p[:,1])
	plt.show()

##########################
# using spark to run LDA
def lda_spark(sc, X=None, clusters=3):
	if X is None:
		X = users_as_parallelizable_sparse_data(users)
	X = sc.parallelize(X)
	X = X.zipWithIndex().map(lambda x: [x[1], x[0]]).cache()
	ldaModel = LDA.train(X, k=clusters)
	topics = ldaModel.topicsMatrix()
	f, (ax1) = sns.plt.subplots(1, sharex=False, sharey=False)
	f.suptitle("Results of running LDA on spark", fontsize=20)
	ax1.set_title("Heatmap over topics matrix")
	sns.heatmap(topics, ax=ax1)
	# for topic in range(3):
	#     print("Topic " + str(topic) + ":")
	#     for word in range(0, ldaModel.vocabSize()):
	#         print(" " + str(topics[word][topic]))

##########################
def pca_spark(sc, X=None, k=2):
	if X is None:
		X = users_as_parallelizable_sparse_data(users)
	X = sc.parallelize(X)
	model = sparkPCA(k).fit(X)
	transformed = model.transform(X)

##########################
def gmm_spark(sc, X=None, clusters=3):
	if X is None:
		X = users_as_parallelizable_sparse_data(users)
	X = sc.parallelize(X)
	gmm = GaussianMixture.train(X, k=clusters)
	for i in range(2):
		print ("weight = ", gmm.weights[i], "mu = ", gmm.gaussians[i].mu, "sigma = ", gmm.gaussians[i].sigma.toArray())

if "SPARK" in what_to_run:
	sc = pyspark.SparkContext("local[7]", "Simple App")
	conf = pyspark.SparkConf()
	conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
	conf.set("spark.storage.memoryFraction", "0.x")
	conf.set("spark.executor.cores", "70")
	conf.set("spark.executor.memory", "20G")
	if "PCA" in what_to_run:
		pca_spark(sc)
	if "LDA" in what_to_run:
		lda_spark(sc)
	if "GMM" in what_to_run:
		gmm_spark(sc)

else:
	import random
	users = random.sample(set(users.index), int(0.005*len(users.index)))
	usr = users_as_real_vectors(users)
	if "SVD" in what_to_run:
		run_svd(usr)
	if "LDA" in what_to_run:
		run_latent_dirichlet_allocation(usr)
