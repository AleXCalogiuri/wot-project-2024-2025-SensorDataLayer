#classe che gestice il modello

from app.ml_model.model_loader import model_info
from app.ml_model.model_loader import model
from app.services.sensor_service import SensorService
from app.utils.sensor_utl import SensorUTL
from app.services.model_loader import model, model_info



class PredictionService:

    #qui carica il modello
    def __init__(self, model, model_info):  # Riceve i modelli come parametri
        self.model = model
        self.model_info = model_info

    def send_prediction(self, predicition_request_dto):
        try:

            '''chiama il servizio dei sensori'''
            sensore_attivato = SensorService.get_sensor(predicition_request_dto.sensor_id)
            if sensore_attivato is None: #se non trova il sensore allora lo aggiunge
                return {'error': 'Non risulta alcun sensore con questo id, operazione annullata'}, 404

            #prima proviamo a caricare i dati già disponibili, poi dopo verifica che ce ne siano di nuovi
            #dati_sensore = SensorDataService.get_dati_sensore(predicition_request_dto.sensor_data_id)
            gps_latitude = predicition_request_dto.gps_latitude
            gps_longitude = predicition_request_dto.gps_longitude

            features = [predicition_request_dto.acc_x, predicition_request_dto.acc_y,
                        predicition_request_dto.gyro_x, predicition_request_dto.gyro_y, predicition_request_dto.gyro_z]
            #crea l'array con i dati del sensore
            prediction = self.__predict(features)
            #prepara il json da restiuire

            response = {
                            'sensor_productor': SensorUTL.toDto(sensore_attivato) ,
                            'classificazione': prediction,
                            'posizione_gps_latitude': gps_latitude,
                            'posizione_gps_longitude': gps_longitude
                        }
            return response,200

        except FileNotFoundError as e:
            return {'error': 'Model file not found'}, 500
        except ValueError as e:
            return {'error': f'Invalid data: {str(e)}'}, 400
        except Exception as e:
            return {'error': f'Internal error: {str(e)}'}, 500


    def __predict(self, sensor_data_dto):
        #NB non cambiare l'ordine perché è come le vuole il modello
        features = [sensor_data_dto.accelerometer_x,
                    sensor_data_dto.accelerometer_y,
                    sensor_data_dto.gyroscope_x,
                    sensor_data_dto.gyroscope_y,
                    sensor_data_dto.gyroscope_z
                    ]

        #Validazione
        if any(x is None for x in features):
            raise ValueError("Missing sensor data values")

        if not all(isinstance(x, (int, float)) for x in features):
            raise ValueError("All sensor values must be numeric")

        prediction = self.model.predict([features])
        result = model_info['class_mapping'][prediction[0]]
        return result