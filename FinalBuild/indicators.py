import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import cv2
import time
import threading
from wifi_monitor import WiFiMonitor

class Indicators:
    def __init__(self, drone, w, h):
        # Initialize a variable to start/stop indicator updates
        self.update = False

        # Initialize dimensions and drone object
        self.w = w
        self.h = h
        self.drone = drone

        # Initialize battery and Wi-Fi monitor
        self.battery = self.drone.get_battery()
        self.wifi_monitor = WiFiMonitor()
        self.wifi_monitor.start_monitoring()
        self.signal_strength = 0  # Default signal strength

        # Start update thread
        self.update_thread = threading.Thread(target=self.update_indicators)
        self.update_thread.start()

    def update_indicators(self) -> None:
        """Continuously update battery level and Wi-Fi signal strength."""
        self.update = True
        while self.update:
            self.battery = self.drone.get_battery()
            self.signal_strength = self.wifi_monitor.signal_strength or 0
            time.sleep(1)

    def shutdown(self) -> None:
        """Stops indicator updates and safely terminates threads."""
        self.update = False
        self.wifi_monitor.stop_monitoring()
        self.update_thread.join()
        print("Indicators: Shutdown complete.")

    def draw_battery_indicator(self, frame) -> None:
        """Draw battery indicator with percentage representation."""
        cv2.rectangle(frame, (10, 30), (60, 50), (255, 255, 255), -1)
        cv2.rectangle(frame, (60, 35), (65, 45), (255, 255, 255), -1)

        color = (0, 255, 0) if self.battery >= 70 else (0, 255, 255) if self.battery >= 40 else (0, 0, 255)
        battery_level = self.battery // 10

        for i in range(battery_level):
            cv2.line(frame, (15 + (i * 5), 32), (15 + (i * 5), 48), color, 2)

        cv2.putText(frame, f"{self.battery}%", (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def draw_wifi_indicator(self, frame) -> None:
        """Draw Wi-Fi signal strength indicator below the battery indicator."""
        x_start, y_start = 10, 90  # Position of Wi-Fi indicator
        bar_height = 5
        bar_width = 15
        max_bars = 5

        # Determine color based on signal strength
        if self.signal_strength >= 90:
            color = (0, 255, 0)
        elif self.signal_strength >= 70:
            color = (0, 255, 255)
        else:
            color = (0, 0, 255)

        # Draw Wi-Fi bars
        for i in range(max_bars):
            bar_y = y_start - (i * (bar_height + 2))
            if self.signal_strength >= (i + 1) * 20:
                cv2.rectangle(frame, (x_start, bar_y), (x_start + bar_width, bar_y + bar_height), color, -1)
            else:
                cv2.rectangle(frame, (x_start, bar_y), (x_start + bar_width, bar_y + bar_height), (255, 255, 255), 1)

        # Display signal strength percentage
        cv2.putText(frame, f"{self.signal_strength}%", (x_start + 25, y_start - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)