import numpy as np

# Load the .npz file
input_file = 'code/poli3.npz'
data = np.load(input_file)

# Create dictionaries to hold the split data
data_keys = list(data.keys())
split_point = len(data_keys) // 2
first_half = {key: data[key] for key in data_keys[:split_point]}
second_half = {key: data[key] for key in data_keys[split_point:]}

# Save the halves to separate .npz files
np.savez('poli3_1.npz', **first_half)
np.savez('poli3_2.npz', **second_half)

print(f"Data split into 'poli3_1.npz' and 'poli3_2.npz'")
