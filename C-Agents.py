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

    last_term = (a ** s) / (mpmath.factorial(s) * (1 - rho))
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

    # Iterate to find the minimum number of agents s that satisfies the target service level
    s = mpmath.ceil(a)
    while True:
        prob_w_leq_t = waiting_time_probability(s, a, mu, target_time)
        if prob_w_leq_t >= target_service_level:
            return int(s)
        s += 1

# Given values
lambda_ = 10500 / 3600  # arrival rate (calls per second)
mu = 1 / 3000  # service rate (calls per second)
target_service_level = 0.8  # 80% of calls answered within the target time
target_time = 30  # target time in seconds

# Find the required number of agents
required_agents = find_agents(lambda_, mu, target_service_level, target_time)
print(f"Number of agents required: {required_agents}")
