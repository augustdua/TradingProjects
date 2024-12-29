import numpy as np

# Parameters
initial_time = 100  # initial total time (X)
time_increase_per_renewal = 5  # increase in time after each renewal
p = 0.2  # probability of renewal in each spin
n_simulations = 10000  # number of simulations


def simulate_renewal_process(initial_time, time_increase, p, n_simulations):
    renewals = []

    for _ in range(n_simulations):
        time_remaining = initial_time
        n_renewals = 0

        while time_remaining > 0:
            # Draw from geometric distribution to find next renewal time
            next_renewal = np.random.geometric(p)

            if next_renewal <= time_remaining:
                n_renewals += 1
                time_remaining += time_increase - next_renewal
            else:
                break

        renewals.append(n_renewals)

    return np.mean(renewals), np.std(renewals)


# Perform simulation
avg_renewals, std_renewals = simulate_renewal_process(initial_time, time_increase_per_renewal, p, n_simulations)

print(avg_renewals, std_renewals)
