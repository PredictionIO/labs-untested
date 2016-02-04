# Classification

* xgBoost
  * month > 5000
    * sensitivity: 0.902374
    * specificity: 0.428027
    *roc: 0.902379

  * month > 0
    * sensitivity: 0.925298
    * specificity: 0.436468
    * roc: 0.931682

  * month - week > 0 
    * sensitivity: 0.777304
    * specificity: 0.421820
    * roc: 0.778657

* gam
  * month - week > 0
    * ensitivity: 0.756614
    * specificity: 0.400501
    * roc: 0.757866

  * month > 0 
    * sensitivity: 0.919140
    * specificity: 0.403976
    * roc: 0.925453

  * month > 5000
    * miserable - all measures are pretty bad

* nnet
  * memory problems occured, with sampling miserable results (terribly bad specificity)

* glmnet
  * month > 5000
    * miserable - solid auc roc, but terribly bad specificity

# Regression

* baseline models
  * rewrite the first week revenue: RMSE 37.11299
  * week revenue + average of the month revenues with the first week excluded: RMSE 33.97474
  * week revenue + average of the positive month revenues with the first week excluded: RMSE 33.93392
  
* cross-validated linear regression on the full features set: RMSE 35.1259108 (worse than the baselines)

* linear regression with feature selection (leapBackward): RMSE 30.1135687 

* ross-validated ridge regression with variable selection: RMSE 28.5529995

* random forest
  * super slow, with sampling gives miserable results

* xgboost
  * definitely the worst regression model (unbelievably large RMSE), the best classification model though
  
* combine classification and regression (classify users with positive month - week, then predict month revenues only for that selected group) - dissapointing results even with fairly good classificators (mostly because of the inadequate specificity)

