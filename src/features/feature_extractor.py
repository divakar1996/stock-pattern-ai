import pandas as pd
import numpy as np
import os

def add_technical_indicators(df):
    """
    Add technical indicators to the dataframe.
    These will be used as features for the machine learning model.
    """
    # Moving Averages
    df['SMA_50'] = df['Close'].rolling(window=50).mean()  # 50-period simple moving average
    df['SMA_200'] = df['Close'].rolling(window=200).mean()  # 200-period simple moving average

    # Exponential Moving Averages (EMA)
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()  # 12-period EMA
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()  # 26-period EMA

    # Relative Strength Index (RSI)
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Moving Average Convergence Divergence (MACD)
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    df['BB_upper'] = df['SMA_50'] + (2 * df['Close'].rolling(window=50).std())
    df['BB_lower'] = df['SMA_50'] - (2 * df['Close'].rolling(window=50).std())

    # Volume-related Indicators
    df['Volume_MA'] = df['Volume'].rolling(window=50).mean()  # 50-period volume moving average
    df['Volatility'] = df['Close'].pct_change().rolling(window=14).std()  # 14-period volatility (rolling standard deviation)

    return df


def extract_features(ticker: str, interval: str = "1d", processed_path: str = "data/processed", save_path: str = "data/features"):
    """
    Extract features from stock data and save the resulting data to CSV.
    """
    file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
    file_path = os.path.join(processed_path, file_name)

    if not os.path.exists(file_path):
        print(f"Processed file not found for: {ticker}")
        return

    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # Add technical indicators as features
    df = add_technical_indicators(df)

    # Drop NaN values created during feature engineering
    df.dropna(inplace=True)

    os.makedirs(save_path, exist_ok=True)
    out_path = os.path.join(save_path, f"{ticker.replace('.', '_')}_{interval}_features.csv")
    df.to_csv(out_path)

    print(f"Features saved to: {out_path}")
    return df


if __name__ == "__main__":
    extract_features("RELIANCE.NS", interval="1d")
