"""
    Himadri Saha
    LivePhase.py

    This acts as the main script for the module. It runs all other scripts and controls the user interface.

    Updated:
    - Uses predict_proba() to classify with confidence threshold.
    - If confidence is below threshold, classify as "A - Neutral".

"""

# Imports
import pickle
import cv2
import numpy as np
from utils import get_face_landmarks

# Vars
emotions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']  # Include "A" for Neutral
CONFIDENCE_THRESHOLD = 0.7  # Adjust this threshold as needed

# Load trained model
with open('FaceDectetionModule\ScikitLearn\model', 'rb') as f:
    model = pickle.load(f)

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Stop if no frame is read

    face_landmarks = get_face_landmarks(frame, draw=True, static_image_mode=False)
    
    if face_landmarks is None or len(face_landmarks) == 0:
        print("No face landmarks detected.")
        continue

    # Get prediction probabilities
    probabilities = model.predict_proba([face_landmarks])[0]  # Returns an array of probabilities
    max_prob = np.max(probabilities)  # Get highest probability
    predicted_index = np.argmax(probabilities)  # Get index of highest probability class

    # Check confidence threshold
    if max_prob < CONFIDENCE_THRESHOLD:
        output_label = 'A'  # Classify as Neutral if below threshold
    else:
        output_label = emotions[predicted_index]  # Otherwise, classify normally

    # Display prediction
    cv2.putText(frame,
                f"{output_label} ({max_prob:.2f})",  # Show confidence value too
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)
    
    cv2.imshow('frame', frame)

    # Exit on 'q' key press
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
