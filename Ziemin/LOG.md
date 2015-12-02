## 8.11.2015
- loaded and cleaned input data into PostgreSQL database
- created some basic features (as in queries.sql file)
- ran some basic models on the entire dataset and compared results i.e:
    - logistic regression
    - ridge regression
    - bayesian ridge regression

## 15.11.2015
- code refactoring. created python library to check different models and print some
  statistics more comfortably
- checked correlations between used features (stats.py prints appropriate plot)

## 21.11.2015
- tried to check different approaches towards feature selection
- saved some outputs not to generate them over and over again
- saved plots (feature correlation, RFECV features performance)

## 24.11.2015
- further analysis of features (random forest regressor, variances)
- created some new plots to visualize different aspects of prepared features
- next step would be looking into different methods of model evaluation
  and creating some pipelines using only subsets of features with different scalings

## 29.11.2015
- checked different regression models - nearly all of them did poorly or at least worse
  than simple linear regression in combination with pca, feature selection, scaling 
  and polynomial features
- tried to look at data differently - created some cross validation prediction plots
- identified some groups of users with KMeans

## 30.11.2015
- tried clustering samples followed by separate prediction for every cluster - got rather poor results
- tried training models only on users with view_count > 0 - got as good results as before but with smaller
  standard deviation, the same for first_week > 0
- the number of people who spent anything in the rest of the month (after first week) is only 26988 which
  is just about 0.4% of all users - recognizing these users and training model against them seem to be the key part   of the problem

  a lot of them do not spend anything in the first week - but they have a lot of views - this group of people is
  23764 which is 88% of all people spending money only in the the last 3 weeks of month
  
- one idea could be dividing users into groups:
    * users spending nothing at all
    * users spending only in the first week
    * users spending through entire month

- working on the smaller group of people (spenders) we could try to predict which items users would buy
  and using it try to estimate their entire spendings

- 1.5 mln of people did nothing at all on the service - they can be removed in advance - if there is no view
  in the first week

- users which did not spend anything and had views_count <= than:
  * 1 - 2889068
  * 2 - 3704066
  * 3 - 4148705
  * 4 - 4459405
  * 5 - 4664367
