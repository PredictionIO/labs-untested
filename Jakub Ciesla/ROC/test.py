import numpy as np
from sklearn import datasets, linear_model, svm
from sklearn import cross_validation
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

f = open("test_ROC.csv")
data = np.loadtxt(f, delimiter=",")

Y = data[:, 3]
X = data[:, [1, 4, 5, 6, 7, 8, 9]]

X_training, X_test, Y_training, Y_test = cross_validation.train_test_split(
	X, Y, test_size=0.2, random_state=2)


print "Dataset prepared", "\n"

# average as result
avg = np.mean(Y_training)
print avg
result = np.mean((Y_test - avg) ** 2)
print "Average: ", result, "\n"
####################


#ShuffleSplit with linear regression
N = len(X)
iter_number = 1
ss = cross_validation.ShuffleSplit(N, n_iter=iter_number, test_size=0.2,
	random_state=0)
MSE = 0
results = []
for train_index, test_index in ss:
	X_training, Y_training, X_test, Y_test = [], [], [], []
	for i in train_index:
		X_training.append(X[i])
		Y_training.append(Y[i])
	for i in test_index:
		X_test.append(X[i])
		Y_test.append(Y[i])
	classifier = svm.SVC(probability=True)
	probas_ = classifier.fit(X_training, Y_training).predict_proba(X_test)
	# Compute ROC curve and area the curve
    	fpr, tpr, thresholds = roc_curve(Y_test, probas_[:, 1])
    	roc_auc = auc(fpr, tpr)
    	plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)' % (roc_auc))
	
plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
