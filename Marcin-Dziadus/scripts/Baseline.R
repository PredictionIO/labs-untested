approach1 <- function(dataset) {
  predict <- dataset$week_revenue
  postResample(predict, dataset$month_revenue)
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
