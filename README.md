# TimeSeriesSymulation

A multi‑language sandbox for time‑series modelling, forecasting and visualisation.  
The repository gathers three independent mini‑projects written in **Python**, **R** and **Java**.

---

## Sub‑projects

| Folder | Language | Purpose |
|--------|----------|---------|
| `CountryProject` | Python & R | ARIMA / ARIMAX forecasting of Eurostat macro indicators for selected EU countries. |
| `FRED_Analitics` | R | U.S. labour‑market analytics powered by the FRED® API, including data wrangling and interactive plots. |
| `IntrestRateProject` | Java (Maven) | Interest‑rate, CPI and unemployment‑rate modelling with automatic seasonal adjustment and residual diagnostics. |

---

## Quick start

### 1. Clone

```bash
git clone https://github.com/<user>/TimeSeriesSymulation.git
cd TimeSeriesSymulation
```

### 2. CountryProject (Python)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r CountryProject/main/Python/requrements.txt
python CountryProject/main/Python/data_arimax13.py
```

### 3. FRED_Analitics (R)

```r
# inside R console
renv::restore()          # installs locked package versions
source("r_main/r_main.R")
```

### 4. IntrestRateProject (Java)

```bash
cd IntrestRateProject/java/project
mvn clean package
java -jar target/project.jar
```

---

## Data

Raw time series (CSV / Excel) live under each project’s `data/` folder.  
Generated artefacts such as model summaries, residual plots and cleaned series are stored in the corresponding `output/` directories.

---

## Requirements summary

* Python 3.9+
* R 4.3+ with `renv`
* Java 17+ and Maven 3.9+
* Common Python libs: `pandas`, `statsmodels`, `openpyxl`, `matplotlib`
* Common R libs: `tidyverse`, `forecast`, `ggplot2`, `httr`
* Graphviz for saving tree/diagram outputs (optional)

---

## License

MIT
