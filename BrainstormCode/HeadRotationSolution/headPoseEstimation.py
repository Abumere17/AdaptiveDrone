"""
    headPoseEstimation.py

    Added:
    - Head tilt detection (existing)
    - Quick nod detection for left, right, up, and down.
      The operator only needs to have their head angle within the candidate range 
      (defined by NOD_THRESHOLD_MIN and NOD_THRESHOLD_MAX) to output the nod direction.
    - Visual gauges are drawn to help the user see the candidate zones.
"""

import cv2
import mediapipe as mp
import numpy as np
import time

# Constants
TILT_THRESHOLD = 30         # Pixel threshold for head tilt detection
NOD_THRESHOLD_MIN = 5       # Minimum angle (in degrees) for nod candidate
NOD_THRESHOLD_MAX = 10      # Maximum angle (in degrees) for nod candidate
SCALE = 10                  # Pixels per degree for visual gauges

def get_nod_candidate(x_angle, y_angle):
    """
    Return a string indicating the nod candidate direction if the head angle 
    is within the candidate range, otherwise return None.
    """
    candidate = None
    # Check yaw for left/right nods
    if -NOD_THRESHOLD_MAX < y_angle < -NOD_THRESHOLD_MIN:
        candidate = "Nod Left"
    elif NOD_THRESHOLD_MIN < y_angle < NOD_THRESHOLD_MAX:
        candidate = "Nod Right"
    # Check pitch for up/down nods
    elif NOD_THRESHOLD_MIN < x_angle < NOD_THRESHOLD_MAX:
        candidate = "Nod Up"
    elif -NOD_THRESHOLD_MAX < x_angle < -NOD_THRESHOLD_MIN:
        candidate = "Nod Down"
    return candidate

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

    # Flip image for selfie view and convert BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process with MediaPipe Face Mesh
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, _ = image.shape

    # Default texts for display
    head_pose_text = ""
    nod_text = ""

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Build dictionary of landmark coordinates
            landmarks_dict = {}
            for idx, lm in enumerate(face_landmarks.landmark):
                x, y = int(lm.x * img_w), int(lm.y * img_h)
                landmarks_dict[idx] = (x, y, lm.z)

            # Prepare arrays for head pose estimation using selected landmarks
            face_2d = []
            face_3d = []
            indices_for_pose = [33, 263, 1, 61, 291, 199]  # Example indices
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

            # Camera matrix and distortion coefficients
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

            # Decompose rotation matrix to get head angles (in degrees)
            rmat, _ = cv2.Rodrigues(rot_vec)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
            x_angle = angles[0] * 360  # Pitch (up/down)
            y_angle = angles[1] * 360  # Yaw (left/right)
            z_angle = angles[2] * 360  # Roll

            # Regular head orientation detection for continuous commands
            if y_angle < -10:
                head_pose_text = "Looking Left"
            elif y_angle > 10:
                head_pose_text = "Looking Right"
            elif x_angle < -10:
                head_pose_text = "Looking Down"
            elif x_angle > 10:
                head_pose_text = "Looking Up"
            else:
                head_pose_text = "Forward"

            # Draw the nose direction for visualization
            nose_3d_projection, _ = cv2.projectPoints(
                nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix
            )
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y_angle * 10), int(nose_2d[1] - x_angle * 10))
            cv2.line(image, p1, p2, (255, 0, 0), 3)

            # --- Head Tilt Detection (Existing) ---
            if 152 in landmarks_dict and 234 in landmarks_dict and 454 in landmarks_dict:
                chin_x, chin_y, _ = landmarks_dict[152]
                right_ear_x, right_ear_y, _ = landmarks_dict[234]
                left_ear_x, left_ear_y, _ = landmarks_dict[454]
                cv2.line(image, (0, chin_y), (img_w, chin_y), (0, 255, 255), 2)
                left_distance = abs(left_ear_y - chin_y)
                right_distance = abs(right_ear_y - chin_y)
                if (left_distance - right_distance) > TILT_THRESHOLD:
                    tilt_text = "Tilt Left"
                elif (right_distance - left_distance) > TILT_THRESHOLD:
                    tilt_text = "Tilt Right"
                else:
                    tilt_text = "No Tilt"
                cv2.putText(image, tilt_text, (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 2)

            # --- Immediate Nod Detection Based on Visual Gauge ---
            # Determine nod candidate from current head angles
            candidate = get_nod_candidate(x_angle, y_angle)
            if candidate is not None:
                nod_text = candidate
            else:
                nod_text = ""

            # Display the regular head pose text and nod result
            cv2.putText(image, head_pose_text, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            cv2.putText(image, "x: " + str(np.round(x_angle, 2)), (500, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "y: " + str(np.round(y_angle, 2)), (500, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "z: " + str(np.round(z_angle, 2)), (500, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if nod_text:
                cv2.putText(image, nod_text, (20, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

            # --- Draw Visual Gauges for Nodding Ranges ---
            # Horizontal gauge for yaw (left/right nod)
            gauge_width = int(NOD_THRESHOLD_MAX * SCALE * 2)
            gauge_height = 20
            gauge_center_x = img_w // 2
            gauge_y = img_h - 50
            # Background gauge
            cv2.rectangle(image, (gauge_center_x - gauge_width // 2, gauge_y),
                          (gauge_center_x + gauge_width // 2, gauge_y + gauge_height),
                          (50, 50, 50), -1)
            # Center line
            cv2.line(image, (gauge_center_x, gauge_y),
                     (gauge_center_x, gauge_y + gauge_height), (255, 255, 255), 2)
            # Candidate zone for Nod Right
            cv2.rectangle(
                image,
                (gauge_center_x + int(NOD_THRESHOLD_MIN * SCALE), gauge_y),
                (gauge_center_x + int(NOD_THRESHOLD_MAX * SCALE), gauge_y + gauge_height),
                (0, 255, 0), -1
            )
            # Candidate zone for Nod Left
            cv2.rectangle(
                image,
                (gauge_center_x - int(NOD_THRESHOLD_MAX * SCALE), gauge_y),
                (gauge_center_x - int(NOD_THRESHOLD_MIN * SCALE), gauge_y + gauge_height),
                (0, 255, 0), -1
            )
            # Current yaw marker
            current_offset = int(y_angle * SCALE)
            marker_x = gauge_center_x + current_offset
            cv2.circle(image, (marker_x, gauge_y + gauge_height // 2), 8, (0, 0, 255), -1)

            # Vertical gauge for pitch (up/down nod)
            gauge_height_pitch = int(NOD_THRESHOLD_MAX * SCALE * 2)
            gauge_width_pitch = 20
            gauge_center_y = img_h // 2
            gauge_x = 50
            # Background gauge
            cv2.rectangle(image, (gauge_x, gauge_center_y - gauge_height_pitch // 2),
                          (gauge_x + gauge_width_pitch, gauge_center_y + gauge_height_pitch // 2),
                          (50, 50, 50), -1)
            # Center line
            cv2.line(image, (gauge_x, gauge_center_y),
                     (gauge_x + gauge_width_pitch, gauge_center_y), (255, 255, 255), 2)
            # Candidate zone for Nod Up (looking up)
            cv2.rectangle(
                image,
                (gauge_x, gauge_center_y - int(NOD_THRESHOLD_MAX * SCALE)),
                (gauge_x + gauge_width_pitch, gauge_center_y - int(NOD_THRESHOLD_MIN * SCALE)),
                (0, 255, 0), -1
            )
            # Candidate zone for Nod Down
            cv2.rectangle(
                image,
                (gauge_x, gauge_center_y + int(NOD_THRESHOLD_MIN * SCALE)),
                (gauge_x + gauge_width_pitch, gauge_center_y + int(NOD_THRESHOLD_MAX * SCALE)),
                (0, 255, 0), -1
            )
            # Current pitch marker (note: higher pitch means up, so subtract offset)
            current_offset_pitch = int(x_angle * SCALE)
            marker_y = gauge_center_y - current_offset_pitch
            cv2.circle(image, (gauge_x + gauge_width_pitch // 2, marker_y), 8, (0, 0, 255), -1)

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
