import datetime

from ..models.sensor_data import SensorData # Import the class and enum
from ..dto.sensor_data_dto import SensorDataDTO  # Import the DTO class
from ..utils.sensor_data_utl import SensorDataUTL


#classe di servizio per sensor_data


class SensorDataService:

    @staticmethod
    def get_dati_sensore(sensor_data_id):
        """Retrieves a sensor by ID and returns as DTO"""
        try:

            #crea un istanza del sensore
            sensor_data_tuple = SensorData.find_by_sensor_id(sensor_data_id)
            result = SensorDataUTL.to_dto(sensor_data_tuple)


            return result.to_dict()


        except Exception as e:
            return {'SENSORSERVICE : error': f'Failed to retrieve sensor data: {str(e)}'}, 500


