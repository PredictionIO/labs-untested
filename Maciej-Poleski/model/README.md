Scratching basic requirements for predictive model

Two scripts in python estimating revenue after 30 days on set of users who ever bought something.
Both of them require 'input_data_shuffled.csv' - exported 'users_features' view from database (database/)
Next four (*_reduced.py, dtr.py and dtc.py) require 'input_data_reduced_shuffled.py' - exported 'users_features_reduced' view.
All of data should be shuffled.

simple.py - Apply Ordinary Least Squares model (var = 0.64)
ridge.py - Apply Ridge Regression model (var = 0.64)
*_reduced.py - Improve above results by removing ads feature and normalizing time interval (var = 0.65)
dtr.py - Apply Decision Trees Regression on reduced set (var ~~0.44)

After extending model by 3 new features (number of views by type)
*_reduced.py - Worsen results (var = 0.6)
dtr.py - Improved results (var ~~ 0.63), still bad
dtc.py - Perfect fit (var = 1.00), almost unbelievable (almost, because the 'OK' set is very small)
ridge_reduced2.py
dtr2.py
lasso_reduced2.py
elasticnet_reduced2.py
dtr3.py
elasticnet_reduced3.py
^^ - work on appropriate input data

utm_extractor.cpp - tool used to translate discrete features (like utm tags or items properties) into bit vector.

input_data_reduced?.csv is dumped from users_features_reduced
then it is shuffled into input_data_reduced?_shuffled.csv
then it is unpacked using extractor (currently on 6 column) into input_data_reduced?_shuffled_unpacked.csv
the last file is used by appropriate scripts

Corollary:
ML models like Continuous functions and very dislike discrete ones.
Linear Regression is anyway very primitive building block of ML.
Decision Trees seems be very interesting approach to above problem, BUT INEFFECTIVE regression
and PERFECT(?) decisions.

Problem:
How to divide data into chunks to achieve:
 - Good continuous linear (approximation) functions
 - Big sample
 - Unquestionable fit to particular chunk

Data should be consistent between dimensions? (to get low variance)
DTs seemed to be the solution, but it fails at regression...
