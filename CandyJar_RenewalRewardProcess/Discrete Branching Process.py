import numpy as np

# Parameters
Z0 = 10  # Initial number of individuals (free spins)
lambda_ = 0.78  # Average number of offspring (retriggers) per spin

# Initialize
current_generation = [1] * Z0  # Represent each initial spin as an individual
total_spins = len(current_generation)  # Total count of spins

# Initialize generation counter
generation = 0

# Branching process
while current_generation:
    generation += 1  # Increment generation counter
    print(f"Generation {generation}: Starting with {len(current_generation)} spins.")

    next_generation = []
    for individual in current_generation:
        # Determine the number of offspring for this individual using Poisson distribution
        offspring_count = np.random.poisson(lambda_)
        next_generation.extend([1] * offspring_count)  # Add offspring to the next generation

    # Update total spins
    total_spins += len(next_generation)

    # Output update for the end of the generation
    print(f"Generation {generation}: Ended with {len(next_generation)} new spins.")

    # Prepare for the next iteration
    current_generation = next_generation

# Output the result
print(f"\nTotal Free Spins: {total_spins}")
