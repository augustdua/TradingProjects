# Trading Strategy Backtesting Framework

This repository provides a modular and dynamic framework to backtest trading strategies. It supports various strategies, such as moving averages, breakout strategies, and mean reversion. The framework is designed to allow users to select and test strategies, optimize parameters, and evaluate their performance.

---

## Features
- **Dynamic Strategy Selection**: Choose from multiple trading strategies using a modular design.
- **Backtesting Engine**: Simulates portfolio performance using historical data.
- **Performance Metrics**: Calculate key performance indicators, such as profit, hit ratio, and maximum drawdown.
- **Data Fetching**: Integrates with Yahoo Finance to fetch historical stock data.
- **Signal Visualization**: Visualize strategy signals and results using charts.
- **Optimization**: Automatically optimize strategy parameters for maximum Sharpe Ratio.
- **Volume Confirmation**: Enhance breakout strategies with volume-based confirmation.

---

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Running the Framework](#1-running-the-framework)
  - [2. Adding a New Strategy](#2-adding-a-new-strategy)
- [Strategies](#strategies)
  - [Moving Average Strategy](#moving-average-strategy)
  - [Breakout Strategy](#breakout-strategy)
- [Backtesting Engine](#backtesting-engine)
- [Performance Evaluation](#performance-evaluation)
- [Future Enhancements](#future-enhancements)

---

## Requirements
- Python 3.8 or later
- Libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `yfinance`
  - `scipy`

Install the required libraries using:
```bash
pip install -r requirements.txt
