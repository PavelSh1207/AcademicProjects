import numpy as np
import pandas as pd
from statsmodels.tsa.x13 import x13_arima_analysis
import matplotlib.pyplot as plt

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
        
class TramsoSeats(Transform):
    def __init__(self, name):
        super().__init__(name)
        self.countries = self.dataFrame['geo'].unique()
        for idx, country in enumerate(self.countries):
            results = x13_arima_analysis(self.dataFrame['geo'] == self.countries, print_stdout=True)

# Ensure any reference to 'model' is removed from the function

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

    def plot_decomposition(self, decomposition_results):
        # Plot trend, seasonality, and residuals for each country
        for country, decomposition in decomposition_results.items():
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
            fig.suptitle(f'{country} Decomposition', fontsize=16)

            ax1.plot(decomposition.trend, label='Trend')
            ax1.set_title('Trend')
            ax2.plot(decomposition.seasonal, label='Seasonality')
            ax2.set_title('Seasonality')
            ax3.plot(decomposition.resid, label='Residuals')
            ax3.set_title('Residuals')

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()

# Re-instantiate analysis to avoid referencing any cached or old objects
data = EurostatData("./dane_eurostat.xlsx")
analysis = DecompositionAnalysis(data.df)

# Perform and plot only the additive decomposition to verify functionality
additive_decomposition = analysis.perform_decomposition(model='additive')
analysis.plot_decomposition(additive_decomposition)

            
            




       