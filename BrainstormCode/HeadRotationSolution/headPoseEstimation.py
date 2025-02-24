"""
    headPoseEstimation.py
"""
import cv2
import mediapipe as mp
import numpy as np
import time

# Constants
TILT_THRESHOLD = 30  # Pixel threshold for head tilt detection

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    start = time.time()

    # Flip the image horizontally for a selfie-view display and convert BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image with MediaPipe Face Mesh
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, _ = image.shape

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Build a dictionary of all landmark coordinates (x, y, z)
            landmarks_dict = {}
            for idx, lm in enumerate(face_landmarks.landmark):
                x, y = int(lm.x * img_w), int(lm.y * img_h)
                landmarks_dict[idx] = (x, y, lm.z)

            # Prepare arrays for head pose estimation using selected landmarks
            face_2d = []
            face_3d = []
            # Indices used for pose estimation (example: eyes, nose, mouth landmarks)
            indices_for_pose = [33, 263, 1, 61, 291, 199]
            for i in indices_for_pose:
                if i in landmarks_dict:
                    x, y, z = landmarks_dict[i]
                    face_2d.append([x, y])
                    face_3d.append([x, y, z])
                    if i == 1:
                        nose_2d = (x, y)
                        nose_3d = (x, y, z * 3000)

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            # Define the camera matrix
            focal_length = img_w
            cam_matrix = np.array([
                [focal_length, 0, img_w / 2],
                [0, focal_length, img_h / 2],
                [0, 0, 1]
            ])

            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Solve PnP to estimate head pose
            success_pnp, rot_vec, trans_vec = cv2.solvePnP(
                face_3d, face_2d, cam_matrix, dist_matrix
            )

            # Get rotation matrix and decompose it to get angles
            rmat, _ = cv2.Rodrigues(rot_vec)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
            x_angle = angles[0] * 360
            y_angle = angles[1] * 360
            z_angle = angles[2] * 360

            # Determine head orientation based on angles
            if y_angle < -10:
                text = "Looking Left"
            elif y_angle > 10:
                text = "Looking Right"
            elif x_angle < -10:
                text = "Looking Down"
            elif x_angle > 10:
                text = "Looking Up"
            else:
                text = "Forward"

            # Draw the nose direction
            nose_3d_projection, _ = cv2.projectPoints(
                nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix
            )
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y_angle * 10), int(nose_2d[1] - x_angle * 10))
            cv2.line(image, p1, p2, (255, 0, 0), 3)

            # Display head orientation info on the image
            cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 255, 0), 2)
            cv2.putText(image, "x: " + str(np.round(x_angle, 2)),
                        (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "y: " + str(np.round(y_angle, 2)),
                        (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "z: " + str(np.round(z_angle, 2)),
                        (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # --- Head Tilt Detection ---
            # Check if required landmarks for chin and ears are available:
            # Chin: 152, Right Ear: 234, Left Ear: 454
            if 152 in landmarks_dict and 234 in landmarks_dict and 454 in landmarks_dict:
                chin_x, chin_y, _ = landmarks_dict[152]
                right_ear_x, right_ear_y, _ = landmarks_dict[234]
                left_ear_x, left_ear_y, _ = landmarks_dict[454]

                # Draw a horizontal line through the chin
                cv2.line(image, (0, chin_y), (img_w, chin_y), (0, 255, 255), 2)

                # Calculate the vertical distances from the chin line to each ear
                left_distance = abs(left_ear_y - chin_y)
                right_distance = abs(right_ear_y - chin_y)

                # Determine head tilt based on the difference between ear distances
                if (left_distance - right_distance) > TILT_THRESHOLD:
                    tilt_text = "Tilt Left"
                elif (right_distance - left_distance) > TILT_THRESHOLD:
                    tilt_text = "Tilt Right"
                else:
                    tilt_text = "No Tilt"

                cv2.putText(image, tilt_text, (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (255, 255, 0), 2)

            end = time.time()
            total_time = end - start
            fps = 1 / total_time if total_time > 0 else 0
            cv2.putText(image, f'FPS: {int(fps)}', (20, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

    cv2.imshow('Head Pose Estimation', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
