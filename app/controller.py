import math
import time
import threading
from app.mqtt_handler import MQTTHandler
from app.ir_sensor import IRSensor
from app.charger import Charger
class Controller:
    STATE_NO_VEHICLE = 1
    STATE_VEHICLE_NOT_CHECKED_IN = 2
    STATE_VEHICLE_CHECKED_IN = 3
    STATE_ILLEGAL_VEHICLE = 4

    def __init__(self):
        self.state = self.STATE_NO_VEHICLE
        self.lock = threading.Lock()
        self.session_start_time = None
        self.not_checked_in_start = None
        self.ir_sensor = IRSensor()
        self.charger = Charger(1)
        self.mqtt_handler = MQTTHandler()
        self.mqtt_handler.mqtt_client.on_message = self.on_controller_message

        while not self.mqtt_handler.is_connected:
            time.sleep(1)

        self.sensor_thread = threading.Thread(target=self.monitor_sensor, daemon=True)
        self.sensor_thread.start()

    def on_controller_message(self, client, userdata, message):
        with self.lock:
            payload = message.payload.decode("utf-8")
            print(f"Received MQTT message on topic {message.topic}: {payload}")

            if message.topic.endswith("/check-in"):
                self.handle_check_in()
            elif message.topic.endswith("/checkout"):
                self.handle_check_out()
            elif message.topic.endswith("/illegal"):
                self.state = self.STATE_ILLEGAL_VEHICLE
                print("Illegal vehicle detected.")
            else:
                print("Unrecognized topic")

    def monitor_sensor(self):
        while True:
            vehicle_present = self.ir_sensor.detect_vehicle()
            with self.lock:
                if vehicle_present and self.state == self.STATE_NO_VEHICLE:
                    print("Vehicle arrived. Notifying main application...")
                    self.state = self.STATE_VEHICLE_NOT_CHECKED_IN
                    self.not_checked_in_start = time.time()
                    self.mqtt_handler.notify_topic(
                        "/evantage/system/arrive",
                        "{\"message\": \"Vehicle arrived\"}"
                    )
                elif not vehicle_present and self.state != self.STATE_NO_VEHICLE:
                    print("Vehicle departed. Resetting state and disabling charger.")
                    self.state = self.STATE_NO_VEHICLE
                    self.not_checked_in_start = None
                    self.charger.turn_off()

                if self.state == self.STATE_VEHICLE_NOT_CHECKED_IN and self.not_checked_in_start:
                    elapsed = time.time() - self.not_checked_in_start
                    if elapsed >= 600:
                        print("Vehicle stayed in NOT_CHECKED_IN for 10+ minutes. Marking as illegal.")
                        self.state = self.STATE_ILLEGAL_VEHICLE
                        self.mqtt_handler.notify_topic(
                            "/evantage/system/illegal",
                            "{\"message\": \"Illegal vehicle detected\", \"chargerId\": " + str(self.charger.id) + "}"
                        )
                        self.not_checked_in_start = None
            time.sleep(60)

    def handle_check_in(self):
        self.state = self.STATE_VEHICLE_CHECKED_IN
        self.session_start_time = time.time()
        self.charger.turn_on()
        print("Vehicle checked in. Charger enabled.")

    def handle_check_out(self):
        if self.state == self.STATE_VEHICLE_CHECKED_IN:
            self.send_session_summary()
        else:
            print("Checkout called but vehicle wasn't in checked-in state.")

        self.reset_session()

    def send_session_summary(self):
        end_time = time.time()
        if self.session_start_time is None:
            print("No session start time recorded. Cannot send summary.")
            return

        duration_hours = (end_time - self.session_start_time) / 3600.0
        hours_charged = math.ceil(duration_hours)

        summary_data = {
            "charger_id": self.charger.id,
            "start_time": self.session_start_time,
            "end_time": end_time,
            "hours_charged": hours_charged,
            "session_energy": self.charger.session_energy
        }

        summary_json = str(summary_data).replace("'", '"')
        print(f"Sending session summary: {summary_json}")

        self.mqtt_handler.notify_topic(
            "/evantage/system/summary",
            summary_json
        )

    def reset_session(self):
        self.charger.turn_off()
        self.session_start_time = None
        self.charger.session_energy = 0.0
