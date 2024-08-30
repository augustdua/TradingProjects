import numpy as np
import matplotlib.pyplot as plt

# Parameters for the random walk
n_steps = 1000000
steps = np.where(np.random.rand(n_steps) > 0.5, 1, -1)
walk = np.cumsum(steps)

# Time spent positive
time_positive = np.sum(walk > 0) / n_steps

# Last zero crossing
last_zero = np.max(np.where(walk == 0)[0]) / n_steps if np.any(walk == 0) else 0

# Time at which the maximum is achieved
time_of_max = np.argmax(walk) / n_steps

# Plot the random walk
plt.figure(figsize=(14, 6))
plt.plot(walk, label='Random Walk')
plt.title('Symmetric Random Walk')
plt.xlabel('Steps')
plt.ylabel('Position')

# Mark the last zero crossing
if last_zero > 0:
    plt.axvline(x=last_zero * n_steps, color='red', label=f'Last Zero Crossing at {last_zero:.2f}')

# Mark the time at which the maximum is achieved
plt.axvline(x=time_of_max * n_steps, color='green', label=f'Max at {time_of_max:.2f}')

# Highlight the time spent positive
plt.fill_between(range(n_steps), walk, where=(walk > 0), color='yellow', alpha=0.5, label=f'Time Positive: {time_positive:.2f}')

plt.legend()
plt.show()
