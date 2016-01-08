tests/scikit.py
It is a simple example of using scikit. It based on http://stackoverflow.com/questions/10526579/use-scikit-learn-to-classify-into-multiple-categories

tests/linear_models.py
Set of tests with different ML methods.

tests/cross_validation.py
A file to generate a plot with MSE results for different training (80%) / tests (20%) sets.

tests/cross_validation.png
A plot with MSE for different training/tests sets (avg. 1637.12).

cls/cls.py
An example of generating a plot of features importance.

cls/ExtraTrees_10.png
ExtraTreesClassifier, 10 estimators

cls/ExtraTrees_20.png
ExtraTreesClassifier, 20 estimators

cls/RandomForest
RandomForestClassifier, 20 estimators

clustering/KMeans.py
A test with KMeans clustering.

clustering/KMeans.png
A plot with result from KMeans.py.

clustering/0_1.py
A test with dividing dataset into two sets: first_week = 0 and first_week > 0 (avg. 1638.51). 

clustering/0_1.png
A plot with result from 0_1.py.

sql/query.sql
Some useful SQL queries which were used to create features for ML.

sql/features_not_equal.sql
Some useful SQL queries which were used to create features for ML (only for people who have not equal first_week and first_month).

sql/features_ROC.sql
Some useful SQL queries which were used to create features for ML (features for ROC AUC).

sql/test_db.out
Database dump.

not_equal/classifier.py
A script which generate a plot with information about feature importances for set of people who have not equal first_week and first_month.

not_equal/feature_importances.png
A plot with result from classifier.py.

not_equal/linear_model.py
A test with prediction results for group of people who have not equal first_week and first_month.

not_equal/linear_model.png
A plot with result from linear_model.py.

ROC/test.py
A script which I used to compute AUC from prediciton scores.

ROC/AUC_first_week>0.png
A plot with result from test.py on the set of people who have first_week > 0.

pyspark/binary_classification_simple.py
Test of prediction if first_week is equal first_month or not (using linear regression with SGD). The same test and training data.

pyspark/SVMWithSGD.py
Test of prediction if first_week is equal first_month or not(using SVM with SGD). Test data - 20%, training data - 80%.

logisticRegressionWithSGD.py
Test of prediction if first_week is equal first_month or not(using linear regression with SGD). Test data - 20%, training data - 80%.
