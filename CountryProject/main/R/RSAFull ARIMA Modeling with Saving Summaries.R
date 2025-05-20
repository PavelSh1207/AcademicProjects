library(tidyverse)
library(forecast)
library(RJDemetra)
library(lubridate)
library(zoo)

# 1. Data Loading and Preparation
load_data <- function(filepath) {
  data <- readxl::read_excel(filepath) %>%
    mutate(time = as.Date(time)) %>%
    filter(time >= as.Date("2010-01-01"))
  return(data)
}

# 2. Decomposition Analysis with Saving
perform_decomposition <- function(data, model = "additive") {
  decomposition_results <- list()
  countries <- unique(data$geo)
  
  for (country in countries) {
    country_data <- data %>% filter(geo == country) %>% select(time, values) %>%
      arrange(time)
    ts_data <- ts(country_data$values, frequency = 12, start = c(year(min(country_data$time)), month(min(country_data$time))))
    
    decomposition <- decompose(ts_data, type = model)
    decomposition_results[[country]] <- decomposition

    # Save decomposition components
    result_df <- data.frame(
      date = as.Date(time(ts_data)),
      trend = decomposition$trend,
      seasonal = decomposition$seasonal,
      residual = decomposition$random
    )
    write.csv(result_df, paste0(country, "_decomposition_", model, ".csv"), row.names = FALSE)
  }
  return(decomposition_results)
}

# 3. Outlier Removal with Saving
remove_outliers <- function(decomposition_results, start_date = "2020-01-01", end_date = "2021-12-31") {
  cleaned_results <- list()
  covid_period <- seq(as.Date(start_date), as.Date(end_date), by = "days")
  
  for (country in names(decomposition_results)) {
    residuals <- decomposition_results[[country]]$random
    residuals_time <- time(residuals)
    
    non_covid_residuals <- residuals[!residuals_time %in% covid_period]
    result_df <- data.frame(date = as.Date(time(non_covid_residuals)), residuals = non_covid_residuals)
    write.csv(result_df, paste0(country, "_cleaned_residuals.csv"), row.names = FALSE)
    cleaned_results[[country]] <- non_covid_residuals
  }
  return(cleaned_results)
}

# 4. RSAFull ARIMA Modeling with Saving Summaries
fit_rsafull_arima <- function(cleaned_residuals, order = c(1, 1, 1), seasonal_order = c(0, 1, 1, 12)) {
  models <- list()
  
  for (country in names(cleaned_residuals)) {
    residuals <- cleaned_residuals[[country]]
    ts_data <- ts(residuals, frequency = 12)
    working_days <- ifelse(weekdays(as.Date(time(ts_data))) %in% c("Saturday", "Sunday"), 0, 1)
    
    tryCatch({
      model <- auto.arima(ts_data, xreg = working_days, seasonal = TRUE, approximation = FALSE, stepwise = FALSE)
      models[[country]] <- model
      
      # Save model summary to text file
      sink(paste0(country, "_rsafull_model_summary.txt"))
      print(summary(model))
      sink()
    }, error = function(e) {
      message(paste("Failed to fit RSAFull ARIMA model for", country, ":", e$message))
    })
  }
  return(models)
}

# Final Script Usage
data <- load_data("dane_eurostat.xlsx")
decomposition_results <- perform_decomposition(data, model = "additive")
cleaned_residuals <- remove_outliers(decomposition_results, start_date = "2020-01-01", end_date = "2021-12-31")
rsafull_models <- fit_rsafull_arima(cleaned_residuals, order = c(1, 1, 1), seasonal



