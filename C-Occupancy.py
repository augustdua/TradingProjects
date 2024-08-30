def calculate_utilization(agents, calls_per_hour, service_rate):
    """Calculate the expected utilization in steady state for a call center."""
    lambda_ = calls_per_hour / 3600  # Convert calls per hour to calls per second
    mu = service_rate  # Service rate in calls per second
    s = agents  # Number of agents

    # Calculate utilization (rho)
    utilization = lambda_ / (s * mu)

    return utilization

# Given values
agents = 56  # Number of agents
calls_per_hour = 500  # Calls received in an hour
service_rate = 1 / 400  # Service rate (calls per second)

# Calculate utilization
utilization = calculate_utilization(agents, calls_per_hour, service_rate)
print(f"Expected Utilization (rho): {utilization}")
