#classe che gestice il modello
from ..dto.prediction_dto import PredictionDTO
from ..dto.prediction_request_dto import PredictRequestDTO
from ..models.sensor import Sensor
from ..models.sensor_data import SensorData
from ..senders.rabbit_mq_sender import RabbitMQSender

import pandas as pd



class PredictionService:

    #qui carica il modello
    def __init__(self, model, model_info,rabbitmq_sender: RabbitMQSender = None):  # Riceve i modelli come parametri
        self.model = model
        self.model_info = model_info
        self.rabbitmq_sender = rabbitmq_sender or RabbitMQSender()

    @staticmethod
    def validate_json_request(json_data, prediction_service: "PredictionService"):
        """Validates JSON data and send request"""
        result = PredictRequestDTO.from_request(json_data)

        if isinstance(result, tuple) and result[0] == "ValidationError":
            return {'error': 'Validation failed', 'details': result[1]}, 400

        if isinstance(result, dict):
            try:
                result = PredictRequestDTO(**result)
            except Exception as e:
                return {'error': 'Failed to create DTO instance', 'details': str(e)}, 500

        print(f"PredictionService.validate_json_request: validato DTO {result}")
        return prediction_service.send_prediction(result)

    def send_prediction(self, prediction_request_dto: PredictRequestDTO):
        try:
            print(f"PredictionService.send_prediction: chiamo il servizio dei sensori")

            sensor_id = str(prediction_request_dto.sensor_id)
            sensore_attivato_tuple = Sensor.find_by_sensor_id(sensor_id)

            if sensore_attivato_tuple is None:
                return {'error': 'Nessun sensore trovato'}, 404

            #id, modello, seriale = sensore_attivato_tuple

            sensor_data_id = str(prediction_request_dto.sensor_data_id)
            sensor_data = SensorData.find_by_sensor_id(sensor_data_id)

            if sensor_data:
                datasets = [
                    sensor_data[0],
                    sensor_data[1],
                    sensor_data[2],
                    sensor_data[3],
                    sensor_data[4],
                ]
                gps_latitude = sensor_data[6]
                gps_longitude = sensor_data[7]
            else:
                datasets = [
                    prediction_request_dto.acc_x,
                    prediction_request_dto.acc_y,
                    prediction_request_dto.gyro_x,
                    prediction_request_dto.gyro_y,
                    prediction_request_dto.gyro_z,
                ]
                gps_latitude = prediction_request_dto.gps_latitude
                gps_longitude = prediction_request_dto.gps_longitude

            # usa direttamente self
            prediction = self.predict(datasets)
            print(f"prediction: {prediction}")

            prediction_dto = PredictionDTO(
                classificazione=str(prediction),
                posizione_gps_latitude=gps_latitude,
                posizione_gps_longitude=gps_longitude,
                strada_rilevamento=prediction_request_dto.strada_rilevamento,
            )

            response = prediction_dto.to_dict()
            send_message = self.send_queue(prediction_dto)

            result = {
                'process': response,
                'message': send_message
            }
            if send_message['rabbit_status'] != 'message_OK':
                return result, 500
            return response, 200

        except FileNotFoundError:
            return {'error': 'Model file not found'}, 500
        except ValueError as e:
            return {'error': f'PredictionService: Invalid data: {str(e)}'}, 400
        except Exception as e:
            return {'error': f'Internal error: {str(e)}'}, 500




    def send_queue(self,data_to_send : PredictionDTO):

        try:

            result_send = self.rabbitmq_sender.publish_sensor_data(data_to_send.to_dict())

            if result_send:
                return {'rabbit_status': 'message_OK'}
            else:
                return {'rabbit_status': 'message_KO'}

        except Exception as e:

            return {'rabbit_status': 'message_KO_exception', 'error': str(e)}



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
        valutazione = ''
        if prediction == 0:
            valutazione = "GOOD_AND_PAVED"
        elif prediction == 1:
            valutazione = "GOOD_AND_UNPAVED"
        elif prediction == 2:
            valutazione = "BAD_AND_PAVED"
        elif prediction == 3:
            valutazione = "BAD_AND_UNPAVED"

        return valutazione