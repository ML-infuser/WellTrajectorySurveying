import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
import math

def calculate_angle(v1, v2):
    """Calculate the angle between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))  # Clip to avoid numerical errors
    return np.degrees(angle)

def has_curve(points, threshold=10):
    """Detect if the curve starts based on angle changes."""
    for i in range(1, len(points)-1):
        v1 = points[i] - points[i-1]
        v2 = points[i+1] - points[i]
        angle = calculate_angle(v1, v2)
        if angle > threshold:
            return True, i
    return False, None

n = int(input("How many types you want to compare: "))
types = []

print("Enter types: ")
for i in range(n):
    val = int(input())
    if val < 1 or val > 5:
        print("Invalid Type")
        exit()
    types.append(val)

# Run scripts for each type
for val in types:
    subprocess.run(["python", f"3d_view_type_{val}.py"])

# Set up 3D plot
plt.figure()
ax = plt.axes(projection='3d')
plt.xlabel("East")
plt.ylabel("North")
ax.set_zlabel('Depth')
ax.invert_zaxis()  # Invert Z-axis

colors = ['blue', 'green', 'red', 'purple', 'orange']
plotted_points = []

# Load data into dictionaries and KDTree for faster lookups
data = {}
trees = {}

for val in types:
    df = pd.read_csv(f'type_{val}.csv')
    data[val] = df
    points = np.column_stack((df['n'], df['e'], df['d']))
    trees[val] = KDTree(points)

# Plot lines for each type and detect curvature
curve_detected = False
for val in types:
    df = data[val]
    points = np.column_stack((df['n'], df['e'], df['d']))

    # Detect if the curve starts
    curve_detected, curve_index = has_curve(points)

    # Plot the line
    ax.plot(df['e'], df['n'], df['d'], color=colors[val-1])

    if curve_detected:
        print(f"Curve detected for type {val} starting at point {curve_index}")
        continue  # Stop if curve detected, so we can plot scatter points only after this point.

# Find close points and plot scatter points only after the curve
if curve_detected:
    for i in range(curve_index, len(points)):
        point = points[i]

        for val1 in types:
            if val1 == val:
                continue

            # Query nearby points from other type within distance threshold
            distances, indices = trees[val1].query(point, k=1, distance_upper_bound=20)

            # Check if valid neighbor found
            if distances != np.inf:
                close_point = data[val1].iloc[indices]
                ax.scatter(point[1], point[0], point[2], color='red', edgecolor='black', marker='o')
                ax.scatter(close_point['e'], close_point['n'], close_point['d'], color='red', edgecolor='black', marker='o')

plt.show()