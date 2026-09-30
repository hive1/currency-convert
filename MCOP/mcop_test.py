import numpy as np

# The model's mean/drift parameter for the stock's underlying process
u = 1.0
# The stock's volatility (standard deviaion parameters)
o = 0.1
# The strike price of the option
K = 1
# The number of time steps/periods being simulated
n = 10
# The discout factor per period
B = 0.95
# Simulation sizee
M = 10000000

# Random number generator
rng = np.random.default_rng()

# Monte Carlo approximation
S = np.exp(u + o * rng.standard_normal(M))
return_draws = np.maximum(S - K, 0)
P = B**n * np.mean(return_draws)
print(f"The Monte Carlo option price is approximately {P:3f}")

