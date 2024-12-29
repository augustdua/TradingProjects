import numpy as np

# Hawkes process parameters
T = 80  # Total time for simulation
lambda_0 = 0.4  # Base intensity
alpha = 0.32  # Excitation parameter
beta = 0.5  # Decay parameter
Y = 1.5  # Jump size

# Function to calculate the intensity at the current time
def intensity_function(last_time, events, alpha, beta, Y):
    return lambda_0 + np.sum(Y * alpha * np.exp(-beta * (last_time - np.array(events))))

# Function to run a single Hawkes process simulation and return event times
def run_hawkes_process(T, lambda_0, alpha, beta, Y):
    times = []  # List to store event times
    intensity = lambda_0  # Current intensity
    last_time = 0

    while last_time < T:
        lambda_star = intensity
        U = np.random.uniform(0, 1)
        W = -np.log(U) / lambda_star
        next_time = last_time + W

        if next_time > T:
            break

        D = np.random.uniform(0, 1)
        lambda_next = intensity_function(next_time, times, alpha, beta, Y)

        if D <= lambda_next / lambda_star:
            times.append(next_time)
            intensity = lambda_next

        last_time = next_time

    return times

# Parameters for the simulation
num_simulations = 100000
inter_arrival_times = []

# Running the simulations and accumulating the inter-arrival times
for _ in range(num_simulations):
    event_times = run_hawkes_process(T, lambda_0, alpha, beta, Y)
    inter_arrival_times.extend(np.diff(event_times))

# Calculating the average inter-arrival time across all events and simulations
average_inter_arrival_time = np.mean(inter_arrival_times)
print(f"Average inter-arrival time: {average_inter_arrival_time}")
