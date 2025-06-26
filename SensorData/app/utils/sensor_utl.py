from ..dto.sensor_dto import SensorDTO
from ..models.sensor import Sensor, Status


class SensorUTL:

    def __init__(self,sensor_dto):
        self.sensor_dto = sensor_dto

    @staticmethod
    def to_dto(sensor):
        # Se sensor è una tupla, accedi per indice
        if isinstance(sensor, tuple):
            dto = {
                'sensorId': sensor[0],  # sensorId
                'serialNumber': sensor[1],  # serial (se serve nel DTO)
                'model': sensor[2],  # model
                'status': sensor[3]  # status
            }
        else:
            # Se sensor è un oggetto, accedi per attributo
            dto = {
                'sensorId': sensor.sensorId,
                'serialNumber': sensor.serialNumber,
                'model': sensor.model,
                'status': sensor.status.value if hasattr(sensor.status, 'value') else str(sensor.status)
            }
        return SensorDTO(**dto)

    @staticmethod
    def to_model(sensor_dto):
        return Sensor(
            sensorId=sensor_dto.sensorId,
            serial=sensor_dto.serialNumber,
            model=sensor_dto.model,
            status=Status(sensor_dto.status)
        )