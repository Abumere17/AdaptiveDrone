"""
<<<<<<< HEAD
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
=======
DJI Tello Drone GUI Controller
Created by Abumere Okhihan

This GUI serves as the main menu for launching and managing a face-gesture-controlled
DJI Tello drone system. Users can connect the drone, access the head-movement control interface,
read help instructions, or exit the program.
"""

import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from BrainstormCode.HeadRotationSolution.LivePhaseRotationWorking import Rotation_Hub
>>>>>>> main

class MainMenu:
    def __init__(self, root):
        self.root = root
<<<<<<< HEAD
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
        """Handles connecting a new drone."""
        print("Initializing new drone setup...")
        self.drone.setup_new_drone()

    def setup_new_user(self):
        """Handles setting up a new user."""
        print("Starting new user setup...")
        self.setup.run_calibration()
 
    def start_flight_mode(self):
        print("Launching flight mode...")
        self.control_screen.start_hub(self.drone)

    # Displays help instructions
    def show_help(self):
        print("Displaying help menu...")

=======
        self.root.title("Drone Control Main Menu")
        self.root.geometry("400x300")

        # Main title
        tk.Label(root, text="DJI Tello Drone Control", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Buttons for drone setup and control
        tk.Button(root, text="New Drone", command=self.connect_drone, width=20).pack(pady=5)
        tk.Button(root, text="Fly", command=self.launch_rotation_hub, width=20).pack(pady=5)
        tk.Button(root, text="Help", command=self.show_help, width=20).pack(pady=5)
        tk.Button(root, text="Quit", command=self.quit_program, width=20).pack(pady=20)

        # Internal state tracking
        self.drone_connected = False
        self.rotation_hub_process = None

    def connect_drone(self):
        """
        Simulates drone connection check.
        If successful, sets internal flag to True and shows a confirmation popup.
        """
        try: # does not return an exception when drone isnt connected
            self.rotation_hub = Rotation_Hub(False, self.root)
            self.drone_connected = True
            messagebox.showinfo("Connection", "Tello Drone connected successfully!")

        except Exception as e:
            messagebox.showerror("Connection Failed", f"Could not connect to the drone.\n{e}")

    def launch_rotation_hub(self):
        """
        Launches the drone's head-movement control GUI in a separate subprocess.
        Only works after the drone is successfully connected.
        """

        if not self.drone_connected:
            messagebox.showwarning("Drone Not Connected", "Please connect to the drone first using 'New Drone'.")
            return
        
        try:
            self.rotation_hub.run()
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch drone controller.\n{e}")
            
    def show_help(self):
        """
        Displays a help message box with instructions on using the drone system
        and details on the supported head gesture commands.
        """
        help_text = (
            "How to Connect & Fly:\n\n"
            "1. Click 'New Drone' to connect to the Tello drone.\n"
            "2. Click 'Fly' to start the camera-based flight interface.\n"
            "3. Inside the fly window, use the buttons:\n"
            "   - 'Takeoff/Land': Start or stop flying.\n"
            "   - 'Kill Switch': Emergency stop and exit.\n\n"
            "Head Gestures:\n"
            "- Look up: Ascend\n"
            "- Look down: Descend\n"
            "- Look left/right: Rotate\n"
            "- Nod up: Move forward\n"
            "- Nod down: Move backward\n"
        )
        messagebox.showinfo("Help", help_text)

    def quit_program(self):
        """
        Gracefully exits the main menu GUI.
        """
        self.root.quit()

        try:
            self.rotation_hub.cleanup()
        except Exception as e:
            pass

# Entry point of the program
>>>>>>> main
if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
