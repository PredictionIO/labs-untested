# Load the required package.
library(MASS)

monthRevenuePreprocess <- function(data) {
  data$month_revenue
}

monthRevenuePostprocess <- function(data, prediction) {
  pmax(prediction, 0)
}

monthRevenueWithWeekExcludedPreprocess <- function(data) {
  data$month_revenue - data$week_revenue
}

monthRevenueWithWeekExcludedPostprocess <- function(data, prediction) {
  pmax(prediction,0) + data$week_revenue
}

prepareFrameForRegression <- function(data, process) {
  data$outcome <- process(data)
  dropColumn(data,"month_revenue")
}

linearRegressionModelWithAllFeatures <- function(training, testing) {
  model <- lm(outcome ~ ., data=training)
  prediction <- predict(model, newdata=testing)
  featuresImportanceForModel(model)
  return(prediction)
}

linearRegressionWithBasicFeatures <- function(training, testing) {
  model <- lm(outcome ~ week_revenue + adds_count + items_bought + discount_ratio + categories_seen + categories_bought,
              data=training)
  prediction <- predict(model, newdata=testing)
  featuresImportanceForModel(model)
  return(prediction) 
}

ridgeRegressionModelWithVariableSelection <- function(training, testing) {
  library(foba)
  model <- train(outcome ~ week_revenue + adds_count + items_bought + discount_ratio + categories_seen + categories_bought,
                 data=training,
                 trControl = fitControl(5,5),
                 method="foba")
  prediction <- predict(model, newdata=testing)
  featuresImportanceForModel(model)
  return(prediction) 
}

linearRegressionModelWithCV <- function(training, testing) {
  model <- train(x = dropColumn(training, "month_revenue")
                 y = training$outcome,
                 trControl = fitControl(5,5),
                 method="lm")
  prediction <- predict(model, newdata=testing)
  featuresImportanceForModel(model)
  return(prediction)
}

linearRegressionWithFeatureSelection <- function(training, testing) {
  library(leaps)
  summary(training)
  model <- train(outcome ~ week_revenue + hour_revenue + adds_count + items_bought + discount_ratio + categories_seen + categories_bought,
                 data = training,
                 trControl = fitControl(5,5),
                 method = "leapBackward")
  prediction <- predict(model, newdata=testing)
  featuresImportanceForModel(model)
  return(prediction)
}

regressionModelWithXgboost <- function(training, testing) {
  library(xgboost)
  
  model <- xgboost(data = as.matrix(dropColumn(training,"outcome")), label = training$outcome, nround=100, objective="reg:linear")
  prediction <- predict(model, newdata=as.matrix(dropColumn(testing, "outcome")))
  
  names <- dimnames(as.matrix(dropColumn(testing, "class")))[[2]]
  importance_matrix <- xgb.importance(names, model = model)
  print(importance_matrix)
  
  return(prediction)
}

# Super slow. Sampling needed.
randomForestModel <- function(training, testing) {
  library(randomForest)
  
  model <- train(month_revenue ~ ., data = training, method="ranger")
  prediction <- predict(model, newdata=testing)
  featuresImportanceForModel(model)
  
  return(prediction)
}

evaluateModel <- function(dataset, preprocessor, postprocessor, model) {
  library(caret)
  library(unbalanced)
  library(e1071)
  
  partition <- makePartition(dataset, 42, 0.8, dataset$month_revenue)
  training <- prepareFrameForRegression(partition$training, preprocessor)
  testing <- partition$testing
  
  prediction <- model(training, testing)
  prediction <- postprocessor(testing, prediction)
  print(summary(prediction))
  postResample(prediction, testing$month_revenue)
}
