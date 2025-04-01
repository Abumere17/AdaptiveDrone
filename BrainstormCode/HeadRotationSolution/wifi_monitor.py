import subprocess
import time
import threading

class WiFiMonitor:
    def __init__(self, update_interval=2):
        self.ssid = None
        self.signal_strength = None
        self.update_interval = update_interval
        self.running = False
        self.thread = None

    def get_wifi_info(self):
        """Retrieves Wi-Fi SSID and signal strength on Windows."""
        try:
            result = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
            ssid = None
            signal_strength = None

            for line in result.split("\n"):
                if "SSID" in line and "BSSID" not in line:  
                    ssid = line.split(":")[1].strip()
                if "Signal" in line:
                    signal_strength = int(line.split(":")[1].strip().replace("%", ""))

            return ssid, signal_strength
        except subprocess.CalledProcessError:
            return None, None  
        except Exception as e:
            print(f"Error retrieving Wi-Fi info: {e}")
            return None, None

    def evaluate_signal_strength(self, signal_strength):
        """Classifies the signal strength percentage."""
        if signal_strength is None:
            return "❌ Signal Disconnected"
        elif signal_strength > 95:
            return "✅ Excellent Signal"
        elif 90 <= signal_strength <= 95:
            return "Good Signal"
        elif 80 <= signal_strength < 90:
            return "⚠️ Weak Signal"
        else:
            return "❌ Very Weak Signal (Possible Disconnection)"

    def monitor_wifi(self):
        """Continuously monitors Wi-Fi status in a separate thread."""
        self.running = True
        while self.running:
            self.ssid, self.signal_strength = self.get_wifi_info()
            status = self.evaluate_signal_strength(self.signal_strength)
            print(f"Wi-Fi: {self.ssid if self.ssid else 'N/A'} | Signal: {self.signal_strength if self.signal_strength is not None else 'N/A'}% - {status}")
            time.sleep(self.update_interval)

    def start_monitoring(self):
        """Starts the monitoring thread."""
        if not self.running:
            self.thread = threading.Thread(target=self.monitor_wifi, daemon=True)
            self.thread.start()

    def stop_monitoring(self):
        """Stops the monitoring thread."""
        self.running = False

if __name__ == "__main__":
    wifiObject = WiFiMonitor()
    wifiObject.start_monitoring()

    try:
        while True:
            time.sleep(2)  # Keep the main thread running while WiFi monitoring runs in background
    except KeyboardInterrupt:
        print("\nStopping WiFi monitoring...")
        wifiObject.stop_monitoring()