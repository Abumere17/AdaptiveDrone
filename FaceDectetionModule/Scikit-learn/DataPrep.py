"""
    DataPrep.py
    Himadri Saha
    
    This script itirates through all preloaded images and collects facial landmark positions. 
    Outputs as a .txt file, which will be used to train the NN
    
    Adapted from 
    https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbUo1WU5hUnpfM1NLbkluMVRsT0FfOEhtOUhIUXxBQ3Jtc0tuX0xobUJBX2JsSk44eEtOS3RzOHp5SkpzVzI5NDhFbW85RjdBQnhaNmkzb2xpX1ZoWDBoaVhvb284ZTJEaHB3TlBCNXpnMVhKUkp1VHpCX0R3cGxjT3dDTTJicDUzRW9zb2VtUlU5OENfcXZJcjdjTQ&q=https%3A%2F%2Fgithub.com%2Fcomputervisioneng%2Femotion-recognition-python-scikit-learn-mediapipe&v=h0LoewzGzhc

    SO FAR:
    - Got a .txt file to be outputted in ./SetupData
    - Deletes any exisitng file for clarity

    TODO:
    - See if the SetupData.txt file is even valid
    
"""

# Imports
import os
import cv2
import numpy as np
from utils import get_face_landmarks

# Vars and define preloaded data directory (fix)
data_dir = 'FaceDectetionModule\Scikit-learn\PreloadedData'
output = []
output_dir = 'FaceDectetionModule\Scikit-learn\SetupData'
output_file = os.path.join(output_dir, "SetupData.txt")

# Check output_dir exists
os.makedirs(output_dir, exist_ok=True)

# Ititrate through each folder in preloaded data and collect landmarks (fix)
for emotion_indx, emotion in enumerate(sorted(os.listdir(data_dir))):
    for image_path_ in os.listdir(os.path.join(data_dir, emotion)):
        image_path = os.path.join(data_dir, emotion, image_path_)

        image = cv2.imread(image_path)

        face_landmarks = get_face_landmarks(image)

        if len(face_landmarks) == 1404:
            face_landmarks.append(int(emotion_indx))
            output.append(face_landmarks)

# Save in a .txt file, delete if the file exists
if os.path.exists(output_file):
    os.remove(output_file)

np.savetxt(output_file, np.asarray(output))