"""
    Himadri Saha
    SetupPhase.py

    Runs the Setup phase to calibrate user faical expressions to trained model.
    On startup, all previous user data will be deleted
    User will iritrate through each control expresssion: 
    - an image will be captured to be stored in preloaded data starting with "User_"

    TODO:
    - smoothen out quit function
    - Confrim face expressions are good enough
    - UI: Finalize text

"""

# Imports
import pickle
import cv2
import os
from utils import get_face_landmarks

# Vars
output_dir = "FaceDectetionModule/Scikit-learn/UserSetupImg"
expressions = {
    "Open Mouth": "FaceDectetionModule\Scikit-learn\PreloadedData\BOpenMouth",
    "Teeth Smile": "FaceDectetionModule\Scikit-learn\PreloadedData\CTeethSmile",
    "Frown": "FaceDectetionModule\Scikit-learn\PreloadedData\DFrown",
    "Scrunch Mouth Right": "FaceDectetionModule\Scikit-learn\PreloadedData\EScrunchRight",
    "Scrunch Mouth Left": "FaceDectetionModule\Scikit-learn\PreloadedData\FScrunchLeft",
    "Puffed Right Cheek": "FaceDectetionModule\Scikit-learn\PreloadedData\GPuffedRightCheek",
    "Puffed Left Cheek": "FaceDectetionModule\Scikit-learn\PreloadedData\HPuffedLeftCheek",
    "Eyebrows Furrowed": "FaceDectetionModule\Scikit-learn\PreloadedData\IEyebrowsFurrowed",
    "Scrunch Mouth Full": "FaceDectetionModule\Scikit-learn\PreloadedData\JScrunchMouthFull",
    "Raised Eyebrows": "FaceDectetionModule\Scikit-learn\PreloadedData\KRaiseEyebrows"
}
i = 0
quitFlag = False

# Delete all user images
for i in range(len(expressions)):
    folder_path = list(expressions.values())[i]

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.startswith("User_"):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)  # Delete the file
            print(f"Deleted: {file_path}")
print("Cleared all past user data")


# Start video capture
i = 0
cap = cv2.VideoCapture(0)
for i in range(len(expressions)):
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Check that camera works
        if not ret:
            print("Error: Failed to capture image.")
            quitFlag = True
            break

        # Overlay gray box for prompts
        height, width, _ = frame.shape  
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, int(height * 0.12)), (50, 50, 50), -1) 
        alpha = 0.5  # Opacity level (0 = fully transparent, 1 = solid)
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        # Write prompt
        cv2.putText(frame, f"Please make the following expression: {list(expressions.keys())[i]}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, "Press 's' to save this expression.",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Check 's' and take photo
        if cv2.waitKey(1) & 0xFF == ord('s'):
            img_path = os.path.join(list(expressions.values())[i], f"User_{list(expressions.keys())[i]}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"Saved {list(expressions.keys())[i]} to {img_path}")
            break

        # Check 'q' and quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            quitFlag = True
            break

        # Display frame
        cv2.imshow("Calibration", frame)

        # Delay for frame smoothness
        cv2.waitKey(25)
    
    # Quit 
    if quitFlag == True:
        break

cap.release()
cv2.destroyAllWindows()