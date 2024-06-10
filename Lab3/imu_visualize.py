import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R

# Directory containing CSV files
directory = '../CSV_Files'

# Find CSV files with 'imu' in the filename
imu_files = [f for f in os.listdir(directory) if 'imu' in f.lower()]

# Separate accelerometer and gyroscope files
acc_files = [f for f in imu_files if 'acc' in f.lower()]
gyro_files = [f for f in imu_files if 'gyro' in f.lower()]

# Check if any accelerometer and gyroscope files are found
if not acc_files or not gyro_files:
    print("No accelerometer or gyroscope files found in the directory.")
    exit()

# Function to draw a cube
def draw_cube(ax, rotation):
    # Define the vertices of the cube
    r = 1
    vertices = np.array([
        [r, r, r], [-r, r, r], [-r, -r, r], [r, -r, r],
        [r, r, -r], [-r, r, -r], [-r, -r, -r], [r, -r, -r]
    ])

    # Apply the rotation to the vertices
    rotated_vertices = rotation.apply(vertices)

    # Define the six faces of the cube
    faces = [
        [rotated_vertices[j] for j in [0, 1, 2, 3]],
        [rotated_vertices[j] for j in [4, 5, 6, 7]],
        [rotated_vertices[j] for j in [0, 3, 7, 4]],
        [rotated_vertices[j] for j in [1, 2, 6, 5]],
        [rotated_vertices[j] for j in [0, 1, 5, 4]],
        [rotated_vertices[j] for j in [2, 3, 7, 6]]
    ]

    # Draw the cube
    ax.add_collection3d(Poly3DCollection(faces, 
                                         facecolors='cyan', 
                                         linewidths=1, 
                                         edgecolors='r', 
                                         alpha=0.25))

# Function to merge accelerometer and gyroscope data
def merge_data(acc_file, gyro_file):
    acc_data = pd.read_csv(acc_file)
    gyro_data = pd.read_csv(gyro_file)

    # Merge on the time column (assuming the first column is time)
    merged_data = pd.merge_asof(acc_data, gyro_data, on=acc_data.columns[0], direction='nearest')
    return merged_data

# Iterate through the pairs of accelerometer and gyroscope files
for acc_file, gyro_file in zip(acc_files, gyro_files):
    acc_file_path = os.path.join(directory, acc_file)
    gyro_file_path = os.path.join(directory, gyro_file)
    
    # Merge the data
    data = merge_data(acc_file_path, gyro_file_path)
    
    # Extract the column labels
    column_labels = data.columns
    
    # Assuming the columns are ordered as follows: Time, AccX, AccY, AccZ, GyroX, GyroY, GyroZ
    if len(column_labels) < 7:
        print(f"Files {acc_file} and {gyro_file} do not have enough columns for Time, AccX, AccY, AccZ, GyroX, GyroY, GyroZ.")
        continue
    
    time = data.iloc[:, 0]  # First column: Time
    acc_x = data.iloc[:, 1]  # Second column: Acceleration in X
    acc_y = data.iloc[:, 2]  # Third column: Acceleration in Y
    acc_z = data.iloc[:, 3]  # Fourth column: Acceleration in Z
    gyro_x = data.iloc[:, 4]  # Fifth column: Gyroscope in X
    gyro_y = data.iloc[:, 5]  # Sixth column: Gyroscope in Y
    gyro_z = data.iloc[:, 6]  # Seventh column: Gyroscope in Z

    # Initial orientation (identity quaternion)
    orientation = R.from_quat([0, 0, 0, 1])
    
    # Time difference (assuming constant sampling rate)
    dt = np.mean(np.diff(time))
    
    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the cube orientation over time
    for gx, gy, gz in zip(gyro_x, gyro_y, gyro_z):
        # Convert gyroscope data to radians per second
        gx, gy, gz = np.radians([gx, gy, gz])
        
        # Update the orientation
        rotation_vector = np.array([gx, gy, gz]) * dt
        delta_orientation = R.from_rotvec(rotation_vector)
        orientation = delta_orientation * orientation
        
        # Clear the plot
        ax.cla()
        
        # Draw the cube with the updated orientation
        draw_cube(ax, orientation)
        
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Orientation Visualization for {acc_file} and {gyro_file}')
        
        # Set the limits
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        
        # Draw the plot
        plt.pause(0.01)
    
    plt.show()
