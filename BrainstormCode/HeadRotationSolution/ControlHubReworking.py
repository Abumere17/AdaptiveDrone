'''
    Himadri Saha
    ControlHubReworking.py
    
    Seprate file to rework ControlHub.py

    Controls:
    Look up: fly up
    look down: fly down
    look left: rotate left
    look right: rotate right
    nod up: forward
    nod down: backwards

    TODO:
    - add keyboard commands
    - Rework functions

    ex.
    class ControlHub:
        def __init__(self, TelloDrone, root_of_tk_window): # Initalizes class
            # Attempt drone connection    
        
        def start(self): # Runs when fly button is pushed
            # Initalize frames
            # indicators
            # control parameters
            # on screen buttons

        def update_drone_stream(self): # update FPV frame
            # Display drone FPV frame
            # Display indicators 
            # Control gauges
            # selfie cam
            self.update_selfie()
            
        def update_selfie(self): # draws the selife frame
            # draw selfie frame
            # Update frame variable
            self.selfie_frame = frame

        def main_control_loop(self): # Maybe acts as run?
            # Need to promote/adjust the location of the variables required to get results.multi_face_landmarks
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks: 
                    # display frames
                    self.update_drone_stream()
                    self.update_selfie()

                    # collect head pose info and send drone command
                    next_command = self.get_head_pose()
                    if next_command != last_command_sent:
                        last_command_sent = next_command
                        self.send_drone_command(next_command)

            # Face landmarks not decteted - cleanup after 5 sec
            else:
                print("No landmarks dectected")
                self.root.after(10, self.update_head_pose)

                # Close app if face not dectected for 5 sec
                if time.time() - self.last_detected_time > 5:
                    print("No face detected for 5 seconds. Landing the drone and exiting...")
                    self.drone_controller.land()
                    self.cleanup()
                    exit(0)
                
        def get_head_pose(self): # outputs the head pose based on current frame
            selfie_frame = self.selfie_frame
            # Do all the calculations ...
            # output command from drone
            return current_headpose
        
        def send_drone_command(self, current_headpose): # send drone command using facial landmarks
        
        def takeoff_land(self): 
        
        def killswitch(self): 

        def cleanup(self): # exit the code 

'''

# Imports
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import time
import threading
import cv2
import mediapipe as mp
import numpy as np
from tkinter import Tk, Label, Button, Frame, Toplevel
from PIL import Image, ImageTk
from djitellopy import tello
from FinalBuild.flight_commands import start_flying, stop_flying
from FinalBuild.indicators import Indicators
from TellDroneTest import TestTello
from FinalBuild.take_pictures import take_picture

# Constants
TILT_THRESHOLD = 30
NOD_THRESHOLD_MIN = 5
NOD_THRESHOLD_MAX = 10
SCALE = 10

