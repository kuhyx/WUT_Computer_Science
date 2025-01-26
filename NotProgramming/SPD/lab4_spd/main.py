import matplotlib.pyplot as plt

# Prepare the datasets
datasets_200Hz = []
datasets_400Hz = []

# Dataset 1: Wieloton 200 Hz, 7 (1400 Hz), 3 składowe
# Starting x value is 1400 Hz
datasets_200Hz.append({
    'name': '200 Hz, 7 (1400 Hz), 3 składowe',
    'x': [1400 + 0, 1400 + 50, 1400 + 100, 1400 + 150],
    'y': [200, 200, 215, 230]
})

# Dataset 2: Wieloton 200 Hz, 7 (1400 Hz), 7 składowych
datasets_200Hz.append({
    'name': '200 Hz, 7 (1400 Hz), 7 składowych',
    'x': [1400 + 0, 1400 + 50, 1400 + 100, 1400 + 150],
    'y': [190, 190, 200, 195]
})

# Dataset 3: Wieloton 200 Hz, 10 (2000 Hz), 3 składowe
# Starting x value is 2000 Hz
datasets_200Hz.append({
    'name': '200 Hz, 10 (2000 Hz), 3 składowe',
    'x': [2000 + 0, 2000 + 50, 2000 + 100, 2000 + 150],
    'y': [225, 215, 220, 265]
})

# Dataset 4: Wieloton 200 Hz, 10 (2000 Hz), 7 składowych
datasets_200Hz.append({
    'name': '200 Hz, 10 (2000 Hz), 7 składowych',
    'x': [2000 + 0, 2000 + 50, 2000 + 100, 2000 + 150],
    'y': [190, 205, 205, 210]
})

# Dataset 4: Wieloton 200 Hz, 10 (2000 Hz), 7 składowych
datasets_200Hz.append({
    'name': 'Shouten - 7',
    'x': [1400 + 0, 1400 + 50, 1400 + 100, 1400 + 150],
    'y': [200, 207.5, 214, 222]
})

# Dataset 4: Wieloton 200 Hz, 10 (2000 Hz), 7 składowych
datasets_200Hz.append({
    'name': 'Shouten - 10',
    'x': [2000 + 0, 2000 + 50, 2000 + 100, 2000 + 150],
    'y': [200, 205, 210, 215]
})



# Dataset 5: Wieloton 400 Hz, 7 (2800 Hz), 3 składowe
# Starting x value is 2800 Hz
datasets_400Hz.append({
    'name': '400 Hz, 7 (2800 Hz), 3 składowe',
    'x': [2800 + 0, 2800 + 100, 2800 + 200, 2800 + 300],
    'y': [405, 410, 410, 405]
})

# Dataset 6: Wieloton 400 Hz, 7 (2800 Hz), 7 składowych
datasets_400Hz.append({
    'name': '400 Hz, 7 (2800 Hz), 7 składowych',
    'x': [2800 + 0, 2800 + 100, 2800 + 200, 2800 + 300],
    'y': [410, 420, 420, 425]
})

# Dataset 7: Wieloton 400 Hz, 10 (4000 Hz), 3 składowe
# Starting x value is 4000 Hz
datasets_400Hz.append({
    'name': '400 Hz, 10 (4000 Hz), 3 składowe',
    'x': [4000 + 0, 4000 + 100, 4000 + 200, 4000 + 300],
    'y': [407, 419, 425, 425]
})

# Dataset 8: Wieloton 400 Hz, 10 (4000 Hz), 7 składowych
# Note: The last two 'Wynik [Hz]' values seem inconsistent.
# They are much lower than expected based on prior values.
# Assuming there might be typos, and they should be 2200 and 2400
# instead of 220 and 240.
datasets_400Hz.append({
    'name': '400 Hz, 10 (4000 Hz), 7 składowych',
    'x': [4000 + 0, 4000 + 100, 4000 + 200, 4000 + 300],
    'y': [405, 410, 415, 415]  # Original data
})

datasets_400Hz.append({
    'name': 'Shouten - 7',
    'x': [2800 + 0, 2800 + 100, 2800 + 200, 2800 + 300],
    'y': [400, 414, 428, 443]
})


datasets_400Hz.append({
    'name': 'Shouten - 10',
    'x': [4000 + 0, 4000 + 100, 4000 + 200, 4000 + 300],
    'y': [400, 410, 420, 430]  # Original data
})

# Plot the data for 200 Hz
plt.figure(figsize=(12, 8))
for dataset in datasets_200Hz:
    if 'Shouten' in dataset['name']:
        plt.plot(dataset['x'], dataset['y'], marker='s', color='red', label=dataset['name'])  # Shouten datasets
    else:
        plt.plot(dataset['x'], dataset['y'], marker='o', label=dataset['name'])  # Other datasets
plt.xlabel('Frequency [Hz]')
plt.ylabel('Result [Hz]')
plt.title('Combined Graph of Results for 200 Hz')
plt.legend()
plt.grid(True)
plt.savefig('results_200Hz.png')  # Save the plot
plt.show()

# Plot the data for 400 Hz
plt.figure(figsize=(12, 8))
for dataset in datasets_400Hz:
    if 'Shouten' in dataset['name']:
        plt.plot(dataset['x'], dataset['y'], marker='s', color='red', label=dataset['name'])  # Shouten datasets
    else:
        plt.plot(dataset['x'], dataset['y'], marker='o', label=dataset['name'])  # Other datasets
plt.xlabel('Frequency [Hz]')
plt.ylabel('Result [Hz]')
plt.title('Combined Graph of Results for 400 Hz')
plt.legend()
plt.grid(True)
plt.savefig('results_400Hz.png')  # Save the plot
plt.show()