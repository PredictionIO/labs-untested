import numpy as np
from sklearn import datasets, linear_model, svm
from sklearn import cross_validation
import matplotlib.pyplot as plt
from pyspark.mllib.classification import LogisticRegressionWithSGD, LogisticRegressionWithLBFGS, SVMWithSGD
from pyspark import SparkContext
from numpy import array
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc

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
		
	model = LogisticRegressionWithSGD.train(sc.parallelize(parsedData))
	model.clearThreshold()
	probas = []
	
	for i in range(0, len(X_test)):
		b = model.predict(X_test[i])
		probas.append(b)
	# Compute ROC curve and area the curve
    	tpr, fpr, thresholds = roc_curve(Y_test, probas)
    	roc_auc = auc(fpr, tpr)
    	plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)' % (roc_auc))
	
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
	 

