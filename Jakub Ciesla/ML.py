import numpy as np
from sklearn import datasets, linear_model

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

N = len(X)
ratio = 0.9

X_training = X[0:ratio*N]
Y_training = Y[0:ratio*N]
X_test = X[ratio*N:N]
Y_test = Y[ratio*N:N]


print "Dataset prepared", "\n"

# average as result
avg = np.mean(Y_training)
result = np.mean((Y_test - avg) ** 2)
print "Average: ", result, "\n"
####################

# copy first_week colums as result

result = np.mean((Y_test - X_test[:, 0]) ** 2)
print "Copy first week: ", result, "\n"
####################

# Linear regression
print "Linear regression", "\n"
# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_training, Y_training)

# The coefficients
print 'Coefficients: \n', regr.coef_
# The mean square error
print ("Residual sum of squares: %.2f"
      % np.mean((regr.predict(X_test) - Y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print ('Variance score: %.2f' % regr.score(X_test, Y_test))
print "\n" 
####################

# Ridge
print "Ridge", "\n"
# Create linear regression object
regr = linear_model.Ridge(alpha=.01, normalize=True)

# Train the model using the training sets
regr.fit(X_training, Y_training)

# The coefficients
print 'Coefficients: \n', regr.coef_
# The mean square error
print ("Residual sum of squares: %.2f"
      % np.mean((regr.predict(X_test) - Y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print ('Variance score: %.2f' % regr.score(X_test, Y_test)) 
####################

