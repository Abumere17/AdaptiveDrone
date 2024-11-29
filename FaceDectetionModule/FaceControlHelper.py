"""
    FaceControlHelper.py 
    Himadri Saha
    Helper functions for Distance control main
    Includes helper functions to dectect each facial expression
    TODO: 
    - Address what theresholds should be tested for during a set up phase for the program
    - Test cases to make sure no expressions overlaps
"""

'''
    Only one exprssion will be checked in each group 

    A: Neutral Face - No command
    B: Open Mouth - Take Photo
    C: Teeth Smile - Up  
    D: Frown - Down 
    E: Scrunch Mouth Right - Rotate right 
    F: Scrunch Mouth Left - Rotate Left 
    G: Puffed Right Cheek - Fly right 
    H: Puffed Left Cheek - Fly left
    I: Eyebrows furrowed - Forwards
    J: Scrunch Mouth Full - Backwards 
    K: - Multipurpose
'''
from DroneFaceControlMain import *
from collections import defaultdict

# Initialize Relative Positions Dict to hold 
relative_positions = defaultdict(list)
for char in "ABCDEFGHIJK":
    relative_positions[char] = []

# Generalized Distance Calculator function for distance between 2 landmarks
def calculate_distance(landmark1, landmark2):
    '''
        Args:
            landmark1: (x, y) tuple of location 1
            landmark2: (x, y) tuple of location 2

        Return:
            (x, y) tuple of x and y distance between location 1 and 2
    '''
    x1, y1 = landmark1
    x2, y2 = landmark2
    return (x2 - x1, y2 - y1)

def get_relative_positions(relevant_landmarks_nums):
    '''
        - get position of the tip of the nose
        - iterate through each relevant_landmarks 
            - calculate distance from tip of nose
        - return 

        Args:
            List of landmark numbers (as show in the MideaPipe documentation) tuples
            ex. (94, 61, 100)
        
        Return: A list of tuples with all of the reltive distances of each relevant landmark
        
    '''
    # Get all face mesh landmarks
    landmarks = results.multi_face_landmarks[0].landmark
    
    # Get nose tip position
    nose_tip = landmarks[1]
    nose_tip_pos = (int(nose_tip.x * w), int(nose_tip.y * h))

    # Get Relevant Landmark positions 

    i = 0

    for i in len(relevant_landmarks_nums):
        i += 1
        relevant_landmark_pos = landmarks[relevant_landmarks_nums]
        relative_pos = calculate_distance(nose_tip_pos, relevant_landmark_pos)

    # Some loop to make sure all relevant_landmark_pos are got
        # Calculate distance of each relevant landmark from the current nose tip