# Stock Market Prediction Pipeline — Version 1 (ETL + SQLite Integration)
*Python + SQL + Web Scraping + API Ingestion (AAPL/NVDA/TSLA focus)*

## Overview
Version 1 is the **data engineering / ETL build** for a multi-source market dataset. The goal is to demonstrate how to collect, clean, and unify:
- **Economic indicators** (FRED flat files)
- **World events** (Wikipedia web scraping)
- **Market + fundamentals** (Yahoo Finance via `yfinance` API)

Outputs are stored in a local **SQLite database** (`finalproject.db`) with separate fact tables plus a merged table.

---

## Data sources (implemented)
- **FRED (flat files):** macro time series (mixed daily/weekly/monthly/quarterly)
- **Wikipedia (web):** year pages with daily “Events” listings (text cleaned)
- **Yahoo Finance / yfinance (API):** daily OHLCV + corporate actions + selected quarterly fundamentals  
  **Tickers:** AAPL, NVDA, TSLA (2020-01-01 to 2024-09-01 in the API script)

---

## What I built (code + notebooks)
### Notebooks (Version 1 milestones)
- **`Project Version 1 Milestone 2 Python Notebook.ipynb`** — clean/transform FRED flat files (5+ cleansing steps)
- **`Project Version 1 Milestone 3 Python Notebook.ipynb`** — scrape/clean Wikipedia “Events” section (5+ cleansing steps)
- **`Project Version 1 Milestone 4 Python Notebook.ipynb`** — pull and clean API data (yfinance OHLCV + fundamentals)
- **`Project Version 1 Milestone 5 Python Notebook.ipynb`** — load tables into SQLite, join into `merged_data`, and visualize

### Reusable Python module
- **`finalproject_function.py`**
  - `stock_api_wrangling()` downloads OHLCV + corporate actions for AAPL/NVDA/TSLA and merges quarterly fundamentals
  - includes a manual earnings-release mapping to shift fundamentals from quarter-end dates to release dates

---

## Database (SQLite) schema
SQLite file: **`finalproject.db`**

Tables (confirmed in the database):
- **`fctecon`** (11 cols): economic series aligned to date
- **`fctworldevet`** (2 cols): `event_date`, `event_cleaned`
- **`fctapi`** (49 cols): AAPL/NVDA/TSLA OHLCV + actions + fundamentals
- **`merged_data`** (60 cols): joined table used for downstream analysis/visualization

---

## How to run (Version 1)
### 1) Create an environment
```bash
conda create -n market-etl-v1 python=3.11 -y
conda activate market-etl-v1
pip install pandas numpy matplotlib requests beautifulsoup4 yfinance openpyxl
```

### 2) Run notebooks in order
1. Milestone 2: FRED cleaning  
2. Milestone 3: Wikipedia scraping  
3. Milestone 4: API ingestion (`finalproject_function.py`)  
4. Milestone 5: SQLite load + merge + charts  

After Milestone 5, you should have an updated `finalproject.db` containing the tables above.

---

## Notes / limitations
- Economic series are mixed frequency; aligning them to a common date index requires assumptions (e.g., forward-fill).
- Wikipedia events in Version 1 are cleaned as text (sentiment modeling comes in Version 2).
- This version focuses on ETL and storage; forecasting results are documented in Version 2.

---

## Author
**Chance Xu**  
GitHub: https://github.com/chance-analytics
