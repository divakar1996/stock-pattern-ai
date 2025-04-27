# # Code to fetch and preprocess stock data
# # src/data_loader.py

# import yfinance as yf
# import pandas as pd
# import os

# def fetch_stock_data(ticker: str, start: str, end: str, interval: str = "1d", save_path: str = "data/raw"):
#     """
#     Fetch stock OHLCV data using yfinance and save it as CSV.

#     :param ticker: Stock ticker symbol (e.g., 'AAPL')
#     :param start: Start date (YYYY-MM-DD)
#     :param end: End date (YYYY-MM-DD)
#     :param interval: Data interval ('1d', '1h', '5m', etc.)
#     :param save_path: Folder to save the CSV
#     """
#     print(f"Fetching data for {ticker} from {start} to {end} at {interval} interval...")
#     df = yf.download(ticker, start=start, end=end, interval=interval)
    
#     if not df.empty:
#         os.makedirs(save_path, exist_ok=True)
#         file_path = os.path.join(save_path, f"{ticker.replace('.','_')}_{interval}.csv")
#         df.to_csv(file_path)
#         print(f"Saved to {file_path}")
#         return df
#     else:
#         print("No data found.")
#         return None


# if __name__ == "__main__":
#     fetch_stock_data("RELIANCE.NS", start="2023-01-01", end="2024-12-31", interval="1d")




# src/data_loader.py
# src/data_loader.py

import yfinance as yf
import pandas as pd
import os
import time
from typing import List

def fetch_single_stock(
    ticker: str, 
    start: str, 
    end: str, 
    interval: str = "1d", 
    save_path: str = "data/raw"
):
    """
    Fetch OHLCV data for a single stock and save as CSV.
    """
    print(f"Fetching: {ticker} | Interval: {interval} | From: {start} To: {end}")
    try:
        df = yf.download(ticker, start=start, end=end, interval=interval, progress=False)
        
        if not df.empty:
            os.makedirs(save_path, exist_ok=True)
            file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
            file_path = os.path.join(save_path, file_name)
            df.to_csv(file_path)
            print(f"Saved: {file_path}")
            return df
        else:
            print(f"Warning: No data found for {ticker}.")
            return None

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def fetch_multiple_stocks(
    tickers: List[str], 
    start: str, 
    end: str, 
    interval: str = "1d", 
    save_path: str = "data/raw",
    delay: float = 1.0
):
    """
    Fetch OHLCV data for multiple stocks sequentially.
    """
    for ticker in tickers:
        fetch_single_stock(ticker, start, end, interval, save_path)
        time.sleep(delay)  # To avoid hitting API limits

if __name__ == "__main__":
    # Example run
    TICKERS = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]  # Add as many as you want
    fetch_multiple_stocks(
        tickers=TICKERS,
        start="2023-01-01",
        end="2024-12-31",
        interval="1d",
        save_path="data/raw"
    )
