import mpmath

# Input Variables
lambda_ = 254 / 3600  # arrival rate (calls per second)
average_call_duration = 300  # average duration of a call in seconds
mu = 1 / average_call_duration  # service rate (calls per second)
alpha = lambda_/mu  # offered load in Erlangs


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


def expected_waiting_time(alpha, s, mu, K):
    p = steady_state_probabilities(alpha, s, K)
    p_K = m_m_s_k_blocking_probability(alpha, s, K)

    sum_terms = mpmath.mpf(0)
    for n in range(s, K):
        sum_terms += (n - s + 1) * p[n]

    W_q = 1 / (s * mu * (1 - p_K)) * sum_terms
    return W_q


# Verification code

# Test parameters
s = 27  # number of servers
K = 33  # system capacity6
time = 30  # test time for CDF

# Verify steady-state probabilities
p = steady_state_probabilities(alpha, s, K)
print("Steady-state probabilities (p_n):")
for n in range(K + 1):
    print(f"p_{n} = {p[n]}")

# Verify waiting time CDF
print("\nWaiting time CDF (F_W(t)):")
prob_w_leq_t = waiting_time_probability(s, alpha, mu, time, K)
print(f"F_W({time}) = {prob_w_leq_t}")

# Calculate expected waiting time
W_q = expected_waiting_time(alpha, s, mu, K)
print(f"\nExpected waiting time in the queue (W_q): {W_q}")

# Blocking probability
blocking_prob = m_m_s_k_blocking_probability(alpha, s, K)
print(f"\nBlocking Probability = {blocking_prob}")
