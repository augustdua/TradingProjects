import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, period="5y", interval="1d"):
    """
    Fetch historical stock data from Yahoo Finance.
    
    Args:
        ticker (str): Stock symbol (e.g., "AAPL").
        period (str): Lookback period (e.g., "5y").
        interval (str): Data interval (e.g., "1d").
        
    Returns:
        pd.DataFrame: Historical stock data.
    """
    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False)
        if data.empty:
            raise ValueError(f"No data found for {ticker}")
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def generate_signals(data, lookback_window, threshold, ticker):
    """
    Generate buy and sell signals for a mean reversion strategy.
    
    The idea is that the price tends to revert to its mean. The mean is estimated 
    by a Simple Moving Average (SMA) over a specified lookback window. If the current 
    price deviates from the SMA by more than a specified threshold:
      - A buy signal (Signal = 1) is generated when the price is significantly below the SMA.
      - A sell signal (Signal = -1) is generated when the price is significantly above the SMA.
    
    Args:
        data (pd.DataFrame): Historical stock data.
        lookback_window (int): Number of periods to calculate the SMA.
        threshold (float): Deviation threshold (in decimal, e.g., 0.05 for 5%).
        ticker (str): Stock ticker symbol.
        
    Returns:
        pd.DataFrame: Updated data with 'SMA', 'Deviation', and 'Signal' columns.
    """
    # Determine the close price column: if a ticker-specific column exists, use it.
    close_col = f"Close_{ticker}" if f"Close_{ticker}" in data.columns else "Close"
    
    # Extract the close price as a Series (handle MultiIndex issues if necessary)
    close_series = data[close_col]
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]
    
    # Calculate the Simple Moving Average (SMA) over the specified lookback window.
    data['SMA'] = close_series.rolling(window=lookback_window).mean()
    
    # Calculate the percentage deviation from the SMA: (Close - SMA) / SMA.
    data['Deviation'] = (close_series - data['SMA']) / data['SMA']
    
    # Initialize the Signal column to 0 (neutral).
    data['Signal'] = 0
    
    # Generate a buy signal when the deviation is less than -threshold.
    data.loc[data['Deviation'] < -threshold, 'Signal'] = 1
    
    # Generate a sell signal when the deviation is greater than threshold.
    data.loc[data['Deviation'] > threshold, 'Signal'] = -1
    
    return data

def optimize_strategy(data, lookback_range, threshold_range, initial_capital=10000, ticker=""):
    """
    Optimize the mean reversion strategy by testing different lookback windows and thresholds.
    
    For each combination of parameters, the strategy is backtested using the generated signals.
    The performance is measured via the annualized Sharpe ratio, and the best parameters are chosen.
    
    Args:
        data (pd.DataFrame): Historical stock data.
        lookback_range (range): Range of lookback window values to test.
        threshold_range (iterable): Iterable of threshold values (e.g., np.arange(0.01, 0.1, 0.01)).
        initial_capital (float): Starting capital for backtesting.
        ticker (str): Stock ticker for column reference.
        
    Returns:
        dict: Best parameters and performance metrics.
    """
    best_params = None
    best_sharpe = -np.inf
    
    for lookback_window in lookback_range:
        for threshold in threshold_range:
            temp_data = generate_signals(data.copy(), lookback_window, threshold, ticker)
            # Simulate entering positions on the next day.
            temp_data['Position'] = temp_data['Signal'].shift().fillna(0)
            close_col = f"Close_{ticker}" if f"Close_{ticker}" in temp_data.columns else "Close"
            temp_data['Daily Returns'] = temp_data[close_col].pct_change()
            temp_data['Strategy Returns'] = temp_data['Position'] * temp_data['Daily Returns']
            temp_data['Portfolio Value'] = (1 + temp_data['Strategy Returns']).cumprod() * initial_capital
            
            std_returns = temp_data['Strategy Returns'].std()
            if std_returns != 0:
                sharpe_ratio = temp_data['Strategy Returns'].mean() / std_returns * (252 ** 0.5)
            else:
                sharpe_ratio = -np.inf
            
            if sharpe_ratio > best_sharpe:
                best_sharpe = sharpe_ratio
                best_params = {
                    "lookback_window": lookback_window,
                    "threshold": threshold,
                    "sharpe_ratio": sharpe_ratio,
                    # Dummy Kelly parameters for demonstration (optional)
                    "kelly_params": {"win_rate": 0.55, "avg_win": 0.015, "avg_loss": 0.01},
                }
    return best_params

