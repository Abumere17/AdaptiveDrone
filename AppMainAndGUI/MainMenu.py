import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ensure Python can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import Classes
from TelloControlModule.TellControlMain import TelloControl
from FaceDectetionModule.ScikitLearn.ControlHub import Control_Hub 
from BrainstormCode.HeadRotationSolution.LivePhaseRotationWorking import Rotation_Hub

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Drone Project - 7 Hills")

        # Initialize Modules
        self.drone = TelloControl()
        self.control_screen = Control_Hub()
        self.rotation_hub = None  # Only create when needed

        # Create UI Elements
        self.label = tk.Label(root, text="Welcome!", font=("Georgia", 14))
        self.label.pack(pady=10)

        # Buttons
        self.create_button("New Drone", self.setup_new_drone)

        # Flight mode button (initialize before calling check_drone_status)
        self.flight_button = tk.Button(self.root, text="Fly", font=("Georgia", 12), command=self.start_flight_mode, state=tk.DISABLED)
        self.flight_button.pack(pady=5)

        self.create_button("Help", self.show_help)

        # Quit Button
        close_button = tk.Button(root, text="Quit", command=root.quit, font=("Georgia", 12), bg="red", fg="white")
        close_button.pack(pady=10)

        # Check drone status after defining flight_button
        self.root.after(100, self.check_drone_status, False)  # Delay execution to ensure flight_button exists

    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, font=("Georgia", 12), command=command)
        button.pack(pady=5)

    def check_drone_status(self, show_warning=True):
        """Checks if the drone is connected and enables/disables the flight button."""
        if hasattr(self.drone, 'is_connected') and self.drone.is_connected():
            self.flight_button.config(state=tk.NORMAL)
        else:
            self.flight_button.config(state=tk.DISABLED)
            if show_warning:
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

    def start_flight_mode(self):
        """Starts the Rotation Hub if a drone is connected."""
        if hasattr(self.drone, 'is_connected') and self.drone.is_connected():
            print("Launching flight mode...")
            if self.rotation_hub is None:
                self.rotation_hub = Rotation_Hub(self.drone)  # Only create when needed
            self.root.withdraw()  # Hide main menu when flight mode starts
            self.rotation_hub.start()
        else:
            messagebox.showerror("Error", "No drone connected! Please connect a drone first.")

    def show_help(self):
        """Displays help information."""
        help_text = """
        Adaptive Drone Project Help:
        - 'New Drone': Connect a new drone.
        - 'Fly': Start flight mode (enabled only when a drone is connected).
        - 'Quit': Exit the application.
        """
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
