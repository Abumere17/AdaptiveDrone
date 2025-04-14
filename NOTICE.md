# NOTICE

This application includes adapted or referenced code from the following open-source contributors and repositories. All rights and ownership of the original source code remain with their respective authors.

## 🧑‍💻 Project Contributors

1. **Abumere Okhihan**
   - **Role:** GUI Integration Developer , In-App Help System

2. **Himadri Saha**
   - **Role:** Drone Control System Developer (Flight Movement & Responsiveness)

3. **Tejas Patil**
   - **Role:** Documentation, In-App Help System, and User Guidance

4. **Daniel Diep**
   - **Role:** Drone Backward/Downward Movement Refinement and Safety Logic

---

## 🧠 Referenced Code & Open Source Libraries

1. **Jacob Pitsenberger**
   - **Used In:** `take_pictures.py`
   - **Source:** [Tello Video Stream + Picture Capture](https://github.com/Jacob-Pitsenberger/Tello-Flight-Routine-with-Video-Stream)
   - **Note:** Referenced for video streaming and frame capture with Tello drone.

2. **Charles Yuan**
   - **Used In:** `flight_commands.py`
   - **Source:** [Flydo – Tello Control](https://github.com/Chubbyman2/flydo)
   - **Note:** Referenced for drone movement commands and control structures.

3. **DJI Ryze Tello SDK**
   - **Used In:** `tello.py`, general drone control
   - **Source:** [Official Tello SDK](https://github.com/dji-sdk/Tello-Python)
   - **Note:** This project uses DJI’s official SDK to interface with the Tello drone.

4. **Nicolai Høirup Nielsen**
   - **Used In:** `headPoseEstimation.py`
   - **Source:** [Computer Vision – Head Pose](https://github.com/niconielsen32/ComputerVision/blob/master/headPoseEstimation.py)
   - **Note:** Referenced for MediaPipe facial landmark detection and head pose logic.

---

## 📦 Python Packages Used

The following Python libraries are used and distributed under their respective licenses:

- **mediapipe==0.10.9** – Facial landmark tracking  
- **opencv-python==4.9.0.80** – Video processing and webcam feed  
- **numpy==1.26.3** – Numerical processing  
- **scikit-learn==1.4.0** – Optional for model-based features  
- **djitellopy==2.5.0** – Python wrapper for controlling the DJI Tello drone

Please refer to the respective repositories and package licenses for more information.