def filter_params_for_function(params, function):
    """
    Filter a dictionary of parameters to include only those that are valid for a given function.
    
    This ensures that when passing parameters via **kwargs, only the expected ones are included.
    
    Args:
        params (dict): Dictionary of parameters.
        function (callable): The target function.
        
    Returns:
        dict: Filtered dictionary of valid parameters.
    """
    import inspect
    valid_keys = inspect.signature(function).parameters.keys()
    return {key: value for key, value in params.items() if key in valid_keys}

def get_best_params(data, ticker):
    """
    Wrapper function to obtain the best parameters for the mean reversion strategy.
    
    Defines parameter ranges, calls the optimization routine, and returns the best settings.
    
    Args:
        data (pd.DataFrame): Historical stock data.
        ticker (str): Stock ticker for column references.
        
    Returns:
        dict: Best parameters for the strategy.
    """
    lookback_range = range(5, 50, 5)  # For example: 5, 10, 15, ... 45 days.
    threshold_range = np.arange(0.01, 0.1, 0.01)  # Thresholds from 1% to 9%.
    best_params = optimize_strategy(data, lookback_range, threshold_range, ticker=ticker)
    return {
        "lookback_window": best_params["lookback_window"],
        "threshold": best_params["threshold"],
        "kelly_params": best_params["kelly_params"],
    }

def visualize_results(data, ticker, title="Mean Reversion Strategy Results"):
    """
    Visualize the backtest results of the mean reversion strategy.
    
    The plot shows the stock’s close price, the SMA, and marks buy (Signal = 1) and sell (Signal = -1) signals.
    
    Args:
        data (pd.DataFrame): Backtest results containing 'Close', 'SMA', and 'Signal'.
        ticker (str): Stock ticker for column references.
        title (str): Title of the visualization.
    """
    close_col = f"Close_{ticker}" if f"Close_{ticker}" in data.columns else "Close"
    
    plt.figure(figsize=(12, 6))
    plt.plot(data[close_col], label="Close Price", linewidth=2, color="blue")
    if 'SMA' in data.columns:
        plt.plot(data['SMA'], label="SMA", linewidth=1.5, linestyle="--", color="orange")
    
    # Mark buy signals (Signal = 1) and sell signals (Signal = -1)
    buys = data[data['Signal'] == 1]
    sells = data[data['Signal'] == -1]
    plt.scatter(buys.index, buys[close_col], marker="^", color="green", label="Buy Signal")
    plt.scatter(sells.index, sells[close_col], marker="v", color="red", label="Sell Signal")
    
    plt.title(title, fontsize=16)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.legend()
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Specify the stock ticker
    stock_ticker = "BA"
    print(f"Fetching data for {stock_ticker}...")
    
    # Fetch historical data using yfinance
    stock_data = fetch_stock_data(stock_ticker)
    if stock_data is None:
        print(f"Failed to fetch data for {stock_ticker}. Exiting.")
        exit()
    
    print(f"Loaded data for {stock_ticker}.")
    
    # Get best parameters for the mean reversion strategy
    print("Optimizing strategy parameters...")
    best_params = get_best_params(stock_data, stock_ticker)
    print("Best Parameters:")
    print(best_params)
    
    # Generate signals using the best parameters
    print("Generating signals...")
    optimized_data = generate_signals(stock_data.copy(), best_params["lookback_window"], best_params["threshold"], stock_ticker)
    
    # (Optional) You can integrate a backtesting engine here similar to your moving average strategy.
    # For demonstration, we will simply visualize the results.
    print("Visualizing results...")
    visualize_results(optimized_data, stock_ticker, title="Mean Reversion Strategy Backtest")
