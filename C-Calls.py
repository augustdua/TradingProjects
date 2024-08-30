import mpmath


def erlang_c(s, a):
    """Calculate the Erlang C probability of waiting formula using mpmath for high precision."""
    rho = a / s
    if rho >= 1:
        return 1.0

    # Calculate P0 using a numerically stable approach
    sum_terms = mpmath.mpf(0)
    for n in range(int(s)):  # Convert s to integer for range
        sum_terms += mpmath.power(a, n) / mpmath.factorial(n)

    last_term = mpmath.power(a, s) / (mpmath.factorial(s) * (1 - rho))
    p0 = 1 / (sum_terms + last_term)

    # Calculate Pw (probability that an arriving customer has to wait)
    pw = last_term * p0

    return pw


def waiting_time_probability(s, a, mu, t):
    """Calculate the probability that waiting time is less than or equal to t."""
    pw = erlang_c(s, a)
    rho = a / s
    prob_w_leq_t = 1 - pw * mpmath.exp(-mu * (s - a) * t)
    return prob_w_leq_t


def find_max_calls(s, mu, target_service_level, target_time):
    """Find the maximum number of calls that can be handled to meet the target service level."""
    lower_bound = 0
    upper_bound = 1
    increment = 1

    # Find an upper bound
    while True:
        a = upper_bound / mu  # offered load in Erlangs
        prob_w_leq_t = waiting_time_probability(s, a, mu, target_time)
        if prob_w_leq_t < target_service_level:
            break
        upper_bound *= 2

    # Binary search for more precise lambda
    while upper_bound - lower_bound > 1e-10:  # Precision threshold
        lambda_ = (lower_bound + upper_bound) / 2
        a = lambda_ / mu  # offered load in Erlangs
        prob_w_leq_t = waiting_time_probability(s, a, mu, target_time)
        if prob_w_leq_t >= target_service_level:
            lower_bound = lambda_
        else:
            upper_bound = lambda_

    return lower_bound * 3600  # Convert arrival rate to calls per hour


# Given values
agents = 10000  # Number of agents
mu = 1 / 300  # service rate (calls per second)
target_service_level = 0.8  # 80% of calls answered within the target time
target_time = 30  # target time in seconds

# Find the maximum number of calls that can be handled per hour
max_calls_per_hour = find_max_calls(agents, mu, target_service_level, target_time)
print(f"Maximum number of calls that can be handled per hour: {max_calls_per_hour}")
