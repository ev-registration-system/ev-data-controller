class IRSensor:
    def __init__(self):
        self.vehicle_present = False

    def detect_vehicle(self):
        return self.vehicle_present

    def set_vehicle_presence(self, presence: bool):
        self.vehicle_present = presence