# Eurostat Industrial Production Time-Series Analysis

This project analyses monthly **Industrial Production Index (IPI)** data for selected European countries using seasonal decomposition and ARIMA modelling (RSA-full specification).  
Both **Python** and **R** implementations are provided so you can reproduce the entire workflow in the ecosystem you prefer.

---

## 1. Project goals

* **Clean and transform** raw Eurostat time-series data (from January 2010 onward).  
* **Decompose** each country’s series into trend, seasonal and irregular components.  
* **Fit ARIMA models with regressors (RSA-full)** to capture residual structure.  
* **Evaluate and export** diagnostic statistics, residuals and model summaries for further research or reporting.

---

## 2. Repository structure

```text
CountryProject/
├── data/
│   └── dane_eurostat.xlsx
├── main/
│   ├── Python/
│   │   ├── data_arimax13.py
│   │   ├── RSAFull ARIMA model with regressors.py
│   │   ├── RSAFull ARIMA Modeling with Saving Summaries.py
│   │   └── requrements.txt
│   └── R/
│       ├── RSAFull ARIMA Modeling with Regressors.R
│       └── RSAFull ARIMA Modeling with Saving Summaries.R
├── output/
│   ├── <CC>_cleaned_residuals.csv
│   ├── <CC>_decomposition_additive.csv
│   └── <CC>_rsafull_model_summary.txt
└── README.md
```

> **Tip:** `CC` stands for the two-letter ISO country code (DE, ES, FR, IT, NL, PL…).

---

## 3. Quick start

### 3.1 Python workflow

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r main/Python/requrements.txt

python main/Python/data_arimax13.py
```

The script will:

1. Load **`data/dane_eurostat.xlsx`**,
2. Filter the period 2010-01-01 → present,
3. Generate decompositions and ARIMA fits,
4. Save residuals & diagnostics inside **`output/`**.

### 3.2 R workflow

```r
install.packages(c("tidyverse", "forecast", "RJDemetra", "lubridate", "zoo"))

source("main/R/RSAFull ARIMA Modeling with Regressors.R")
```

---

## 4. Data source

* **Industrial Production Index, monthly (adjusted data)**  
  Provider: [Eurostat](https://ec.europa.eu/eurostat)  
  Dataset code: `PRD_B-D_I21_SCA` (manufacturing production, seasonally & calendar adjusted).  
  Licence: © European Union, reuse allowed under the Commission’s **CC-BY 4.0** licence.

The original extract is included for convenience. Consider downloading an updated version if you need the latest observations.

---

## 5. Results & interpretation

Each script writes country-specific artefacts to **`output/`**:

| File | Description |
|------|-------------|
| `*_decomposition_additive.csv` | Trend, seasonal and irregular components returned by `statsmodels.seasonal_decompose()` (Python) or `decompose()` (R). |
| `*_cleaned_residuals.csv` | Residuals after removing trend & seasonality – useful for stationarity checks. |
| `*_rsafull_model_summary.txt` | Detailed ARIMA parameter estimates and fit statistics. |

Plots are displayed interactively during execution and can be saved manually.

---

## 6. Extending the project

* Swap **additive** for **multiplicative** decomposition by changing the `model` argument.
* Adapt the **country list** by filtering different `geo` codes.
* Plug additional **exogenous regressors** (e.g. macro-economic indicators) into the ARIMA models.
* Convert scripts into **Jupyter notebooks** or **R Markdown** for richer narrative reports.

Pull requests are welcome – please open an issue first to discuss major changes.

---

## 7. Contributing

1. Fork the repository and create a feature branch.  
2. Follow the existing code style (PEP 8 for Python, tidyverse for R).  
3. Add/adjust unit tests where relevant.  
4. Submit a pull request describing the change.

---

## 8. Licence

Distributed under the **MIT License** – see `LICENSE` for details.

---

## 9. Contact

Questions or suggestions?  
Open an issue or reach out to **_your_email@example.com_**.

---

_Enjoy exploring European industrial trends!_