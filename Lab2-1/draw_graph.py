import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Directory containing CSV files
directory = '../CSV_Files'

# Create a list of CSV files in the directory
csv_files = [f for f in os.listdir(directory)]

# Determine the number of files
num_files = len(csv_files)

# Calculate number of rows needed for subplots
num_rows = int(np.ceil(num_files / 2))

# Create subplots
fig, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(12, num_rows * 6))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Hide any unused subplots
for ax in axes[num_files:]:
    ax.set_visible(False)

# Iterate through the CSV files and plot each one
for ax, csv_file in zip(axes, csv_files):
    # Construct the full file path
    file_path = os.path.join(directory, csv_file)

    # Read the CSV file
    data = pd.read_csv(file_path)

    # Extract the column labels
    column_labels = data.columns

    # Extract the columns for x and y axes
    x = data.iloc[:, 1]  # Second column
    y = data.iloc[:, 2]  # Third column

    # Plot the data
    ax.plot(x, y, marker='o', linestyle='-', color='b')
    ax.set_xlabel(column_labels[1])
    ax.set_ylabel(column_labels[2])
    ax.set_title("{}".format(csv_file))
    ax.grid(True)

# Adjust layout with custom spacing using subplots_adjust
plt.subplots_adjust(wspace=0.4, hspace=0.6)

plt.show()
