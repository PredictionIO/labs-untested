# Load required packages.
library(gam)
library(nnet)
library(klaR)
library(glmnet)

positiveMonthRevenue <- function(data) {
  factor(ifelse(data$month_revenue > 0, 1, 0))
}
  
positiveMonthRevenueWithFirstWeekExcluded <- function(data) {
  factor(ifelse(data$month_revenue > data$week_revenue, 1, 0))
}
  
revenueBiggerThan5000 <- function(data) {
  factor(ifelse(data$month_revenue > 5000, 1, 0))
}

prepareFrameForClassification <- function(data, classifier) {
  frame <- dropColumn(data,"month_revenue")
  frame$class <- classifier(data)
  frame
}

measureClassifierPerformance <- function(prediction, labels) {
  sens <- sensitivity(prediction, labels)
  cat(sprintf("sensitivity: %f\n", auc(sens)))
  
  spec <- specificity(prediction, labels)
  cat(sprintf("specificity: %f\n", auc(spec)))
  
  roc <- roc(prediction, labels)
  cat(sprintf("roc: %f\n", auc(roc)))
  
  plot(roc)
}

classifyWithGlm <- function(dataset) {  
  partition <- makePartition(dataset, 1, 0.8, dataset$class)
  training <- partition$training
  testing <- partition$testing
  
  model <- glm(class ~ ., data = training, family="binomial")
  prediction <- predict(model, newdata=testing, type="response")
  
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

classifyWithGam <- function(dataset) {
  partition <- makePartition(dataset, 1, 0.8, dataset$class)
  training <- partition$training
  testing <- partition$testing
  
  model <- gam(class ~ ., data = training, family="binomial")
  prediction <- predict(model, newdata=testing, type="response")
  
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

classifyWithNnet <- function(dataset) {  
  partition <- makePartition(dataset, 1, 0.8, dataset$class)
  training <- partition$training
  testing <- partition$testing
  
  model <- multinom(class ~ ., data = training)
  prediction <- predict(model, newdata=testing, type="probs")
  
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

