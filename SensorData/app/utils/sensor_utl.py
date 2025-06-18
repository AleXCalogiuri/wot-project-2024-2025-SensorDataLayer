
class SensorUTL:

    def __init__(self,sensor_dto):
        self.sensor_dto = sensor_dto

    def toDto(self,sensor_dto):

        dto = {
                'sensorId': sensor_dto.sensorId,
                'model': sensor_dto.model,
                'installationDate': sensor_dto.installationDate,
                'lastCalibrationDate': sensor_dto.lastCalibrationDate,
                'status': sensor_dto.status
               }
        return dto