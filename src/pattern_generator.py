# # Code to generate or label chart patterns
# # src/pattern_generator.py

# import pandas as pd
# import os

# def detect_double_bottom(df, threshold=0.02):
#     """
#     Detects Double Bottom pattern from OHLC data.
#     Returns list of index pairs where pattern is detected.
#     """
#     bottoms = []
#     for i in range(2, len(df) - 2):
#         if df["Low"][i] < df["Low"][i-1] and df["Low"][i] < df["Low"][i+1]:
#             bottoms.append((i, df["Low"][i]))

#     # Compare bottoms for closeness in value (within threshold)
#     patterns = []
#     for i in range(len(bottoms)-1):
#         idx1, low1 = bottoms[i]
#         idx2, low2 = bottoms[i+1]
#         if abs(low1 - low2) / max(low1, low2) < threshold and idx2 - idx1 < 30:
#             patterns.append((idx1, idx2))

#     return patterns

# def detect_double_top(df, threshold=0.02):
#     tops = []
#     for i in range(2, len(df) - 2):
#         if df["High"][i] > df["High"][i-1] and df["High"][i] > df["High"][i+1]:
#             tops.append((i, df["High"][i]))

#     patterns = []
#     for i in range(len(tops)-1):
#         idx1, high1 = tops[i]
#         idx2, high2 = tops[i+1]
#         if abs(high1 - high2) / max(high1, high2) < threshold and idx2 - idx1 < 30:
#             patterns.append((idx1, idx2))

#     return patterns

# def detect_patterns_for_stock(ticker, interval="1d", processed_path="data/processed", save_path="data/patterns"):
#     file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
#     file_path = os.path.join(processed_path, file_name)

#     if not os.path.exists(file_path):
#         print(f"Processed file not found for: {ticker}")
#         return

#     df = pd.read_csv(file_path)

#     df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors='coerce')
#     df.dropna(inplace=True)
    
#     double_bottoms = detect_double_bottom(df)
#     double_tops = detect_double_top(df)

#     result = {
#         "ticker": ticker,
#         "double_bottoms": double_bottoms,
#         "double_tops": double_tops
#     }

#     os.makedirs(save_path, exist_ok=True)
#     out_path = os.path.join(save_path, f"{ticker.replace('.', '_')}_patterns.json")
#     pd.Series(result).to_json(out_path, indent=2)

#     print(f"Patterns saved to: {out_path}")


# if __name__ == "__main__":
#     detect_patterns_for_stock("RELIANCE.NS", interval="1d")


# import pandas as pd
# import os

# def detect_double_bottom(df, threshold=0.02):
#     """
#     Detects Double Bottom pattern from OHLC data.
#     Returns list of index pairs where pattern is detected.
#     """
#     bottoms = []
#     for i in range(2, len(df) - 2):
#         if df["Low"][i] < df["Low"][i-1] and df["Low"][i] < df["Low"][i+1]:
#             bottoms.append((i, df["Low"][i]))

#     # Compare bottoms for closeness in value (within threshold)
#     patterns = []
#     for i in range(len(bottoms)-1):
#         idx1, low1 = bottoms[i]
#         idx2, low2 = bottoms[i+1]
#         if abs(low1 - low2) / max(low1, low2) < threshold and idx2 - idx1 < 30:
#             patterns.append((idx1, idx2))

#     return patterns

# def detect_double_top(df, threshold=0.02):
#     """
#     Detects Double Top pattern from OHLC data.
#     Returns list of index pairs where pattern is detected.
#     """
#     tops = []
#     for i in range(2, len(df) - 2):
#         if df["High"][i] > df["High"][i-1] and df["High"][i] > df["High"][i+1]:
#             tops.append((i, df["High"][i]))

#     # Compare tops for closeness in value (within threshold)
#     patterns = []
#     for i in range(len(tops)-1):
#         idx1, high1 = tops[i]
#         idx2, high2 = tops[i+1]
#         if abs(high1 - high2) / max(high1, high2) < threshold and idx2 - idx1 < 30:
#             patterns.append((idx1, idx2))

#     return patterns

# def detect_patterns_for_stock(ticker, interval="1d", processed_path="data/processed", save_path="data/patterns"):
#     """
#     Detect patterns (Double Bottom and Double Top) for a given stock ticker.
#     The patterns are saved in a JSON file.
#     """
#     file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
#     file_path = os.path.join(processed_path, file_name)

#     if not os.path.exists(file_path):
#         print(f"Processed file not found for: {ticker}")
#         return

#     df = pd.read_csv(file_path)

#     # Convert necessary columns to numeric and clean data
#     df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].apply(pd.to_numeric, errors='coerce')
#     df.dropna(inplace=True)
    
#     # Detect patterns
#     double_bottoms = detect_double_bottom(df)
#     double_tops = detect_double_top(df)

#     # Prepare result data
#     result = {
#         "ticker": ticker,
#         "double_bottoms": double_bottoms,
#         "double_tops": double_tops
#     }

#     # Save the detected patterns to JSON
#     os.makedirs(save_path, exist_ok=True)
#     out_path = os.path.join(save_path, f"{ticker.replace('.', '_')}_patterns.json")
#     pd.Series(result).to_json(out_path, indent=2)

#     print(f"Patterns saved to: {out_path}")


