import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

#%matplotlib inline 

# Data loading and preparation class
class EurostatData:
    def __init__(self, filepath):
        # Load and filter data for time series analysis
        self.df = pd.read_excel(filepath)
        self.df['time'] = pd.to_datetime(self.df['time'])
        self.df = self.df[self.df['time'] >= '2010-01-01']

# Decomposition class for SEATS-like decomposition
class DecompositionAnalysis:
    def __init__(self, data):
        self.data = data
        self.countries = data['geo'].unique()

    def perform_decomposition(self, model='additive'):
        # Perform seasonal decomposition for each country
        decomposition_results = {}
        for country in self.countries:
            country_data = self.data[self.data['geo'] == country].set_index('time')['values'].dropna()
            if len(country_data) < 24:  # Ensure enough data points for monthly decomposition
                continue
            decomposition = seasonal_decompose(country_data, model=model, period=12)
            decomposition_results[country] = decomposition
        return decomposition_results

# Outlier removal class
class OutlierRemoval:
    def __init__(self, decomposition_results, start_date="2020-01-01", end_date="2021-12-31"):
        self.decomposition_results = decomposition_results
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.cleaned_results = {}

    def remove_outliers(self):
        # Iterate over each country's decomposition and remove COVID-19 period residuals
        for country, decomposition in self.decomposition_results.items():
            residuals = decomposition.resid.dropna()
            residuals_df = residuals.to_frame(name='residuals')
            residuals_df['date'] = residuals_df.index

            # Filter out residuals within the COVID-19 period
            covid_period = (residuals_df['date'] >= self.start_date) & (residuals_df['date'] <= self.end_date)
            residuals_df = residuals_df[~covid_period]  # Keep only dates outside the COVID period

            # Store the cleaned residuals for this country
            self.cleaned_results[country] = residuals_df.set_index('date')['residuals']
        return self.cleaned_results

# SEATS approximation class
class SeatsApproximation:
    def __init__(self, cleaned_residuals):
        self.cleaned_residuals = cleaned_residuals
        self.seats_results = {}

    def seats_decomposition(self, model='additive'):
        # Perform SEATS-like decomposition (additive or multiplicative)
        decomposition_results = {}
        for country, residuals in self.cleaned_residuals.items():
            try:
                decomposition = seasonal_decompose(residuals, model=model, period=12)
                decomposition_results[country] = decomposition
                print(f"SEATS approximation completed for {country}.\n")
            except Exception as e:
                print(f"Could not decompose {country}: {e}")
        self.seats_results = decomposition_results

    def plot_seats_components(self, country_code):
        # Plot SEATS-like decomposition for a specific country
        if country_code in self.seats_results:
            decomposition = self.seats_results[country_code]
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
            fig.suptitle(f'{country_code} - SEATS Approximation', fontsize=16)

            ax1.plot(decomposition.trend, label='Trend', color='green')
            ax1.set_title('Trend')
            ax2.plot(decomposition.seasonal, label='Seasonal', color='blue')
            ax2.set_title('Seasonal')
            ax3.plot(decomposition.resid, label='Irregular', color='red')
            ax3.set_title('Irregular')

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()
        else:
            print(f"No SEATS approximation found for {country_code}.")

# RSAFull ARIMA model with working day regressors
class RSAFullModel:
    def __init__(self, cleaned_residuals):
        self.cleaned_residuals = cleaned_residuals
        self.models = {}

    def fit_arima_with_regressors(self, order=(1, 1, 1), seasonal_order=(0, 1, 1, 12)):
        for country, residuals in self.cleaned_residuals.items():
            # Create a working days regressor (1 for weekdays, 0 for weekends)
            residuals_df = residuals.to_frame(name='residuals')
            residuals_df['working_day'] = np.where(residuals_df.index.dayofweek < 5, 1, 0)

            try:
                # Fit ARIMA model with working day regressor
                model = ARIMA(residuals_df['residuals'], order=order, seasonal_order=seasonal_order, exog=residuals_df[['working_day']])
                fitted_model = model.fit()
                self.models[country] = fitted_model
                print(f"Fitted RSAFull ARIMA model with regressors for {country}")
                print(fitted_model.summary())
                print("\n" + "-" * 60 + "\n")

            except Exception as e:
                print(f"Could not fit RSAFull ARIMA model for {country}: {e}")

    def plot_diagnostics(self, country_code):
        if country_code in self.models:
            self.models[country_code].plot_diagnostics(figsize=(10, 8))
            plt.suptitle(f'Diagnostics for {country_code} RSAFull ARIMA Model')
            plt.show()
        else:
            print(f"No model found for country: {country_code}")

# Example usage with the final integrated script

# 1. Load and prepare the data
data = EurostatData("./dane_eurostat.xlsx")

# 2. Perform additive decomposition
analysis = DecompositionAnalysis(data.df)
additive_decomposition_results = analysis.perform_decomposition(model='additive')

# 3. Remove outliers for COVID-19 period
outlier_removal = OutlierRemoval(additive_decomposition_results, start_date="2020-01-01", end_date="2021-12-31")
cleaned_residuals = outlier_removal.remove_outliers()

# 4. SEATS approximation
seats_model = SeatsApproximation(cleaned_residuals)
seats_model.seats_decomposition(model='additive')

# Optional: Plot SEATS-like components for a specific country
# seats_model.plot_seats_components('DE')

# 5. RSAFull ARIMA model with regressors
rsafull_model = RSAFullModel(cleaned_residuals)
rsafull_model.fit_arima_with_regressors(order=(1, 1, 1), seasonal_order=(0, 1, 1, 12))

# Optional: Plot diagnostics for a specific country
# rsafull_model.plot_diagnostics('DE')
