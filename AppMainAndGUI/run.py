"""
    Himadri Saha
    run.py

    This will act as the "main" script, integrating all modules into the app. Run this to start the app

    TODO:
    - 

"""
# Imports Dependicies
import sys
import os
import tkinter as tk

"""Import classes"""
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from TelloControlModule.TellControlMain import TelloControl
from FaceDectetionModule.ScikitLearn.SetupPhase import SetupPhase
from AppMainAndGUI.MainMenu import MainMenu

# Vars

# Main function
def main():
    # Get all modules as objects
    drone = TelloControl()
    setup = SetupPhase()
    root = tk.Tk()
    
    # Start main menu
    startMenu = MainMenu(root, drone, setup)
    root.mainloop()

# Run Main
if __name__ == "__main__":
    main()