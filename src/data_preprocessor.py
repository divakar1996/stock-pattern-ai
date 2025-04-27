# # import pandas as pd
# # import os

# # def preprocess_stock_data(ticker: str, interval: str = "1d", raw_path: str = "data/raw", save_path: str = "data/processed"):
# #     """
# #     Load raw CSV, clean nulls, filter columns, and save to processed folder.
# #     """
# #     file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
# #     file_path = os.path.join(raw_path, file_name)

# #     if not os.path.exists(file_path):
# #         print(f"File not found: {file_path}")
# #         return None

# #     print(f"Preprocessing {file_name}...")
# #     df = pd.read_csv(file_path, parse_dates=True, index_col=0)

# #     # Drop rows with null values
# #     df.dropna(inplace=True)

# #     # Optional: filter only useful columns
# #     df = df[["Open", "High", "Low", "Close", "Volume"]]

# #     os.makedirs(save_path, exist_ok=True)
# #     output_path = os.path.join(save_path, file_name)
# #     df.to_csv(output_path)

# #     print(f"Processed data saved to: {output_path}")
# #     return df

# # # Sample run
# # if __name__ == "__main__":
# #     preprocess_stock_data("RELIANCE.NS", interval="1d")

# import pandas as pd

# def preprocess_stock_data(file_path, output_file_path, interval="1d"):
#     """
#     Preprocess stock data from a CSV file and save the processed data to a new file.
    
#     Parameters:
#     - file_path: str, path to the CSV file
#     - output_file_path: str, path to save the preprocessed data
#     - interval: str, interval for stock data (default is "1d")
#     """
#     print(f"Preprocessing {file_path}...")

#     # Read the CSV file and skip the first row if it contains metadata like 'Ticker'
#     try:
#         df = pd.read_csv(file_path, header=0, parse_dates=True, index_col=0, skiprows=1)
#     except Exception as e:
#         print(f"Error reading the file: {e}")
#         return

#     # Check for rows where the first column might contain non-date values like 'Ticker'
#     # If so, remove those rows
#     df = df[~df.iloc[:, 0].str.contains('Ticker', na=False)]

#     # If the 'Date' column is not automatically detected, you can manually convert it
#     if df.index.dtype != 'datetime64[ns]':
#         try:
#             df.index = pd.to_datetime(df.index)
#         except Exception as e:
#             print(f"Error converting dates: {e}")
#             return

#     # Optionally, process the data further if needed (e.g., resampling, feature engineering)

#     # Save the processed data to a new CSV file
#     try:
#         df.to_csv(output_file_path)
#         print(f"Processed data saved to {output_file_path}")
#     except Exception as e:
#         print(f"Error saving the file: {e}")

# # Example usage:
# # preprocess_stock_data("RELIANCE.NS", "processed_RELIANCE_NS.csv", interval="1d")



# src/data_preprocessor.py

# src/data_preprocessor.py
# src/data_preprocessor.py

# import pandas as pd
# import os
# import logging

# def setup_logging():
#     """
#     Setup logging configuration.
#     """
#     logging.basicConfig(
#         format="%(asctime)s - %(levelname)s - %(message)s", 
#         level=logging.INFO
#     )

# def preprocess_single_stock(file_path: str, save_path: str = "data/processed"):
#     """
#     Preprocess a single stock data: Remove nulls, standardize columns.
#     """
#     try:
#         # Check if file exists
#         if not os.path.exists(file_path):
#             logging.warning(f"File not found: {file_path}")
#             return None
        
#         logging.info(f"Preprocessing: {file_path}")
        
#         # Load CSV and inspect the first few rows to find the date column
#         df = pd.read_csv(file_path)
        
#         # Display the first few rows to check column names
#         logging.info(f"Columns in the file: {df.columns}")
        
#         # Adjust column name to the correct one
#         date_column = 'Date'  # Update this to the actual date column name if different (e.g., 'timestamp')
        
#         # If the column is named something else, adjust the line below:
#         if date_column not in df.columns:
#             logging.error(f"Date column '{date_column}' not found in the data file.")
#             return None
        
#         # Convert the date column to datetime (adjusting to the correct column name if necessary)
#         df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

