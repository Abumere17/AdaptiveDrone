"""
SetupPhase.py - Runs the Setup phase to calibrate user facial expressions.

Author: Himadri Saha

Updates:
- Removed the process of clearing user data on each run.

"""

# Imports
import cv2
import os

class SetupPhase:
    # Initialize SetupPhase with required variables
    def __init__(self):
        self.expressions = {
            "Open Mouth": "FaceDectetionModule/ScikitLearn/PreloadedData/BOpenMouth",
            "Teeth Smile": "FaceDectetionModule/ScikitLearn/PreloadedData/CTeethSmile",
            "Frown": "FaceDectetionModule/ScikitLearn/PreloadedData/DFrown",
            "Scrunch Mouth Right": "FaceDectetionModule/ScikitLearn/PreloadedData/EScrunchRight",
            "Scrunch Mouth Left": "FaceDectetionModule/ScikitLearn/PreloadedData/FScrunchLeft",
            "Puffed Right Cheek": "FaceDectetionModule/ScikitLearn/PreloadedData/GPuffedRightCheek",
            "Puffed Left Cheek": "FaceDectetionModule/ScikitLearn/PreloadedData/HPuffedLeftCheek",
            "Eyebrows Furrowed": "FaceDectetionModule/ScikitLearn/PreloadedData/IEyebrowsFurrowed",
            "Scrunch Mouth Full": "FaceDectetionModule/ScikitLearn/PreloadedData/JScrunchMouthFull",
            "Raised Eyebrows": "FaceDectetionModule/ScikitLearn/PreloadedData/KRaiseEyebrows"
        }
        self.cap = cv2.VideoCapture(0)
        self.quit_flag = False

    def display_prompt(self, frame, expression):
        """Overlays a prompt on the video feed to guide the user."""
        height, width, _ = frame.shape
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, int(height * 0.12)), (50, 50, 50), -1)  # Dark overlay box
        alpha = 0.5
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        # Display prompt text
        cv2.putText(frame, f"Please make the following expression: {expression}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, "Press 's' to save this expression.",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return frame

    def capture_image(self, frame, expression):
        """Captures an image of the user's expression and saves it."""
        img_path = os.path.join(self.expressions[expression], f"User_{expression}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Saved {expression} to {img_path}")

    def run_calibration(self):
        """Runs the setup phase to calibrate user facial expressions."""
        for expression in self.expressions.keys():
            while True:
                ret, frame = self.cap.read()
                frame = cv2.flip(frame, 1)  # Mirror image

                if not ret:
                    print("Error: Failed to capture image.")
                    self.quit_flag = True
                    break

                # Display calibration prompt
                frame = self.display_prompt(frame, expression)

                # Show frame to user
                cv2.imshow("Calibration", frame)

                # Wait for user input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):  # Save image on 's' key press
                    self.capture_image(frame, expression)
                    break
                elif key == ord('q'):  # Quit calibration on 'q' key press
                    self.quit_flag = True
                    break

            if self.quit_flag:
                break

        self.cleanup()

    def cleanup(self):
        """Releases camera resources and closes OpenCV windows."""
        self.cap.release()
        cv2.destroyAllWindows()

# Test class
if __name__ == "__main__":
    setup = SetupPhase()
    setup.run_calibration()
