import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL')
    MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT'))
    MQTT_USERNAME = os.getenv('MQTT_USERNAME')
    MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
