# Code to plot candlestick charts
import pandas as pd
import mplfinance as mpf
import os

def visualize_patterns(ticker, interval="1d", processed_path="data/processed", pattern_path="data/patterns"):
    file_name = f"{ticker.replace('.', '_')}_{interval}.csv"
    csv_path = os.path.join(processed_path, file_name)
    pattern_file = os.path.join(pattern_path, f"{ticker.replace('.', '_')}_patterns.json")

    if not os.path.exists(csv_path) or not os.path.exists(pattern_file):
        print(f"Missing data or pattern file for {ticker}")
        return

    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.sort_index(inplace=True)

    patterns = pd.read_json(pattern_file)

    # Convert pattern indices to markers
    bottom_indices = patterns["double_bottoms"]
    top_indices = patterns["double_tops"]

    bottom_marks = [int(i[0]) for i in bottom_indices] + [int(i[1]) for i in bottom_indices]
    top_marks = [int(i[0]) for i in top_indices] + [int(i[1]) for i in top_indices]

    # Create marker series
    mark_bottom = df.iloc[bottom_marks]
    mark_top = df.iloc[top_marks]

    apds = [
        mpf.make_addplot(mark_bottom["Low"], type='scatter', markersize=200, marker='v', color='g'),
        mpf.make_addplot(mark_top["High"], type='scatter', markersize=200, marker='^', color='r')
    ]

    mpf.plot(
        df,
        type="candle",
        style="charles",
        title=f"{ticker} with Detected Reversal Patterns",
        volume=True,
        addplot=apds
    )

# Sample usage
if __name__ == "__main__":
    visualize_patterns("RELIANCE.NS", interval="1d")

