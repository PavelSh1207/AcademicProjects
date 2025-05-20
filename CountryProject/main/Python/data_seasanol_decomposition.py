import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose 



class GetData():
    def __init__(self, name):
        self.name = name
        self.df = pd.read_excel(self.name)
        
class Transform(GetData):
     def __init__(self, name):
        super().__init__(name)
        self.columns = ['time', 'geo', 'values']
        self.dataFrame = self.df[self.columns]
        self.dataFrame['time'] = pd.to_datetime(self.dataFrame['time'])
        self.dataFrame = self.dataFrame[self.dataFrame['time'] >= '2010-01-01']
        
class Plots(Transform):
    def __init__(self, name):
        super().__init__(name)
        self.plot_all_countries()

    def plot_all_countries(self):
        """Generuje wykresy dla wszystkich krajów na jednej planszy."""
        countries = self.dataFrame['geo'].unique()
        num_countries = len(countries)
        
        # Konfiguracja siatki podwykresów
        cols = 3
        rows = (num_countries // cols) + (num_countries % cols > 0)
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows), squeeze=False)
        fig.suptitle("Wykresy dla poszczególnych krajów", fontsize=16)

        for idx, country in enumerate(countries):
            row, col = divmod(idx, cols)
            country_data = self.dataFrame[self.dataFrame['geo'] == country]
            ax = axes[row, col]
            ax.plot(country_data['time'], country_data['values'], marker='o', label=country)
            ax.set_title(f"Kraj: {country}")
            ax.set_xlabel("Czas")
            ax.set_ylabel("Wartości")
            ax.grid(True)
        
        # Usuwanie pustych osi, jeśli liczba krajów nie jest wielokrotnością liczby kolumn
        for i in range(num_countries, rows * cols):
            fig.delaxes(axes.flatten()[i])

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show() 

class DecompositionPlots(Transform):
    def __init__(self, name):
        super().__init__(name)
        self.countries = self.dataFrame['geo'].unique()
        self.plot_decomposition()

    def plot_decomposition(self):
        # Ustawienia wykresów
        cols = 3
        rows = (len(self.countries) // cols) + (len(self.countries) % cols > 0)
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows), squeeze=False)
        fig.suptitle("Dekompozycja szeregów czasowych dla poszczególnych krajów", fontsize=16)

        for idx, country in enumerate(self.countries):
            country_data = self.dataFrame[self.dataFrame['geo'] == country]
            country_data.set_index('time', inplace=True)  # Ustawienie czasu jako indeksu dla dekompozycji
            
            # Wykonanie dekompozycji
            decomposition = seasonal_decompose(country_data['values'], model="additive", period=12)
            
            # Rysowanie składników dekompozycji
            ax = axes[idx // cols, idx % cols]
            ax.plot(decomposition.trend, label='Trend', color='blue')
            ax.plot(decomposition.seasonal, label='Sezonowość', color='orange')
            ax.plot(decomposition.resid, label='Reszty', color='green')
            ax.set_title(f"Dekompozycja: {country}")
            ax.legend()
        
        # Usunięcie pustych osi, jeśli liczba krajów nie jest wielokrotnością liczby kolumn
        for i in range(len(self.countries), rows * cols):
            fig.delaxes(axes.flatten()[i])
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

class WithoutwWorkingDay(Transform):
    def __init__(self, name):
        super().__init__(name)
        self.countries = self.dataFrame['geo'].unique()
        self.dataFrame = self.dataFrame[self.dataFrame['time'].dt.dayofweek < 5]
        self.plot_decomposition()

    def plot_decomposition(self):
        # Ustawienia wykresów
        cols = 3
        rows = (len(self.countries) // cols) + (len(self.countries) % cols > 0)
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows), squeeze=False)
        fig.suptitle("Dekompozycja szeregów czasowych dla poszczególnych krajów", fontsize=16)

        for idx, country in enumerate(self.countries):
            country_data = self.dataFrame[self.dataFrame['geo'] == country]
            country_data.set_index('time', inplace=True)  # Ustawienie czasu jako indeksu dla dekompozycji
            
            # Wykonanie dekompozycji
            decomposition = seasonal_decompose(country_data['values'], model="additive", period=12)
            
            # Rysowanie składników dekompozycji
            ax = axes[idx // cols, idx % cols]
            ax.plot(decomposition.trend, label='Trend', color='blue')
            ax.plot(decomposition.seasonal, label='Sezonowość', color='orange')
            ax.plot(decomposition.resid, label='Reszty', color='green')
            ax.set_title(f"Dekompozycja: {country}")
            ax.legend()
        
        # Usunięcie pustych osi, jeśli liczba krajów nie jest wielokrotnością liczby kolumn
        for i in range(len(self.countries), rows * cols):
            fig.delaxes(axes.flatten()[i])
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
#DecompositionPlots("dane_eurostat.xlsx")
WithoutwWorkingDay("./dane_eurostat.xlsx")
            



from datetime import datetime

class OutlierRemoval:
    def __init__(self, decomposition_results, start_date="2020-01-01", end_date="2021-12-31"):
        self.decomposition_results = decomposition_results
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.cleaned_results = {}

    def remove_outliers(self):
        # Iterate over each country's decomposition and remove COVID-19 period residuals
        for country, decomposition in self.decomposition_results.items():
            # Convert residuals to a DataFrame for easy date-based filtering
            residuals = decomposition.resid.dropna()
            residuals_df = residuals.to_frame(name='residuals')
            residuals_df['date'] = residuals_df.index

            # Filter out residuals within the COVID-19 period
            covid_period = (residuals_df['date'] >= self.start_date) & (residuals_df['date'] <= self.end_date)
            residuals_df = residuals_df[~covid_period]  # Keep only dates outside the COVID period

            # Store the cleaned residuals for this country
            self.cleaned_results[country] = residuals_df.set_index('date')['residuals']

        return self.cleaned_results

    def plot_cleaned_residuals(self):
        # Plot the cleaned residuals for each country
        for country, residuals in self.cleaned_results.items():
            plt.figure(figsize=(10, 4))
            plt.plot(residuals, label='Cleaned Residuals', color='blue')
            plt.title(f'Cleaned Residuals (excluding COVID-19 period) - {country}')
            plt.xlabel('Date')
            plt.ylabel('Residual')
            plt.legend()
            plt.show()

# Initialize and apply the outlier removal process
outlier_removal = OutlierRemoval(additive_decomposition_results, start_date="2020-01-01", end_date="2021-12-31")
cleaned_residuals = outlier_removal.remove_outliers()

# Plot the cleaned residuals to verify outlier removal
outlier_removal.plot_cleaned_residuals()
