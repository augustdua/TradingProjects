import mpmath

# Input Variables
lambda_ = 1050/ 3600  # arrival rate (calls per second)
average_call_duration = 250  # average duration of a call in seconds
mu = 1 / average_call_duration  # service rate (calls per second)
alpha = lambda_ / mu  # offered load in Erlangs
target_time = 20  # target time in seconds
blocking_percentage = 0.05  # 5% blocking probability
target_service_level = 0.8  # 80% of calls answered within the target time

def m_m_s_k_p0(alpha, s, k):
    rho = alpha / s
    sum_terms = mpmath.fsum(mpmath.power(alpha, r) / mpmath.factorial(r) for r in range(s))
    if rho != 1:
        last_term = (mpmath.power(alpha, s) / mpmath.factorial(s)) * ((1 - mpmath.power(rho, k - s + 1)) / (1 - rho))
    else:
        last_term = (mpmath.power(alpha, s) / mpmath.factorial(s)) * (k - s + 1)
    p_0 = 1 / (sum_terms + last_term)
    return p_0

def m_m_s_k_blocking_probability(alpha, s, k):
    p_0 = m_m_s_k_p0(alpha, s, k)
    rho = alpha / s
    p_s = (mpmath.power(alpha, s) / mpmath.factorial(s)) * p_0
    p_k = p_s * mpmath.power(rho, k - s)
    return p_k

def find_required_capacity(alpha, s, blocking_percentage):
    low, high = s, 10 * s  # Start with a larger upper bound
    while low < high:
        mid = (low + high) // 2
        blocking_prob = m_m_s_k_blocking_probability(alpha, s, mid)
        if blocking_prob <= blocking_percentage:
            high = mid
        else:
            low = mid + 1
    return low

def steady_state_probabilities(alpha, s, K):
    rho = alpha / s
    p = [mpmath.mpf(0)] * (K + 1)
    p_0 = m_m_s_k_p0(alpha, s, K)
    p[0] = p_0

    for n in range(1, s + 1):
        p[n] = (mpmath.power(alpha, n) / mpmath.factorial(n)) * p_0

    for n in range(s + 1, K + 1):
        p[n] = p[s] * mpmath.power(rho, n - s)

    return p

def waiting_time_probability(s, alpha, mu, t, K):
    p_K = m_m_s_k_blocking_probability(alpha, s, K)
    p = steady_state_probabilities(alpha, s, K)

    sum1 = mpmath.mpf(0)
    for n in range(s, K):
        sum2 = mpmath.mpf(0)
        for r in range(n - s + 1):
            sum2 += mpmath.exp(-s * mu * t) * mpmath.power(s * mu * t, r) / mpmath.factorial(r)
        sum1 += p[n] * sum2

    F_q_t = 1 - (1 / (1 - p_K)) * sum1
    return F_q_t

def find_agents_and_capacity(alpha, mu, target_service_level, target_time, blocking_percentage):
    low, high = 1, 1000
    best_agents, best_capacity = None, None
    best_waiting_time_prob, best_blocking_prob = None, None

    while low < high:
        s = (low + high) // 2

        try:
            K = find_required_capacity(alpha, s, blocking_percentage)
        except ValueError:
            low = s + 1
            continue

        prob_w_leq_t = waiting_time_probability(s, alpha, mu, target_time, K)
        blocking_prob = m_m_s_k_blocking_probability(alpha, s, K)

        if prob_w_leq_t >= target_service_level and blocking_prob <= blocking_percentage:
            best_agents, best_capacity = s, K
            best_waiting_time_prob = prob_w_leq_t
            best_blocking_prob = blocking_prob
            high = s
        else:
            low = s + 1

    if best_agents is None or best_capacity is None:
        raise ValueError("Unable to find the required number of agents and capacity within the given bounds")

    return best_agents, best_capacity, best_waiting_time_prob, best_blocking_prob

required_agents, required_capacity, prob_w_leq_t, blocking_prob = find_agents_and_capacity(alpha, mu, target_service_level, target_time, blocking_percentage)
print(f"Number of agents required: {required_agents}")
print(f"System capacity required: {required_capacity}")
print(f"Probability that waiting time is <= {target_time} seconds: {prob_w_leq_t}")
print(f"Blocking Probability: {blocking_prob}")
