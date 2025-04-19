# Code to generate or label chart patterns
# src/pattern_generator.py

import pandas as pd
import os

def detect_double_bottom(df, threshold=0.02):
    """
    Detects Double Bottom pattern from OHLC data.
    Returns list of index pairs where pattern is detected.
    """
    bottoms = []
    for i in range(2, len(df) - 2):
        if df["Low"][i] < df["Low"][i-1] and df["Low"][i] < df["Low"][i+1]:
            bottoms.append((i, df["Low"][i]))

    # Compare bottoms for closeness in value (within threshold)
    patterns = []
    for i in range(len(bottoms)-1):
        idx1, low1 = bottoms[i]
        idx2, low2 = bottoms[i+1]
        if abs(low1 - low2) / max(low1, low2) < threshold and idx2 - idx1 < 30:
            patterns.append((idx1, idx2))

    return patterns

def detect_double_top(df, threshold=0.02):
    tops = []
    for i in range(2, len(df) - 2):
        if df["High"][i] > df["High"][i-1] and df["High"][i] > df["High"][i+1]:
            tops.append((i, df["High"][i]))

    patterns = []
    for i in range(len(tops)-1):
        idx1, high1 = tops[i]
        idx2, high2 = tops[i+1]
        if abs(high1 - high2) / max(high1, high2) < threshold and idx2 - idx1 < 30:
            patterns.append((idx1, idx2))

    return patterns

def detect_patterns_for_stock(ticker, interval="1d", processed_path="data/processed", save_path="data/patterns"):
    file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
    file_path = os.path.join(processed_path, file_name)

    if not os.path.exists(file_path):
        print(f"Processed file not found for: {ticker}")
        return

    df = pd.read_csv(file_path)

    df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)
    
    double_bottoms = detect_double_bottom(df)
    double_tops = detect_double_top(df)

    result = {
        "ticker": ticker,
        "double_bottoms": double_bottoms,
        "double_tops": double_tops
    }

    os.makedirs(save_path, exist_ok=True)
    out_path = os.path.join(save_path, f"{ticker.replace('.', '_')}_patterns.json")
    pd.Series(result).to_json(out_path, indent=2)

    print(f"Patterns saved to: {out_path}")


if __name__ == "__main__":
    detect_patterns_for_stock("RELIANCE.NS", interval="1d")

