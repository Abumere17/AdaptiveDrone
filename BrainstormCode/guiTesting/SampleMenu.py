import tkinter as tk

class SimpleMenu:
    def __init__(self, root):
        """Initialize the GUI menu."""
        self.root = root
        self.root.title("Simple GUI Menu")

        # Create a label to display the last button pressed
        self.label = tk.Label(root, text="Press a button", font=("Arial", 14))
        self.label.pack(pady=10)

        # Create buttons
        self.create_button("Button 1", "You pressed Button 1")
        self.create_button("Button 2", "You pressed Button 2")
        self.create_button("Button 3", "You pressed Button 3")
        self.create_button("Button 4", "You pressed Button 4")

        # Close button
        close_button = tk.Button(root, text="Close", command=root.quit, font=("Georgia", 12), bg="red", fg="white")
        close_button.pack(pady=10)

    def create_button(self, text, message):
        """Helper function to create a button."""
        button = tk.Button(self.root, text=text, font=("Georgia", 12), command=lambda: self.on_button_press(message))
        button.pack(pady=5)

        def on_button_press(self, message):
            """Handles button presses."""
            print(message)  # Output message in console
            self.label.config(text=message)  # Update label in GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMenu(root)
    root.mainloop()
