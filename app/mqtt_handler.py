import paho.mqtt.client as mqtt
import ssl
from config import Config

def on_connect(client, userdata, flags, rc, props):
    print(f'Connected to HiveMQ with result code {rc}')
    client.subscribe('evantage/controller')

def on_message(client, userdata, msg):
    print(f'{msg.topic}: {msg.payload}')

def notify_topic(topic, message):
    mqtt_client.publish(topic, message)
    print(f'Published to {topic}: {message}')

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
mqtt_client.tls_set()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(Config.MQTT_BROKER_URL, Config.MQTT_BROKER_PORT, 60)
#mqtt_client.loop_forever()
