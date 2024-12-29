from scipy.stats import poisson


def simulate_time_to_threshold(lambda_val, threshold=5):
    sum_poisson = 0
    count_rvs = 0  # Count of Poisson RVs generated

    # Continue generating Poisson RVs until the cumulative sum reaches/exceeds the threshold
    while sum_poisson < threshold:
        poisson_rv = poisson.rvs(mu=lambda_val)
        sum_poisson += poisson_rv
        count_rvs += 1

    return count_rvs


# Example simulation parameters
lambda_val = 1
num_simulations = 1000000    # Number of simulations to run

# Run simulations and accumulate total time to threshold
total_time_to_threshold = sum(simulate_time_to_threshold(lambda_val) for _ in range(num_simulations))

# Calculate the expected time (average number of RVs) to reach or exceed the threshold
expected_time_to_threshold = total_time_to_threshold / num_simulations

print(f"Expected time (in terms of Poisson RVs generated) to threshold: {expected_time_to_threshold}")
