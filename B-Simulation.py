import simpy
import numpy as np


class MMSKQueue:
    def __init__(self, env, num_servers, max_customers, arrival_rate, service_rate):
        self.env = env
        self.server = simpy.Resource(env, num_servers)
        self.num_servers = num_servers
        self.max_customers = max_customers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate

        self.total_customers = 0
        self.blocked_customers = 0
        self.total_waiting_time = 0
        self.total_served_customers = 0
        self.waiting_times = []

    def arrival(self):
        while True:
            yield self.env.timeout(np.random.exponential(1 / self.arrival_rate))
            self.total_customers += 1
            if self.server.count + len(self.server.queue) < self.max_customers:
                self.env.process(self.service())
            else:
                self.blocked_customers += 1

    def service(self):
        arrival_time = self.env.now
        with self.server.request() as request:
            yield request
            self.total_waiting_time += self.env.now - arrival_time
            self.waiting_times.append(self.env.now - arrival_time)
            yield self.env.timeout(np.random.exponential(1 / self.service_rate))
            self.total_served_customers += 1


def run_simulation(arrival_rate, service_rate, num_servers, max_customers, simulation_time, waiting_time_threshold):
    env = simpy.Environment()
    queue = MMSKQueue(env, num_servers, max_customers, arrival_rate, service_rate)
    env.process(queue.arrival())
    env.run(until=simulation_time)

    blocking_probability = queue.blocked_customers / queue.total_customers
    average_waiting_time = (queue.total_waiting_time / queue.total_served_customers
                            if queue.total_served_customers > 0 else float('inf'))

    # Calculate the probability that the waiting time is less than the given threshold
    if queue.waiting_times:
        waiting_time_probability = sum(1 for w in queue.waiting_times if w <= waiting_time_threshold) / len(
            queue.waiting_times)
    else:
        waiting_time_probability = float('inf')

    return blocking_probability, average_waiting_time, waiting_time_probability


# Parameters based on your input
lambda_ = 254 / 3600  # arrival rate (calls per second)
average_call_duration = 300  # average duration of a call in seconds
mu = 1 / average_call_duration  # service rate (calls per second)
num_servers = 27  # Example number of servers
max_customers = 33  # Example maximum customers in the system (including those being served)
simulation_time = 10000000  # Maximum simulation time
waiting_time_threshold = 30  # Example waiting time threshold in seconds

# Run the simulation
blocking_probability, avg_waiting_time, waiting_time_probability = run_simulation(
    lambda_, mu, num_servers, max_customers, simulation_time, waiting_time_threshold
)

print(f"Blocking Probability: {blocking_probability:.4f}")
print(f"Average Waiting Time: {avg_waiting_time:.4f}")
print(f"Probability that waiting time <= {waiting_time_threshold} seconds: {waiting_time_probability:.4f}")
