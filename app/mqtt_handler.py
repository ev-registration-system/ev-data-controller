import paho.mqtt.client as mqtt
import ssl
import certifi
from config import Config

class MQTTHandler:
    def on_connect(client, userdata, flags, rc, props):
        print(f'Connected to HiveMQ with result code {rc}')
        client.subscribe('evantage/controller')

    def notify_topic(self, topic, message):
        self.mqtt_client.publish(topic, message)
        print(f'Published to {topic}: {message}')

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
    mqtt_client.tls_set(ca_certs=certifi.where())
    mqtt_client.on_connect = on_connect
