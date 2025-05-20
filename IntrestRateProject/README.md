# Interest Rate Project

A **cross‑language analytical toolkit** that demonstrates how to decompose and forecast key macro‑economic time‑series—*consumer price index (CPI)*, *short‑term interest rates*, and *unemployment rate*—using **Java + TRAMO/SEATS**, **Python + statsmodels**, and **R + forecast/fable**. The same monthly data set is explored with parallel techniques so you can compare results, performance and developer experience side‑by‑side.

---

## 1  Quick start

```bash
git clone https://github.com/<your‑org>/InterestRateProject.git
cd InterestRateProject

cd java/project
mvn clean package
java -jar target/project‑1.0‑SNAPSHOT.jar

cd ../..
cd python
python -m venv .venv && source .venv/bin/activate
python install_lib.py
python arima_model_core.py

cd ../r
Rscript -e "source('install_lib.R')"
Rscript arima_model_core.R
```

Generated charts (PNG) and logs are written to the respective `java/project`, `python`, or `r` folders.

---

## 2  Project layout

```text
InterestRateProject/
├─ java/
│  └─ project/              # Maven project (src, pom.xml, target/, graphs)
├─ python/
│  ├─ arima_model_core.py   # ARIMA pipeline (Python)
│  ├─ var_model_core.py     # VAR   pipeline (Python)
│  ├─ ardl_model_core.py    # ARDL  pipeline (Python)
│  └─ install_lib.py        # one‑shot dependency installer
├─ r/
│  ├─ arima_model_core.R    # ARIMA pipeline (R)
│  ├─ var_model_core.R      # VAR   pipeline (R)
│  ├─ ardl_model_core.R     # ARDL  pipeline (R)
│  └─ install_lib.R         # one‑shot dependency installer
└─ mainDataSet.csv          # Shared data set
```

| Folder | Highlights |
|--------|------------|
| **java/project** | TRAMO/SEATS seasonal‑adjustment via *nbdemetra‑sa*; data wrangling with Tablesaw; visualisation with JFreeChart; JUnit 5 tests |
| **python** | Classic econometric models in *statsmodels* (ADF test, ACF/PACF, ARIMA/VAR/ARDL); Matplotlib charts; self‑contained virtual‑environment setup |
| **r** | Modern tidy‑time‑series workflow with *tsibble*, *fable*, and *forecast*; ggplot2 visualisations; helper script *install_lib.R* installs required packages |

---

## 3  Data

`mainDataSet.csv` contains monthly observations from **January 2010 – April 2025** with four columns:

| Column | Description |
|--------|-------------|
| `observation_date` | Month‑end date (YYYY‑MM‑DD) |
| `Consumer_Price_Index` | CPI (2015 = 100) |
| `Interest_Rates` | Short‑term nominal interest rate (%) |
| `Unemployment_Rate` | Harmonised unemployment rate (%) |

Source: European Central Bank Statistical Data Warehouse (downloaded 2025‑05‑01).

---

## 4  Running the analyses

### 4.1 Java — TRAMO/SEATS

```bash
mvn exec:java -Dexec.mainClass="org.example.Main" -Dexec.args="--file mainDataSet.csv --column Interest_Rates --type trend"
```

### 4.2 Python — statsmodels

```bash
python arima_model_core.py --column Interest_Rates --forecast 12
```

### 4.3 R — fable/forecast

```bash
Rscript arima_model_core.R --column Interest_Rates --forecast 12
```

---

## 5  Requirements

| Language | Min version | Key libraries |
|----------|------------|---------------|
| **Java 17** | 17 | `tablesaw‑core`, `jfreechart`, `nbdemetra‑core`, `nbdemetra‑sa`, `junit‑jupiter` |
| **Python 3.10** | 3.8+ | `numpy`, `pandas`, `statsmodels`, `matplotlib` |
| **R 4.2** | 4.0+ | `tsibble`, `fable`, `forecast`, `ggplot2`, `tseries` |

Each language folder ships with a minimal installer (`install_lib.py` / `install_lib.R`) for reproducibility.

---

## 6  Testing

```bash
cd java/project && mvn test

cd ../../python && pytest

cd ../r && Rscript -e "testthat::test_dir('tests')"
```

---

## 7  Extending the project

* Swap in your own CSV with the same column names to analyse different countries.
* Add new models (e.g. SARIMAX, Prophet, ETS).
* For Java, inject additional processors such as X‑13ARIMA‑SEATS by implementing `IProcessing`.
* For R, plug‑in the *prophet* package or use *fable* functions for ensemble forecasts.

---

## 8  License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 9  Contact

Created by Pavel Shapavalau <https://www.linkedin.com/in/pavel-shapavalau-8a081b354?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app> for academic purposes at Kozminsky University. Feel free to open an issue or reach out via email.
