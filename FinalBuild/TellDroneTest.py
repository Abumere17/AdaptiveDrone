"""
    Himadri Saha
    TelloDroneTest.py

    Class to mock DJI drone during development and testing 
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import time
import threading
import cv2
import mediapipe as mp
import numpy as np
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
from djitellopy import tello
from flight_commands import start_flying, stop_flying
from indicators import Indicators

class TestTello:
    """Mock Tello drone class for testing without an actual drone."""
    def __init__(self):
        print("TestTello: Initialized as a mock drone.")
        self.is_flying = False
        self.speed = 50
        self.shutdown = False  # New flag to track emergency shutdown

    def connect(self):
        if not self.shutdown:
            print("TestTello: Simulating connection.")

    def streamon(self):
        if not self.shutdown:
            print("TestTello: Simulating video stream activation.")

    def takeoff(self):
        if not self.shutdown:
            self.is_flying = True
            print("TestTello: Simulating takeoff.")

    def land(self):
        if not self.shutdown:
            self.is_flying = False
            print("TestTello: Simulating landing.")

    def emergency(self):
        """Simulates an emergency shutdown."""
        print("TestTello: Simulating emergency shutdown.")
        self.shutdown = True  # Set shutdown flag
        self.is_flying = False

    def end(self):
        """Simulates ending connection."""
        print("TestTello: Simulating ending connection.")
        self.shutdown = True  # Ensure shutdown occurs

    def get_frame_read(self):
        """Simulates retrieving a video frame."""
        return self
    
    @property
    def frame(self):
        """Returns a blank image for the simulated drone stream."""
        return np.zeros((480, 720, 3), dtype=np.uint8) if not self.shutdown else None

    def get_battery(self):
        """Simulates getting battery level."""
        if not self.shutdown:
            print("TestTello: Simulating battery level retrieval.")
            return 100  # Return a mock battery level
        else:
            return None 

    def send_rc_control(self, left_right, forward_backward, up_down, yaw):
        """Simulates sending RC control commands."""
        if not self.shutdown:
            print(f"TestTello: Simulating RC Control: LR={left_right}, FB={forward_backward}, UD={up_down}, Yaw={yaw}")
