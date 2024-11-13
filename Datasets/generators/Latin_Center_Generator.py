import numpy as np
from pyDOE import lhs

# Set the number of samples and dimensions
n_samples = 500
n_dimensions = 2

# Generate Latin hypercube samples
lhs_samples = lhs(n_dimensions, samples=n_samples)

# Save to CSV file, one data point per line
filename = f'latin_center_{n_dimensions}d_{n_samples}s.csv'
np.savetxt(filename, lhs_samples, delimiter=",")

print(f"CSV file '{filename}' created with {n_samples} samples in {n_dimensions} dimensions.")
