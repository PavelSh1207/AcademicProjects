import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

# 1. Data Loading and Preparation
class EurostatData:
    def __init__(self, filepath):
        self.df = pd.read_excel(filepath)
        self.df['time'] = pd.to_datetime(self.df['time'])
        self.df = self.df[self.df['time'] >= '2010-01-01']

# 2. Decomposition Analysis
class DecompositionAnalysis:
    def __init__(self, data):
        self.data = data
        self.countries = data['geo'].unique()

    def perform_decomposition(self, model='additive'):
        decomposition_results = {}
        for country in self.countries:
            country_data = self.data[self.data['geo'] == country].set_index('time')['values'].dropna()
            if len(country_data) < 24:
                continue
            decomposition = seasonal_decompose(country_data, model=model, period=12)
            decomposition_results[country] = decomposition
            # Save decomposition components for each country
            result_df = pd.DataFrame({
                "trend": decomposition.trend,
                "seasonal": decomposition.seasonal,
                "residual": decomposition.resid
            })
            result_df.to_csv(f"{country}_decomposition_{model}.csv", index_label="date")
        return decomposition_results

# 3. Outlier Removal
class OutlierRemoval:
    def __init__(self, decomposition_results, start_date="2020-01-01", end_date="2021-12-31"):
        self.decomposition_results = decomposition_results
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.cleaned_results = {}

    def remove_outliers(self):
        for country, decomposition in self.decomposition_results.items():
            residuals = decomposition.resid.dropna()
            residuals_df = residuals.to_frame(name='residuals')
            residuals_df['date'] = residuals_df.index

            covid_period = (residuals_df['date'] >= self.start_date) & (residuals_df['date'] <= self.end_date)
            residuals_df = residuals_df[~covid_period]
            residuals_df.to_csv(f"{country}_cleaned_residuals.csv", index=False)
            self.cleaned_results[country] = residuals_df.set_index('date')['residuals']
        return self.cleaned_results

# 4. RSAFull ARIMA Modeling with Saving Summaries
class RSAFullModel:
    def __init__(self, cleaned_residuals):
        self.cleaned_residuals = cleaned_residuals
        self.models = {}

    def fit_arima_with_regressors(self, order=(1, 1, 1), seasonal_order=(0, 1, 1, 12)):
        for country, residuals in self.cleaned_residuals.items():
            residuals_df = residuals.to_frame(name='residuals')
            residuals_df['working_day'] = np.where(residuals_df.index.dayofweek < 5, 1, 0)
            try:
                model = ARIMA(residuals_df['residuals'], order=order, seasonal_order=seasonal_order, exog=residuals_df[['working_day']])
                fitted_model = model.fit()
                self.models[country] = fitted_model
                
                # Save model summary to a text file
                with open(f"{country}_rsafull_model_summary.txt", "w") as f:
                    f.write(f"RSAFull ARIMA Model Summary for {country}\n")
                    f.write(fitted_model.summary().as_text())
            except Exception as e:
                print(f"Could not fit RSAFull ARIMA model for {country}: {e}")

# Final Script Usage
data = EurostatData("./dane_eurostat.xlsx")
analysis = DecompositionAnalysis(data.df)
decomposition_results = analysis.perform_decomposition(model='additive')

outlier_removal = OutlierRemoval(decomposition_results, start_date="2020-01-01", end_date="2021-12-31")
cleaned_residuals = outlier_removal.remove_outliers()

rsafull_model = RSAFullModel(cleaned_residuals)
rsafull_model.fit_arima_with_regressors(order=(1, 1, 1), seasonal_order=(0, 1, 1, 12))
