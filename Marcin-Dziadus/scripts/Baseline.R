approach1 <- function(training, testing) {
  predict <- testing$week_revenue
  postResample(predict, testing$month_revenue)
}

approach2 <- function(trainingData, testingData) {
  avg <- mean(trainingData$month_revenue - trainingData$week_revenue)
  predict <- testingData$week_revenue + avg
  postResample(predict, testingData$month_revenue)
}

approach3 <- function(trainingData, testingData) {
  avg <- mean(trainingData$month_revenue - trainingData$week_revenue)
  aux <- sign(testingData$week_revenue)
  predict <- testingData$week_revenue + aux * avg
  postResample(predict, testingData$month_revenue)
}

evaluateModelWithCV <- function(model, dataset, iters) {
  err <- 0
  
  for(i in 1:iters) {
    seed <- sample(1:1000, 1)
    
    partition <- makePartition(dataset, seed, 0.8, dataset$month_revenue)
    training <- partition$training
    testing <- partition$testing
    
    err <- err + model(training, testing)["RMSE"]
  }
  
  err <- err / iters
  return(err)
}

# Using the cross-validation procedure from caret package for customized models requires to write some boilerplate. 
evaluateBaselineModels <- function(dataset) {  
  print("Rewrite the week_revenue:")
  print(evaluateModelWithCV(approach1, dataset, 10))
  
  print("week_revenue + the average of month_revenue with week_revenue excluded:")
  print(evaluateModelWithCV(approach2, dataset, 10))
  
  print("The same as previously, but only for those with positive week_revenue:")
  print(evaluateModelWithCV(approach3, dataset, 10))
}
