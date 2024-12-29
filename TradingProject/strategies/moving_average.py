import pandas as pd
import numpy as np


def generate_signals(data, short_window, long_window):
    """
    Generate buy and sell signals based on moving average crossovers.
    Args:
        data (pd.DataFrame): Historical stock data.
        short_window (int): Period for the short EMA.
        long_window (int): Period for the long EMA.
    Returns:
        pd.DataFrame: Updated data with EMA and signal columns.
    """
    data['EMA_Short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_Long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['Signal'] = 0
    data.loc[data['EMA_Short'] > data['EMA_Long'], 'Signal'] = 1
    data.loc[data['EMA_Short'] < data['EMA_Long'], 'Signal'] = -1
    return data


def optimize_strategy(data, short_window_range, long_window_range, initial_capital=10000):
    """
    Optimize the moving average crossover strategy by tuning short and long windows.
    Args:
        data (pd.DataFrame): Historical stock data.
        short_window_range (range): Range of short window values to test.
        long_window_range (range): Range of long window values to test.
        initial_capital (float): Initial capital for backtesting.
    Returns:
        dict: Best parameters and corresponding performance metrics.
    """
    best_params = None
    best_sharpe = -np.inf

    for short_window in short_window_range:
        for long_window in long_window_range:
            if short_window >= long_window:  # Ensure short_window < long_window
                continue
            temp_data = generate_signals(data.copy(), short_window, long_window)
            temp_data['Position'] = temp_data['Signal'].shift().fillna(0)
            temp_data['Daily Returns'] = temp_data['Close'].pct_change()
            temp_data['Strategy Returns'] = temp_data['Position'] * temp_data['Daily Returns']
            temp_data['Portfolio Value'] = (1 + temp_data['Strategy Returns']).cumprod() * initial_capital

            # Calculate Sharpe ratio
            sharpe_ratio = temp_data['Strategy Returns'].mean() / temp_data['Strategy Returns'].std() * (252 ** 0.5)

            # Update best parameters
            if sharpe_ratio > best_sharpe:
                best_sharpe = sharpe_ratio
                best_params = {
                    "short_window": short_window,
                    "long_window": long_window,
                    "sharpe_ratio": sharpe_ratio,
                    # Adding dummy Kelly parameters for demonstration
                    "kelly_params": {"win_rate": 0.6, "avg_win": 0.02, "avg_loss": 0.01},
                }

    return best_params


def filter_params_for_function(params, function):
    """
    Filter a dictionary of parameters to only include those that are valid for a given function.
    Args:
        params (dict): Dictionary of parameters.
        function (callable): The function to check parameters against.
    Returns:
        dict: Filtered dictionary containing only parameters valid for the function.
    """
    import inspect

    valid_keys = inspect.signature(function).parameters.keys()
    return {key: value for key, value in params.items() if key in valid_keys}


def get_best_params(data,ticker):
    """
    Wrapper to get the best parameters for the moving average strategy.
    Args:
        data (pd.DataFrame): Historical stock data.
    Returns:
        dict: Best parameters for the strategy.
    """
    short_window_range = range(5, 30, 3)
    long_window_range = range(20, 200, 5)
    best_params = optimize_strategy(data, short_window_range, long_window_range)

    # Return only the parameters relevant for the strategy
    return {
        "short_window": best_params["short_window"],
        "long_window": best_params["long_window"],
        "kelly_params": best_params["kelly_params"],  # Include Kelly parameters
    }

import matplotlib.pyplot as plt

def visualize_results(data, title="Moving Average Strategy Results"):
    """
    Visualize the Moving Average Strategy backtest results.
    Args:
        data (pd.DataFrame): Backtest results containing 'Close', 'EMA_Short', and 'EMA_Long'.
        title (str): Title of the visualization.
    """
    plt.figure(figsize=(12, 6))
    
    # Plot Close price
    plt.plot(data['Close'], label="Close Price", linewidth=2, color='blue')
    
    # Plot EMA Short
    if 'EMA_Short' in data.columns:
        plt.plot(data['EMA_Short'], label="EMA Short", linewidth=1.5, linestyle="--", color='orange')
    
    # Plot EMA Long
    if 'EMA_Long' in data.columns:
        plt.plot(data['EMA_Long'], label="EMA Long", linewidth=1.5, linestyle=":", color='green')
    
    # Add labels and legend
    plt.title(title, fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.legend()
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.show()

