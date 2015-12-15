import numpy as np
from sklearn import datasets, linear_model
from sklearn import cross_validation
import matplotlib.pyplot as plt

# features columns: 
# 0 user_id
# 1 first_week
# 2 first_month
# 3 items
# 4 views

f = open("test.csv")
data = np.loadtxt(f, delimiter=",")

Y = data[:, 2]
X = data[:, [1, 3, 4]] #first_week, item, views

X_training, X_test, Y_training, Y_test = cross_validation.train_test_split(
	X, Y, test_size=0.2, random_state=2)


print "Dataset prepared", "\n"

# average as result
avg = np.mean(Y_training)
print avg
result = np.mean((Y_test - avg) ** 2)
print "Average: ", result, "\n"
####################

N = len(X)
iter_number = 20
ss = cross_validation.ShuffleSplit(N, n_iter=iter_number, test_size=0.2,
	random_state=0)
MSE = 0
results = []
for train_index, test_index in ss:
	X_training, Y_training, X_test, Y_test = [], [], [], []
	X_test_0, Y_test_0_predict, Y_test_0_real = [], [], []
	for i in train_index:
		if X[i, 0] > 0:
			X_training.append(X[i])
			Y_training.append(Y[i])
	for i in test_index:
		if X[i, 0] > 0:
			X_test.append(X[i])
			Y_test.append(Y[i])
		else:
			Y_test_0_predict.append(0)
			Y_test_0_real.append(Y[i])
			
	regr = linear_model.LinearRegression()
	regr.fit(X_training, Y_training)
	Y_predict = np.concatenate((regr.predict(X_test),Y_test_0_predict))
	Y_test = np.concatenate((Y_test, Y_test_0_real))
	res = np.mean((Y_predict - Y_test) ** 2)
	MSE += res
	results.append(res)
	print ("Residual sum of squares: %.2f"
      		% res)
	print "\n" 
print ("MSE: %.2f" % 
	(MSE/iter_number))
	
plt.figure()
plt.title("MSE results")
plt.bar(range(0, iter_number), results,
       color="r", align="center")
plt.xticks(range(0, iter_number), results)
plt.xlim([-1, iter_number])
plt.show()
