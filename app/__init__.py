from flask import Flask
import app.mqtt_handler

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    return app