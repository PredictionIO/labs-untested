loadData <- function() {
  dataDirectory <- "/home/marcin"
  data <- read.csv(paste(dataDirectory, 'data.csv', sep="/"), header = TRUE)
  # skip the column with user_id and convert everything to a data frame
  frame <- data.frame(data[-1])
}

makePartition <- function(dataset, seed) {
  set.seed(seed)
  trainIndex <- createDataPartition(dataset$month_revenue, p = .8,
                                    list = FALSE,
                                    times = 1)
}

baselineApproach1 <- function(dataset) {
  predict <- dataset$week_revenue
  postResample(predict, dataset$month_revenue)
}

baselineApproach2 <- function(trainingData, testingData) {
  avg <- mean(trainingData$month_revenue - trainingData$week_revenue)
  predict <- testingData$week_revenue + avg
  postResample(predict, testingData$month_revenue)
}

baselineApproach3 <- function(trainingData, testingData) {
  avg <- mean(trainingData$month_revenue - trainingData$week_revenue)
  aux <- sign(testingData$week_revenue)
  predict <- testingData$week_revenue + aux * avg
  postResample(predict, testingData$month_revenue)
}

simpleLinearRegression <- function(trainingData, testingData) {
  trainingData$week_revenue <- trainingData$week_revenue
  model <- lm(month_revenue ~ ., data=trainingData)
  predict <- predict.lm(model, newdata=testingData)
  predict <- predict + 1
  postResample(predict, testingData$month_revenue)
}

testModels <- function(dataset) {  
  # Split data on training and testing sets.
  idxs <- makePartition(dataset, 123)
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

testModels(frame)

featuresCorrelation <- function(dataset) {
  depVars <- dataset[, !(colnames(dataset) %in% c("month_revenue"))]
  corrMatrix <- cor(depVars)
  print(corrMatrix)
}

featuresImportanceForModel <- function(model) {
  importance <- varImp(model, scale=FALSE)
  print(importance)
}

featureSelection <- function(dataset) {
  # Caused by the efficiency reasones.
  idxs <- createDataPartition(dataset$month_revenue, p = .01,
                                    list = FALSE,
                                    times = 1)
  dataSample <- dataset[idxs,]
  
  control <- rfeControl(functions = lmFuncs,
                     method = "repeatedcv",
                     repeats = 5,
                     verbose = FALSE)
  
  rfe(dataSample[,-grep("month_revenue", colnames(dataSample))], dataSample$month_revenue, rfeControl = control)
}

linearRegression <- function(dataset) {
  # cross-validation
  control <- trainControl(method="cv", number=5)
  model <- train(month_revenue~., data=dataset, trControl=control, method="lm")
  predict <- predict(model, newdata=dataset)
  postResample(predict, data$month_revenue)
}
