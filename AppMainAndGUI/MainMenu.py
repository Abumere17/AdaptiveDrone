"""
    Himadri Saha
    MainMenu.py

    Class to a main menu 

    TODO:
    - Connect new drone
    - New user
    - 

"""
# Imports
import tkinter as tk

class MainMenu:
    # Initalize Menu
    def __init__(self, root, drone=None, setup=None): # should include all other objects for other modules
        self.root = root
        self.root.title("Adaptive Drone Project - 7 Hills")

        # Create the top prompt, buttons, and close button
        self.label = tk.Label(root, text="Press a button", font=("Georgia", 14)) # change
        self.label.pack(pady=10)

        self.create_button("New Drone", "You pressed Button 1")
        self.create_button("New User", "You pressed Button 2")
        self.create_button("Fly", "You pressed Button 3")
        self.create_button("Help", "You pressed Button 4")
        
        close_button = tk.Button(root, text="Quit", command=root.quit, font=("Georgia", 12), bg="red", fg="white")
        close_button.pack(pady=10)

    # Button functions
    # tx.button() - last param needs to be changed to the correspoding function
    def create_button(self, text, message):
        button = tk.Button(self.root, text=text, font=("Georgia", 12), command=lambda: self.on_button_press(message))
        button.pack(pady=5)

    def on_button_press(self, message):
        print(message)
        self.label.config(text=message)  # Update label in GUI

    # Connect new drone
    def connect_new_drone(self):
        pass

    # New user

    # Cleanup
    def close_menu(self):
        pass

    def quit_app(self):
        pass

# Test class here
if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()
