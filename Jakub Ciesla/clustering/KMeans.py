import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

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
X = data[:, [1, 2]] #first_week, first month

X_training, X_test, Y_training, Y_test = cross_validation.train_test_split(
	X, Y, test_size=0.99, random_state=2)


print "Dataset prepared", "\n"

# average as result
avg = np.mean(Y_training)
print avg
result = np.mean((Y_test - avg) ** 2)
print "Average: ", result, "\n"
####################_

# Incorrect number of clusters
y_pred = KMeans(n_clusters=4, random_state=0).fit_predict(X_training)

plt.scatter(X_training[:, 0], X_training[:, 1], c = y_pred)
plt.title("First week / First month")

plt.show()
