library(caret)

loadData <- function(file_name) {
  # [TODO]: The data_directory should not be hardcoded.
  data_directory <- '/home/marcin/fb'
  data <- read.csv(paste(data_directory, file_name, sep="/"), header = TRUE)
  # skip the column with user_id and convert everything to a data frame
  frame <- data.frame(data[-1])
}

makePartition <- function(dataset, seed, prob, column) {
  set.seed(seed)
  trainIndexes <- createDataPartition(column, p = prob,
                                    list = FALSE,
                                    times = 1)
  trainData <- dataset[trainIndexes,]
  testData <- dataset[-trainIndexes,]
  list("training"=trainData, "testing"=testData)
}

featureSelection <- function(dataset) {
  # Caused by the efficiency reasones.
  partition <- makePartition(dataset, 1, .1, dataset$month_revenue)
  dataSample <- partition$training
  
  control <- rfeControl(functions = lmFuncs,
                        method = "repeatedcv",
                        repeats = 5,
                        verbose = FALSE)
  
  rfe(dataSample[,-grep("month_revenue", colnames(dataSample))], dataSample$month_revenue, rfeControl = control)
}

featuresCorrelation <- function(dataset) {
  depVars <- dataset#[, !(colnames(dataset) %in% c("month_revenue"))]
  corrMatrix <- cor(depVars)
}

featuresImportanceForModel <- function(model) {
  importance <- varImp(model, scale=FALSE)
  print(importance)
}

sanitize <- function(pred) {
  pmax(pred,0)
}

dropColumn <- function(frame, colName) {
  keep <- names(frame) %in% c(colName)
  frame[,!keep]
}


