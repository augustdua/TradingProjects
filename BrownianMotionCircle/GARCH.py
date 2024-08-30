import numpy as np
from arch import arch_model

# Parameters
n_turns = 100
initial_capital = 10000
price_initial = 100


# Simulate a GARCH(1,1) price series
def simulate_garch(n, omega=0.1, alpha=0.1, beta=0.8):
    vol = np.zeros(n)
    price = np.zeros(n)
    price[0] = price_initial
    shock = np.random.normal(0, 1, n)
    for t in range(1, n):
        vol[t] = np.sqrt(omega + alpha * shock[t - 1] ** 2 + beta * vol[t - 1] ** 2)
        price[t] = price[t - 1] + vol[t] * shock[t]
    return price


# Main game loop
def play_game():
    capital = initial_capital
    price_series = simulate_garch(n_turns)
    for turn in range(n_turns):
        # Display market status
        print(f"Turn {turn + 1}, Current Price: {price_series[turn]}, Your Capital: {capital}")
        # Get player decision
        decision = input("Enter 'buy', 'sell', or 'hold': ")
        # Process decision
        if decision == 'buy' or decision == 'sell':
            # Simplified trading logic
            capital += (price_series[turn] - price_series[turn - 1]) if decision == 'sell' else -(
                        price_series[turn] - price_series[turn - 1])
    return capital


# Start the game
final_capital = play_game()
print(f"Game Over! Your final capital is {final_capital}")
