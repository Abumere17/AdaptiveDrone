import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import time
import threading
import cv2
import mediapipe as mp
import numpy as np
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
from djitellopy import tello
from TelloControlModule.flight_commands import start_flying, stop_flying
from TelloControlModule.indicators import Indicators


class Rotation_Hub:
    def __init__(self):
        # Initialize MediaPipe face mesh
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        # Initialize webcam capture
        self.cap = cv2.VideoCapture(0)

        # Initialize Tello drone controller and video stream
        self.drone_controller = tello.Tello()
        self.drone_controller.connect()
        self.drone_controller.streamon()
        self.drone_controller.speed = 50

        # Set dimensions for display
        self.h = 480
        self.w = 720

        # Initialize Tkinter window and layout
        self.root = Tk()
        self.root.title("Rotation Hub")

        self.video_frame = Frame(self.root)
        self.video_frame.pack()

        # Label for head pose (webcam) stream
        self.head_pose_lbl = Label(self.video_frame)
        self.head_pose_lbl.pack(side="left", padx=10, pady=10)

        # Label for Tello video stream
        self.drone_stream_lbl = Label(self.video_frame)
        self.drone_stream_lbl.pack(side="right", padx=10, pady=10)

        # Control frame for buttons
        self.control_frame = Frame(self.root)
        self.control_frame.pack(pady=10)

        # Button to toggle takeoff/land
        self.takeoff_land_btn = Button(
            self.control_frame,
            text="Takeoff/Land",
            command=self.takeoff_land
        )
        self.takeoff_land_btn.pack(side="left", padx=5)

        # Button for kill switch to immediately shutdown the drone and exit
        self.kill_switch_btn = Button(
            self.control_frame,
            text="Kill Switch",
            command=self.kill_switch,
            fg="white",
            bg="red"
        )
        self.kill_switch_btn.pack(side="left", padx=5)

        self.indicators = Indicators(self.drone_controller, self.w, self.h)

        # Variables for throttling RC commands
        self.last_command = "neutral"
        self.last_rc_time = time.time()
        self.rc_interval = 0.2  # Minimum interval in seconds between commands

    def update_head_pose(self):
        """Capture webcam frames, process head pose, and update the Tkinter label."""
        success, image = self.cap.read()
        if not success:
            self.root.after(10, self.update_head_pose)
            return

        # Flip the image for mirror effect and process colors
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, _ = image.shape
        face_3d = []
        face_2d = []
        text = "Neutral - No Movement"
        nose_2d = (0, 0)
        nose_3d = (0, 0, 0)
        new_command = "neutral"

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx in [33, 263, 1, 61, 291, 199]:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                        x_coord, y_coord = int(lm.x * img_w), int(lm.y * img_h)
                        face_2d.append([x_coord, y_coord])
                        face_3d.append([x_coord, y_coord, lm.z])
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                focal_length = img_w
                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])
                dist_matrix = np.zeros((4, 1), dtype=np.float64)
                success_pnp, rot_vec, trans_vec = cv2.solvePnP(
                    face_3d, face_2d, cam_matrix, dist_matrix
                )
                rmat, _ = cv2.Rodrigues(rot_vec)
                angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

                # Calculate head rotation angles (in degrees)
                pitch = angles[0] * 360
                yaw = angles[1] * 360
                roll = angles[2] * 360

                # Determine the new command based on head pose angles
                if yaw < -12:
                    new_command = "yaw_left"
                    text = "Looking Left"
                elif yaw > 12:
                    new_command = "yaw_right"
                    text = "Looking Right"
                elif pitch < -12:
                    new_command = "downward"
                    text = "Looking Down"
                elif pitch > 12:
                    new_command = "upward"
                    text = "Looking Up"
                else:
                    new_command = "neutral"
                    text = "Neutral - No Movement"

                # Throttle RC commands: only send if command changed and interval elapsed
                current_time = time.time()
                if (new_command != self.last_command and 
                        (current_time - self.last_rc_time) >= self.rc_interval):
                    try:
                        if new_command == "neutral":
                            stop_flying(None, self.drone_controller)
                        else:
                            start_flying(None, new_command, self.drone_controller,
                                         self.drone_controller.speed)
                        self.last_command = new_command
                        self.last_rc_time = current_time
                    except Exception as e:
                        print("Error sending RC command:", e)

                # Visual pointer for head pose
                nose_3d_projection, _ = cv2.projectPoints(
                    nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix
                )
                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + yaw * 10), int(nose_2d[1] - pitch * 10))
                cv2.line(image, p1, p2, (255, 0, 0), 3)
                cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 255, 0), 2)
                cv2.putText(image, f'Pitch: {np.round(pitch, 2)}', (500, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, f'Yaw: {np.round(yaw, 2)}', (500, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, f'Roll: {np.round(roll, 2)}', (500, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                break  # Process only the first detected face

        # Convert the processed frame for Tkinter display
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(image_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        self.head_pose_lbl.imgtk = imgtk
        self.head_pose_lbl.configure(image=imgtk)
        self.root.after(10, self.update_head_pose)

    def takeoff_land(self):
        # Toggle the drone's takeoff/land state in a separate thread
        if self.drone_controller.is_flying:
            threading.Thread(target=lambda: self.drone_controller.land()).start()
        else:
            threading.Thread(target=lambda: self.drone_controller.takeoff()).start()

    def update_drone_stream(self):
        """Capture from the Tello video stream and update the Tkinter label."""
        frame = self.drone_controller.get_frame_read().frame
        frame = cv2.resize(frame, (self.w, self.h))
        self.indicators.draw_battery_indicator(frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        self.drone_stream_lbl.imgtk = imgtk
        self.drone_stream_lbl.configure(image=imgtk)
        self.root.after(10, self.update_drone_stream)

    def kill_switch(self):
        """
        Immediately send an emergency shutdown to the drone and exit the program.
        """
        try:
            # Send emergency command to shut off the drone
            threading.Thread(target=lambda: self.drone_controller.emergency()).start()
            # Allow time for the command to be sent
            time.sleep(1)
        except Exception as e:
            print("Error during kill switch:", e)
        finally:
            self.cleanup()
            self.root.destroy()
            exit(0)

    def run(self):
        """Start updating both video streams and run the Tkinter main loop."""
        self.update_head_pose()
        self.update_drone_stream()
        self.root.mainloop()

    def cleanup(self):
        try:
            self.cap.release()
            cv2.destroyAllWindows()
            self.drone_controller.end()
            self.root.quit()
        except Exception as e:
            print(f"Error during cleanup: {e}")


if __name__ == "__main__":
    rotation_hub = Rotation_Hub()
    rotation_hub.run()
