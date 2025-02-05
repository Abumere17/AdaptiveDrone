"""
    DroneFaceControllerChat.py
    Himadri Saha
    This is the main Face dectetion module that outputs the control symbol to the drone control module. 
    TODO: 
"""

# Libraries
import cv2
import mediapipe as mp
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score  # For evaluation (optional)
import numpy as np  # For numerical operations
import time  # For adding delays if needed

# -----------------------------------------
# Variables and Constants
# -----------------------------------------

# Camera settings
CAMERA_INDEX = 0  # Default camera
FRAME_WIDTH = 640  # Width of the video frame
FRAME_HEIGHT = 480  # Height of the video frame

# Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Placeholder for calibration data and labels
calibration_data = []  # List to store feature vectors
labels = []  # List to store expression labels (e.g., "Take Photo", "Fly Up")

# Placeholder for trained model
model = None  # Will hold the trained machine learning model

# Predefined expressions and their labels
predefined_expressions = {
    "neutral": "Neutral",
    "open_mouth": "Take Photo",
    "smile": "Fly Up",
    "frown": "Fly Down",
    "scrunch_mouth_right": "Rotate Right",
    "scrunch_mouth_left": "Rotate Left",
    "puff_right_cheek": "Fly Right",
    "puff_left_cheek": "Fly Left",
    "eyebrows_furrowed": "Move Forward",
    "scrunch_full_mouth": "Move Backward",
}

# Placeholder for live feature extraction
live_relative_distance = None  # To hold distances in live phase

# Threshold for expression detection (can be adjusted)
SIMILARITY_THRESHOLD = 0.1

# Flags and state variables
calibration_complete = False  # To track if calibration is done
live_detection_active = False  # To track if live detection is running


# Camera Feed
camera = cv2.VideoCapture(0)  # 0 is usually the default camera

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Press 'q' to quit the video feed.")

while True:
    # Capture a single frame
    ret, frame = camera.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame in a window
    cv2.imshow("Camera Feed", frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()

# -----------------------------------------
# Calibration Phase
# -----------------------------------------
def calibrate_expressions():
    """
    Guides the user through the calibration process to collect data
    for each predefined expression.
    """
    global calibration_data, labels

    print("Starting calibration...")

    for expression, label in predefined_expressions.items():
        print(f"Please perform the expression: {expression}")
        print("Press 's' to save the expression, or 'q' to quit calibration.")

        while True:
            # Capture frame from camera
            ret, frame = camera.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            frame = cv2.flip(frame, 1)
            
            # Detect facial landmarks
            results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Draw facial landmarks for visualization
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS
                    )

            # Display the frame with overlay
            cv2.imshow("Calibration - Perform Expression", frame)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):  # Save the expression
                if results.multi_face_landmarks:
                    # Extract features from the landmarks
                    features = extract_features(face_landmarks)
                    calibration_data.append(features)
                    labels.append(label)
                    print(f"Expression '{expression}' saved.")
                else:
                    print("No face detected. Please try again.")
                break
            elif key == ord('q'):  # Quit calibration
                print("Exiting calibration...")
                return

    print("Calibration complete.")

def extract_features(face_landmarks):
    """
    Extracts features (e.g., distances between landmarks) from detected facial landmarks.
    """
    key_points = [1, 33, 61, 199, 263, 291]  # Example landmark indices (adjust as needed)
    nose_tip = face_landmarks.landmark[1]  # Using nose tip as a reference point
    features = []

    for idx in key_points:
        point = face_landmarks.landmark[idx]
        distance = np.sqrt(
            (point.x - nose_tip.x) ** 2 + 
            (point.y - nose_tip.y) ** 2 + 
            (point.z - nose_tip.z) ** 2
        )
        features.append(distance)

    return features

if __name__ == "__main__":
    # Start with calibration phase
    calibrate_expressions()

    # Placeholder for next steps (e.g., training phase, live control phase)
    print("Proceeding to the next phase...")
