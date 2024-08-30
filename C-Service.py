import mpmath


def calculate_p0(s, a):
    """Calculate P0 for the Erlang C model using mpmath for high precision."""
    sum_terms = mpmath.mpf(0)
    for n in range(int(s)):  # Convert s to integer for range
        sum_terms += mpmath.power(a, n) / mpmath.factorial(n)

    last_term = mpmath.power(a, s) / (mpmath.factorial(s) * (1 - a / s))
    p0 = 1 / (sum_terms + last_term)
    return p0


def calculate_percentage_answered_within(s, calls_per_hour, service_rate, target_time):
    """Estimate the percentage of calls that will be answered within a specified service time."""
    lambda_ = calls_per_hour / 3600  # Convert calls per hour to calls per second
    mu = service_rate  # Service rate in calls per second
    a = lambda_ / mu  # Traffic intensity

    # Ensure rho is less than 1 for the formula to be valid
    rho = a / s
    if rho >= 1:
        raise ValueError("Traffic intensity rho must be less than 1 for a stable system.")

    # Calculate P0
    p0 = calculate_p0(s, a)

    # Calculate Pw (probability that an arriving customer has to wait)
    pw = (mpmath.power(a, s) / (mpmath.factorial(s) * (1 - rho))) * p0

    # Calculate the probability that waiting time is less than or equal to target_time
    prob_w_leq_t = 1 - pw * mpmath.exp(-mu * (s - a) * target_time)

    # Convert to percentage
    percentage_answered_within = prob_w_leq_t * 100

    return percentage_answered_within


# Given values
agents = 20  # Number of agents
calls_per_hour = 300  # Calls received in an hour
service_rate = 1 / 180  # Service rate (calls per second)
target_time = 20  # Target service time in seconds

# Calculate the percentage of calls answered within the target service time
percentage_answered_within = calculate_percentage_answered_within(agents, calls_per_hour, service_rate, target_time)
print(f"Percentage of calls answered within {target_time} seconds: {percentage_answered_within}%")
