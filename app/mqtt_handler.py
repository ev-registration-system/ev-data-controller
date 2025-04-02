import paho.mqtt.client as mqtt
import certifi
from config import Config

class MQTTHandler:
    def __init__(self):
        self.is_connected = False
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
        self.mqtt_client.tls_set(ca_certs=certifi.where())
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.connect(Config.MQTT_BROKER_URL, Config.MQTT_BROKER_PORT, 60)
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc, props):
        print(f'Connected to HiveMQ with result code {rc}')
        self.is_connected = True
        client.subscribe("/evantage/controller/check-in")
        client.subscribe("/evantage/controller/checkout")
        client.subscribe("/evantage/controller/illegal")

    def notify_topic(self, topic, message):
        self.mqtt_client.publish(topic, message)
        print(f'Published to {topic}: {message}')
