import mpmath


def calculate_p0(s, a):
    """Calculate P0 for the Erlang C model using mpmath for high precision."""
    sum_terms = mpmath.mpf(0)
    for n in range(s):
        sum_terms += mpmath.power(a, n) / mpmath.factorial(n)

    last_term = mpmath.power(a, s) / (mpmath.factorial(s) * (1 - a / s))
    p0 = 1 / (sum_terms + last_term)
    return p0


def calculate_asa(agents, calls_per_hour, service_rate):
    """Calculate the Average Speed of Answer (ASA) for a call center."""
    lambda_ = calls_per_hour / 3600  # Convert calls per hour to calls per second
    mu = service_rate  # Service rate in calls per second
    s = agents  # Number of agents
    a = lambda_ / mu  # Traffic intensity

    # Ensure rho is less than 1 for the formula to be valid
    rho = a / s
    if rho >= 1:
        raise ValueError("Traffic intensity rho must be less than 1 for a stable system.")

    # Calculate P0
    p0 = calculate_p0(s, a)

    # Calculate Pw (probability that an arriving customer has to wait)
    pw = (mpmath.power(a, s) / (mpmath.factorial(s) * (1 - rho))) * p0

    # Calculate ASA using the given formula
    asa = pw / (s * mu * (1 - rho))

    return asa


# Given values
agents = 16  # Number of agents
calls_per_hour = 135  # Calls received in an hour
service_rate = 1 / 300  # Service rate (calls per second)

# Calculate ASA
asa = calculate_asa(agents, calls_per_hour, service_rate)
print(f"Average Speed of Answer (ASA): {asa} seconds")
