"""
    @ computervisioneng
    LivePhase.py

    Script for decteting and predicting live face dectetion. Used to brainstorm FaceControlModule.py

    Adapted from: test_model.py
    https://github.com/computervisioneng/emotion-recognition-python-scikit-learn-mediapipe/blob/main/test_model.py
"""
# Imports
import pickle
import cv2
from utils import get_face_landmarks

# Change to match expressions
emotions = ['HAPPY', 'SAD', 'SURPRISED']

# Load in trained model (change path of trained model)
with open('./model', 'rb') as f:
    model = pickle.load(f)

# Main loop to predict live expressions
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
while ret:
    ret, frame = cap.read()

    # Capture live face expressions and predict face expression
    face_landmarks = get_face_landmarks(frame, draw=True, static_image_mode=False)
    output = model.predict([face_landmarks])

    # Display creted frame
    cv2.putText(frame,
                emotions[int(output[0])],
               (10, frame.shape[0] - 1),
               cv2.FONT_HERSHEY_SIMPLEX,
               3,
               (0, 255, 0),
               5)
    cv2.imshow('frame', frame)
    cv2.waitKey(25)

# Cleanup
cap.release()
cv2.destroyAllWindows()