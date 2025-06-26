from ..dto.sensor_data_dto import SensorDataDTO
from ..models.sensor_data import SensorData


class SensorDataUTL:

    def __init__(self, sensor_data_dto):
        self.sensor_dto = sensor_data_dto

    @staticmethod
    def to_dto(sensor_data):
        # Se sensorData è una tupla, accedi per indice
        if isinstance(sensor_data, tuple):
            dto = {
                'sensorDataId': sensor_data[0],  # sensorDataId
                'accelerometer_x': sensor_data[1],  # accelerometer_x
                'accelerometer_y': sensor_data[2],  # accelerometer_y
                'accelerometer_z': sensor_data[3],  # accelerometer_z
                'gyroscope_x': sensor_data[4], #gyroscope_x
                'gyroscope_y': sensor_data[5], #gyroscope_y
                'gyroscope_z': sensor_data[6], #gyroscope_z
                'timestamp': sensor_data[7], #timestamp
                'gps_latitude': sensor_data[8], #gps_latitude
                'gps_longitude': sensor_data[9], #gps_longitude
            }
        else:
            # Se sensorData è un oggetto, accedi per attributo
            dto = {
                'sensorId': sensor_data.sensorId,
                'model': sensor_data.model,
                'status': sensor_data.status.value if hasattr(sensor_data.status, 'value') else str(sensor_data.status)
            }
        return SensorDataDTO(**dto)

    @staticmethod
    def to_model(sensor_data_dto):
        return SensorData(sensor_data_dto.sensorDataId,
                          sensor_data_dto.accelerometer_x,
                          sensor_data_dto.accelerometer_y,
                          sensor_data_dto.accelerometer_z,
                          sensor_data_dto.gyroscope_x,
                          sensor_data_dto.gyroscope_y,
                          sensor_data_dto.gyroscope_z,
                          sensor_data_dto.timestamp,
                          sensor_data_dto.gps_latitude,
                          sensor_data_dto.gps_longitude)