# Code Sprint Summary:
- loaded data into database
- discovered and got rid of inconsistencies in the data set
- created features using SQL queries
- testing a simple model based on the linear regression (scikit-learn)
- compared an accuracy of the created model with some other (simple) ones

# General Summary:
* **Challanges:**
  * highly imbalanced dataset
    * #users: 5670169
    * #users with week_revenue > 0: 59505 (about 1% of users number)
    * #users with month_revenue > 0: 83865
    * #users with week_revenue > 5000: 53 (!)
    * #users with month_revenue > 5000: 79 (!)
  * many observations
    * hard to fit dataset in memory for some models (e.g. nnet)
    * some computations take quite a long time
    * problematic sampling (imbalanced dataset) - not possible to simply get rid of some of the observations
  * short period of time (one week) to predict the future behaviour

* **Outcomes:**
  * extracted features from unstructured data
  * acquired the knowledge about the machine learning
    * common techniques for classification and regression
    * features extraction
    * features selection
    * cross-validation
    * many more
  * familiarized myself with R
    * good choice for prototyping
    * rstudio makes prototyping smoother
    * R is not working well with large datasets
  * learned about some of R packages
    * **caret** - set of tools for models training
    * **AUC** - performance measureing
    * **unbalanced** - preprocessing of the imbalanced datasets
    * **glmnet**, **nnet**, **gam**, **xgboost**, **rfe**, **xgboost** - regression and classification models
    * a few more
