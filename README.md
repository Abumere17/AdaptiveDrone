
# **Adaptive Drone Codebase**

Adaptive Drone is an assistive drone controller application designed to enable users with quadriplegia to pilot a DJI Tello drone using head movements. Built in Python, the application uses MediaPipe for facial mesh tracking and the Tello SDK for drone communication.

---

## Features
- **Head Pose Rotation Control**: Real-time pitch/yaw detection to adjust drone movement.
- **Keyboard Override Support**: Developers can manually control the drone with `WASD`, `Shift`, and `Space`.
- **Live FPV Feed**: View the drone's camera feed in the app window.

---

## Setup Instructions
1. **Prerequisites:**
- Python 3.9 or higher
- Install dependencies with: pip install -r requirements.txt

## Developer Tips
- **Modifying Drone Commands**: Head to ControlHub.py, and find the gesture mapping logic in the main loop.
- **Testing Without a Drone**: Use tello_mock_gui.py to simulate drone responses if you don’t have hardware connected.
- **Facial Threshold Calibration**: This happens at the start — you can modify how expressions are detected by editing the calibration logic.
- **Visual Overlays**: Customize indicators.py if you want to change how UI elements are displayed on the drone feed.

---

## Facial Gesture Mapping
**Gesture         Command**
Nod Up	        Fly Forward
Fully Up	    Fly Up
Nod Down	    Fly Backward
Fully Down	    Fly Down
Nod Right	    Take Photo
Fully Right	    Rotate Right
Fully Left	    Rotate Left

---

## Contributors
Himadri Saha - Face pose dectetion devlopment 
Daniel Diep - Drone controller devloper
Tejas Patil - Drone controller and communication integration
Abumere Okhihan - GUI and app architecture devlopment 

---

## Contact
Contact Himadri_Saha@student.uml.edu for support