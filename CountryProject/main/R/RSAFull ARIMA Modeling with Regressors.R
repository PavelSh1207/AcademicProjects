# Load required libraries
library(tidyverse)
library(forecast)
library(RJDemetra)
library(lubridate)
library(zoo)

# 1. Data Loading and Preparation
load_data <- function(filepath) {
  # Load data from Excel and filter to start from 2010
  data <- readxl::read_excel(filepath) %>%
    mutate(time = as.Date(time)) %>%
    filter(time >= as.Date("2010-01-01"))
  return(data)
}

# 2. Decomposition Analysis (SEATS Approximation)
perform_decomposition <- function(data, model = "additive") {
  decomposition_results <- list()
  
  # Loop through each country
  countries <- unique(data$geo)
  for (country in countries) {
    country_data <- data %>% filter(geo == country) %>% select(time, values) %>%
      arrange(time)
    ts_data <- ts(country_data$values, frequency = 12, start = c(year(min(country_data$time)), month(min(country_data$time))))
    
    if (model == "multiplicative") {
      # Handle cases where multiplicative decomposition is possible
      if (all(ts_data > 0)) {
        decomposition <- decompose(ts_data, type = "multiplicative")
        decomposition_results[[country]] <- decomposition
      }
    } else {
      # Additive decomposition
      decomposition <- decompose(ts_data, type = "additive")
      decomposition_results[[country]] <- decomposition
    }
  }
  return(decomposition_results)
}

# 3. Outlier Removal (COVID-19 period)
remove_outliers <- function(decomposition_results, start_date = "2020-01-01", end_date = "2021-12-31") {
  cleaned_results <- list()
  covid_period <- as.Date(start_date):as.Date(end_date)
  
  for (country in names(decomposition_results)) {
    residuals <- decomposition_results[[country]]$random
    residuals_time <- time(residuals)
    
    # Filter out residuals within the COVID-19 period
    non_covid_residuals <- residuals[!residuals_time %in% covid_period]
    cleaned_results[[country]] <- non_covid_residuals
  }
  return(cleaned_results)
}

# 4. SEATS Approximation (Additive Model)
seats_approximation <- function(cleaned_residuals, model = "additive") {
  seats_results <- list()
  
  for (country in names(cleaned_residuals)) {
    residuals <- cleaned_residuals[[country]]
    ts_data <- ts(residuals, frequency = 12)
    
    if (model == "additive") {
      decomposition <- decompose(ts_data, type = "additive")
      seats_results[[country]] <- decomposition
    } else {
      if (all(ts_data > 0)) {
        decomposition <- decompose(ts_data, type = "multiplicative")
        seats_results[[country]] <- decomposition
      } else {
        message(paste("Multiplicative seasonality not suitable for", country))
      }
    }
  }
  return(seats_results)
}

# 5. RSAFull ARIMA Modeling with Regressors (e.g., Working Days)
fit_rsafull_arima <- function(cleaned_residuals, order = c(1, 1, 1), seasonal_order = c(0, 1, 1, 12)) {
  models <- list()
  
  for (country in names(cleaned_residuals)) {
    residuals <- cleaned_residuals[[country]]
    ts_data <- ts(residuals, frequency = 12)
    
    # Create working day regressor (1 for weekdays, 0 for weekends)
    working_days <- ifelse(weekdays(as.Date(time(ts_data))) %in% c("Saturday", "Sunday"), 0, 1)
    
    # Fit ARIMA with external regressor
    tryCatch({
      model <- auto.arima(ts_data, xreg = working_days, seasonal = TRUE, approximation = FALSE, stepwise = FALSE)
      models[[country]] <- model
      print(paste("Fitted RSAFull ARIMA model with regressors for", country))
      print(summary(model))
    }, error = function(e) {
      message(paste("Failed to fit RSAFull ARIMA model for", country, ":", e$message))
    })
  }
  return(models)
}

# Plot SEATS-like components for a country
plot_seats_components <- function(seats_results, country_code) {
  if (!is.null(seats_results[[country_code]])) {
    decomposition <- seats_results[[country_code]]
    
    par(mfrow = c(3, 1))
    plot(decomposition$trend, main = paste(country_code, "- Trend"))
    plot(decomposition$seasonal, main = paste(country_code, "- Seasonal"))
    plot(decomposition$random, main = paste(country_code, "- Irregular"))
    par(mfrow = c(1, 1))
  } else {
    message(paste("No SEATS approximation found for", country_code))
  }
}

# Example Usage

# 1. Load and prepare the data
data <- load_data("dane_eurostat.xlsx")

# 2. Perform additive decomposition
additive_decomposition_results <- perform_decomposition(data, model = "additive")

# 3. Remove outliers for COVID-19 period
cleaned_residuals <- remove_outliers(additive_decomposition_results, start_date = "2020-01-01", end_date = "2021-12-31")

# 4. SEATS approximation
seats_results <- seats_approximation(cleaned_residuals, model = "additive")

# Optional: Plot SEATS-like components for a specific country
# plot_seats_components(seats_results, 'DE')

# 5. RSAFull ARIMA model with regressors
rsafull_models <- fit_rsafull_arima(cleaned_residuals, order = c(1, 1, 1), seasonal_order = c(0, 1, 1, 12))
