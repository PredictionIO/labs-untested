library(caret)

simpleLinearRegression <- function(trainingData, testingData) {
  trainingData$week_revenue <- trainingData$week_revenue
  model <- lm(month_revenue ~ ., data=trainingData)
  predict <- predict.lm(model, newdata=testingData)
  predict <- predict + 1
  postResample(predict, testingData$month_revenue)
}

testModels <- function(dataset) {  
  # Split data on training and testing sets.
  idxs <- makePartition(dataset, 123, 0.8, "month_revenue")
  trainingData <- dataset[idxs,]
  testingData <- dataset[-idxs,]
  
  print("Rewrite the week_revenue:")
  print(baselineApproach1(dataset))
  
  print("week_revenue + the average of month_revenue with week_revenue excluded:")
  print(baselineApproach2(trainingData, testingData))
  
  print("The same as previously, but only for those with positive week_revenue:")
  print(baselineApproach3(trainingData, testingData))
  
  print("Linear regression:")
  print(simpleLinearRegression(trainingData, testingData)) 
}

evaluateTests <- function() {
  dataset <- loadData()
  testModels(dataset)
}

linearRegression <- function(dataset) {
  # cross-validation
  control <- trainControl(method="cv", number=5)
  model <- train(month_revenue~., data=dataset, trControl=control, method="lm")
  predict <- predict(model, newdata=dataset)
  postResample(predict, data$month_revenue)
}

