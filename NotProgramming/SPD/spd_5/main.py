import matplotlib.pyplot as plt
import numpy as np

# Data
delta_t = np.array([500, 200, 100, 50, 20, 10, 5, 3])
ton_60_db = [60, 60, 59, 58, 50, 46, 42, 39]
szum_20_db_per_hz = [20, 19, 18, 16, 12, 11, 8, 8]
ton_60_db_minus = [ton - 60 for ton in ton_60_db]
szum_20_db_per_hz_minus = [szum - 20 for szum in szum_20_db_per_hz]

# Theoretical lines
delta_t_line = np.logspace(np.log10(3), np.log10(500), 100)
log_delta_t_line = np.log10(delta_t_line)

# Equations in terms of log(delta_t)
# For Broadband Noise: y = 10 * log10(delta_t) - 25
y_broadband_line = 10 * log_delta_t_line - 25

# For Pure Tone: y = 9 * log10(delta_t) - 19
y_pure_tone_line = 9 * log_delta_t_line - 19

# Plotting
plt.figure(figsize=(10, 6))

# Plot the experimental data
plt.semilogx(delta_t, ton_60_db_minus, 'o', label='Ton eksperymentalny 60 dB')
plt.semilogx(delta_t, szum_20_db_per_hz_minus, 's', label='Szum eksperymentalny 20 dB/Hz')

# Plot the theoretical lines
plt.semilogx(delta_t_line, y_pure_tone_line, label='Ton - krzywa teoretyczna')
plt.semilogx(delta_t_line, y_broadband_line, label='Szum - krzywa teoereyczna')

plt.xlabel('Czas trwania sygnału [ms]', fontsize=40)
plt.ylabel('Poziom względny głośności [dB]', fontsize=40)
plt.title('Głośnośc vs czas', fontsize=48)
plt.legend(fontsize=32)
plt.grid(True, which="both", ls="--")

plt.xticks(fontsize=32)
plt.yticks(fontsize=32)

plt.show()