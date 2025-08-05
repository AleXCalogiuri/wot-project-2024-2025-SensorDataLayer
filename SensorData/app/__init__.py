from flask import Flask
from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    from app.routes.sensor_routes import sensor_bp
    app.register_blueprint(sensor_bp, url_prefix='/api/v1')

    return app