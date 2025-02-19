class Controller:
    def __init__(self):
        # Init controller. turn on senor
        pass

    def handle_sensor_state_change(self, vehicle_present):
        # Handle incoming/leaving car. I.E either let user check in or notify security
        pass
        
    def start(self):
        print("[Controller] Starting controller and sensor monitoring.")
        self.sensor.start_monitoring()

    def stop(self):
        print("[Controller] Stopping controller and sensor monitoring.")
        self.sensor.stop()
        
controller = Controller()