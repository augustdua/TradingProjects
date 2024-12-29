import numpy as np


def simulate_game(S, p, R, threshold, simulations=10000):
    total_rewards = 0

    for _ in range(simulations):
        candies = 0
        for _ in range(S):
            # Simulate the number of spins to get a candy based on the geometric distribution
            candies += np.random.geometric(p)   # Subtracting 1 because we start counting from 0

        # Calculate rewards for this simulation
        total_rewards += (candies // threshold) * R

    # Calculate the average reward
    average_reward = total_rewards / simulations
    return average_reward


# Example usage
S = 12  # Number of spins
p = 0.1  # Probability of winning a candy in a single spin
R = 1  # Reward for every 5 candies
threshold = 3
average_reward = simulate_game(S, p, R, threshold)
print(f"Average reward: {average_reward}")
