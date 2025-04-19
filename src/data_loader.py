# Code to fetch and preprocess stock data
# src/data_loader.py

import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(ticker: str, start: str, end: str, interval: str = "1d", save_path: str = "data/raw"):
    """
    Fetch stock OHLCV data using yfinance and save it as CSV.

    :param ticker: Stock ticker symbol (e.g., 'AAPL')
    :param start: Start date (YYYY-MM-DD)
    :param end: End date (YYYY-MM-DD)
    :param interval: Data interval ('1d', '1h', '5m', etc.)
    :param save_path: Folder to save the CSV
    """
    print(f"Fetching data for {ticker} from {start} to {end} at {interval} interval...")
    df = yf.download(ticker, start=start, end=end, interval=interval)
    
    if not df.empty:
        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, f"{ticker.replace('.','_')}_{interval}.csv")
        df.to_csv(file_path)
        print(f"Saved to {file_path}")
        return df
    else:
        print("No data found.")
        return None


if __name__ == "__main__":
    fetch_stock_data("RELIANCE.NS", start="2023-01-01", end="2024-12-31", interval="1d")
