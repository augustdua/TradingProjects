from scipy.stats import poisson

def simulate_poisson_renewals(lambda_val, t, threshold=5):
    """
    Simulate a process where renewals occur when the cumulative sum of Poisson-distributed
    random variables crosses a specified threshold, here 5. The process is simulated for
    't' time steps, with each step generating a Poisson random variable with mean 'lambda_val'.

    Parameters:
    - lambda_val: Mean of the Poisson distribution.
    - t: Total number of time steps to simulate.
    - threshold: The sum threshold triggering a renewal.

    Returns:
    - The number of renewals observed in the simulation.
    """
    sum_poisson = 0
    renewals = 0

    for _ in range(t):
        # Generate a Poisson random variable
        poisson_rv = poisson.rvs(mu=lambda_val)
        sum_poisson += poisson_rv

        # Check if the cumulative sum crosses the threshold
        if sum_poisson >= threshold:
            renewals += 1
            sum_poisson -= threshold  # Reset the sum by subtracting the threshold

    return renewals

# Example simulation parameters
lambda_val = 1
t = 10  # Number of Poisson RVs to generate, representing discrete time steps
num_simulations = 100000000
update_interval = 10000  # How often to print progress updates

total_renewals = 0
for i in range(1, num_simulations + 1):
    total_renewals += simulate_poisson_renewals(lambda_val, t)
    if i % update_interval == 0:
        current_avg = total_renewals / i
        print(f"After {i} simulations, the current average number of renewals is: {current_avg}")

expected_renewals = total_renewals / num_simulations
print(f"Expected number of renewals by time {t}: {expected_renewals}")
