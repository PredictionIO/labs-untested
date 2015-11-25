#http://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html#example-ensemble-plot-forest-importances-py
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier

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
ratio = 0.2

X_training = X[0:ratio*N]
Y_training = Y[0:ratio*N]
X_test = X[ratio*N:N]
Y_test = Y[ratio*N:N]


print "Dataset prepared", "\n"

# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=30, random_state=0)
#forest = RandomForestClassifier(n_estimators=30, random_state=0)

forest.fit(X_training, Y_training)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), indices)
plt.xlim([-1, X.shape[1]])
plt.show()
