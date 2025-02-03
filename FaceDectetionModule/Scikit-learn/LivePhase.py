"""
    Himadri Saha
    FaceControlModule.py

    This is the main script for the module. It runs all other scripts and controls the user interface

    Adapted from:
    https://github.com/computervisioneng/emotion-recognition-python-scikit-learn-mediapipe/tree/main

    TODO:
    - Add setup phase, Live phase, and user text prompts
    - Get setup data into preloaded data
    - Consider having setup in a seprate script? The app might not need to recalibrate every single use, just when there is a "new user"

"""

# Imports
import pickle
import cv2
from utils import get_face_landmarks

# Vars
emotions = ['HAPPY', 'SAD', 'SURPRISED'] # Change for each catogory

# Load in NN model (fix path)
with open('./model', 'rb') as f:
    model = pickle.load(f)

# Run video capture feed (add setup phase, Live phase, and user text prompts)
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
while ret:
    # Set up phase - Prompt user to make face, press s to take photo, save photo in correspodning folder, and repeat for all expressions #


    # Live phase - #
    ret, frame = cap.read() # get next frame

    face_landmarks = get_face_landmarks(frame, draw=True, static_image_mode=False) # get face landparks

    output = model.predict([face_landmarks]) # predict using model

    # Display video and text here
    cv2.putText(frame,
                emotions[int(output[0])],
               (10, frame.shape[0] - 1),
               cv2.FONT_HERSHEY_SIMPLEX,
               3,
               (0, 255, 0),
               5)
    cv2.imshow('frame', frame) 

    cv2.waitKey(25) # delay next frame for smoothness


cap.release()
cv2.destroyAllWindows()