# if __name__ == "__main__":
#     detect_patterns_for_stock("RELIANCE.NS", interval="1d")




# import pandas as pd
# import os
# import numpy as np

# def detect_patterns(df, window_size=5, threshold=0.02):
#     """
#     Detect simple reversal patterns: Double Bottom and Double Top
#     :param df: pandas DataFrame, processed stock data with Open, High, Low, Close, Volume
#     :param window_size: int, number of days to look back and forward
#     :param threshold: float, minimum % difference to consider patterns
#     :return: list of detected patterns with their dates and types
#     """
#     patterns = []

#     # Loop over the dataframe
#     for i in range(window_size, len(df) - window_size):
#         window = df.iloc[i - window_size:i + window_size + 1]

#         center_close = df.iloc[i]['Close']
#         left_min = window.iloc[:window_size]['Close'].min()
#         right_min = window.iloc[window_size + 1:]['Close'].min()
#         left_max = window.iloc[:window_size]['Close'].max()
#         right_max = window.iloc[window_size + 1:]['Close'].max()

#         # Check for Double Bottom
#         if (abs(center_close - left_min) / center_close < threshold) and \
#            (abs(center_close - right_min) / center_close < threshold):
#             patterns.append({'Date': df.index[i], 'Pattern': 'Double Bottom'})

#         # Check for Double Top
#         if (abs(center_close - left_max) / center_close < threshold) and \
#            (abs(center_close - right_max) / center_close < threshold):
#             patterns.append({'Date': df.index[i], 'Pattern': 'Double Top'})

#     return patterns

# def process_files_for_patterns(processed_path="data/processed", patterns_path="data/patterns"):
#     """
#     Detect patterns across all processed stock files.
#     Save the detected patterns as JSON file for each stock.
#     """
#     os.makedirs(patterns_path, exist_ok=True)

#     for file_name in os.listdir(processed_path):
#         if file_name.endswith(".csv"):
#             file_path = os.path.join(processed_path, file_name)
#             df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

#             print(f"🔍 Detecting patterns in {file_name}...")
#             patterns = detect_patterns(df)

#             if patterns:
#                 # Save patterns
#                 stock_name = file_name.replace(".csv", "")
#                 output_file = os.path.join(patterns_path, f"{stock_name}_patterns.json")
#                 pd.DataFrame(patterns).to_json(output_file, orient='records', indent=4, date_format='iso')
#                 print(f"✅ Patterns saved for {stock_name}: {output_file}")
#             else:
#                 print(f"⚡ No patterns found in {file_name}")

# if __name__ == "__main__":
#     process_files_for_patterns()




import pandas as pd
import numpy as np
import json
import os
import matplotlib.pyplot as plt

def detect_double_bottoms(data, window=30, threshold=0.03):
    """
    Detect double bottom patterns in stock price data.
    """
    double_bottoms = []
    prices = data['Close'].values
    dates = data.index.to_list()

    for i in range(window, len(prices) - window):
        left_window = prices[i - window:i]
        right_window = prices[i:i + window]
        min_left = np.min(left_window)
        min_right = np.min(right_window)

        if (
            abs(min_left - min_right) / min_left < threshold
            and prices[i] == np.min(prices[i - window:i + window])
        ):
            double_bottoms.append((dates[i - window], dates[i], dates[i + window - 1]))

    return double_bottoms

def detect_double_tops(data, window=30, threshold=0.03):
    """
    Detect double top patterns in stock price data.
    """
    double_tops = []
    prices = data['Close'].values
    dates = data.index.to_list()

    for i in range(window, len(prices) - window):
        left_window = prices[i - window:i]
        right_window = prices[i:i + window]
        max_left = np.max(left_window)
        max_right = np.max(right_window)

        if (
            abs(max_left - max_right) / max_left < threshold
            and prices[i] == np.max(prices[i - window:i + window])
        ):
            double_tops.append((dates[i - window], dates[i], dates[i + window - 1]))

    return double_tops

def visualize_patterns(data, patterns, pattern_type="double_bottom"):
    """
    Plot stock data with highlighted patterns.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], label="Close Price", color='blue')

    for pattern in patterns:
        for date in pattern:
            plt.axvline(x=date, color='red' if pattern_type == "double_top" else 'green', linestyle='--')

    plt.title(f"Detected {pattern_type.replace('_', ' ').title()} Patterns")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

def detect_patterns_for_all(processed_folder="data/processed", patterns_folder="data/patterns"):
    """
    Detect patterns in all processed stock data files and save the results.
    """
    os.makedirs(patterns_folder, exist_ok=True)

    for file_name in os.listdir(processed_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(processed_folder, file_name)
            data = pd.read_csv(file_path, index_col="Date", parse_dates=True)

            print(f"Detecting patterns for {file_name}...")
            double_bottoms = detect_double_bottoms(data)
            double_tops = detect_double_tops(data)

            # Save properly as dictionary
            pattern_data = {
                "double_bottoms": double_bottoms,
                "double_tops": double_tops
            }

            output_file = os.path.join(patterns_folder, file_name.replace(".csv", "_patterns.json"))
            with open(output_file, "w") as f:
                json.dump(pattern_data, f, indent=4, default=str)

            print(f"✅ Saved patterns to {output_file}")

if __name__ == "__main__":
    detect_patterns_for_all()
