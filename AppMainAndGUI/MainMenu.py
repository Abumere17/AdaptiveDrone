"""
    Himadri Saha and Abumere Okhihan
    MainMenu.py

    Class for the main menu, which directly controls drone functions and user setup. Main runner of the app

    TODO:
    - Connect new drone
    - New user
"""

# Import Dependencies
import sys
import os
import tkinter as tk

# Ensure Python can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import Classes
from TelloControlModule.TellControlMain import TelloControl
from FaceDectetionModule.ScikitLearn.SetupPhase import SetupPhase
from FaceDectetionModule.ScikitLearn.ControlHub import Control_Hub
from FaceDectetionModule.ScikitLearn.utils import get_face_landmarks

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Drone Project - 7 Hills")

        # Initialize Modules
        self.drone = TelloControl()
        self.setup = SetupPhase()
        self.control_screen = Control_Hub()

        # Create the top prompt, buttons, and close button
        self.label = tk.Label(root, text="Welcome!", font=("Georgia", 14))
        self.label.pack(pady=10)

        # Create buttons for each module
        self.create_button("New Drone", self.setup_new_drone)
        self.create_button("New User", self.setup_new_user)
        self.create_button("Fly", self.start_flight_mode)
        self.create_button("Help", self.show_help)

        # Quit Button
        close_button = tk.Button(root, text="Quit", command=root.quit, font=("Georgia", 12), bg="red", fg="white")
        close_button.pack(pady=10)

    # Helper function to create buttons
    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, font=("Georgia", 12), command=command)
        button.pack(pady=5)

    def setup_new_drone(self):
        print("Initializing new drone setup...")
        self.drone.setup_new_drone()

    def setup_new_user(self):
        print("Starting new user setup...")
        self.setup.run_calibration()

    def start_flight_mode(self):
        print("Launching flight mode...")
        self.control_screen.start_hub(self.drone)

    # Displays help instructions
    def show_help(self):
        print("Displaying help menu...")

if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
