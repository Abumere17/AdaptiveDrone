"""
    Himadri Saha
    SetupPhase.py

    Runs the Setup phase to calibrate user faical expressions to trained model. 
    User will iritrate through each control expresssion: 
    - an image will be captured to be stored in preloaded data
    OR 
    - the images will be stored in a seprate userData folder, data will be prepared on userData, and appended on to SetupData.txt

    TODO:
    - smoothen out quit function
    - catogorize saved images

"""

# Imports
import pickle
import cv2
import os
from utils import get_face_landmarks

# Vars
output_dir = "FaceDectetionModule/Scikit-learn/UserSetupImg"
expressions = [
    "Open Mouth",
    "Teeth Smile",
    "Frown",
    "Scrunch Mouth Right",
    "Scrunch Mouth Left",
    "Puffed Right Cheek",
    "Puffed Left Cheek",
    "Eyebrows Furrowed",
    "Scrunch Mouth Full"
]
i = 0
quitFlag = False

# Start video capture
cap = cv2.VideoCapture(0)
for i in range(len(expressions)):
    while True:
        ret, frame = cap.read()

        # Write prompt
        cv2.putText(frame, f"Please make the following expression: {expressions[i]}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Press 's' to save this expression.",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Check 's' and take photo
        if cv2.waitKey(1) & 0xFF == ord('s'):
            img_path = os.path.join(output_dir, f"{expressions[i]}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"Saved {expressions[i]} to {img_path}")
            break

        # Check 'q' and quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            quitFlag = True
            break

        # Display frame
        cv2.imshow("Calibration", frame)
    
    # Quit 
    if quitFlag == True:
        break

cap.release()
cv2.destroyAllWindows()