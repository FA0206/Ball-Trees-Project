import numpy as np
from scipy.stats import qmc

def generate_sobol_samples(n, k):
    # Create a Sobol sequence sampler for k dimensions
    sampler = qmc.Sobol(d=k, scramble=True)
    points = sampler.random(n)  # Generate n samples
    return points

# Set the number of samples and the dimensionality
n_samples = 4096
k_dimensions = 2 

# Generate Sobol samples
data = generate_sobol_samples(n_samples, k_dimensions)

# Save to CSV file, one data point per line
filename = f'sobol_data_{k_dimensions}d.csv'
np.savetxt(filename, data, delimiter=",")

print(f"CSV file '{filename}' created with {n_samples} samples in {k_dimensions} dimensions.")
