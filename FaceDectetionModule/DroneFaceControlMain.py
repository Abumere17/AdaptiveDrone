'''
    DroneFaceControlMain.py
    Himadri Saha
    Main loop for facial recognition module

    Logic flow:
    Set-up phase
        - Prompt user to make a facial expression
        - Save expression
            - Claculate distance of each node (or only relevant nodes) from from the tip of the nose
            - stored in a db by symbol: RelativePos['A']
    
    Live Phase
        - Calculate reletaive distances from tip of the nose
        - If the current RelativePos of all node are equal (or close to equal) to the RelativePos of a saved expression, than return that symbol
        - Else: Return neutral expression symbol
'''
import cv2
import mediapipe as mp
from FaceControlHelper import *

# Initialize MediaPipe Face Mesh loop
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
cap = cv2.VideoCapture(0)

# Loop per frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip frame for a selfie view and processing to get face landmarks
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    h, w, _ = frame.shape

    # Get the landmarks of the first face and Draw the face mesh
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark # Can be considred the live face mesh itself
        landmark_coords = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        reference_point = landmark_coords[1]  # Use the nose tip as the reference point
        for coord in landmark_coords:
            cv2.circle(frame, coord, 1, (0, 255, 0), -1)

        ## MAIN loop contents 
        setup_flag = True

        # Setup phase
        if setup_flag: 
            for char in "ABCDEFGHIJK":
                # Print text in the top right cornner and wait till user presses 's'
                cv2.putText(frame, "Press 's' to save this expression.",
                        (10, 60), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 255, 255), 1)
                if cv2.waitKey(1) & 0xFF == ord('s'): # TODO: Change Trigger to save expression
                    # relative_positions[expression] = relative_landmarks
                    relative_positions[char] = get_relative_positions()

            # setup_flag = False

        # Live Face Dectection Phase 
        # else: 

    # Display face mesh and exit on pressing 'q'
    cv2.imshow("Face Mesh", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()