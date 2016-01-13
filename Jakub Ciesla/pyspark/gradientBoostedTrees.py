import numpy as np
from sklearn import datasets, linear_model, svm
from sklearn import cross_validation
import matplotlib.pyplot as plt
from pyspark.mllib.classification import LogisticRegressionWithSGD, LogisticRegressionWithLBFGS, SVMWithSGD
from pyspark import SparkContext
from numpy import array
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.tree import GradientBoostedTrees

# features columns: 
# 0 user_id
# 1 first_week
# 2 first_month
# 3 equal
# 4 items
# 5 views
# 6 collection_views
# 7 product_views
# 8 country
# 9 user_ads

sc = SparkContext("local", "prediction.io")

f = open("/tmp/test_ROC.csv")
data = np.loadtxt(f, delimiter=",")

Y = data[:, 3]
X = data[:, [1, 4, 5, 6, 7, 9]]

N = len(X)
iter_number = 1
ss = cross_validation.ShuffleSplit(N, n_iter=iter_number, test_size=0.2,
	random_state=0)
Err = 0.0
results = []
for train_index, test_index in ss:
	X_training, Y_training, X_test, Y_test = [], [], [], []
	for i in train_index:
		X_training.append(X[i])
		Y_training.append(Y[i])
	for i in test_index:
		X_test.append(X[i])
		Y_test.append(Y[i])
		
	parsedData = []
	for i in range(0, len(X_training)):
		parsedData.append(LabeledPoint(Y_training[i], X_training[i]))
		
	model = GradientBoostedTrees.trainClassifier(sc.parallelize(parsedData), {}, numIterations=10)
		
	testErr = 0
	for i in range(0, len(X_test)):
		a = Y_test[i]
		b = model.predict(X_test[i])
		#b = 1
		if a != b:
			testErr += 1
		
	Err += float(testErr) / float(len(X_test))

	 
print ("AVG test error: %.6f" % 
	(Err/iter_number))

