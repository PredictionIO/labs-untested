# Load required packages.
library(caret)
library(MASS)
library(randomForest)

# For cross-validation purposes.
fitControl <- trainControl(
  method = "repeatedcv",
  number = 4,
  repeats = 10,
  savePred = TRUE)

linearRegressionModel <- function(dataset) {
  partition <- makePartition(dataset, 300, 0.8, dataset$month_revenue)
  training <- partition$training
  testing <- partition$testing
  
  model <- lm(month_revenue ~ ., data=training)
  predict <- predict(model, newdata=testing)
  
  featuresImportanceForModel(model)
  postResample(predict, testing$month_revenue)
}

randomForestModel <- function(dataset) {
  partition <- makePartition(dataset, 300, 0.8, dataset$month_revenue)
  training <- partition$training
  testing <- partition$testing
  
  model <- train(month_revenue ~ ., data = training, method="rf")
  predict <- predict(model, newdata=testing)
  
  featuresImportanceForModel(model)
  postResample(predict, testing$month_revenue) 
}

linearRegressionModelWithCV <- function(dataset) {
  model <- train(month_revenue ~ ., data = dataset, trControl=fitControl, method="lm")
  featuresImportanceForModel(model)  
  model
}

linearRegressionWithFeatureSelection <- function(dataset) {
  model <- train(month_revenue ~ week_revenue + hour_revenue + adds_count + items_bought + discount_ratio + categories_seen,
                 data = dataset,
                 trControl = fitControl,
                 method = "leapBackward")
  featuresImportanceForModel(model)
  model
}