#         # Drop rows with invalid date entries
#         df.dropna(subset=[date_column], inplace=True)
        
#         # Set the date column as index
#         df.set_index(date_column, inplace=True)
        
#         # Standardize columns (if needed)
#         df = df[["Open", "High", "Low", "Close", "Volume"]]  # Adjust if there are more columns
        
#         # Ensure correct data types
#         df = df.apply(pd.to_numeric, errors='coerce')

#         # Save the processed data
#         os.makedirs(save_path, exist_ok=True)
#         processed_file_name = os.path.basename(file_path)
#         processed_file_path = os.path.join(save_path, processed_file_name)
#         df.to_csv(processed_file_path)
        
#         logging.info(f"Processed data saved to {processed_file_path}")
#         return df

#     except Exception as e:
#         logging.error(f"Error processing {file_path}: {e}")
#         return None

# def preprocess_multiple_stocks(file_paths: list, save_path: str = "data/processed"):
#     """
#     Preprocess multiple stock data files.
#     """
#     for file_path in file_paths:
#         preprocess_single_stock(file_path, save_path)

# if __name__ == "__main__":
#     # Example run for one stock
#     raw_file = "data/raw/RELIANCE_NS_1d.csv"
#     preprocess_single_stock(raw_file, save_path="data/processed")
    
#     # Example run for multiple stocks
#     raw_files = [
#         "data/raw/RELIANCE_NS_1d.csv", 
#         "data/raw/TCS_NS_1d.csv", 
#         "data/raw/INFY_NS_1d.csv"
#     ]
#     preprocess_multiple_stocks(raw_files, save_path="data/processed")


# import pandas as pd

# def check_csv_columns(file_path):
#     """
#     Check the columns of the CSV to find the correct date column.
#     """
#     try:
#         df = pd.read_csv(file_path)
#         print(f"Columns in {file_path}: {df.columns}")
#         print(f"First few rows:\n{df.head()}")
#     except Exception as e:
#         print(f"Error reading file {file_path}: {e}")

# # Example usage: Check columns for a specific CSV file
# check_csv_columns("data/raw/RELIANCE_NS_1d.csv")



# src/data_preprocessor.py

# import pandas as pd
# import os

# def preprocess_stock_data(file_path, output_file_path):
#     """
#     Preprocess stock data from a CSV file, handle header misalignment,
#     and save the processed data to a new file.

#     :param file_path: str, path to the raw CSV file
#     :param output_file_path: str, path where the processed file should be saved
#     """
#     try:
#         # Read the file, skip the first row (which contains "Ticker"), and set the second row as header
#         df = pd.read_csv(file_path, header=2, parse_dates=['Date'], index_col='Date')
        
#         # Debugging: print the column names and first few rows
#         print(f"Columns in {file_path}: {df.columns}")
#         print(f"First few rows in {file_path}:")
#         print(df.head())

#         # Ensure the columns exist in the dataset
#         required_columns = ["Price", "Close", "High", "Low", "Open", "Volume"]
        
#         # Check if the required columns are in the dataframe
#         if not all(col in df.columns for col in required_columns):
#             print(f"Warning: Missing required columns in {file_path}. Skipping this file.")
#             return
        
#         # Now that the header is aligned and the Date column is parsed, proceed with data cleaning
#         df = df[["Price", "Close", "High", "Low", "Open", "Volume"]]  # Keep only relevant columns
#         df.dropna(inplace=True)  # Drop rows with missing values
        
#         # Save the processed data to a new CSV file
#         df.to_csv(output_file_path)
#         print(f"Processed data saved to {output_file_path}")
    
#     except Exception as e:
#         print(f"Error processing file {file_path}: {e}")

# def process_multiple_files(raw_path="data/raw", processed_path="data/processed"):
#     """
#     Process multiple stock data files from the raw data folder.

#     :param raw_path: str, folder path containing the raw CSV files
#     :param processed_path: str, folder path to save processed files
#     """
#     os.makedirs(processed_path, exist_ok=True)
    
#     # Loop over all CSV files in the raw data folder
#     for file_name in os.listdir(raw_path):
#         if file_name.endswith(".csv"):
#             file_path = os.path.join(raw_path, file_name)
#             output_file_path = os.path.join(processed_path, file_name)

