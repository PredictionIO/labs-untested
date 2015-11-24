Scratching basic requirements for predictive model

Two scripts in python estimating revenue after 30 days on set of users who ever bought something.
Both of them require 'input_data.csv' - exported 'users_features' view from database (database/)

simple.py - Apply Ordinary Least Squares model (var = 0.64)
ridge.py - Apply Ridge Regression model (var = 0.64)


Corollary:
ML models like Continuous functions and very dislike discrete ones.
Linear Regression is anyway very primitive building block of ML.

Problem:
How to divide data into chunks to achieve:
 - Good continuous linear (approximation) functions
 - Big sample
 - Unquestionable fit to particular chunk

Data should be consistent between dimensions? (to get low variance)
