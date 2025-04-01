import pandas as pd
import threading
from datetime import datetime
import time

class IRSensor:
    def __init__(self, csv_file, controller):
        self.csv_file = csv_file
        self.data = self.load_csv_data()
        self.vehicle_present = False
        self.stop_event = threading.Event()
        if controller is None:
            raise ValueError("Controller cannot be None")
        self.controller = controller


# Load CSV data into a pandas df. The CSV should have 'timestamp' and 'ir_value' columns.
    def load_csv_data(self):
        try:
            df = pd.read_csv(self.csv_file, parse_dates=['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None

# Get the current system time rounded to the nearest 30 minute interval.
    def get_system_time(self):
        current_time = datetime.now()
        # hardcoded the date to 2025, 3, 11
        hardcoded_time = datetime(2025, 3, 11, current_time.hour, current_time.minute, current_time.second)
        return current_time.replace(minute=(hardcoded_time.minute // 30) * 30, second=0, microsecond=0)

# Check the df for the current 30 minute interval and update the state.
    def update_state(self):
        if self.data is None:
            print("No data available for current time.")
            return

        current_time = self.get_system_time()
        cuurent_ir_val = self.data[self.data['timestamp'] == current_time]

        if not cuurent_ir_val.empty:
            ir_value = cuurent_ir_val['ir_value'].values[0]
            vehicle_present = ir_value >= 0.7
            print(f"[{current_time}] IR Value: {ir_value}, Vehicle Present: {vehicle_present}")
            if vehicle_present != self.vehicle_present:
                self.vehicle_present = vehicle_present
                self.controller.handle_sensor_state_change(vehicle_present)  # Trigger the controller action
        else:
            print(f"[{current_time}] No ir sensor data found for this time slot.")

# Continuously check sensor data at 30 minute intervals in a separate thread, to not block main thread
    def start_monitoring(self):
        print("Starting IR Sensor monitoring...")
        while not self.stop_event.is_set():
            self.update_state()
            self.stop_event.wait(20)  # Sleep for 30 minutes, changed to 20 sec for test purposes 

# Start monitoring in a new thread
    def run_in_thread(self):
        self.thread = threading.Thread(target=self.start_monitoring, daemon=True)
        self.thread.start()

# Stop the monitoring thread 
    def stop_monitoring(self):
        self.stop_event.set()
        self.thread.join()
