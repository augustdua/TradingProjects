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
    Calculate liquidity, volatility, ATR, and trend score for a single stock.
    Args:
        data (pd.DataFrame): Historical stock data.
        ticker (str): Stock ticker symbol.
    Returns:
        dict: Metrics including average volume, volatility, ATR, and trend score.
    """
    try:
        # Flatten MultiIndex columns if needed
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [f"{col[0]}_{ticker}" if col[1] else col[0] for col in data.columns]
            # print("Flattened columns:", data.columns)

        # Ensure sufficient data
        if len(data) < 50:
            raise ValueError("Insufficient data for moving averages (less than 50 rows)")

        # Debugging the data before calculating EMA_50
        # print(f"First few rows before EMA_50 calculation for {ticker}:")
        # print(data.head())

        # Calculate average volume and daily percentage volatility
        avg_volume = data[f'Volume_{ticker}']
        avg_volume = avg_volume.mean()
        daily_pct_change = data[f'Close_{ticker}'].pct_change()
        volatility = daily_pct_change.std() * 100

        # Calculate ATR (Average True Range)
        data[f'High-Low_{ticker}'] = data[f'High_{ticker}'] - data[f'Low_{ticker}']
        data[f'High-Close_{ticker}'] = np.abs(data[f'High_{ticker}'] - data[f'Close_{ticker}'].shift(1))
        data[f'Low-Close_{ticker}'] = np.abs(data[f'Low_{ticker}'] - data[f'Close_{ticker}'].shift(1))
        data[f'True Range_{ticker}'] = data[
            [f'High-Low_{ticker}', f'High-Close_{ticker}', f'Low-Close_{ticker}']
        ].max(axis=1)
        atr = data[f'True Range_{ticker}'].rolling(window=14).mean().iloc[-1] if len(data) >= 14 else 0

        # Calculate EMA_50
        sma_initial = data[f'Close_{ticker}'].iloc[:50].mean()  # Initial SMA for the first 50 rows
        data[f'EMA_50_{ticker}'] = data[f'Close_{ticker}'].ewm(span=50, adjust=False).mean()
        data.iloc[49, data.columns.get_loc(f'EMA_50_{ticker}')] = sma_initial

        # Debugging after calculating EMA_50
        # print(f"EMA_50 head before handling SMA for {ticker}:")
        # print(data[f'EMA_50_{ticker}'].head())
        # print(f"NaN count in EMA_50 before SMA initialization for {ticker}:", data[f'EMA_50_{ticker}'].isna().sum())

        # Drop rows with NaN in EMA_50
        data = data.dropna(subset=[f'EMA_50_{ticker}'])

        # Calculate trend score
        trend_score = (data[f'Close_{ticker}'] > data[f'EMA_50_{ticker}']).mean() * 100

        # Calculate average price
        avg_price = data[f'Close_{ticker}'].mean()

        return {
            "avg_volume": avg_volume,
            "volatility": volatility,
            "atr": atr,
            "trend_score": trend_score,
            "avg_price": avg_price
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


def filter_moving_average_stocks(stock_list, volume_threshold=1_000_000, volatility_range=(2, 5), trend_score_threshold=50):
    """
    Filter stocks suitable for a moving average strategy.
    Args:
        stock_list (list): List of stock tickers.
        volume_threshold (int): Minimum average volume.
        volatility_range (tuple): Acceptable range for daily volatility (%).
        trend_score_threshold (float): Minimum trend alignment score (%).
    Returns:
        pd.DataFrame: Filtered stocks and their metrics.
    """
    filtered_stocks = []
    for ticker in stock_list:
        print(f"Processing {ticker}...")
        try:
            data = fetch_stock_data(ticker)
            if data is None:
                continue

            metrics = calculate_metrics(data, ticker)
            if metrics is None:
                continue

            # Check if the stock meets criteria
            if (
                metrics["avg_volume"] >= volume_threshold and
                volatility_range[0] <= metrics["volatility"] <= volatility_range[1] and
                metrics["trend_score"] >= trend_score_threshold
            ):
                filtered_stocks.append({
                    "ticker": ticker,
                    "avg_volume": metrics["avg_volume"],
                    "volatility": metrics["volatility"],
                    "atr": metrics["atr"],
                    "trend_score": metrics["trend_score"],
                    "avg_price": metrics["avg_price"]
                })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return pd.DataFrame(filtered_stocks)


if __name__ == "__main__":
    # Fetch S&P 500 tickers
    stock_list = fetch_sp500_tickers()
    print(f"Fetched {len(stock_list)} tickers from S&P 500")

    # Filter stocks for moving average strategy
    filtered_stocks = filter_moving_average_stocks(
        stock_list,
        volume_threshold=5_000_000,
        volatility_range=(3, 4.5),
        trend_score_threshold=70
    )

    # Save filtered stocks to a CSV file
    if not filtered_stocks.empty:
        filtered_stocks.to_csv("moving_average_stocks.csv", index=False)
        print("Filtered stocks saved to 'moving_average_stocks.csv'")
    else:
        print("No stocks met the criteria.")
