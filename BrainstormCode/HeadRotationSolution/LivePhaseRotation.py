"""
    Himadri Saha
    LivePhaseRotation.py

    Adapted from:
    https://github.com/niconielsen32/ComputerVision/blob/37b279fa44e28fe3ea859bc8f14f5353a6b93e54/headPoseEstimation.py#L4

    Main changes:
    - Class refactoring
    - Head tilt tracking
    - Drone command implementation

    Brainstroming code that uses Live face rotation to send commands to drone as the control hub
    Press "Esc" to close

    Idea to control drone using head roation AND face expression:
    Look up: Fly up
    Look down: Fly down
    Look left: Rotate Left
    Look right: Rotate right
    Tilt head left: Take photo*
    Tilt head right: Take video*
    Expression 1: Forward*
    Expression 2: Backward*

    Head tilt brainstorm:
    - Create a horizontal line from the chin
    - Calculate the distance between the line and each ear
    - Get diffrence of each distance
    - If diffrence is abvove / below thresholds, trigger corresponding tilt

    TODO:
    - Track tilt head (Himadri - A)
    - Implement face expression (Abu - B)
    - Implement drone control code (Dan - C)
    - Create signal strength warrnings (Tejas - D)

"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import cv2
import mediapipe as mp
import numpy as np
import time

class Rotation_Hub:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.cap = cv2.VideoCapture(0)
        self.droneControler = droneControler

    def start_rotation(self):
        # Main camera loop
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                break
            
            # Adjust image and overlay face mesh
            start = time.time()
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.face_mesh.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract 3D landmarks
            img_h, img_w, img_c = image.shape
            face_3d = []
            face_2d = []

            # Select Key landmarks and in 3D and 2D
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                        if idx in [33, 263, 1, 61, 291, 199]: # Key landmarks
                            if idx == 1:
                                nose_2d = (lm.x * img_w, lm.y * img_h)
                                nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                            x, y = int(lm.x * img_w), int(lm.y * img_h)
                            face_2d.append([x, y])
                            face_3d.append([x, y, lm.z])
                    

                    face_2d = np.array(face_2d, dtype=np.float64)
                    face_3d = np.array(face_3d, dtype=np.float64)

                    focal_length = 1 * img_w
                    cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                           [0, focal_length, img_w / 2],
                                           [0, 0, 1]])
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)
                    
                    # Use solvePnP to estimate head pose reletaive to camera
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                    rmat, jac = cv2.Rodrigues(rot_vec)
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360

                    # Classify pose (Adjust for clinet) and add more controls
                    if y < -10:
                        text = "Looking Left"
                    elif y > 10:
                        text = "Looking Right"
                    elif x < -10:
                        text = "Looking Down"
                    elif x > 10:
                        text = "Looking Up"
                    else:
                        text = "Forward"

                    # Project pointer and create image
                    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
                    p1 = (int(nose_2d[0]), int(nose_2d[1]))
                    p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))
                    
                    cv2.line(image, p1, p2, (255, 0, 0), 3)
                    cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    cv2.putText(image, "x: " + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image, "y: " + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    end = time.time()
                    totalTime = end - start
                    fps = 1 / totalTime if totalTime > 0 else 0

                    cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
                    self.mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=self.drawing_spec,
                        connection_drawing_spec=self.drawing_spec)

            cv2.imshow('Head Pose Estimation', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def takeoff_land(self):
        pass

    def video_stream(self):
        pass

    def cleanup(self):
        pass

if __name__ == "__main__":
    rotation_hub = Rotation_Hub()
    rotation_hub.start_rotation()
