# U.S. Labor-Market Analytics with **FRED®** Data (R)

This repository demonstrates how to **fetch**, **prepare** and **model** key U.S. labour-market indicators from the St. Louis Fed’s **FRED®** database.  
An **Autoregressive Distributed Lag (ARDL)** specification with stepwise selection is implemented to assess short-run relationships between non-farm payrolls and three high-frequency predictors.

---

## 1. Why this project?

* **Single-script workflow** – run `r_main.R` and obtain tidy input data, unit-root diagnostics, and an ARDL model summary in one go.
* **Fully reproducible** – the `renv/` lock-file captures exact R-package versions.
* **Minimal dependencies** – relies only on base R + a handful of tidyverse / econometrics packages.

---

## 2. Data series

| Series ID | Description | Transformation |
|-----------|-------------|-----------------|
| `PAYEMS`  | All Employees: Total Nonfarm | Month-over-month change (∆) |
| `NPPTTL`  | ADP® Total Private Payroll Employment | Month-over-month change (∆) |
| `ICSA`    | Initial Claims, Seasonally Adjusted | Month-over-month change (∆) |
| `CCSA`    | Continued Claims, Seasonally Adjusted | Month-over-month change (∆) |

All series are pulled at **monthly frequency** for the default window **2010-01-01 → 2022-01-01** (editable in `load_data()`).

---

## 3. Repository structure

```text
FRED_Analitic/
└── r_main/
    ├── r_main.R          # Main workflow script
    ├── renv/             # Package-management folder (auto-generated)
    └── .Rproj            # RStudio project (optional)
```

> **Note**: Output Excel files are written to an `output/` folder created at runtime.

---

## 4. Quick start

1. **Clone** the repo and open the `r_main` sub-folder in **RStudio** or another R IDE.
2. Run **`renv::restore()`** to install the exact package versions captured in `renv.lock`.
3. Supply your **FRED API key**:  
   ```r
   Sys.setenv(FRED_API_KEY = "YOUR_KEY_HERE")
   ```
   – or edit the hard-coded `fredr_set_key()` line inside `load_data()`.
4. Source `r_main.R` **F5**.  
   The script will:  
   * download the four series,  
   * difference them,  
   * run **ADF tests** for stationarity,  
   * estimate an **ARDL(p, q)** model with up to *l* lags (default 3) chosen via `dynlm` + `stepAIC`,  
   * print the final equation and diagnostic messages.

---

## 5. Key functions

* **`write_to_excel(df, name)`** – thin wrapper around **`writexl::write_xlsx()`**.
* **`load_data()`** – fetches raw FRED series and saves them to `output/payroll_data.xlsx`, `output/adp_data.xlsx` …
* **`data_preparing()`** – returns a *differenced* data-frame suitable for ARDL.
* **`adf_test_func()`** – loops over columns, prints ADF statistics.
* **`model_ardl_step(df, l)`** – fits `dynlm()` model and applies `MASS::stepAIC()` for lag-order reduction.

---

## 6. Extending the analysis

* **Change the forecast horizon** – adjust `data_start` / `data_end` in `load_data()`.
* **Add macro regressors** – include additional FRED series (e.g. CPI, ISM PMI) and extend `data_preparing()` accordingly.
* **Different model** – swap ARDL for **VAR** or **ARIMAX** using the prepared time-series frame.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|------|
| *“HTTP 403 – Invalid API key”* | FRED key missing or wrong | Set `Sys.setenv(FRED_API_KEY = "…")` before sourcing. |
| *`package ‘XYZ’ is not available`* | Locked dependency not on CRAN anymore | Run `renv::hydrate()` to use a local cache or update `renv.lock`. |
| *Lag length loop never ends* | `l` argument set too high | Pass a smaller lag order to `model_ardl_step(df, l)`. |

---

## 8. License

Released under the MIT License – see `LICENSE` for details.

FRED® and Federal Reserve Bank of St. Louis marks are used in accordance with their **terms of use**. This project is **not** endorsed by or affiliated with the Federal Reserve System.

---

## 9. Contact

Questions or suggestions?  
Open an issue or email **your_email@example.com**.

---

_“In God we trust. All others must bring data.” – W. Edwards Deming_
