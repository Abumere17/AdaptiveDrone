import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import sys

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Control Main Menu")
        self.root.geometry("400x300")

        tk.Label(root, text="DJI Tello Drone Control", font=("Helvetica", 16, "bold")).pack(pady=20)

        tk.Button(root, text="New Drone", command=self.connect_drone, width=20).pack(pady=5)
        tk.Button(root, text="Fly", command=self.launch_rotation_hub, width=20).pack(pady=5)
        tk.Button(root, text="Help", command=self.show_help, width=20).pack(pady=5)
        tk.Button(root, text="Quit", command=self.quit_program, width=20).pack(pady=20)

        self.drone_connected = False
        self.rotation_hub_process = None

    def connect_drone(self):
        # Simulated connection test or setup
        try:
            import djitellopy
            self.drone_connected = True
            messagebox.showinfo("Connection", "Tello Drone connected successfully!")
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Could not connect to the drone.\n{e}")

    def launch_rotation_hub(self):
        if not self.drone_connected:
            messagebox.showwarning("Drone Not Connected", "Please connect to the drone first using 'New Drone'.")
            return

        try:
            # Launch Rotation_Hub as a new subprocess so it has its own window
            subprocess.Popen([sys.executable, "LivePhaseRotationWorking.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch drone controller.\n{e}")

    def show_help(self):
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
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
