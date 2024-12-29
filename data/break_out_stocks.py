import yfinance as yf
import pandas as pd
import numpy as np


def fetch_stock_data(ticker, period="5y", interval="1d"):
    """
    Fetch historical stock data from Yahoo Finance.
    Args:
        ticker (str): Stock symbol (e.g., "AAPL").
        period (str): Lookback period (e.g., "6mo").
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


def calculate_metrics(data, ticker):
    """
    Calculate liquidity, volatility, ATR, and proximity to breakout levels for a single stock.
    Args:
        data (pd.DataFrame): Historical stock data.
        ticker (str): Stock ticker symbol.
    Returns:
        dict: Metrics including average volume, volatility, ATR, and proximity to breakout levels.
    """
    try:
        # Flatten MultiIndex columns if needed
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [f"{col[0]}_{ticker}" if col[1] else col[0] for col in data.columns]

        # Ensure sufficient data
        if len(data) < 50:
            raise ValueError("Insufficient data for analysis (less than 50 rows)")

        # Calculate average volume
        avg_volume = data[f"Volume_{ticker}"].mean()

        # Calculate daily percentage volatility
        daily_pct_change = data[f"Close_{ticker}"].pct_change()
        volatility = daily_pct_change.std() * 100

        # Calculate ATR (Average True Range)
        high_low = data[f"High_{ticker}"] - data[f"Low_{ticker}"]
        high_close = abs(data[f"High_{ticker}"] - data[f"Close_{ticker}"].shift())
        low_close = abs(data[f"Low_{ticker}"] - data[f"Close_{ticker}"].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=14).mean().iloc[-1] if len(data) >= 14 else 0

        # Calculate proximity to 20-day high
        recent_high = data[f"Close_{ticker}"].rolling(window=20).max().iloc[-1]
        current_price = data[f"Close_{ticker}"].iloc[-1]
        proximity_to_high = (recent_high - current_price) / recent_high

        return {
            "avg_volume": avg_volume,
            "volatility": volatility,
            "atr": atr,
            "recent_high": recent_high,
            "current_price": current_price,
            "proximity_to_high": proximity_to_high,
        }
    except Exception as e:
        print(f"Error calculating metrics for {ticker}: {e}")
        return None


def fetch_sp500_tickers():
    """
    Fetch the S&P 500 tickers dynamically from Wikipedia.
    Returns:
        list: List of S&P 500 stock tickers.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    try:
        sp500_table = pd.read_html(url)[0]
        return sp500_table["Symbol"].tolist()
    except Exception as e:
        print(f"Error fetching S&P 500 tickers: {e}")
        return []


def filter_breakout_stocks(
    stock_list,
    volume_threshold=1_000_000,
    volatility_threshold=2,
    atr_threshold=1.5,
    proximity_threshold=0.05
):
    """
    Filter stocks suitable for a breakout strategy.
    Args:
        stock_list (list): List of stock tickers.
        volume_threshold (int): Minimum average volume.
        volatility_threshold (float): Minimum daily volatility (%).
        atr_threshold (float): Minimum ATR value.
        proximity_threshold (float): Maximum distance from recent high/low as a percentage.
    Returns:
        pd.DataFrame: Filtered stocks and their metrics.
    """
    filtered_stocks = []

    for ticker in stock_list:
        print(f"Processing {ticker}...")

        try:
            # Fetch stock data
            data = fetch_stock_data(ticker)
            if data is None:
                print(f"Failed to fetch data for {ticker}.")
                continue

            # Calculate stock metrics
            metrics = calculate_metrics(data, ticker)
            if metrics is None:
                print(f"Failed to calculate metrics for {ticker}.")
                continue

            # Filter criteria for breakout strategy
            if (
                metrics["avg_volume"] >= volume_threshold
                and metrics["volatility"] >= volatility_threshold
                and metrics["atr"] >= atr_threshold
                and metrics["proximity_to_high"] <= proximity_threshold
            ):
                filtered_stocks.append({
                    "ticker": ticker,
                    "avg_volume": metrics["avg_volume"],
                    "volatility": metrics["volatility"],
                    "atr": metrics["atr"],
                    "recent_high": metrics["recent_high"],
                    "current_price": metrics["current_price"],
                    "proximity_to_high": metrics["proximity_to_high"]
                })

        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return pd.DataFrame(filtered_stocks)


if __name__ == "__main__":
    # Fetch S&P 500 tickers
    stock_list = fetch_sp500_tickers()
    print(f"Fetched {len(stock_list)} tickers from S&P 500")

    # Filter stocks for breakout strategy
    filtered_stocks = filter_breakout_stocks(
        stock_list,
        volume_threshold=2_000_000,
        volatility_threshold=2.5,
        atr_threshold=2,
        proximity_threshold=0.02
    )

    # Save filtered stocks to a CSV file
    if not filtered_stocks.empty:
        filtered_stocks.to_csv("breakout_stocks.csv", index=False)
        print("Filtered stocks saved to 'breakout_stocks.csv'")
    else:
        print("No stocks met the criteria.")