class Control_Hub:
    def __init__(self, testTello = False, parent=None):
        """
            Runs when new drone button is pressed
        """
        self.parent = parent
        
        # Connect drone or testDrone
        if not testTello:
            self.drone_controller = tello.Tello()
            self.drone_controller.connect()
            self.drone_controller.streamon()
            self.drone_controller.speed = 50
            print("Tello drone successfully connected.")
        else:
            self.drone_controller = TestTello()

    def start(self):
        """
            Runs when fly is pressed in main menu
        """

        # Initialize webcam capture and MediaPipe face mesh
        self.cap = cv2.VideoCapture(0)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        # Flag to check that frames are ready to display
        self.frameReady = True
                
        # Initialize Tkinter window and layout
        self.root = Toplevel(self.parent)
        self.root.title("Control Hub")
        self.video_frame = Frame(self.root)
        self.video_frame.pack()
        self.h = 480
        self.w = 720

        # Initalize webcam stream
        self.head_pose_lbl = Label(self.video_frame)
        self.head_pose_lbl.pack(side="left", padx=10, pady=10)

        # Label for Tello video stream
        self.drone_stream_lbl = Label(self.video_frame)
        self.drone_stream_lbl.pack(side="right", padx=10, pady=10)

        # Initalize buttons
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

        # Initalize Indicator objects 
        self.indicators = Indicators(self.drone_controller, self.w, self.h)

        # Initalize variables for sending drone commands
        self.last_command = "neutral"
        self.last_rc_time = time.time()
        self.rc_interval = 0.2  # Minimum interval in seconds between commands

    def takeoff_land(self):
        # Toggle the drone's takeoff/land state in a separate thread
        if self.drone_controller.is_flying:
            threading.Thread(target=lambda: self.drone_controller.land()).start()
        else:
            threading.Thread(target=lambda: self.drone_controller.takeoff()).start()

    def kill_switch(self):
        """
        Immediately send an emergency shutdown to the drone and exit the program.
        """
        try:
            # Send emergency command to shut off the drone
            threading.Thread(target=lambda: self.drone_controller.emergency()).start()
            time.sleep(1)
        except Exception as e:
            print("Error during kill switch:", e)
        finally:
            self.cleanup()
            self.root.destroy()
            exit(0)

    def update_drone_stream(self):
        """Capture from the Tello video stream and update the Tkinter label."""
        # Get drone FPV
        frame = self.drone_controller.get_frame_read().frame
        frame = cv2.resize(frame, (self.w, self.h))

        # Draw indicators
        self.indicators.draw_battery_indicator(frame)
        self.indicators.draw_wifi_indicator(frame)

        # Format frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        self.drone_stream_lbl.imgtk = imgtk
        self.drone_stream_lbl.configure(image=imgtk)
        self.root.after(10, self.update_drone_stream)

    def get_head_pose(self, face_landmarks, img_h, img_w):
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

        return [x_angle, y_angle, landmarks_dict]

    def update_selfie(self):
        ''' Updates webcam display and outputs user landmark data for send_drone_command() '''
        ## Initalize values ##
        # Default texts for display, Timer for drone
        head_pose_text = ""
        nod_text = ""
        success, image = self.cap.read()
        start = time.time()

        # Flip image for selfie view and convert BGR to RGB, Collect landmarks from image
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        img_h, img_w, _ = image.shape

        # Start face pose loop
        if results.multi_face_landmarks:
            self.last_detected_time = time.time()  # Reset detection time if face is found

            for face_landmarks in results.multi_face_landmarks:
                ## Get head pose
                headPoseArray = self.get_head_pose(face_landmarks, img_h, img_w)
                y_angle = headPoseArray[1]
                x_angle = headPoseArray[2]
                landmarks_dict = headPoseArray[3]

                ## Send command
                head_pose_text, nod_text = self.send_drone_command(y_angle, x_angle, landmarks_dict, image, img_w)

                ## Draw frame
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

                # Draw the nose direction for visualization
                nose_3d_projection, _ = cv2.projectPoints(
                    nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix
                )
                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y_angle * 10), int(nose_2d[1] - x_angle * 10))
                cv2.line(image, p1, p2, (255, 0, 0), 3)

                #  Draw Visual Gauges for Nodding Ranges 
                gauge_width = int(NOD_THRESHOLD_MAX * SCALE * 2)
                gauge_height = 20
                gauge_center_x = img_w // 2
                gauge_y = img_h - 50

                # Background gauge, Center line, Candidate zone for Nod Right and left
                cv2.rectangle(image, (gauge_center_x - gauge_width // 2, gauge_y),
                            (gauge_center_x + gauge_width // 2, gauge_y + gauge_height),
                            (50, 50, 50), -1)
                # 
                cv2.line(image, (gauge_center_x, gauge_y),
                        (gauge_center_x, gauge_y + gauge_height), (255, 255, 255), 2)
                cv2.rectangle(
                    image,
                    (gauge_center_x + int(NOD_THRESHOLD_MIN * SCALE), gauge_y),
                    (gauge_center_x + int(NOD_THRESHOLD_MAX * SCALE), gauge_y + gauge_height),
                    (0, 255, 0), -1
                )
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

                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.drawing_spec
                )

                # Convert the processed frame for Tkinter display
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(image_rgb)
                imgtk = ImageTk.PhotoImage(image=img_pil)
                self.head_pose_lbl.imgtk = imgtk
                self.head_pose_lbl.configure(image=imgtk)
                self.root.after(10, self.update_head_pose)
        
        else:
            print("No landmarks dectected")
            self.root.after(10, self.update_head_pose)

            # Close app if face not dectected for 5 sec
            if time.time() - self.last_detected_time > 5:
                print("No face detected for 5 seconds. Landing the drone and exiting...")
                self.drone_controller.land()
                self.cleanup()
                exit(0)

    def send_drone_command(self, y_angle, x_angle, landmarks_dict, image, img_w):
        ''' Sends drone command based on head pose angles '''
        # Get Regular head orientation position
        if y_angle < -12:
            new_command = "yaw_left"
            head_pose_text = "Looking Left"
        elif y_angle > 12:
            new_command = "yaw_right"
            head_pose_text = "Looking Right"
        elif x_angle < -12:
            new_command = "downward"
            head_pose_text = "Looking Down"
        elif x_angle > 12:
            new_command = "upward"
            head_pose_text = "Looking Up"
        else:
            new_command = "neutral"
            head_pose_text = "Forward"

        # Head Tilt Detection
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

        # Immediate Nod Detection Based on Visual Gauge
        candidate = None
        if -NOD_THRESHOLD_MAX < y_angle < -NOD_THRESHOLD_MIN:
            candidate = "Nod Left"
        elif NOD_THRESHOLD_MIN < y_angle < NOD_THRESHOLD_MAX:
            candidate = "Nod Right"
        elif NOD_THRESHOLD_MIN < x_angle < NOD_THRESHOLD_MAX:
            candidate = "Nod Up"
        elif -NOD_THRESHOLD_MAX < x_angle < -NOD_THRESHOLD_MIN:
            candidate = "Nod Down"
        if candidate is not None:
            nod_text = candidate
            if nod_text == 'Nod Up':
                new_command = "forward"
            elif nod_text == 'Nod Down':
                new_command = "backward"
            elif nod_text == 'Nod Left':
                new_command = "neutral" # change
            elif nod_text == 'Nod Right':
                new_command = "take photo"
        else:
            nod_text = ""

        ## Send drone command: only send if command changed and interval elapsed ##
        current_time = time.time()
        if (new_command != self.last_command and 
                (current_time - self.last_rc_time) >= self.rc_interval):
            try:
                if new_command == "neutral":
                    stop_flying(None, self.drone_controller)
                elif new_command == "take photo":
                    print("Taking Photo.")
                    frame = self.drone_controller.get_frame_read().frame
                    take_picture(frame)
                else:
                    start_flying(None, new_command, self.drone_controller,
                                self.drone_controller.speed)
                self.last_command = new_command
                self.last_rc_time = current_time
            except Exception as e:
                print("Error sending RC command:", e)

        return head_pose_text, nod_text

    def run(self):
        """Start updating both video streams and run the Tkinter main loop."""
        self.start()
        self.update_head_pose()
        self.update_drone_stream()
        if self.frameReady == False:
            self.error_window()
            return
        else:
            self.root.mainloop()

    def cleanup(self):
        try:
            self.cap.release()
            cv2.destroyAllWindows()
            self.drone_controller.end()
            self.root.quit()
            self.indicators.shutdown()
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    testTello = False
    rotation_hub = Control_Hub(testTello)
    rotation_hub.run()
