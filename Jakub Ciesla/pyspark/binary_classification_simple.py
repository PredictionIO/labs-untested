import numpy as np
from sklearn import datasets, linear_model, svm
from sklearn import cross_validation
import matplotlib.pyplot as plt
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark import SparkContext
from numpy import array
from pyspark.mllib.regression import LabeledPoint

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

#f = sc.textFile("/tmp/test_ROC.csv")
#data = f.map(lambda line: array([float(x) for x in line.replace(',', ' ').split(' ')]))

Y = data[:, 3]
X = data[:, [1, 4, 5, 6, 7, 8, 9]]

N = len(X)
parsedData = []
for i in range(0, N):
	parsedData.append(LabeledPoint(Y[i], X[i]))

#X = [LabeledPoint(1.0, [1.0, 0.0, 3.0])]

print "Dataset prepared", "\n"

model = LogisticRegressionWithSGD.train(sc.parallelize(parsedData))
# Build the model

trainErr = 0
for i in range(0, N):
	a = Y[i]
	b = model.predict(X[i])
	#print(str(a) + " " + str(b))
	if a != b:
		trainErr += 1
# Evaluating the model on training data

print trainErr
print N
print("Training Error = " + str(float(trainErr) / float(N)))

