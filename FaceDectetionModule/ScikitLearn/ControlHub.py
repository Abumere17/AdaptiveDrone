"""
    Himadri Saha
    ControlHub.py

    This is the class to run the live phase of the app. It takes user face experssions and flys the drone. 

    params: (drone)

    Adapted from:
    https://github.com/computervisioneng/emotion-recognition-python-scikit-learn-mediapipe/tree/main

    Functions:
    - start control hub
    - predcit users face and output character (with confindence)
    - decide what output character does and fly drone

    TODO:
    - 

"""
# Imports
import pickle
import cv2
from utils import get_face_landmarks

# Vars

class Control_Hub:
    def __init__(self):
        pass

    def start_hub(drone=None):
        print("Openning control hub...")
        if drone == None:
            print("No drone connected!")
        else:
            print("Drone connected")

    def predict_face():
        pass

    def send_command():
        pass

# Test class
if __name__ == "__main__":
    screen = Control_Hub()
    screen.start_hub()