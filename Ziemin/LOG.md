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
