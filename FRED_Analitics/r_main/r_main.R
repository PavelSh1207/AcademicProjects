# Install and load the required libraries
#install.packages("fredr")
#install.packages("writexl")
#install.packages("openxlsx")
#install.packages("tseries")
#install.packages("MASS")
#install.packages("dplyr")
#install.packages("tidyr")
#install.packages("dynlm")
library(tseries)
library(openxlsx)
library(fredr)
library(writexl)
library(MASS)
library(dplyr)
library(tidyr)
library(dynlm)

# Define a custom function that exports data to Excel
write_to_excel <- function(data, name) {
  write_xlsx(data, path = paste0(name, ".xlsx"))
}

# Define a function that loads data from FRED
load_data <- function(variables) {
  data_start <- "2010-01-01"
  data_end <- "2022-01-01"
  
  # Set the FRED API key
  key <- "8d569db4341475c8864ad88497f2059d"
  fredr_set_key(key)
  
  # Fetch payroll data and write it to Excel
  payrolle <- fredr(series_id = "PAYEMS", 
                    frequency = "m", 
                    units = "chg", 
                    observation_start = as.Date(data_start),
                    observation_end = as.Date(data_end)
  )
  write_to_excel(payrolle, "payroll_data")
  
  # Fetch additional data series and write them to Excel
  adp_employment <- fredr(series_id = "NPPTTL", 
                          frequency = "m", 
                          units = "chg", 
                          observation_start = as.Date(data_start),
                          observation_end = as.Date(data_end)
  )
  write_to_excel(adp_employment, "adp_employment_data")
  
  initial_claims <- fredr(series_id = "ICSA", 
                          frequency = "m", 
                          units = "chg", 
                          observation_start = as.Date(data_start),
                          observation_end = as.Date(data_end)
  )
  write_to_excel(initial_claims, "initial_claims_data")
  
  continuous_claims <- fredr(series_id = "CCSA", 
                             frequency = "m", 
                             units = "chg", 
                             observation_start = as.Date(data_start),
                             observation_end = as.Date(data_end)
  )
  write_to_excel(continuous_claims, "continuous_claims_data")
  
  date <- c(payrolle$date)
  pay <- c(payrolle$value)
  adp <- c(adp_employment$value)
  init_claims <- c(initial_claims$value)
  con_claims <- c(continuous_claims$value)
  
  if (length(pay) == length(adp) & length(adp) == length(init_claims) & length(init_claims) == length(con_claims) & length(date) == length(con_claims)) {
    print("TRUE")
      general_data <- data.frame(
        date = date,
        pay = pay,
        adp = adp,
        init_claims = init_claims,
        con_claims = con_claims
  )
  write_to_excel(general_data, "d:\\Kozminski\\KozminskiProjects\\zd_II\\r_main\\general_data")

  } else {
    print("FALSE")
  }

  return (general_data)
}

data_preparing <- function(d){

  data_diff <- data.frame(
    pay_diff = diff(d$pay),
    adp_diff = diff(d$adp),
    init_claims_diff = diff(d$init_claims),
    con_claims_diff = diff(d$con_claims)
  )
  return(data_diff)
}

adf_test_func <- function(get_data){
  for(i in names(get_data)){
    adf_test <- adf.test(get_data[[i]], alternative = "stationary") #return Return columns as vectors for the ADF test because adf.test does not accept data‑frame subsets
    print(adf_test)
  }
  return(adf_test)
}

model_ardl_step <- function(diff_data, l){
  diff_data <- na.omit(diff_data)  # Remove any rows containing NA values introduced by differencing and lagging
  lg <- 0
  while(lg < l || lg == l){
    message_ardl <- paste("===============================================","model lag = ", lg, "ARDL MODEL", "===============================================", "")
    message_step <- paste("===============================================","model lag = ", lg, "Step Model", "===============================================","")

    # ARDL model
    print(message_ardl)
    ardl_model <- dynlm(pay_diff ~ L(pay_diff, lg) + L(adp_diff, lg) + L(init_claims_diff, lg) + L(con_claims_diff, lg), data = diff_data)
    model_ardl_summary <- summary(ardl_model)
    print(model_ardl_summary)

    # Stepwise model
    step_model <- stepAIC(ardl_model, direction = "both")
    step_model_summary <- summary(step_model)
    print(message_step)
    print(step_model_summary)

    lg <- lg+1
  }

  return(0)

}

# Load the data
d <- load_data()

# Prepare the data
data_prepared <- data_preparing(d)

# ARDL model
model1 <- model_ardl_step(data_prepared,3)

text <- paste("Końcowy model pokazuje, że zmienne L(adp_diff, lg), L(init_claims_diff, lg), i L(con_claims_diff, lg) nie mają dużego wpływu na różnice w zatrudnieniu, podczas gdy autokorelacja w pay_diff (czyli L(pay_diff, lg)) odgrywa dominującą rolę w wyjaśnianiu zmienności w danych. Co nie jest wg mnie podlegającą intuiji ekonomicznej.")
comment <- paste("","===============================================","", text,"","===============================================","")
print(comment)

# The final model shows that the variables L(adp_diff, lg), L(init_claims_diff, lg), and L(con_claims_diff, lg) have little influence on employment differences, whereas autocorrelation in pay_diff (i.e., L(pay_diff, lg)) plays the dominant role in explaining the variability of the data. In my opinion, this does not align with economic intuition.
