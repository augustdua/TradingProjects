import numpy as np
import matplotlib.pyplot as plt

def simulate_martingale_at_stopping_time(mu, sigma, num_simulations, max_stopping_time):
    # Array to store the final value of the martingale for each simulation
    final_martingale_values = np.empty(num_simulations)

    for i in range(num_simulations):
        # Generate a random stopping time for each simulation
        stopping_time = np.random.randint(1, max_stopping_time + 1)

        # Simulate the final martingale value at this stopping time
        final_martingale_values[i] = 0.96 * np.random.lognormal(mean=mu * stopping_time, sigma=sigma * np.sqrt(stopping_time))

    return final_martingale_values

sigma = 0.03
mu = -(sigma ** 2) / 2  # corrected the variable name typo here
num_simulations = 1000000
max_stopping_time = 1000

# Simulating the martingale process
final_martingale_values = simulate_martingale_at_stopping_time(mu, sigma, num_simulations, max_stopping_time)

# Calculating the average of the final martingale values
average_final_martingale_value = np.mean(final_martingale_values)
print(f"Average final martingale value: {average_final_martingale_value}")

# Plotting the histogram of the final martingale values
plt.figure(figsize=(10, 6))
plt.hist(final_martingale_values, bins=50, alpha=0.7)
plt.title('Histogram of Final Martingale Values')
plt.xlabel('Martingale Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
