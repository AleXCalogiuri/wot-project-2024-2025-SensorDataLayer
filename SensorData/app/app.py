import datetime

from flask import Flask
from flask_cors import CORS
from joblib import load

from .models.sensor import Sensor, Status
from .models.sensor_data import SensorData


'''
     .-.   
    | OO| 
    |   | 
    '^^^' 
'''

def create_app(config_name=None):
    app = Flask(__name__)
    CORS(app)

    # Inizializza le tabelle



    sensor = Sensor("",0,"",Status.ACTIVE)  # Istanza temporanea
    sensor.init_db()
    sensor_data = SensorData(0,0,0,0,0,0,0,str(datetime.datetime.now()),None,None)
    sensor_data.init_db()


    @app.route('/')
    def hello_world():
        return 'Hello World!'

    # QUESTO PER VERIFICARE SE IL BLUEPRINT È STATO MONTATO DA LEVARE IN PROD
    @app.route('/debug/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': rule.rule
            })
        return {'routes': routes}


    #QUESTO PER VERIFICARE SE IL DB È STATO MONTATO DA LEVARE IN PROD
    import os
    @app.route('/debug/filesystem')
    def debug_filesystem():
        return {
            'current_dir': os.getcwd(),
            'files_in_current_dir': os.listdir('.'),
            'app_dir_exists': os.path.exists('/app'),
            'app_dir_contents': os.listdir('/app') if os.path.exists('/app') else 'N/A'
        }

    # Register blueprints
    from .routes.sensor_routes import sensor_bp
    app.register_blueprint(sensor_bp, url_prefix='/api/v1')

    from .routes.prediction_routes import predict_bp
    app.register_blueprint(predict_bp, url_prefix='/api/v1')

    return app


# Crea l'applicazione



if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")
