import numpy as np
import matplotlib.pyplot as plt

# Parameters
lambda_param = 0.1  # Same for both exponential and geometric distributions
time_period = 10  # Time t for which we calculate the average renewals
num_simulations = 100000  # Number of simulations to average over


def simulate_process(lambda_param, time_period, num_simulations, distribution='exponential'):
    total_renewals = np.zeros(num_simulations)

    for i in range(num_simulations):
        if distribution == 'exponential':
            times = np.random.exponential(1/lambda_param, size=time_period)
        elif distribution == 'geometric':
            times = np.random.geometric(lambda_param, size=time_period)
        else:
            raise ValueError("Invalid distribution type.")

        cumulative_times = np.cumsum(times)
        renewals = np.sum(cumulative_times <= time_period)
        total_renewals[i] = renewals

    return np.mean(total_renewals), np.var(total_renewals)


# Simulate both processes and calculate average renewals by time t
avg_renewals_exp, var_renewals_exp = simulate_process(lambda_param, time_period, num_simulations, 'exponential')
avg_renewals_geom, var_renewals_geom = simulate_process(lambda_param, time_period, num_simulations, 'geometric')

print(f"Exponential - Average Renewals by time {time_period}: {avg_renewals_exp}, Variance: {var_renewals_exp}")
print(f"Geometric - Average Renewals by time {time_period}: {avg_renewals_geom}, Variance: {var_renewals_geom}")

# Visual comparison
labels = ['Exponential', 'Geometric']
avg_renewals = [avg_renewals_exp, avg_renewals_geom]

plt.bar(labels, avg_renewals, color=['blue', 'orange'])
plt.xlabel('Distribution Type')
plt.ylabel('Average Renewals by time t')
plt.title(f'Comparison of Average Renewals by time {time_period}')
plt.show()

