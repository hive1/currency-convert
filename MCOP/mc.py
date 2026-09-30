import numpy as np
import matplotlib.pyplot as plt

n = 1000000
p = 0.5
u1, u2, u3 = 0.2, 0.8, 0.4
o1, o2, o3 = 0.1, 0.05, 0.2

# starting a random number generator
rng = np.random.default_rng()

# Calculating expected value (mean) by randomly generating values and finding the median of such

# S = 0.0
# for i in range(n):
# 	x1 = np.exp(u_1 + o_1 * rng.standard_normal())
# 	x2 = np.exp(u_2 + o_2 * rng.standard_normal())
# 	x3 = np.exp(u_3 + o_3 * rng.standard_normal())
# 	S += (x1 + x2 + x3) ** p


def compute_mean_vectorized(n=1000000, rng=rng):
	x1 = np.exp(u1 + o1 * rng.standard_normal(n))
	x2 = np.exp(u2 + o2 * rng.standard_normal(n))
	x3 = np.exp(u3 + o3 * rng.standard_normal(n))
	S = (x1 + x2 + x3) ** p
	return S.mean()

'''A vectorized routine allows for numpy to operate on our entire distribution at once
 allowing us to proceed with our function a lot faster'''

# expected
print(f"Expected value (mean): {compute_mean_vectorized()}")