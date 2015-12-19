
08/11/2015

1. Import testing data to PostgreSQL.
2. A lot of SELECTs to get some information about data, for example how many people buy only one item etc.
3. Prepare some futures for machine learning algorithms.
4. Learn about scikit - python library for machine learning.
5. Work on simple linear regression to predict the revenue of a new visitor in the first month based on first week's behavior using scikit.

17/11/2015
1. Learn about scikit.
2. Use scikit to predict the revenue of a new visitor in the first month based on first week's behavior:

Average:  5524.86403453 

Copy first week:  1385.38536234 

Linear regression 

Coefficients: 
[ 1.07576514,  1.04820752,  0.10243014]
Residual sum of squares: 1349.49
Variance score: 0.76


Ridge 

Coefficients: 
[ 1.06180463,  2.53674116,  0.10226126]
Residual sum of squares: 1351.56
Variance score: 0.76
 


25/11/2015

1. Get some theoretical knowledge about features, features selection.
2. Generate plots for different features selection models.
3. Start the data migration to the new faster machine.

02/12/2015

1. Finish the data migration to the new faster machine.
2. Read about bias, variance, overfitting.
3. Count a MSE for different training/tests sets (cross validation).
4. Generate plot with results (avg. 1637.12).

09/12/2015

1. Get some statistical knowledge about the dataset:
	- 99% of people buy nothing in the first week!!!,
	- 0.4% of people buy something in the first month but nothing in the first week,
	- AVG of the first week is $1.89, AVG of the first month is $2.9.
2. Tests with KMeans - clustering.
3. Get some theoretical knowledge about Clustered Linear Regression:
	- http://yoksis.bilkent.edu.tr/pdf/files/10.1016-S0950-7051(01)00154-X.pdf
	- http://staff.ii.pw.edu.pl/~gawrysia/publ/iis2001.pdf
4. Divide the dataset into two sets: first week > 0 and first week = 0. First week > 0 - solution with linear regression, first week = 0 - result always equals 0. (avg. 1638.54).

16/12/2015

1. Work on set of people who haven't equal first week and first month purchases (26988 people, 23751 people with first week = 0).
2. Use only 3 simple features (first_week, items, views) - avg. MSE is 244138.12!!!
3. Prepare new features to decrease MSE (new result: 243360.32 - really disappointing).
4. Generate a plot with features importances.
