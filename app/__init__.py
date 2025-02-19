from flask import Flask
from app.routes import bp as routes_bp
from app.mqtt_handler import mqtt_client
from app.controller import ChargerController
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(routes_bp)
    return app