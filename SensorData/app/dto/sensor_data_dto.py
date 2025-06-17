from marshmallow import Schema, fields, ValidationError

from app.dto.base_dto import BaseDTO
from app.models.sensor_data import SensorData


class SensorDataDTO(BaseDTO):
    class Schema(Schema):
        sensorDataId = fields.Str
        timestamp = fields.DateTime
        accelerometer_x = fields.Float
        accelerometer_y = fields.Float
        accelerometer_z = fields.Float
        gyroscope_x = fields.Float
        gyroscope_y = fields.Float
        gyroscope_z = fields.Float
        gps_latitude = fields.Float
        gps_longitude = fields.Float

    def __init__(self, sensor_data_id, timestamp, accelerometer_x, accelerometer_y,
                 accelerometer_z,gyroscope_x, gyroscope_y, gyroscope_z,
                 gps_latitude, gps_longitude
                 ):
        self.sensor_data_id = sensor_data_id
        self.timestamp = timestamp
        self.accelerometer_x = accelerometer_x
        self.accelerometer_y = accelerometer_y
        self.accelerometer_z = accelerometer_z
        self.gyroscope_x = gyroscope_x
        self.gyroscope_y = gyroscope_y
        self.gyroscope_z = gyroscope_z
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude

    @classmethod
    def from_request(cls,json_data=None):
        """Parse request data and return a validated SensorDataDTO instance."""
        if json_data is None:
            from flask import request
            json_data = request.get_json()
        schema = cls.Schema()
        try:
            return schema.load(json_data)
        except ValidationError as e:
            return "ValidationError", e.messages



