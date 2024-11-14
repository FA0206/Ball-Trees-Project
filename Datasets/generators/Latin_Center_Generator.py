import numpy as np
from pyDOE import lhs
import os

# Set the number of samples and dimensions
n_samples = 4000
n_dimensions = 3

# Generate Latin hypercube samples
lhs_samples = lhs(n_dimensions, samples=n_samples)

# Define the directory path (going one level up, then into the 'csv' directory)
directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'csv')

# Save to CSV file, one data point per line
# Define the filename with the path to the 'csv' directory
filename = os.path.join(directory_path, f'latin_center_{n_dimensions}d_{n_samples}s.csv')
np.savetxt(filename, lhs_samples, delimiter=",")

print(f"CSV file '{filename}' created with {n_samples} samples in {n_dimensions} dimensions.")
