import logging
import time
from app import create_app
from app.controller import Controller

app = create_app()

if __name__ == '__main__':
    controller = Controller(mqtt_topic_prefix="controller")

    time.sleep(60)
    print('setting vehicle presense to true')
    controller.ir_sensor.set_vehicle_presence(True)

    app.run()
