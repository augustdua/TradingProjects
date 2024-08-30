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


def find_service_rate(s, calls_per_hour, target_service_level, target_time):
    """Find the service rate required to meet the target service level."""
    lambda_ = calls_per_hour / 3600  # Convert calls per hour to calls per second

    # Initial bounds for the service rate (mu)
    lower_bound = 1e-10
    upper_bound = 1.0

    # Binary search for more precise mu
    while upper_bound - lower_bound > 1e-10:  # Precision threshold
        mu = (lower_bound + upper_bound) / 2
        a = lambda_ / mu  # offered load in Erlangs
        prob_w_leq_t = waiting_time_probability(s, a, mu, target_time)
        if prob_w_leq_t >= target_service_level:
            upper_bound = mu
        else:
            lower_bound = mu

    return upper_bound


# Given values
agents = 50  # Number of agents
calls_per_hour = 500  # Calls received in an hour
target_service_level = 0.8  # 80% of calls answered within the target time
target_time = 30  # target time in seconds

# Find the required service rate
required_service_rate = find_service_rate(agents, calls_per_hour, target_service_level, target_time)
print(f"Required service rate (calls per second): {required_service_rate}")
print(f"Average handling time (seconds per call): {1 / required_service_rate}")
