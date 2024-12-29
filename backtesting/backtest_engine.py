# backtesting/backtest_engine.py
import pandas as pd

def backtest_strategy(data, signal_column="Signal", initial_balance=10000, kelly_params=None, use_kelly=False):
    """
    Perform backtesting on the given data.
    Args:
        data (pd.DataFrame): Stock data with columns including 'Close' and the specified 'Signal'.
        signal_column (str): Name of the signal column.
        initial_balance (float): Starting portfolio balance.
        kelly_params (dict): Parameters required for Kelly Criterion calculation.
        use_kelly (bool): Whether to apply the Kelly Criterion.
    Returns:
        pd.DataFrame: Backtest results with portfolio values and returns.
    """
    # Flatten MultiIndex for easier access (if necessary)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(filter(None, col)).strip('_') for col in data.columns]

    # Identify the required columns dynamically
    close_col = next((col for col in data.columns if "Close" in col), None)
    signal_col = signal_column

    if close_col is None or signal_col not in data.columns:
        raise ValueError(f"Required columns ('Close' and '{signal_col}') not found in the DataFrame!")

    # Initialize portfolio simulation columns
    data["Portfolio Value"] = initial_balance
    data["Portfolio Value"] = data["Portfolio Value"].astype(float)  # Ensure float dtype
    data["Position"] = data[signal_col].shift(1).fillna(0).astype(float)

    # Compute Kelly Criterion position multiplier if enabled
    kelly_multiplier = 1  # Default to no leverage
    if use_kelly and kelly_params:
        win_rate = kelly_params.get("win_rate", 0.5)
        avg_win = kelly_params.get("avg_win", 0.01)
        avg_loss = kelly_params.get("avg_loss", 0.01)
        kelly_multiplier = max(0, win_rate - ((1 - win_rate) / (avg_win / abs(avg_loss))))

    # Iterate through the rows to simulate portfolio value
    for i in range(1, len(data)):
        prev_portfolio_value = data.loc[data.index[i - 1], "Portfolio Value"]
        prev_position = data.loc[data.index[i - 1], "Position"]
        current_price = data.loc[data.index[i], close_col]
        prev_price = data.loc[data.index[i - 1], close_col]

        # Update portfolio value based on position
        if prev_position == 1:  # Holding the stock
            data.loc[data.index[i], "Portfolio Value"] = (
                prev_portfolio_value + (current_price - prev_price) * prev_position * kelly_multiplier
            )
        else:  # No position
            data.loc[data.index[i], "Portfolio Value"] = prev_portfolio_value

    # Calculate returns
    data = calculate_returns(data)

    return data


def calculate_returns(data):
    """
    Calculate daily returns based on the 'Portfolio Value'.
    Args:
        data (pd.DataFrame): Backtest data with 'Portfolio Value'.
    Returns:
        pd.DataFrame: Updated DataFrame with 'Returns'.
    """
    data["Returns"] = data["Portfolio Value"].pct_change().fillna(0).astype(float)
    return data
