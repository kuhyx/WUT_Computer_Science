import matplotlib.pyplot as plt

# Values 1
x1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
y1 = [33.2, 35.48, 27.67, 19.41, 15.3, 15.44, 13.59]

# Values 2
x2 = [0.4, 0.5, 0.6, 0.7]
y2 = [13.29, 11.25, 12.55, 13.26]

# Values 3
x3 = [0.4, 0.5, 0.6, 0.7]
y3 = [22.06, 15.48, 18.74, 17.71]

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each line with different styles
plt.plot(x1, y1, marker='o', linestyle='-', color='blue', label='symetrycznie 500 Hz')
plt.plot(x2, y2, marker='s', linestyle='--', color='green', label='asymetrycznie 550 Hz')
plt.plot(x3, y3, marker='^', linestyle='-.', color='red', label='asymetrycznie 450 Hz')

# Add labels and title
plt.xlabel('parametr g', fontsize=40)
plt.ylabel('Prod detekcji syngalu [dB]', fontsize=40)
plt.title('500 Hz', fontsize=48)

# Add a legend
plt.legend(fontsize=32)

# Optional: Add gridlines
plt.grid(True)
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)

# Display the plot
plt.show()

# Values 1
x1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
y1 = [33.06, 35.28, 23.33, 17.14, 14.33, 10.01, 4.43]

# Values 2
x2 = [0.4, 0.5, 0.6, 0.7]
y2 = [15.22, 8.16, 6.45, 6.27]

# Values 3
x3 = [0.4, 0.5, 0.6, 0.7]
y3 = [13.0, 13.06, 7.8, 1.7]

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each line with different styles
plt.plot(x1, y1, marker='o', linestyle='-', color='blue', label='symetrycznie 1500 Hz')
plt.plot(x2, y2, marker='s', linestyle='--', color='green', label='asymetrycznie 1650 Hz')
plt.plot(x3, y3, marker='^', linestyle='-.', color='red', label='asymetrycznie 1350 Hz')

# Add labels and title
plt.xlabel('parametr g', fontsize=40)
plt.ylabel('Prod detekcji syngalu [dB]', fontsize=40)
plt.title('1500 Hz', fontsize=48)

# Add a legend
plt.legend(fontsize=32)

# Optional: Add gridlines
plt.grid(True)
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)

# Display the plot
plt.show()

# Values 1
x1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
y1 = [33.2, 35.48, 27.67, 19.41, 15.3, 15.44, 13.59]

# Values 2
x2 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
y2 = [33.06, 35.28, 23.33, 17.14, 14.33, 10.01, 4.43]

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each line with different styles
plt.plot(x1, y1, marker='o', linestyle='-', color='blue', label='symetrycznie 500 Hz')
plt.plot(x2, y2, marker='s', linestyle='--', color='green', label='symetrycznie 1500 Hz')

# Add labels and title
plt.xlabel('parametr g', fontsize=40)
plt.ylabel('Prod detekcji syngalu [dB]', fontsize=40)
plt.title('500 Hz vs 1500 Hz', fontsize=48)

# Add a legend
plt.legend(fontsize=32)

# Optional: Add gridlines
plt.grid(True)
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)

# Display the plot
plt.show()

# Values 1
x1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
y1 = [33.2, 35.48, 27.67, 19.41, 15.3, 15.44, 13.59]

# Values 2
x2 = [0.005, 0.01, 0.02, 0.05, 0.1, 0.3]
y2 = [81.59, 60.08, 68.48, 58.77, 53.6, 55.46]

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each line with different styles
plt.plot(x1, y1, marker='o', linestyle='-', color='blue', label='pasmowy 500 Hz')
plt.plot(x2, y2, marker='s', linestyle='--', color='green', label='pasmowo-zaporowy 500 Hz')

# Add labels and title
plt.xlabel('parametr g', fontsize=40)
plt.ylabel('Prod detekcji syngalu [dB]', fontsize=40)
plt.title('Porownanie szum pasmowy vs szum pasmowo zaporowy dla 500 Hz', fontsize=48)

# Add a legend
plt.legend(fontsize=32)

# Optional: Add gridlines
plt.grid(True)
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)

# Display the plot
plt.show()

