# src/dataset_builder.py

# import pandas as pd
# import numpy as np
# import json
# import os

# def create_dataset(ticker, window_size=30, interval="1d", processed_path="data/processed", pattern_path="data/patterns"):
#     file_ticker = ticker.replace('.', '_')
#     csv_file = os.path.join(processed_path, f"{file_ticker}_{interval}.csv")
#     pattern_file = os.path.join(pattern_path, f"{file_ticker}_patterns.json")

#     df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
#     features = df[["Open", "High", "Low", "Close", "Volume"]].values

#     with open(pattern_file, 'r') as f:
#         patterns = json.load(f)
    
#     # Merge all patterns into a list of important indices
#     pattern_indices = set()
#     for lst in patterns.get('double_bottoms', []) + patterns.get('double_tops', []):
#         pattern_indices.update(lst)

#     X = []
#     y = []

#     for i in range(len(features) - window_size):
#         window = features[i:i+window_size]
#         window_indices = set(range(i, i + window_size))

#         # Label window as 1 if any pattern falls inside window, else 0
#         label = int(len(window_indices.intersection(pattern_indices)) > 0)

#         X.append(window)
#         y.append(label)

#     X = np.array(X)
#     y = np.array(y)

#     print(f"Created dataset for {ticker}: {X.shape[0]} samples.")
#     return X, y

# # Example Usage:
# # X, y = create_dataset("RELIANCE.NS")



# src/dataset_builder.py




# import os
# import json
# import numpy as np
# import pandas as pd

# def create_dataset(processed_path="data/processed", pattern_path="data/patterns", output_path="data/datasets"):
#     """
#     Create a dataset for training from processed stock data and detected patterns.

#     - Inputs: processed stock CSV files and JSON pattern files
#     - Outputs: .npz file containing features (X) and labels (y)
#     """
#     os.makedirs(output_path, exist_ok=True)

#     X = []
#     y = []

#     for file_name in os.listdir(processed_path):
#         if not file_name.endswith(".csv"):
#             continue

#         ticker = file_name.replace(".csv", "")
#         processed_file = os.path.join(processed_path, file_name)
#         pattern_file = os.path.join(pattern_path, f"{ticker}_patterns.json")

#         # Load stock data
#         df = pd.read_csv(processed_file, index_col=0, parse_dates=True)

#         # Load patterns
#         if not os.path.exists(pattern_file):
#             print(f"Pattern file missing for {ticker}, skipping.")
#             continue

#         with open(pattern_file, "r") as f:
#             patterns = json.load(f)

#         double_bottoms = patterns.get('double_bottoms', [])
#         double_tops = patterns.get('double_tops', [])

#         # Convert patterns to a set of dates
#         pattern_dates = set()
#         for bottom in double_bottoms:
#             pattern_dates.update(bottom)
#         for top in double_tops:
#             pattern_dates.update(top)

#         # Build dataset: each example is a window of past prices
#         window_size = 30

#         for idx in range(window_size, len(df)):
#             window = df.iloc[idx-window_size:idx]
#             feature = window[["Open", "High", "Low", "Close", "Volume"]].values

#             # Normalize (optional, for better model training)
#             feature = (feature - feature.mean(axis=0)) / feature.std(axis=0)

#             date = df.index[idx]

#             label = 0  # Default: no pattern

#             if date.strftime("%Y-%m-%d") in pattern_dates:
#                 # If pattern detected on this day
#                 label = 1

#             X.append(feature)
#             y.append(label)

#     X = np.array(X)
#     y = np.array(y)

#     # Save dataset
#     dataset_file = os.path.join(output_path, "pattern_dataset.npz")
#     np.savez_compressed(dataset_file, X=X, y=y)
#     print(f"✅ Dataset created and saved to {dataset_file}")
#     print(f"X shape: {X.shape}, y shape: {y.shape}")

# if __name__ == "__main__":
#     create_dataset()



import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def load_patterns(patterns_folder="data/patterns"):
    """
    Load detected patterns from JSON files into a dictionary.
    """
    all_patterns = {}
    for file_name in os.listdir(patterns_folder):
        if file_name.endswith("_patterns.json"):
            stock_name = file_name.replace("_patterns.json", "")
            file_path = os.path.join(patterns_folder, file_name)
            with open(file_path, "r") as f:
                pattern_data = json.load(f)
            all_patterns[stock_name] = pattern_data
    return all_patterns

def create_features_and_labels(data, double_bottoms, double_tops, window_size=30):
    """
    Create input features and labels for ML training.
    """
    X = []
    y = []

    # Convert patterns list into set of date strings for fast lookup
    double_bottom_dates = set()
    double_top_dates = set()

    for triple in double_bottoms:
        double_bottom_dates.update([triple[0], triple[1], triple[2]])
    for triple in double_tops:
        double_top_dates.update([triple[0], triple[1], triple[2]])

    dates = data.index.strftime("%Y-%m-%d").tolist()

    for i in range(window_size, len(data)):
        window_data = data.iloc[i - window_size:i]
        close_prices = window_data['Close'].values

        feature = close_prices / close_prices[0] - 1  # Normalize: % changes relative to first
        X.append(feature)

        current_date = dates[i]

        if current_date in double_bottom_dates:
            y.append(1)  # Label 1: Double Bottom
        elif current_date in double_top_dates:
            y.append(2)  # Label 2: Double Top
        else:
            y.append(0)  # Label 0: No Pattern

    return np.array(X), np.array(y)

def create_dataset(processed_folder="data/processed", patterns_folder="data/patterns", output_folder="data/datasets"):
    """
    Build the full dataset (X, y) across all stocks.
    """
    os.makedirs(output_folder, exist_ok=True)

    all_patterns = load_patterns(patterns_folder)

    X_total = []
    y_total = []

    for file_name in os.listdir(processed_folder):
        if file_name.endswith(".csv"):
            stock_name = file_name.replace(".csv", "")
            file_path = os.path.join(processed_folder, file_name)

            data = pd.read_csv(file_path, index_col="Date", parse_dates=True)
            patterns = all_patterns.get(stock_name, {})

            double_bottoms = patterns.get('double_bottoms', [])
            double_tops = patterns.get('double_tops', [])

            if len(data) < 31:
                print(f"Skipping {stock_name} due to insufficient data")
                continue

            X, y = create_features_and_labels(data, double_bottoms, double_tops)

            X_total.append(X)
            y_total.append(y)

    # Merge all stocks
    X_total = np.vstack(X_total)
    y_total = np.concatenate(y_total)

    print(f"✅ Dataset created: {X_total.shape[0]} samples, each input shape {X_total.shape[1]}")

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_total, y_total, test_size=0.2, random_state=42, stratify=y_total)

    # Save datasets
    np.save(os.path.join(output_folder, "X_train.npy"), X_train)
    np.save(os.path.join(output_folder, "y_train.npy"), y_train)
    np.save(os.path.join(output_folder, "X_test.npy"), X_test)
    np.save(os.path.join(output_folder, "y_test.npy"), y_test)

    print(f"✅ Train/Test splits saved in {output_folder}")

if __name__ == "__main__":
    create_dataset()
