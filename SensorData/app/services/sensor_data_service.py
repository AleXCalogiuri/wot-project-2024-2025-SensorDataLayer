import datetime

from app.models.sensor import SensorData, Status  # Import the class and enum
from app.dto.sensor_data_dto import SensorDataDTO  # Import the DTO class
#classe di servizio per sensor_data


class SensorDataService:

    @staticmethod
    def get_sensor(sensor_data_id: str):
        """Retrieves a sensor by ID and returns as DTO"""
        try:

            #crea un istanza del sensore
            sensor_data_model = SensorData("",datetime.datetime.now(),"0","0","0","0","0","0")
            result = sensor_data_model.findBySensorId(sensor_data_id)

            if result:
                # Convert database result to DTO format
                # Note: you'll need to implement a method to get full sensor data
                return {'sensor_data': result}, 200
            else:
                return {'error': 'Sensor Data not found'}, 404

        except Exception as e:
            return {'error': f'Failed to retrieve sensor data: {str(e)}'}, 500

