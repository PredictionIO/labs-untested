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

## 15.12.2015
- worked on improving binary classification - whether user is going to buy anything 
 during the rest of the month after the first week
- the measure I used was recall
- checked many classification models: the best were those based on logistic regression with balanced class weights
(SGDClassifier with loss=log and penalty=elasticnet)
- Recall was on average about 0.55 +/- 0.01
- then I spent a lot of time on add new features, namely categorical ones
  * items based features: how many times user bought an item from some personality or style
  * ads based features: did user see an ad from this or this source and medium
- I generated large files with one hot encoded categories (about 6 GB big each)
- Then I used PCA to reduce dimensionality (from about 160 on average to 10)
- In the end I got features vector of width 39
- Recall was sadly not improved, standard deviation dropped a bit
- Regression methods did not improve either
- I could look for more features - e.g. similar to those items based but based on views, although
I would not expect it to improve my results much
- I suspect that there is a large group of users with almost no activity within first week kept being classified
incorrectly
- I have to look closer at the data and maybe try to see some patterns which I am missing now
- Improving this basic classification problem will let me build better model in the end

## 3.01.2016
- tried different scoring function to recall - roc_curve
- results were pretty much similar for both logistic regression and SGDClassifier all arount 0.77
- installed XGBoost library and used XGBClassifier, recall was equal to 0 for all different parameters but auc was changing (why?). Maybe there is something different in this library comparing to standard sklearn models.

## 8.01.2016
- played a bit with xgboost and got the best results so far
- AUC about 0.80 and Recall 0.68

## 13.01.2016
- moved to problem of classifying users spending more than 5000 dollars during the first month of the registratio
- extensively tested XGBoost classifier and played with parameters for it
- got very promising results, but strangely different for sklearn and normal api of XGBoost
    * sklearn 
        - Auc: 0.95 (+/-) 0.028
        - Recall: 0.73 (+/-) 0.191
    * regular python api
        - Auc: 0.84 (+/-) 0.046
        - Recall: 0.68 (+/-) 0.092
- I am going to spend more time tunning parameters (Grid search)
- I have to find out why there are performance differences between these two apis
- Then I am planning to work on features to improve performance
- After that I'll look how it will work with other models in ensemble (I am going to check vowpal wabbit)

## 14.01.2016
It turned out that sklearn api makes predictions of terribly low precision, even for the same parameters
  (why?). Example:
    * Slearn:
        Roc auc score:  0.95827618036
        Recall score:  0.9375
        Number of qualified as true:  23770
        Number of real true:  16
    * Regular api
        Roc auc score:  0.874925927102
        Recall score:  0.75
        Number of qualified as true:  180
        Number of real true:  16
Even with slightly worse AUC score the second model is so much better.
It's results for 5-fold cv
    F1: 0.21 (+/-) 0.210
    Min: 0.10 Max 0.634
    Roc_Auc: 0.85 (+/-) 0.037
    Min: 0.81 Max 0.906
    Recall: 0.70 (+/-) 0.074
    Min: 0.62 Max 0.812
    Precision: 0.15 (+/-) 0.184
    Min: 0.06 Max 0.520

Now I am planning to define better scoring function (f1-beta) to control the precisionj too.
Then I'll spend some time tuning parameters
   
