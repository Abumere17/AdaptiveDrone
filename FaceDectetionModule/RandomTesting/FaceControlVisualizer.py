import cv2
import mediapipe as mp
import numpy as np

# Helper functions
def calculate_displacement(base_landmarks, current_landmarks, reference_point):
    """Calculate displacement of landmarks relative to the reference point."""
    relative_base = [(x - reference_point[0], y - reference_point[1]) for x, y in base_landmarks]
    relative_current = [(x - reference_point[0], y - reference_point[1]) for x, y in current_landmarks]
    displacements = {
        idx: (current[0] - base[0], current[1] - base[1])
        for idx, (base, current) in enumerate(zip(relative_base, relative_current))
    }
    return displacements

def detect_expression(displacements, thresholds):
    """Determine the facial expression based on displacements."""
    # Example conditions for each expression; adjust thresholds as needed
    if abs(displacements[61][0]) < thresholds["neutral"] and abs(displacements[61][1]) < thresholds["neutral"]:
        return "A"  # Neutral Face
    elif displacements[13][1] > thresholds["open_mouth"]:
        return "B"  # Open Mouth
    elif abs(displacements[291][0]) > thresholds["scrunch_mouth_right"]:
        return "E"  # Scrunch Mouth Right
    elif abs(displacements[61][0]) > thresholds["scrunch_mouth_left"]:
        return "F"  # Scrunch Mouth Left
    elif displacements[13][1] > thresholds["puffed_right_cheek"]:
        return "G"  # Puffed Right Cheek
    elif displacements[5][1] < -thresholds["eyebrows_furrowed"]:
        return "I"  # Eyebrows Furrowed
    return "A"

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Initialize variables for calibration and thresholds
base_landmarks = None
reference_point = None
thresholds = {
    "neutral": 5,                  # Threshold for neutral face
    "open_mouth": 15,              # Threshold for mouth opening
    "scrunch_mouth_right": 8,      # Threshold for scrunching mouth to the right
    "scrunch_mouth_left": 8,       # Threshold for scrunching mouth to the left
    "puffed_right_cheek": 10,      # Threshold for puffing right cheek
    "puffed_left_cheek": 10,       # Threshold for puffing left cheek
    "eyebrows_furrowed": 7,        # Threshold for furrowing eyebrows
    "teeth_smile": 10,             # Threshold for teeth smile
    "frown": 10,                   # Threshold for frowning
    "scrunch_mouth_full": 12       # Threshold for full scrunch
}

setup_phases = ["A: Neutral Face", "B: Open Mouth", "C: Teeth Smile", 
                "D: Frown", "E: Scrunch Mouth Right", "F: Scrunch Mouth Left",
                "G: Puffed Right Cheek", "H: Puffed Left Cheek",
                "I: Eyebrows Furrowed", "J: Scrunch Mouth Full"]

setup_data = {}
current_phase = 0

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a selfie view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to get face landmarks
    results = face_mesh.process(rgb_frame)
    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        # Get the landmarks of the first face
        landmarks = results.multi_face_landmarks[0].landmark
        landmark_coords = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        reference_point = landmark_coords[1]  # Use the nose tip as the reference point

        # Draw the face mesh
        for coord in landmark_coords:
            cv2.circle(frame, coord, 1, (0, 255, 0), -1)

        # Setup phase: Save baseline data for each expression
        if current_phase < len(setup_phases):
            cv2.putText(frame, f"Setup: {setup_phases[current_phase]}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Press 's' to save this expression.",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                # Save relative landmarks for the current expression
                relative_landmarks = [(x - reference_point[0], y - reference_point[1]) for x, y in landmark_coords]
                setup_data[setup_phases[current_phase][0]] = relative_landmarks
                print(f"Saved {setup_phases[current_phase]}")
                current_phase += 1
        else:
            # Live phase: Detect expressions based on movements
            cv2.putText(frame, "Live Phase: Make a facial expression.",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Calculate relative landmarks from the nose***
            relative_landmarks = [(x - reference_point[0], y - reference_point[1]) for x, y in landmark_coords]

            # Calculate displacements***
            displacements = calculate_displacement(setup_data["A"], relative_landmarks, reference_point)

            # Detect expression
            expression = detect_expression(displacements, thresholds)
            cv2.putText(frame, f"Expression: {expression}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # Display the frame
    cv2.imshow("Face Mesh", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
