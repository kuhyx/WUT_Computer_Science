#!/usr/bin/env python3
"""Plot the SPD lab-5 detection thresholds at 600, 2200 and 4400 Hz."""

import matplotlib.pyplot as plt
import numpy as np

# Data (decreasing values)
bandwidth = np.array([40, 100, 160, 300, 600, 1000])
DETECTION_THRESHOLD_600_HZ = np.array([50, 30, 20, 12, 10, 8])
DETECTION_THRESHOLD_2200_HZ = np.array([40, 25, 18, 10, 8, 7])
DETECTION_THRESHOLD_4400_HZ = np.array([35, 22, 15, 9, 7, 6])

# Plot
plt.figure(figsize=(10, 6))
plt.xscale("log")

plt.scatter(bandwidth, DETECTION_THRESHOLD_600_HZ, label="600 Hz", marker="o")
plt.scatter(bandwidth, DETECTION_THRESHOLD_2200_HZ, label="2200 Hz", marker="^")
plt.scatter(bandwidth, DETECTION_THRESHOLD_4400_HZ, label="4400 Hz", marker="s")

plt.xlabel("Szerokość pasma [Hz]")
plt.ylabel("Próg detekcji interwału ciszy [ms]")
plt.title("Górna częstotliwość odcięcia (GCO)")
plt.legend(title="GCO")

plt.grid(visible=True)
plt.show()
