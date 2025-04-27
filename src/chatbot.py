import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the model (ensure it's in the models directory)
model = load_model("models/pattern_model.h5")

# Flask application
app = Flask(__name__)

# Stock pattern classes
PATTERN_CLASSES = ["No Pattern", "Double Bottom", "Double Top"]

# Function to load data and preprocess (you may adjust this based on your dataset)
def preprocess_data(stock_symbol, start_date, end_date):
    """
    Preprocess stock data based on user input.
    This should ideally load the stock data for the given date range.
    """
    # Example: Using random data here - replace with actual data fetching logic.
    # In a real scenario, you'd load the stock data for the given symbol and date range from a data source like an API or database.
    dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
    data = np.random.random(size=(len(dates), 6))  # Random data simulating 'Price', 'Close', etc.

    df = pd.DataFrame(data, columns=["Price", "Close", "High", "Low", "Open", "Volume"], index=dates)

    # Normalize data as needed (example with min-max scaling)
    df_normalized = (df - df.min()) / (df.max() - df.min())  # Normalize features between 0 and 1

    return df_normalized

# Function to predict the stock pattern
def predict_pattern(data):
    """
    Predict stock pattern using the trained model.
    """
    # Ensure data is in the correct shape (samples, timesteps, features)
    data = data.reshape((data.shape[0], data.shape[1], 1))
    
    # Predict the pattern
    prediction = model.predict(data)
    predicted_class = np.argmax(prediction, axis=1)

    # Get the confidence of the prediction
    confidence = np.max(prediction, axis=1)[0]
    
    # Convert confidence to a native Python float
    confidence = float(confidence)

    return PATTERN_CLASSES[predicted_class[0]], confidence


# Define the route for the chatbot API
@app.route('/predict_pattern', methods=['GET'])
def predict_stock_pattern():
    """
    API endpoint to predict stock pattern based on user input.
    """
    try:
        # Get parameters from the request
        stock_symbol = request.args.get('stock_symbol')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not stock_symbol or not start_date or not end_date:
            return jsonify({"error": "Missing parameters. Please provide stock_symbol, start_date, and end_date."}), 400

        # Preprocess the stock data based on user input
        df_normalized = preprocess_data(stock_symbol, start_date, end_date)

        # Prepare data for prediction
        data = df_normalized.values  # Get the normalized feature values
        predicted_pattern, confidence = predict_pattern(data)  # Predict the pattern

        return jsonify({"stock_symbol": stock_symbol, "predicted_pattern": predicted_pattern, "confidence": confidence}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
