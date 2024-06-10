import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to read CSV and calculate power
def calculate_power(voltage_path, current_path):
    if not os.path.exists(voltage_path):
        print(f"File not found: {voltage_path}")
        return None
    if not os.path.exists(current_path):
        print(f"File not found: {current_path}")
        return None
    
    voltage_df = pd.read_csv(voltage_path)
    current_df = pd.read_csv(current_path)
    
    if len(voltage_df) != len(current_df):
        raise ValueError("The CSV files do not have the same number of rows")

    voltage_column = voltage_df.iloc[:, 2]
    current_column = current_df.iloc[:, 2]
    
    power = voltage_column * current_column
    return power

# Directory containing CSV files
directory = '../CSV_Files'

# Collect all files in the directory
files = os.listdir(directory)

# Dictionary to store paths for voltage and current files based on direction
file_dict = {}

# Populate the dictionary with paths for voltage and current files
for file in files:
    if file.endswith('.csv'):
        parts = file.split('_')
        direction = parts[1]  # Extract the x, y, z part from the filename
        sign = parts[0]  # Extract the plus/minus part from the filename
        key = f"{sign}_{direction}"
        
        if key not in file_dict:
            file_dict[key] = {'volt': None, 'curr': None}
        
        if 'volt' in file:
            file_dict[key]['volt'] = os.path.join(directory, file)
        elif 'curr' in file:
            file_dict[key]['curr'] = os.path.join(directory, file)

# Calculate power for each direction
powers = {}
for key, paths in file_dict.items():
    if paths['volt'] and paths['curr']:
        power = calculate_power(paths['volt'], paths['curr'])
        if power is not None:
            powers[key] = power

# Plotting
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 20))

# Flatten the axes array for easy iteration
axes = axes.flatten()

for ax, (key, power) in zip(axes, powers.items()):
    ax.plot(power, marker='o', linestyle='-', color='b', label='Power')
    cumulative_power = power.cumsum()
    ax.plot(cumulative_power, marker='x', linestyle='--', color='r', label='Cumulative Power')
    direction = key.split('_')[1]
    ax.set_title(f'Power Calculation - {key} Direction ({direction})')
    ax.set_xlabel('Sample Time')
    ax.set_ylabel('Power (Watts)')
    ax.legend()
    ax.grid(True)

# Remove unused subplots if there are any missing data
if len(powers) < len(axes):
    for ax in axes[len(powers):]:
        fig.delaxes(ax)

plt.tight_layout()
plt.show()
