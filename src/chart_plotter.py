import json
import pandas as pd
import os

def validate_json_structure(patterns):
    for pattern_list in ['double_bottoms', 'double_tops']:
        valid_patterns = []
        for pattern in patterns.get(pattern_list, []):
            if isinstance(pattern, list) and len(pattern) == 2:
                valid_patterns.append(pattern)
            else:
                print(f"Warning: Skipping invalid pattern in {pattern_list}: {pattern}")
        patterns[pattern_list] = valid_patterns
    return patterns

def visualize_chart_patterns(ticker, interval="1d"):
    # Replace '.' with '_' to match file naming
    file_ticker = ticker.replace('.', '_')

    pattern_file = os.path.join("data", "patterns", f"{file_ticker}_patterns.json")
    csv_file = os.path.join("data", "processed", f"{file_ticker}_{interval}.csv")

    with open(pattern_file, 'r') as file:
        patterns = json.load(file)

    patterns = validate_json_structure(patterns)
    print(f"Patterns after validation: {patterns}")

    df = pd.read_csv(csv_file, index_col=0, parse_dates=True)

    # Plotting code can follow here...

# Run the function
visualize_chart_patterns("RELIANCE.NS", interval="1d")
