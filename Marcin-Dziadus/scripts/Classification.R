library(gam)
library(nnet)

classifyWithGlm <- function(dataset, formula, cutOff) {
  samples <- makePartition(frame, 1, 0.5, frame$class)$training
  
  model <- glm(formula=dataset$class ~ . , data = samples, family="binomial")
  probs <- predict(model, newdata=dataset, type="response")
  
  prediction <- assignToClass(probs, cutOff)
  classificationAccuracy(prediction, frame$class)
}

classifyWithGam <- function(dataset, formula, cutOff) {
  samples <- makePartition(frame, 1, 0.2, frame$class)$training

  model <- gam(formula=formula , data = samples, family="binomial")
  probs <- predict(model, newdata=dataset, type="response")
  
  prediction <- assignToClass(probs, cutOff)
  classificationAccuracy(prediction, frame$class)
}

classifyWithNnet <- function(dataset, formula, cutOff) {  
  samples <- makePartition(frame, 1, 0.2, frame$class)$training
  
  model <- multinom(formula=formula , data = samples, family="binomial")
  probs <- predict(model, newdata=dataset, type="probs")
  
  prediction <- assignToClass(probs, frame$class)
  classificationAccuracy(as.numeric(prediction), frame$class)  
}

prepareForClassification <- function(data, fun) {
  frame <- dropColumn(data,"month_revenue")
  frame$class <- fun(data)
  frame
}

positiveMonthRevenue <- function(data) {
  sign(data$month_revenue)
}

positiveMonthRevenueWithFirstWeekExcluded <- function(data) {
  sign(data$month_revenue - data$week_revenue)
}

evaluate <- function(data) {
  formula <- class ~ adds_count + items_bought + categories_seen + log(week_revenue+1) + 
    log(revenue_day1+1) + log(revenue_day2+1) + log(revenue_day3+1)+ log(revenue_day4+1)+ log(revenue_day5+1)+ log(revenue_day6+1)+ log(revenue_day7+1)
  
  classifyWithGam(prepareForClassification(data,positiveMonthRevenue), formula, 0.1)
}

