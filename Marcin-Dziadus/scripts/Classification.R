positiveMonthRevenue <- function(data) {
  as.factor(ifelse(data$month_revenue > 0, 1, 0))
}
  
positiveMonthRevenueWithFirstWeekExcluded <- function(data) {
  as.factor(ifelse(data$month_revenue > data$week_revenue, 1, 0))
}
  
revenueBiggerThan5000 <- function(data) {
  as.factor(ifelse(data$month_revenue > 5000, 1, 0))
}

prepareFrameForClassification <- function(data, labelMaker) {
  frame <- dropColumn(data,"month_revenue")
  frame$class <- labelMaker(data)
  return(frame)
}

measureClassifierPerformance <- function(prediction, labels) {
  library(AUC)
  sens <- sensitivity(prediction, labels)
  cat(sprintf("sensitivity: %f\n", auc(sens)))
  
  spec <- specificity(prediction, labels)
  cat(sprintf("specificity: %f\n", auc(spec)))
  
  roc <- roc(prediction, labels)
  cat(sprintf("roc: %f\n", auc(roc)))
  
  plot(roc)
}

classifyWithGlm <- function(training, testing) {
  model <- glm(class ~ ., data = training)
  prediction <- predict(model, newdata=testing, type="prob")
  
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

classifyWithGlment <- function(training, testing) {
  library(glmnet)
  
  model <- glmnet(x = data.matrix(dropColumn(training, "class")),
                  y = training$class,
                  family = "binomial",
                  type.logistic = "modified.Newton")
  prediction <- predict(model,
                        newx = data.matrix(dropColumn(training, "class")),
                        type = "response")
  
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

classifyWithGam <- function(training, testing) {
  library(gam)
  
  model <- gam(class ~ ., data = training, family="binomial")
  prediction <- predict(model, newdata=testing, type="response")
  
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

classifyWithNnet <- function(training, testing) {
  library(nnet)
  
  model <- multinom(class ~ ., data = training)  
  prediction <- predict(model, newdata=testing, type="class")
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

classifyWithXgboost <- function(training, testing) {
  library(xgboost)

  training$class <- as.numeric(training$class) - 1
    
  model <- xgboost(data = as.matrix(dropColumn(training,"class")), label = training$class, nround=15, objective="binary:logistic")
  prediction <- predict(model, newdata=as.matrix(dropColumn(testing, "class")))
  
  names <- dimnames(as.matrix(dropColumn(testing, "class")))[[2]]
  importance_matrix <- xgb.importance(names, model = model)
  print(importance_matrix)
  
  measureClassifierPerformance(prediction, testing$class)
  return(model)
}

evaluateModel <- function(dataset, preprocessor, model) {
  library(unbalanced)
  
  dataset <- prepareFrameForClassification(dataset, preprocessor)

  partition <- makePartition(dataset, 42, 0.8, dataset$class)
  training <- partition$training
  testing <- partition$testing
  
  temp <- ubOver(dropColumn(training, "class"), training$class)
  training <- temp$X
  training$class <- temp$Y
  
  model(training, testing)
}
