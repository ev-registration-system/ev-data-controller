import time
import threading
from app.mqtt_handler import MQTTHandler
from app.ir_sensor import IRSensor
from app.charger import Charger
from config import Config

class Controller:
    # This controller needs states:
    # 1. No Vehicle
    # 2. Vehicle Not Checked In
    # 3. Vehicle Checked In
    # 4. Illegal Vehicle

    STATE_NO_VEHICLE = 1
    STATE_VEHICLE_NOT_CHECKED_IN = 2
    STATE_VEHICLE_CHECKED_IN = 3
    STATE_ILLEGAL_VEHICLE = 4

    def __init__(self, mqtt_topic_prefix):
        self.state = self.STATE_NO_VEHICLE
        self.ir_sensor = IRSensor()
        self.charger = Charger()
        self.mqtt_handler = MQTTHandler()
        self.mqtt_topic_prefix = mqtt_topic_prefix
        self.mqtt_handler.mqtt_client.on_message = self.on_controller_message
        self.mqtt_handler.mqtt_client.connect(Config.MQTT_BROKER_URL, Config.MQTT_BROKER_PORT, 60)
        self.mqtt_handler.mqtt_client.subscribe(f"{mqtt_topic_prefix}/#")
        self.mqtt_handler.mqtt_client.loop_start()

        self.sensor_thread = threading.Thread(target=self.monitor_sensor, daemon=True)
        self.sensor_thread.start()

    def on_controller_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        print(f"Received MQTT message on topic {message.topic}: {payload}")

        if message.topic.endswith("/checkin"):
            self.state = self.STATE_VEHICLE_CHECKED_IN
            self.charger.turn_on()
            print("Vehicle checked in. Charger enabled.")
        elif message.topic.endswith("/illegalvehicle"):
            self.state = self.STATE_ILLEGAL_VEHICLE
            print("Illegal vehicle detected.")
        else:
            print("Unrecognized topic")

    def monitor_sensor(self):
        """
        Monitors the IR sensor and manages state transitions based on vehicle detection.
        Runs continuously in a separate thread.
        """
        while True:
            vehicle_present = self.ir_sensor.detect_vehicle()
            if vehicle_present and self.state == self.STATE_NO_VEHICLE:
                self.state = self.STATE_VEHICLE_NOT_CHECKED_IN
                print("Vehicle arrived. Notifying main application...")
                self.mqtt_handler.notify_topic(f"{self.mqtt_topic_prefix}/vehicle_arrival", "Vehicle arrived")

            elif not vehicle_present and self.state != self.STATE_NO_VEHICLE:
                print("Vehicle departed. Resetting state and disabling charger if needed.")
                self.state = self.STATE_NO_VEHICLE
                self.charger.turn_off()

            time.sleep(2)
