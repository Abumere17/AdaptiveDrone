import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Sample facial mesh nodes
nodes = {
    1: (0, 0),  # Nose tip
    2: (-1, 1),
    3: (1, 1),
    4: (-1, -1),
    5: (1, -1),
    6: (0.5, 0.5),
    7: (-0.5, -0.5),
    8: (0.5, -0.5),
    9: (-0.5, 0.5),
}

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title("Setup Phase Visualization")
ax.axis('off')

# Load the background image
background = plt.imread('C:/Users/himad/Desktop/AdaptiveDrone/AdaptiveDrone/FaceDectetionModule/VisulizationStuff/MediaPipeMeshNumbers.png')
ax.imshow(background, extent=[-2, 2, -2, 2], aspect='auto')

# Initialize elements
line, = ax.plot([], [], color='red', lw=2)
text = ax.text(-1.8, -1.8, "Array: []", fontsize=12, color='blue')

# Initialize distances and cycle data
distances = []
selected_nodes = []
cycle = 0

# Function to generate random distances and nodes for the next cycle
def generate_random_data():
    random_distances = [round(random.uniform(1, 10), 1) for _ in range(5)]
    random_nodes = random.sample(list(nodes.keys())[1:], 5)  # Randomly select 5 nodes excluding the nose tip
    return random_distances, random_nodes

# Animation update function
def update(frame):
    global distances, selected_nodes, cycle

    if frame == 0:
        # Frame 1: Empty array
        line.set_data([], [])
        text.set_text(f"Cycle {cycle + 1}: Array: []")
    else:
        # Frames 2 to 6: Draw lines to different nodes and update the array
        node1 = nodes[1]
        node2 = nodes[selected_nodes[frame - 1]]
        line.set_data([node1[0], node2[0]], [node1[1], node2[1]])
        text.set_text(f"Cycle {cycle + 1}: Array: {distances[:frame]}")

    # Reset distances and cycle after 5 frames
    if frame == 5:
        distances, selected_nodes = generate_random_data()
        cycle += 1
    return line, text

# Generate initial random distances and nodes
distances, selected_nodes = generate_random_data()

# Set up animation
ani = FuncAnimation(fig, update, frames=range(6), interval=1000, repeat=True)

# Quit the animation on 'q' key press
def on_key(event):
    if event.key == 'q':
        plt.close(fig)

fig.canvas.mpl_connect('key_press_event', on_key)

# Display the animation
plt.show()
