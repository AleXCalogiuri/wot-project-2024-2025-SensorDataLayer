#classe che gestice il modello
from pyexpat import features

from .sensor_data_service import SensorDataService
from ..dto.prediction_dto import PredictionDTO
from ..dto.prediction_request_dto import PredictRequestDTO
from ..ml_model.model_loader import model,model_info
from ..models.sensor import Sensor
from ..models.sensor_data import SensorData
from ..services.sensor_service import SensorService
from ..utils.sensor_utl import SensorUTL
import pandas as pd



class PredictionService:

    #qui carica il modello
    def __init__(self, model, model_info):  # Riceve i modelli come parametri
        self.model = model
        self.model_info = model_info

    @staticmethod
    def validate_json_request(json_data):
        """Validates JSON data and send request"""
        # Use DTO validation
        result = PredictRequestDTO.from_request(json_data)
        if isinstance(result, tuple) and result[0] == "ValidationError":
            return {'error': 'Validation failed', 'details': result[1]}, 400
            # Verifica che result sia un'istanza di PredictRequestDTO
            # Se result è un dizionario, convertilo in PredictRequestDTO
        if isinstance(result, dict):
            try:
                # Crea un'istanza di PredictRequestDTO dal dizionario
                dto_instance = PredictRequestDTO(**result)
                result = dto_instance
            except Exception as e:
                return {'error': 'Failed to create DTO instance', 'details': str(e)}, 500
        print(
            f"PREDICTION SERVICE.validate_json_request: json validato procedo a prepare i dati per il modello: {result}")

        # Chiamata corretta al metodo statico
        return PredictionService.send_prediction(result)

    @staticmethod
    def send_prediction(predicition_request_dto: PredictRequestDTO):
        try:
            print(f"PREDICTION SERVICE.send_prediction: chiamo il servizio dei sensori")

            # Converti sensor_id in stringa
            sensor_id = str(predicition_request_dto.sensor_id)
            print(f"DEBUG: sensor_id convertito: '{sensor_id}' (type: {type(sensor_id)})")


            sensore_attivato_tuple = Sensor.find_by_sensor_id(sensor_id)
            id=sensore_attivato_tuple[0]
            modello =sensore_attivato_tuple[1]
            seriale= sensore_attivato_tuple[2]
            if sensore_attivato_tuple is None:
                return {'error': 'Non risulta alcun sensore con questo id, operazione annullata'}, 404

            # Converti anche sensor_data_id in stringa se necessario
            sensor_data_id = str(predicition_request_dto.sensor_data_id)
            sensor_data = SensorData.find_by_sensor_id(sensor_data_id)
            # Prepara le features
            if sensor_data is not None and sensor_data:
                print("SONO IN SENSOR DATA LINEA 74")
                datasets = [
                    sensor_data[0], # .get('accelerometer_x'),
                    sensor_data[1], # .get('accelerometer_y'),
                    sensor_data[2],  #.get('gyroscope_x'),
                    sensor_data[3],  #.get('gyroscope_y'),
                    sensor_data[4] #.get('gyroscope_z')
                ]
                gps_latitude = sensor_data[6] #.get('gps_latitude')
                gps_longitude = sensor_data[7] #.get('gps_longitude')
            else:
                gps_latitude = predicition_request_dto.gps_latitude
                gps_longitude = predicition_request_dto.gps_longitude
                datasets = [
                    predicition_request_dto.acc_x,
                    predicition_request_dto.acc_y,
                    predicition_request_dto.gyro_x,
                    predicition_request_dto.gyro_y,
                    predicition_request_dto.gyro_z
                ]

            # Crea la predizione
            # Attenzione che se cambiano i nomi nel modello, bisogna cambiare anche qui!

            prediction_service = PredictionService(model,model_info)
            prediction = prediction_service.predict(datasets)
            print(f"prediction: {prediction}")

            # Crea il DTO di risposta
            prediction_dto = PredictionDTO(
                classificazione=str(prediction),
                posizione_gps_latitude=gps_latitude,
                posizione_gps_longitude=gps_longitude,
                strada_rilevamento= predicition_request_dto.strada_rilevamento
            )
            print(type(id), type(modello), type(seriale), type(prediction), type(gps_latitude), type(gps_longitude))

            print(f"PREDICTION SERVICE response: {prediction_dto}")
            response = prediction_dto.to_dict()
            return response, 200

        except FileNotFoundError as e:
            return {'error': 'Model file not found'}, 500
        except ValueError as e:
            return {'error': f'PREDICTION SERVICE: Invalid data: {str(e)}'}, 400
        except Exception as e:
            return {'error': f'Linea 113 Internal error: {str(e)}'}, 500






    def predict(self, features):
        #NB non cambiare l'ordine perché è come le vuole il modello
        #aggiunta header
        datasets_names = ['acc_x_dashboard', 'acc_y_dashboard', 'gyro_x_dashboard', 'gyro_y_dashboard',
                          'gyro_z_dashboard']
        random_forest_dataset = pd.DataFrame([features], columns=datasets_names)
        # Validazione
        if any(x is None for x in features):
            raise ValueError("Missing sensor data values")

        if not all(isinstance(x, (int, float)) for x in features):
            raise ValueError("All sensor values must be numeric")

        prediction = self.model.predict(random_forest_dataset)

        result = PredictionService.map_prediction_to_label(prediction[0])

        print("f'PredictionService.predict: result: {result}'")
        return result

    @staticmethod
    def map_prediction_to_label(prediction):
        print("PREDICTION SERVICE map_prediction_to_label{prediction}")
        if prediction == 0:
            return "Good & Paved"
        elif prediction == 1:
            return "Good & Unpaved"
        elif prediction == 2:
            return "Bad & Paved"
        elif prediction == 3:
            return "Bad & Unpaved"