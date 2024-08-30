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

def find_agents(lambda_, mu, target_service_level, target_time):
    """Find the number of agents required to meet the target service level."""
    a = lambda_ / mu  # offered load in Erlangs

    # Start with the minimum number of agents needed to handle the load
    s = mpmath.ceil(a)
    lower_bound = s
    upper_bound = s * 2  # Start with an upper bound that is double the lower bound

    # Find an upper bound where the service level condition is met
    while True:
        prob_w_leq_t = waiting_time_probability(upper_bound, a, mu, target_time)
        if prob_w_leq_t >= target_service_level:
            break
        upper_bound *= 2

    # Binary search for the precise number of agents
    while upper_bound - lower_bound > mpmath.mpf(1e-10):  # Precision threshold
        mid = (lower_bound + upper_bound) / 2
        prob_w_leq_t = waiting_time_probability(mid, a, mu, target_time)
        if prob_w_leq_t >= target_service_level:
            upper_bound = mid
        else:
            lower_bound = mid + mpmath.mpf(0.0001)

    return mpmath.ceil(upper_bound)

# Given values
lambda_ =1050 / 3600  # arrival rate (calls per second)
mu = 1 / 250  # service rate (calls per second)
target_service_level = 0.8  # 80% of calls answered within the target time
target_time = 20  # target time in seconds

# Find the required number of agents
required_agents = find_agents(lambda_, mu, target_service_level, target_time)
print(f"Number of agents required: {required_agents}")
