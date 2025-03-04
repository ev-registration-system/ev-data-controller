from ir_sensor import IRSensor

class Controller:
    def __init__(self):
        self.sensor = None  # Initially set sensor to None
    
    def handle_sensor_state_change(self, vehicle_present):
        # Handle incoming/leaving car
        if vehicle_present:
            # Vehicle is present, allow check-in 
            print("Vehicle detected. User can check-in or proceed.")
        else:
            # Vehicle has left, notify security 
            print("No vehicle detected. Notifying security.")
        
    def start(self):
        print("[Controller] Starting controller and sensor monitoring.")
        self.sensor.start_monitoring()

    def stop(self):
        print("[Controller] Stopping controller and sensor monitoring.")
        self.sensor.stop()

# test
controller = Controller() 
sensor = IRSensor("ir_sensor_data.csv", controller)
controller.sensor = sensor
sensor.run_in_thread()
controller.start()
