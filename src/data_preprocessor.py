import pandas as pd
import os

def preprocess_stock_data(ticker: str, interval: str = "1d", raw_path: str = "data/raw", save_path: str = "data/processed"):
    """
    Load raw CSV, clean nulls, filter columns, and save to processed folder.
    """
    file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
    file_path = os.path.join(raw_path, file_name)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    print(f"Preprocessing {file_name}...")
    df = pd.read_csv(file_path, parse_dates=True, index_col=0)

    # Drop rows with null values
    df.dropna(inplace=True)

    # Optional: filter only useful columns
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    os.makedirs(save_path, exist_ok=True)
    output_path = os.path.join(save_path, file_name)
    df.to_csv(output_path)

    print(f"Processed data saved to: {output_path}")
    return df

# Sample run
if __name__ == "__main__":
    preprocess_stock_data("RELIANCE.NS", interval="1d")
