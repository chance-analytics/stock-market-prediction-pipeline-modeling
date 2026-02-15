import pandas as pd
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_colwidth', None)
import re

import yfinance as yf

def update_financial_dates(df, release_dates):
    df.index = df.index.strftime("%Y-%m-%d")
    
    df.index = df.index.map(lambda x: release_dates.get(x, x))  
    
    df.index = pd.to_datetime(df.index)
    
    return df

def stock_api_wrangling():
    tickers = ['AAPL','NVDA','TSLA'] 
    start = '2020-01-01'
    end = '2024-09-01'

    stockdt = yf.download(tickers, start = start, end = end, actions=True) 
    fundamentals = {}

    fundamental_fields = {
        'financials': ['Total Revenue','Gross Profit','Operating Expense','Research And Development', 'EBITDA'],
        'balance_sheet': ['Current Liabilities'],
        'cash_flow': ['Free Cash Flow'],
        'earnings': ['Basic EPS']
    }

    for ticker in tickers:
        stock = yf.Ticker(ticker)
    
        quarterly_financials = stock.quarterly_financials.T
        quarterly_balancesheet = stock.quarterly_balance_sheet.T
        quarterly_cashflow = stock.quarterly_cashflow.T
        quarterly_earnings = stock.quarterly_income_stmt.T
    
        quarterly_financials = quarterly_financials[(quarterly_financials.index >= start) & (quarterly_financials.index <= end)].sort_index()
        quarterly_balancesheet = quarterly_balancesheet[(quarterly_balancesheet.index >= start) & (quarterly_balancesheet.index <= end)].sort_index()
        quarterly_cashflow = quarterly_cashflow[(quarterly_cashflow.index >= start) & (quarterly_cashflow.index <= end)].sort_index()
        quarterly_earnings = quarterly_earnings[(quarterly_earnings.index >= start) & (quarterly_earnings.index <= end)].sort_index()
    
        financial_data = pd.DataFrame()  
    
        for category, fields in fundamental_fields.items():
            if category == "financials" and all(field in quarterly_financials.columns for field in fields):
                financial_data = pd.concat([financial_data, quarterly_financials[fields]], axis=1)
            elif category == "balance_sheet" and all(field in quarterly_balancesheet.columns for field in fields):
                financial_data = pd.concat([financial_data, quarterly_balancesheet[fields]], axis=1)
            elif category == "cash_flow" and all(field in quarterly_cashflow.columns for field in fields):
                financial_data = pd.concat([financial_data, quarterly_cashflow[fields]], axis=1)
            elif category == "earnings" and all(field in quarterly_earnings.columns for field in fields):
                financial_data = pd.concat([financial_data, quarterly_earnings[fields]], axis=1)
    
        fundamentals[ticker] = financial_data

    stockdt.index = pd.to_datetime(stockdt.index.date)
    stockdt.index.name = 'Date'

    merged_data_dict = {}

    for ticker in tickers:
        stock_data_ticker = stockdt[[col for col in stockdt.columns if ticker in col]].copy()
    
        stock_data_ticker.columns = stock_data_ticker.columns.droplevel(1) 
    
        merged_data = stock_data_ticker.join(fundamentals[ticker], how='left')
    
        merged_data_dict[ticker] = merged_data

    earnings_release_dates = {
        'AAPL':{
            '2023-03-31':'2023-05-04',
            '2023-06-30':'2023-08-03',
            '2023-09-30':'2023-11-02',
            '2023-12-31':'2024-02-01',
            '2024-03-31':'2024-05-02',
            '2024-06-30':'2024-08-01'
        },
        'NVDA':{
            '2023-04-30':'2023-05-24',
            '2023-07-31':'2023-08-23',
            '2023-10-31':'2023-11-21',
            '2024-01-31':'2024-02-21',
            '2024-04-30':'2024-05-22',
            '2024-07-31':'2024-08-28'
        },
        'TSLA':{
            '2023-03-31':'2023-04-19',
            '2023-06-30':'2023-07-19',
            '2023-09-30':'2023-10-18',
            '2023-12-31':'2024-01-24',
            '2024-03-31':'2024-04-23',
            '2024-06-30':'2024-07-23'
        }
    }

    for ticker in merged_data_dict:
        ticker_release_dates = earnings_release_dates.get(ticker, {})
        
        fundamentals[ticker] = update_financial_dates(fundamentals[ticker], ticker_release_dates)
        
        stock_data_ticker = merged_data_dict[ticker][[col for col in merged_data_dict[ticker].columns if col not in fundamentals[ticker].columns]]
        
        merged_data_dict[ticker] = stock_data_ticker.join(fundamentals[ticker], how="left")

    for ticker, df in merged_data_dict.items():
        object_columns = df.select_dtypes(include='object').columns
    
        df[object_columns] = df[object_columns].apply(pd.to_numeric).astype('float64')

    for ticker, df in merged_data_dict.items():
        df[['Dividends','Stock Splits']] = df[['Dividends','Stock Splits']].replace(0.0, np.nan)

    return merged_data_dict
