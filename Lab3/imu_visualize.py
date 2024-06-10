import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

# Directory containing CSV files
directory = '../CSV_Files'

# Define the expected filenames without .csv extension
expected_files = {
    'x_acc': 'x_imu_acc',
    'x_gyro': 'x_imu_dps',
    'y_acc': 'y_imu_acc',
    'y_gyro': 'y_imu_dps',
    'z_acc': 'z_imu_acc',
    'z_gyro': 'z_imu_dps'
}

# Verify all expected files are present in the directory
for key, filename in expected_files.items():
    if not os.path.isfile(os.path.join(directory, filename)):
        print(f"Missing file: {filename}")
        exit()

# Function to read the data from CSV files
def read_data(file):
    df = pd.read_csv(file)
    if df.shape[1] < 3:
        raise ValueError(f"File {file} does not have at least 3 columns")
    return df.iloc[:, 2]

# Read all data
x_acc = read_data(os.path.join(directory, expected_files['x_acc']))
x_gyro = read_data(os.path.join(directory, expected_files['x_gyro']))
y_acc = read_data(os.path.join(directory, expected_files['y_acc']))
y_gyro = read_data(os.path.join(directory, expected_files['y_gyro']))
z_acc = read_data(os.path.join(directory, expected_files['z_acc']))
z_gyro = read_data(os.path.join(directory, expected_files['z_gyro']))

# Assume a constant sampling rate and calculate the time difference
dt = 0.01  # Set a default value (e.g., 10ms), modify as necessary

# Initialize orientation (roll, pitch, yaw) in radians
roll = np.zeros(len(x_gyro))
pitch = np.zeros(len(y_gyro))
yaw = np.zeros(len(z_gyro))

# Integrate gyroscope data to get orientation
for i in range(1, len(x_gyro)):
    roll[i] = roll[i-1] + np.radians(x_gyro[i]) * dt
    pitch[i] = pitch[i-1] + np.radians(y_gyro[i]) * dt
    yaw[i] = yaw[i-1] + np.radians(z_gyro[i]) * dt

# Create a time array
time = np.arange(0, len(x_gyro) * dt, dt)

# Plot roll, pitch, and yaw
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

axs[0].plot(time, roll, label='Roll')
axs[0].set_ylabel('Roll (radians)')
axs[0].grid(True)
axs[0].legend()

axs[1].plot(time, pitch, label='Pitch')
axs[1].set_ylabel('Pitch (radians)')
axs[1].grid(True)
axs[1].legend()

axs[2].plot(time, yaw, label='Yaw')
axs[2].set_ylabel('Yaw (radians)')
axs[2].set_xlabel('Time (s)')
axs[2].grid(True)
axs[2].legend()

plt.suptitle('Orientation Visualization (Roll, Pitch, Yaw)')
plt.show()