#             print(f"Processing file: {file_name}")
#             preprocess_stock_data(file_path, output_file_path)

# # Example usage: Process all files in the "data/raw" folder
# if __name__ == "__main__":
#     process_multiple_files(raw_path="data/raw", processed_path="data/processed")



# import pandas as pd
# import os

# def preprocess_stock_data(file_path, output_file_path):
#     """
#     Preprocess stock data from a CSV file, handle header misalignment,
#     and save the processed data to a new file.

#     :param file_path: str, path to the raw CSV file
#     :param output_file_path: str, path where the processed file should be saved
#     """
#     try:
#         # Read the file, skip the first row (which contains "Ticker"), and set the second row as header
#         df = pd.read_csv(file_path, header=2, parse_dates=['Date'], index_col='Date')
        
#         # Debugging: print the column names and first few rows
#         print(f"Columns in {file_path}: {df.columns}")
#         print(f"First few rows in {file_path}:")
#         print(df.head())

#         # Ensure the columns exist in the dataset
#         required_columns = ["Price", "Close", "High", "Low", "Open", "Volume"]
        
#         # Check if the required columns are in the dataframe
#         if not all(col in df.columns for col in required_columns):
#             print(f"Warning: Missing required columns in {file_path}. Skipping this file.")
#             return
        
#         # Now that the header is aligned and the Date column is parsed, proceed with data cleaning
#         df = df[["Price", "Close", "High", "Low", "Open", "Volume"]]  # Keep only relevant columns
#         df.dropna(inplace=True)  # Drop rows with missing values
        
#         # Save the processed data to a new CSV file
#         df.to_csv(output_file_path)
#         print(f"Processed data saved to {output_file_path}")
    
#     except Exception as e:
#         print(f"Error processing file {file_path}: {e}")

# def process_multiple_files(raw_path="data/raw", processed_path="data/processed"):
#     """
#     Process multiple stock data files from the raw data folder.

#     :param raw_path: str, folder path containing the raw CSV files
#     :param processed_path: str, folder path to save processed files
#     """
#     os.makedirs(processed_path, exist_ok=True)
    
#     # Loop over all CSV files in the raw data folder
#     for file_name in os.listdir(raw_path):
#         if file_name.endswith(".csv"):
#             file_path = os.path.join(raw_path, file_name)
#             output_file_path = os.path.join(processed_path, file_name)

#             print(f"Processing file: {file_name}")
#             preprocess_stock_data(file_path, output_file_path)

# # Example usage: Process all files in the "data/raw" folder
# if __name__ == "__main__":
#     process_multiple_files(raw_path="data/raw", processed_path="data/processed")




import pandas as pd
import os

def preprocess_stock_data(file_path, output_file_path):
    try:
        # Step 1: Read raw file
        df_raw = pd.read_csv(file_path, header=None)

        # Step 2: Clean first few rows
        # Drop first two rows (Ticker, Date)
        df_raw = df_raw.iloc[2:].reset_index(drop=True)

        # Step 3: Set correct columns
        df_raw.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

        # Step 4: Parse Date column
        df_raw['Date'] = pd.to_datetime(df_raw['Date'], format='%Y-%m-%d', errors='coerce')

        # Step 5: Drop rows where date parsing failed
        df_raw.dropna(subset=['Date'], inplace=True)

        # Step 6: Set Date as index
        df_raw.set_index('Date', inplace=True)

        # Step 7: Convert numeric fields
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        df_raw[numeric_cols] = df_raw[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Step 8: Drop any rows with missing values
        df_raw.dropna(inplace=True)

        # Step 9: Save processed file
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        df_raw.to_csv(output_file_path)
        print(f"✅ Processed file saved: {output_file_path}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def process_multiple_files(raw_path="data/raw", processed_path="data/processed"):
    os.makedirs(processed_path, exist_ok=True)

    for file_name in os.listdir(raw_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(raw_path, file_name)
            output_file_path = os.path.join(processed_path, file_name)
            print(f"Processing: {file_name}")
            preprocess_stock_data(file_path, output_file_path)

if __name__ == "__main__":
    process_multiple_files()
