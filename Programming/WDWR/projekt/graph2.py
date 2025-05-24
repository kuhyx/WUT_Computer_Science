import matplotlib.pyplot as plt
import numpy as np

# Data for the three scenarios
scenario1_profits = [
    8283.101223531, 8360.092861464, 8023.436774628, 7996.435353438, 8108.734620296,
    8709.702668322, 9236.429507678, 8492.980846575, 8912.962073143, 8201.079841867,
    7947.08574225, 8426.386242154, 8633.510288097, 7925.419317516, 8216.653093455,
    8162.239336848, 10606.276724793, 7766.753696884, 8902.966530729, 8329.954853003,
    8615.534725088, 9307.905933844, 8711.836200338, 7853.713101162, 8160.850707138,
    8505.74747647, 7807.599624626, 8650.006339759, 7571.333855925, 9103.892851116
]

scenario2_profits = [
    8779.880622914, 8905.098118171, 8457.038873118, 8476.337700492, 8611.662470696,
    9284.604268643, 9787.525726881, 9033.316521658, 9469.444921654, 8726.555858861,
    8437.173060618, 8935.043125766, 9172.334141304, 8425.564554151, 8725.52174345,
    8672.538442695, 11321.501722433, 8233.9854963, 9465.167737138, 8841.407418574,
    9162.816556878, 9946.670992861, 9281.411111594, 8349.695093959, 8671.731748701,
    9074.152941559, 8296.712958538, 9208.592940681, 8041.287735389, 9707.228511359
]

scenario3_profits = [
    9268.899026395, 9430.210649623, 8919.631184021, 8944.062758608, 9095.775246456,
    9886.312580673, 10387.393647889, 9637.953603446, 10098.221535588, 9238.913391815,
    8980.977156104, 9414.393022001, 9722.356857713, 8917.726783311, 9178.474614142,
    9167.292074295, 12011.512542804, 8693.048121325, 10039.47692674, 9375.735645214,
    9730.36014247, 10531.376234688, 9750.101324443, 8881.341453044, 9186.289888284,
    9675.754350507, 8773.329747496, 9722.523537949, 8489.277170975, 10325.425491734
]

# Create figure with single plot
plt.figure(figsize=(12, 8))

# Sort the data for each scenario (descending order)
scenario1_sorted = sorted(scenario1_profits, reverse=True)
scenario2_sorted = sorted(scenario2_profits, reverse=True)
scenario3_sorted = sorted(scenario3_profits, reverse=True)

# Create y-axis values (cumulative distribution from 0 to 1)
num_points = len(scenario1_profits)
y_values = [i / num_points for i in range(1, num_points + 1)]

# Plot all three scenarios on the same graph
plt.plot(scenario1_sorted, y_values, 'b-o', label='Scenariusz 1', linewidth=2, markersize=4)
plt.plot(scenario2_sorted, y_values, 'g-s', label='Scenariusz 2', linewidth=2, markersize=4)
plt.plot(scenario3_sorted, y_values, 'r-^', label='Scenariusz 3', linewidth=2, markersize=4)
# Add labels and title
plt.xlabel('Przeciętny Zysk')
plt.ylabel('Odwrotna dystrybuanta')
plt.ylim(0, 1)  # Set y-axis limits to cut off values outside 0-1 range
plt.grid(True, alpha=0.3)
plt.legend()

# Format the plot
plt.tight_layout()

# Show the plot
plt.show()

# Print statistics for each scenario
print("Scenario Statistics:")
print(f"Scenario 1 - Mean: {np.mean(scenario1_profits):.2f}, Std: {np.std(scenario1_profits):.2f}")
print(f"Scenario 2 - Mean: {np.mean(scenario2_profits):.2f}, Std: {np.std(scenario2_profits):.2f}")
print(f"Scenario 3 - Mean: {np.mean(scenario3_profits):.2f}, Std: {np.std(scenario3_profits):.2f}")