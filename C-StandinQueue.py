import mpmath


def calculate_p0(s, a):
    """Calculate P0 for the Erlang C model using mpmath for high precision."""
    sum_terms = mpmath.mpf(0)
    for n in range(int(s)):  # Convert s to integer for range
        sum_terms += mpmath.power(a, n) / mpmath.factorial(n)

    last_term = mpmath.power(a, s) / (mpmath.factorial(s) * (1 - a / s))
    p0 = 1 / (sum_terms + last_term)
    return p0


def calculate_waiting_probability(agents, calls_per_hour, service_rate):
    """Calculate the probability that an arriving customer has to wait."""
    lambda_ = calls_per_hour / 3600  # Convert calls per hour to calls per second
    mu = service_rate  # Service rate in calls per second
    s = agents  # Number of agents
    a = lambda_ / mu  # Traffic intensity (alpha)

    # Ensure rho is less than 1 for the formula to be valid
    rho = a / s
    if rho >= 1:
        raise ValueError("Traffic intensity rho must be less than 1 for a stable system.")

    # Calculate P0
    p0 = calculate_p0(s, a)

    # Calculate rho_s
    rho_s = (mpmath.power(a, s) / mpmath.factorial(s)) * p0

    # Calculate the probability that an arriving customer has to wait
    waiting_probability = rho_s / (1 - rho)

    return waiting_probability


# Given values
agents = 60  # Number of agents
calls_per_hour = 500  # Calls received in an hour
service_rate = 1 / 400  # Service rate (calls per second)

# Calculate waiting probability
waiting_probability = calculate_waiting_probability(agents, calls_per_hour, service_rate)
print(f"Probability that a person has to wait: {waiting_probability}")
