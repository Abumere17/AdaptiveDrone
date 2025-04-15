import tkinter as tk
from tkinter import messagebox

# Mock functions to replace actual drone control commands
def takeoff():
    messagebox.showinfo("Action", "Drone Takeoff")

def land():
    messagebox.showinfo("Action", "Drone Landing")

def move_forward():
    messagebox.showinfo("Action", "Moving Forward")

def move_back():
    messagebox.showinfo("Action", "Moving Back")

def move_left():
    messagebox.showinfo("Action", "Moving Left")

def move_right():
    messagebox.showinfo("Action", "Moving Right")

def rotate_cw():
    messagebox.showinfo("Action", "Rotating Clockwise")

def rotate_ccw():
    messagebox.showinfo("Action", "Rotating Counter-Clockwise")

# Create the main window
root = tk.Tk()
root.title("DJI Tello Drone Control")
root.geometry("300x400")

# Create buttons for each action
tk.Label(root, text="Battery: 100% (Mock)").pack(pady=10)

tk.Button(root, text="Takeoff", command=takeoff).pack(pady=5)
tk.Button(root, text="Land", command=land).pack(pady=5)
tk.Button(root, text="Move Forward", command=move_forward).pack(pady=5)
tk.Button(root, text="Move Back", command=move_back).pack(pady=5)
tk.Button(root, text="Move Left", command=move_left).pack(pady=5)
tk.Button(root, text="Move Right", command=move_right).pack(pady=5)
tk.Button(root, text="Rotate Clockwise", command=rotate_cw).pack(pady=5)
tk.Button(root, text="Rotate Counter-Clockwise", command=rotate_ccw).pack(pady=5)

# Run the GUI loop
root.mainloop()
