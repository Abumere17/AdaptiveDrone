'''
    TODO:
    - Set up cycle for live and set ip phase
    - Create a get_relative_distances function that outputs an array of distances of each landmark from the tip of the nose
        outputting an array of distnaces (or some other data struct)
    - Set threshold values for each expression
    - Implement comparsion algrothim
'''
import cv2
import mediapipe as mp
from collections import defaultdict
import math

## Helper functions
def get_relative_distances():
    # Change 
    return [1, 1]

## Vars
text_setup_phases = ["A: Neutral Face", "B: Open Mouth", "C: Teeth Smile", 
                "D: Frown", "E: Scrunch Mouth Right", "F: Scrunch Mouth Left",
                "G: Puffed Right Cheek", "H: Puffed Left Cheek",
                "I: Eyebrows Furrowed", "J: Scrunch Mouth Full"]
current_setup_phase = 0
# Initialize setup dict 
calibrated_data = {chr(letter): [] for letter in range(ord('A'), ord('K') + 1)}

# Initialize MediaPipe Face Mesh and video capture loop
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a selfie view and Process the frame to get face landmarks
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    h, w, _ = frame.shape

    # Frame by frame loop 
    if results.multi_face_landmarks:
        # Get landmarks of current face and draw the face mesh
        landmarks = results.multi_face_landmarks[0].landmark
        landmark_coords = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        reference_point = landmark_coords[1] # Gets the tip of the nose as the refrences point
        for coord in landmark_coords:
            cv2.circle(frame, coord, 1, (0, 255, 0), -1)

        ## Main loop contents for setup and Live phases
        if current_setup_phase < len(text_setup_phases): # Setup phase
            # Setup text prompt
            cv2.putText(frame, f"Setup: {text_setup_phases[current_setup_phase]}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Press 's' to save this expression.",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Wait for user to press S and save relative landmarks for the current expression
            if cv2.waitKey(1) & 0xFF == ord('s'):
                # get_relative_distances 
                # Save it the setup_data
                print(f"Saved {text_setup_phases[current_setup_phase]}")
                current_setup_phase += 1

        else: # Live Phase  
            pass

    # Display the frame and Exit on pressing 'q'
    cv2.imshow("Face Mesh", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()