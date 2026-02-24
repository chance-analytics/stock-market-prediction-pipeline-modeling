# Stock Market Movement Prediction — Version 2 (Modeling + Evaluation)
*Python + Feature Engineering + ML/NLP (SPY daily Buy/Sell)*

## Overview
Version 2 is the **final implemented modeling workflow**. It builds a daily dataset that combines:
- **Economic indicators** from FRED (aligned to trading days)
- **SPY market data + technical indicators** from Yahoo Finance (`yfinance` + `pandas_ta`)
- **Wikipedia world events** transformed into **daily sentiment features** (VADER)

Then it trains classifiers to predict **next-day SPY direction** (Buy/Sell) using time-based splits.

---

## What’s in the code (Version 2 notebook)
- **`Project Version 2 Python Notebook.ipynb`**
  - pulls/loads FRED series (GDP growth, unemployment rate, fed funds rate, sticky CPI)
  - scrapes Wikipedia yearly pages (2020–2024) and computes sentiment with VADER
  - pulls SPY daily OHLCV and computes EMA/RSI/MACD/Bollinger via `pandas_ta`
  - merges features on trading days and exports **`final_data.csv`**
  - trains/tunes **Random Forest** and **XGBoost** (GridSearchCV)
  - evaluates on a **time-based test set (2024)**

---

## Modeling setup (as implemented)
- **Date range:** 2020–2024 (with lookback beginning mid-2019 for indicators)
- **Final merged dataset:** 1,258 trading-day rows and 17 features (exported as `final_data.csv`)
- **Target label:** next-day Buy if `Close(t+1) > Open(t+1)` else Sell (“Hold” merged into Sell)
- **Split:** train 2021–2023; test 2024 (time-ordered)

---

## Results (2024 test set)
- **Random Forest:** 50.4% accuracy, macro F1 = 0.49 (best balanced)
- **XGBoost:** 52.8% accuracy, macro F1 = 0.38 (high Buy recall, weak Sell recall)

**Takeaway:** technical indicators carried more usable short-horizon signal than macro and Wikipedia sentiment in this setup. Performance near ~50–53% aligns with the difficulty of daily direction prediction.

---

## How to run (Version 2)
```bash
conda create -n market-ml-v2 python=3.11 -y
conda activate market-ml-v2
pip install pandas numpy scikit-learn xgboost yfinance requests beautifulsoup4 vaderSentiment pandas_ta tqdm pyarrow
```

Then open and run:
- `Project Version 2 Python Notebook.ipynb`

The notebook exports `final_data.csv` and prints evaluation metrics.

---

## Limitations
- Daily direction is extremely noisy; small edges are hard to validate statistically.
- Macro series are forward-filled; release timing and “surprise” effects aren’t modeled.
- Wikipedia events are not finance-specific; sentiment is a weak proxy here.
- This is not a transaction-cost-aware backtest.

---

## Author
**Chance Xu**  
GitHub: https://github.com/chance-analytics
