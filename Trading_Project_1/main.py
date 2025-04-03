import os
import importlib
import pandas as pd
from data.moving_average_stocks import fetch_stock_data
from backtesting.backtest_engine import backtest_strategy
from backtesting.performance import evaluate_strategy


def load_strategy(strategy_name, strategies_folder="strategies"):
    """
    Load the specified strategy module dynamically.
    Args:
        strategy_name (str): Name of the strategy to load.
        strategies_folder (str): Path to the strategies folder.
    Returns:
        module: The strategy module if found, otherwise None.
    """
    module_path = f"{strategies_folder}.{strategy_name}"
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError:
        print(f"Strategy '{strategy_name}' not found in {strategies_folder} folder.")
        return None


if __name__ == "__main__":
    # List available strategies
    strategies_folder = "strategies"
    available_strategies = [
        file[:-3]
        for file in os.listdir(strategies_folder)
        if file.endswith(".py") and not file.startswith("__")
    ]
    print("Available Strategies:")
    for idx, strategy in enumerate(available_strategies, 1):
        print(f"{idx}. {strategy}")

    # Prompt user to choose a strategy
    try:
        choice = int(input("\nSelect a strategy by number: ")) - 1
        if choice < 0 or choice >= len(available_strategies):
            raise ValueError("Invalid choice.")
    except ValueError as e:
        print(f"Invalid input. {e}")
        exit()

    chosen_strategy = available_strategies[choice]
    print(f"\nYou selected: {chosen_strategy}")

    # Load the chosen strategy module
    strategy_module = load_strategy(chosen_strategy, strategies_folder=strategies_folder)
    if not strategy_module:
        exit()

    # Specify stock ticker
    stock_ticker = "KO"
    print(f"\nFetching data for {stock_ticker}...")

    # Fetch stock data
    stock_data = fetch_stock_data(stock_ticker)
    if stock_data is not None:
        print(f"Loaded data for {stock_ticker}.")

        try:
            # Get best parameters for the strategy
            print("Fetching best parameters for the strategy...")
            get_best_params = getattr(strategy_module, "get_best_params", None)
            if not get_best_params:
                print(f"No get_best_params function found in strategy {chosen_strategy}.")
                exit()

            best_params = get_best_params(stock_data,stock_ticker)
            print("Best Parameters:")
            print(best_params)

            # Prompt to use Kelly Criterion
            # use_kelly = input("Do you want to apply the Kelly Criterion? (yes/no): ").strip().lower() == "yes"
            use_kelly = False
            # Generate signals
            print("Generating signals...")
            generate_signals = getattr(strategy_module, "generate_signals", None)
            if not generate_signals:
                print(f"No generate_signals function found in strategy {chosen_strategy}.")
                exit()

            from strategies.moving_average import filter_params_for_function

            signal_params = filter_params_for_function(best_params, generate_signals)
            # Write code for if-else for different strategies
            if chosen_strategy == "moving_average":
                print("Using Moving Average strategy...")
                optimized_data = generate_signals(stock_data.copy(), **signal_params)
            elif chosen_strategy == "break_out":
                print("Using Break Out strategy...")
                optimized_data = generate_signals(stock_data.copy(), **signal_params, ticker = stock_ticker)
            else:
                print("Using Mean Reverting strategy...")
                optimized_data = generate_signals(stock_data.copy(), **signal_params, ticker = stock_ticker)
            # optimized_data = generate_signals(stock_data.copy(), **signal_params, ticker=stock_ticker)
            # optimized_data = generate_signals(stock_data.copy(), **signal_params)

            # Perform backtesting
            print("Performing backtest...")
            backtest_results = backtest_strategy(
                optimized_data, 
                kelly_params=best_params.get("kelly_params", None), 
                use_kelly=use_kelly
            )

            # Save backtest results
            results_file = f"backtest_results_{chosen_strategy}_{stock_ticker}.csv"
            backtest_results.to_csv(results_file, index=False)
            print(f"Backtest results saved to {results_file}")

            # Evaluate performance
            print("Evaluating performance...")
            performance_metrics = evaluate_strategy(backtest_results)
            print("Performance Metrics:")
            for metric, value in performance_metrics.items():
                print(f"{metric}: {value:.2f}%")
            
            # # Visualize backtest results
            # visualize_results = getattr(strategy_module, "visualize_results", None)
            # if callable(visualize_results):
            #     print("Visualizing backtest results...")
            #     visualize_results(backtest_results, title=f"{chosen_strategy} - {stock_ticker}")
            # else:
            #     print(f"No visualization function found for strategy '{chosen_strategy}'.")

        except Exception as e:
            print(f"Error executing strategy {chosen_strategy}: {e}")
    else:
        print(f"Failed to fetch data for {stock_ticker}.")
