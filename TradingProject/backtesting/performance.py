# backtesting/performance.py
import pandas as pd
import numpy as np

def calculate_metrics(data):
    """
    Calculate performance metrics from backtesting data.
    Args:
        data (pd.DataFrame): Backtest results containing 'Returns' and 'Portfolio Value'.
    Returns:
        dict: A dictionary containing all the performance metrics.
    """
    try:
        # Ensure required columns exist
        if 'Returns' not in data.columns or 'Portfolio Value' not in data.columns:
            raise ValueError("Missing required columns: 'Returns' or 'Portfolio Value'")

        # Basic metrics
        total_trades = len(data)
        positive_trades = len(data[data['Returns'] > 0])
        hit_ratio = (positive_trades / total_trades) * 100 if total_trades > 0 else 0

        avg_positive_trade = data[data['Returns'] > 0]['Returns'].mean() * 100
        avg_negative_trade = data[data['Returns'] <= 0]['Returns'].mean() * 100
        avg_profit_loss_ratio = (
            avg_positive_trade / abs(avg_negative_trade)
            if avg_negative_trade != 0
            else float('inf')
        )

        variation_of_returns = data['Returns'].std() * 100

        # Cumulative return (Profit)
        profit = (data['Portfolio Value'].iloc[-1] / data['Portfolio Value'].iloc[0] - 1) * 100

        # Maximum drawdown
        rolling_max = data['Portfolio Value'].cummax()
        drawdown = (data['Portfolio Value'] - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        return {
            "Profit": profit,
            "Hit Ratio": hit_ratio,
            "Maximum Drawdown": max_drawdown,
            "Average Positive Trade (%)": avg_positive_trade,
            "Average Negative Trade (%)": avg_negative_trade,
            "Avg. Profit/Avg Loss": avg_profit_loss_ratio,
            "Variation of Returns (%)": variation_of_returns,
        }
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None

def calculate_yearly_returns(data):
    """
    Calculate yearly returns and breakdown by BUY and SELL trades.
    Args:
        data (pd.DataFrame): Backtest results with 'Date', 'Returns', and 'Signal'.
    Returns:
        pd.DataFrame: A DataFrame containing yearly returns.
    """
    try:
        # Ensure the 'Date' column is in datetime format
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

        # Extract year from the date
        data['Year'] = data['Date'].dt.year

        # Calculate yearly returns
        yearly_returns = data.groupby('Year').agg(
            Total_Returns=('Returns', 'sum'),
            BUY_Returns=('Returns', lambda x: x[data['Signal'] == 1].sum()),
            SELL_Returns=('Returns', lambda x: x[data['Signal'] == 0].sum()),
        )

        # Convert to percentage
        yearly_returns = yearly_returns * 100

        return yearly_returns
    except Exception as e:
        print(f"Error calculating yearly returns: {e}")
        return None

def evaluate_strategy(data):
    """
    Evaluate the strategy performance using metrics.
    Args:
        data (pd.DataFrame): Backtest data containing 'Returns', 'Portfolio Value', and 'Signal'.
    Returns:
        dict: Metrics including profit, hit ratio, and maximum drawdown.
    """
    try:
        # Check if necessary columns exist
        required_columns = ['Returns', 'Portfolio Value', 'Signal']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Missing required columns: {required_columns}")

        # Calculate performance metrics
        metrics = calculate_metrics(data)
        return metrics

    except Exception as e:
        print(f"Error in evaluate_strategy: {e}")
        return {}

if __name__ == "__main__":
    # Example usage (this part is typically not needed if called from main.py)
    backtest_file = "backtest_results_PLTR.csv"
    backtest_data = pd.read_csv(backtest_file)

    # Debugging the loaded data
    print("Loaded Backtest Data:")
    print(backtest_data.head())

    # Calculate metrics
    print("\nCalculating Performance Metrics...")
    metrics = calculate_metrics(backtest_data)
    if metrics:
        print("\nPerformance Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value:.2f}%")

    # Calculate yearly returns
    print("\nCalculating Yearly Returns...")
    yearly_returns = calculate_yearly_returns(backtest_data)
    if yearly_returns is not None:
        print("\nYearly Returns:")
        print(yearly_returns)
