import numpy as np

def simulate_candy_distribution(number_of_spins, lambda_candies, candies_for_renewal):
    renewals = 0
    candies_so_far = 0

    for _ in range(number_of_spins):
        candies_this_spin = np.random.poisson(lambda_candies)
        candies_so_far += candies_this_spin

        if candies_so_far >= candies_for_renewal:
            renewals += 1
            candies_so_far -= candies_for_renewal  # Reset candies after each renewal

    return renewals

def theoretical_average_renewals(number_of_spins, lambda_candies, candies_for_renewal):
    # Expected number of candies per spin (Poisson mean)
    E = lambda_candies
    # Theoretical average number of renewals
    return (number_of_spins * E) / candies_for_renewal

def run_multiple_simulations(num_simulations, number_of_spins, lambda_candies, candies_for_renewal):
    total_renewals = 0

    for _ in range(num_simulations):
        total_renewals += simulate_candy_distribution(number_of_spins, lambda_candies, candies_for_renewal)

    average_renewals_per_simulation = total_renewals / num_simulations
    average_time_between_renewals = number_of_spins / average_renewals_per_simulation if average_renewals_per_simulation > 0 else float('inf')

    return average_renewals_per_simulation, average_time_between_renewals

# Simulation parameters
num_simulations = 1000000
number_of_spins = 12
lambda_candies = 0.25  # Average number of candies distributed per spin
candies_for_renewal = 2

# Run multiple simulations
average_renewals, average_time_between = run_multiple_simulations(num_simulations, number_of_spins, lambda_candies, candies_for_renewal)

# Calculate theoretical renewals
theoretical_renewals = theoretical_average_renewals(number_of_spins, lambda_candies, candies_for_renewal)

print(f"Average number of renewals per simulation: {average_renewals}")
print(f"Average time (spins) between renewals: {average_time_between}")
print(f"Theoretical average number of renewals: {theoretical_renewals}")
