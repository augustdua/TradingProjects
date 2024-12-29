import numpy as np

# Re-run the simulation with printing the maximum number of free spins encountered

# Parameters
Z0 = 12  # Initial number of individuals (free spins)
lambda_ = 0.2  # Average number of offspring (retriggers) per spin
iterations = 1000000  # Number of times to run the simulation for averaging


# Function to simulate one iteration of the branching process
def simulate_branching_process(Z0, lambda_):
    current_generation = [1] * Z0  # Represent each initial spin as an individual
    total_spins = len(current_generation)  # Total count of spins

    # Branching process
    while current_generation:
        next_generation = []
        for individual in current_generation:
            # Determine the number of offspring for this individual using Poisson distribution
            offspring_count = np.random.poisson(lambda_)
            next_generation.extend([1] * offspring_count)  # Add offspring to the next generation

        # Update total spins
        total_spins += len(next_generation)

        # Prepare for the next iteration
        current_generation = next_generation

    return total_spins


# Run the simulation multiple times and calculate the average and maximum number of spins
total_spins_list = [simulate_branching_process(Z0, lambda_) for _ in range(iterations)]
average_total_spins = np.mean(total_spins_list)
max_total_spins = np.max(total_spins_list)

print(average_total_spins, max_total_spins)
