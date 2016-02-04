library(caret)

loadData <- function(fileName) {
  # The file should be in the same directory as that script.
  data <- read.csv(paste(fileName, sep="/"), header = TRUE)
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

# For cross-validation purposes.
fitControl <- function(number, repeats) {
  trainControl(
    method = "repeatedcv",
    number = number,
    repeats = repeats,
    savePred = TRUE)
}

featureSelection <- function(dataset) {
  control <- rfeControl(functions = lmFuncs,
                        method = "repeatedcv",
                        repeats = 5,
                        verbose = FALSE)
  
  cols <- c("week_revenue","hour_revenue","revenue_day1","views_day1","views_day2","views_day3",
             "items_bought", "adds_count", "categories_seen", "categories_bought", "discount_ratio")
  results <- rfe(dataset[,cols],
                 dataset$month_revenue,
                 rfeControl = control,
                 size = 6)
  print(results)
  predictors(results)
  plot(results, type = c("o", "g"))
}

featuresCorrelation <- function(dataset) {
  corrMatrix <- cor(dataset)
  highlyCorrelated <- findCorrelation(corrMatrix, cutoff=0.75)
  print(highlyCorrelated)
}

featuresImportanceForModel <- function(model) {
  importance <- varImp(model, scale=FALSE)
  print(importance)
}

dropColumn <- function(frame, colName) {
  keep <- names(frame) %in% c(colName)
  frame[,!keep]
}
