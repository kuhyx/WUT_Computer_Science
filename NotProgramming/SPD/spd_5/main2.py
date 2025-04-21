import matplotlib.pyplot as plt
import numpy as np

# Data (decreasing values)
bandwidth = np.array([40, 100, 160, 300, 600, 1000])
detection_threshold_600Hz = np.array([50, 30, 20, 12, 10, 8])
detection_threshold_2200Hz = np.array([40, 25, 18, 10, 8, 7])
detection_threshold_4400Hz = np.array([35, 22, 15, 9, 7, 6])

# Plot
plt.figure(figsize=(10, 6))
plt.xscale('log')

plt.scatter(bandwidth, detection_threshold_600Hz, label='600 Hz', marker='o')
plt.scatter(bandwidth, detection_threshold_2200Hz, label='2200 Hz', marker='^')
plt.scatter(bandwidth, detection_threshold_4400Hz, label='4400 Hz', marker='s')

plt.xlabel('Szerokość pasma [Hz]')
plt.ylabel('Próg detekcji interwału ciszy [ms]')
plt.title('Górna częstotliwość odcięcia (GCO)')
plt.legend(title='GCO')

plt.grid(True)
plt.show()