#classe che gestice
from pyexpat import features
import joblib
from SensorData.app.dto.prediction_dto import PredictionDTO
from SensorData.app.models.sensor_data import SensorData
from SensorData.app.services.sensor_data_service import SensorDataService
from SensorData.app.services.sensor_service import SensorService
from SensorData.app.utils.sensor_utl import SensorUTL
from SensorData.ml_model.random_forest import RandomForest


class PredictionService:

    #qui carica il modello
    def __init__(self):
        self.model = joblib.load('random_forest.joblib')

    def send_prediction(self, sensor_data_dto,sensor_productor_id):
        try:

            '''chiama il servizio dei sensori'''
            sensore_attivato = SensorService.get_sensor(sensor_productor_id)
            if sensore_attivato is None: #se non trova il sensore allora lo aggiunge
                SensorService.add_sensor(sensore_attivato)
            dati_sensore = SensorDataService.get_dati_sensore(sensor_data_dto.sensor_data_id)

            #crea l'array con i dati del sensore
            prediction = self.__predict(dati_sensore)
            #prepara il json da restiuire

            response = {
                            'sensor_productor': SensorUTL.toDto(sensore_attivato),
                            'classificazione': prediction,
                            'posizione_gps_latitude': dati_sensore.gps_latitude,
                            'posizione_gps_longitude': dati_sensore.gps_longitude
                        }
            return response,200
        except ValueError as e:
            return {'error': f'Invalid status value: {str(e)}'}, 400
        except Exception as e:
            return {'error': f'Internal error: {str(e)}'}, 500

    def __predict(self, sensor_data_dto):
        #TODO controlla bene i campi in input, perché mi sa che devono essere mappati con il nome nel csv
        features = [sensor_data_dto.accelerometer_x,
                    sensor_data_dto.accelerometer_y,
                    sensor_data_dto.gyroscope_x,
                    sensor_data_dto.gyroscope_y,
                    sensor_data_dto.gyroscope_z
                    ]
        # TODO sostituire con file serializzato attualmente non funziona
        prediction = RandomForest.classificatore()
        prediction = self.model.predict([features])
        return prediction[0]