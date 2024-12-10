import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg
import numpy as np

# Load the uploaded image
background_image_path = "C:\\Users\\himad\\OneDrive\\OneDrive - UMass Lowell\\CurrentSchoolDocs\\Capstone Proposal\\MediaPipeMeshNumbers.png" # Update this path to the image location on your PC
background_image = mpimg.imread(background_image_path)

# Simulated points on the mesh for calibration (x, y coordinates normalized for this image)
simulated_landmarks = {
    "Point A": (0.4, 0.6),  # Example points
    "Point B": (0.6, 0.6),
    "Nose Tip": (0.5, 0.5)
}

# Calibration sequence
calibration_sequence = ["Point A", "Point B"]

# Calculate Euclidean distance
def calculate_distance(pt1, pt2):
    return np.linalg.norm(np.array(pt1) - np.array(pt2))

# Setup the plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(background_image)
ax.axis('off')  # Hide axis

# Placeholder for line and text
line, = ax.plot([], [], color='red', linewidth=3)  # Red line with increased width
distance_text = ax.text(0.1, 0.9, '', fontsize=12, color='black', transform=ax.transAxes)
distances_array_text = ax.text(0.1, 0.85, '', fontsize=10, color='black', transform=ax.transAxes)

# Store distances
distances_array = []

# Animation function
def animate(i):
    pt1_label = calibration_sequence[i % len(calibration_sequence)]
    pt1 = simulated_landmarks[pt1_label]
    pt2 = simulated_landmarks["Nose Tip"]

    # Update line with new data
    line.set_data([pt1[0], pt2[0]], [pt1[1], pt2[1]])
    
    # Calculate distance
    distance = calculate_distance(pt1, pt2)
    distances_array.append(round(distance, 4))

    # Update text
    distance_text.set_text(f'Distance from {pt1_label} to Nose: {distance:.4f}')
    distances_array_text.set_text(f'Distances Array: {distances_array}')

    return line, distance_text, distances_array_text

# Create animation
ani = FuncAnimation(fig, animate, frames=len(calibration_sequence) * 3, interval=1000, blit=True)

# Show the animation
plt.show()