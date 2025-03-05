import sys
import os
import tkinter as tk
from tkinter import messagebox
#New line
# Ensure Python can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import Classes
from TelloControlModule.TellControlMain import TelloControl
from FaceDectetionModule.ScikitLearn.SetupPhase import SetupPhase
from FaceDectetionModule.ScikitLearn.ControlHub import Control_Hub 
from FaceDectetionModule.ScikitLearn.utils import get_face_landmarks

class Rotation_Hub:
    """
    Class responsible for handling flight mode operations.
    """
    def __init__(self, drone):
        self.drone = drone

    def start(self):
        if self.drone.is_connected():
            print("Rotation Hub initialized. Ready for flight.")
            # Add flight control logic here
        else:
            print("Error: No drone connected!")

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Drone Project - 7 Hills")

        # Initialize Modules
        self.drone = TelloControl()
        self.setup = SetupPhase()
        self.control_screen = Control_Hub()
        self.rotation_hub = Rotation_Hub(self.drone)

        # Create UI Elements
        self.label = tk.Label(root, text="Welcome!", font=("Georgia", 14))
        self.label.pack(pady=10)

        # Buttons
        self.create_button("New Drone", self.setup_new_drone)
        self.create_button("New User", self.setup_new_user)
        
        # Flight mode button (disabled initially)
        self.flight_button = tk.Button(self.root, text="Fly", font=("Georgia", 12), command=self.start_flight_mode, state=tk.DISABLED)
        self.flight_button.pack(pady=5)

        self.create_button("Help", self.show_help)

        # Quit Button
        close_button = tk.Button(root, text="Quit", command=root.quit, font=("Georgia", 12), bg="red", fg="white")
        close_button.pack(pady=10)

        # Check if drone is connected
        self.check_drone_status()
    
    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, font=("Georgia", 12), command=command)
        button.pack(pady=5)
    
    def check_drone_status(self):
        """Checks if the drone is connected and enables/disables the flight button."""
        if hasattr(self.drone, 'is_connected') and self.drone.is_connected():
            self.flight_button.config(state=tk.NORMAL)
        else:
            self.flight_button.config(state=tk.DISABLED)
            messagebox.showwarning("Drone Not Connected", "Please connect a drone before flying.")
    
    def setup_new_drone(self):
        """Handles connecting a new drone."""
        print("Initializing new drone setup...")
        connected = self.drone.setup_new_drone()
        if connected:
            messagebox.showinfo("Success", "Drone connected successfully!")
            self.check_drone_status()
        else:
            messagebox.showerror("Error", "Failed to connect to drone.")

    def setup_new_user(self):
        """Handles setting up a new user."""
        print("Starting new user setup...")
        self.setup.run_calibration()

    def start_flight_mode(self):
        """Starts the Rotation Hub if a drone is connected."""
        if hasattr(self.drone, 'is_connected') and self.drone.is_connected():
            print("Launching flight mode...")
            self.rotation_hub.start()
        else:
            messagebox.showerror("Error", "No drone connected! Please connect a drone first.")
    
    def show_help(self):
        """Displays help information."""
        help_text = """
        Adaptive Drone Project Help:
        - 'New Drone': Connect a new drone.
        - 'New User': Set up a user profile and face tracking.
        - 'Fly': Start flight mode (enabled only when a drone is connected).
        - 'Quit': Exit the application.
        """
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
