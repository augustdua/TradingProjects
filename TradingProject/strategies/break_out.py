import pandas as pd
import numpy as np

def flatten_columns(data, ticker):
    """
    Flatten MultiIndex columns for easier access.
    Args:
        data (pd.DataFrame): DataFrame with MultiIndex columns.
        ticker (str): Stock ticker to append for unique column names.
    Returns:
        pd.DataFrame: DataFrame with flattened column headers.
    """
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [f"{col[0]}_{ticker}" if col[1] else col[0] for col in data.columns]
    return data

def generate_signals(data, breakout_window, confirmation_window, ticker):
    """
    Generate buy and sell signals based on breakout levels.
    Args:
        data (pd.DataFrame): Historical stock data with MultiIndex or single-level columns.
        breakout_window (int): Number of periods to calculate breakout levels.
        confirmation_window (int): Number of periods for confirmation.
        ticker (str): Stock ticker symbol.
    Returns:
        pd.DataFrame: Updated data with breakout levels and signals.
    """
    # Flatten MultiIndex columns if necessary
    if isinstance(data.columns, pd.MultiIndex):
        if not ticker:
            raise ValueError("Ticker is required when data has MultiIndex columns.")
        data.columns = [f"{col[0]}_{ticker}" if col[1] == ticker else col[0] for col in data.columns]

    # Use ticker to identify specific columns
    close_col = f"Close_{ticker}" if f"Close_{ticker}" in data.columns else "Close"
    high_col = f"High_{ticker}" if f"High_{ticker}" in data.columns else "High"
    low_col = f"Low_{ticker}" if f"Low_{ticker}" in data.columns else "Low"

    # Calculate breakout levels
    data["High_Breakout"] = data[high_col].rolling(window=breakout_window).max()
    data["Low_Breakout"] = data[low_col].rolling(window=breakout_window).min()

    # Generate signals
    data["Signal"] = 0
    data.loc[data[close_col] > data["High_Breakout"].shift(confirmation_window), "Signal"] = 1
    data.loc[data[close_col] < data["Low_Breakout"].shift(confirmation_window), "Signal"] = -1

    return data



def optimize_strategy(data, breakout_window_range, confirmation_window_range, ticker):
    """
    Optimize the breakout strategy by testing different breakout and confirmation windows.
    Args:
        data (pd.DataFrame): Historical stock data.
        breakout_window_range (range): Range of breakout window values to test.
        confirmation_window_range (range): Range of confirmation window values to test.
        ticker (str): Stock ticker to reference correct columns.
    Returns:
        dict: Best parameters and corresponding performance metrics.
    """
    best_params = None
    best_sharpe = -np.inf

    for breakout_window in breakout_window_range:
        for confirmation_window in confirmation_window_range:
            temp_data = generate_signals(data.copy(), breakout_window, confirmation_window, ticker)
            temp_data['Position'] = temp_data['Signal'].shift().fillna(0)
            temp_data['Daily Returns'] = temp_data[f'Close_{ticker}'].pct_change()
            temp_data['Strategy Returns'] = temp_data['Position'] * temp_data['Daily Returns']

            # Calculate Sharpe ratio
            if temp_data['Strategy Returns'].std() != 0:
                sharpe_ratio = temp_data['Strategy Returns'].mean() / temp_data['Strategy Returns'].std() * (252 ** 0.5)
            else:
                sharpe_ratio = -np.inf
            
            if sharpe_ratio > best_sharpe:
                best_sharpe = sharpe_ratio
                best_params = {
                    "breakout_window": breakout_window,
                    "confirmation_window": confirmation_window,
                    "sharpe_ratio": sharpe_ratio
                }

    return best_params

def get_best_params(data, ticker):
    """
    Wrapper to get the best parameters for the breakout strategy.
    Args:
        data (pd.DataFrame): Historical stock data.
        ticker (str): Stock ticker to reference correct columns.
    Returns:
        dict: Best parameters for the strategy.
    """
    breakout_window_range = range(2, 100, 1)
    confirmation_window_range =  range(0, 20, 1)
    best_params = optimize_strategy(data, breakout_window_range, confirmation_window_range, ticker)
    return {
        "breakout_window": best_params["breakout_window"],
        "confirmation_window": best_params["confirmation_window"]
    }

def filter_params_for_function(best_params, func):
    """
    Filter parameters for compatibility with a given function.
    Args:
        best_params (dict): Dictionary of best parameters.
        func (function): Target function to filter parameters for.
    Returns:
        dict: Filtered parameters.
    """
    from inspect import signature
    valid_params = signature(func).parameters
    return {k: v for k, v in best_params.items() if k in valid_params}

def visualize_results(data, ticker, title="Breakout Strategy Results"):
    """
    Visualize the breakout strategy results.
    Args:
        data (pd.DataFrame): Backtest results with signals and portfolio values.
        ticker (str): Stock ticker to reference correct columns.
        title (str): Title for the plot.
    """
    import matplotlib.pyplot as plt

    # Flatten MultiIndex columns for visualization
    data = flatten_columns(data, ticker)

    plt.figure(figsize=(12, 6))
    plt.plot(data[f'Close_{ticker}'], label='Close Price', alpha=0.5)
    plt.plot(data['High_Breakout'], label='High Breakout', linestyle='--')
    plt.plot(data['Low_Breakout'], label='Low Breakout', linestyle='--')
    plt.title(title)
    plt.legend()
    plt.show()
