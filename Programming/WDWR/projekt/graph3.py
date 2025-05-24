import matplotlib.pyplot as plt
import numpy as np

# Data for the three scenarios - Risk values
scenario1_risks = [
    184.458, 195.09, 207.678, 278.26, 220.823, 181.042, 195.281, 199.255, 182.194, 181.295,
    285.773, 185.306, 272.997, 288.405, 223.407, 213.341, 208.693, 354.01, 217.093, 301.892,
    200.499, 637.424, 408.232, 308.314, 181.042, 470.693, 212.039, 184.694, 345.455, 205.291
]

scenario2_risks = [
    403.784, 414.043, 408.225, 664.379, 413.447, 448.303, 513.763, 439.966, 403.784, 408.366,
    773.926, 459.531, 537.056, 795.835, 542.569, 512.817, 471.741, 879.425, 441.46, 533.521,
    659.742, 990.73, 842.758, 776.278, 404.787, 989.35, 481.833, 409.978, 795.275, 421.261
]

scenario3_risks = [
    559.839, 576.633, 596.264, 942.092, 560.045, 679.026, 683.47, 627.607, 559.839, 562.478,
    1245.41, 638.37, 675.366, 1132.8, 784.609, 686.634, 680.842, 1115.92, 572.793, 682.114,
    914.647, 1211.67, 1051.95, 1104.87, 583.36, 1360.71, 743.425, 577.734, 1191.09, 581.791
]

# Create figure with single plot
plt.figure(figsize=(12, 8))

# Sort the data for each scenario (descending order)
scenario1_sorted = sorted(scenario1_risks, reverse=True)
scenario2_sorted = sorted(scenario2_risks, reverse=True)
scenario3_sorted = sorted(scenario3_risks, reverse=True)

# Create y-axis values (cumulative distribution from 0 to 1)
num_points = len(scenario1_risks)
y_values = [i / num_points for i in range(1, num_points + 1)]

# Plot all three scenarios on the same graph
plt.plot(scenario1_sorted, y_values, 'b-o', label='Scenariusz 1', linewidth=2, markersize=4)
plt.plot(scenario2_sorted, y_values, 'g-s', label='Scenariusz 2', linewidth=2, markersize=4)
plt.plot(scenario3_sorted, y_values, 'r-^', label='Scenariusz 3', linewidth=2, markersize=4)

# Add labels and title
plt.xlabel('Ryzyko')
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
print(f"Scenario 1 - Mean: {np.mean(scenario1_risks):.2f}, "
      f"Std: {np.std(scenario1_risks):.2f}")
print(f"Scenario 2 - Mean: {np.mean(scenario2_risks):.2f}, "
      f"Std: {np.std(scenario2_risks):.2f}")
print(f"Scenario 3 - Mean: {np.mean(scenario3_risks):.2f}, "
      f"Std: {np.std(scenario3_risks):.2f}")