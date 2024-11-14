import numpy as np
from scipy.stats import qmc
import os

def generate_sobol_samples(n, k):
    # Create a Sobol sequence sampler for k dimensions
    sampler = qmc.Sobol(d=k, scramble=True)
    points = sampler.random(n)  # Generate n samples
    return points

# Set the number of samples and the dimensionality
n_samples = 1024
k_dimensions = 3

# Generate Sobol samples
data = generate_sobol_samples(n_samples, k_dimensions)

# Define the directory path (going one level up, then into the 'csv' directory)
directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'csv')

# Save to CSV file, one data point per line
# Define the filename with the path to the 'csv' directory
filename = os.path.join(directory_path, f'sobol_data_{k_dimensions}d_{n_samples}s.csv')
np.savetxt(filename, data, delimiter=",")

print(f"CSV file '{filename}' created with {n_samples} samples in {k_dimensions} dimensions.")
