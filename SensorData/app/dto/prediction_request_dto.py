from marshmallow import Schema, fields, validate, post_load, ValidationError
from .base_dto import BaseDTO


class PredictRequestDTO(BaseDTO):
    class Schema(Schema):
        sensor_id = fields.Integer()
        acc_x = fields.Float()
        acc_y = fields.Float()
        gyro_x = fields.Float()
        gyro_y = fields.Float()
        gyro_z = fields.Float()
        gps_latitude = fields.Float()
        gps_longitude = fields.Float()
        sensor_data_id = fields.Integer()


    @post_load
    def make_object(self, data, **kwargs):
        return PredictRequestDTO(**data)


    def __init__(self,sensor_id,acc_x,acc_y,gyro_x,gyro_y,gyro_z,gps_latitude,gps_longitude,sensor_data_id):
        self.sensor_id = sensor_id
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        self.sensor_data_id = sensor_data_id

    @classmethod
    def from_request(cls, json_data=None):
        if json_data is None:
            from flask import request
            json_data = request.get_json()
        schema = cls.Schema()
        try:
            return schema.load(json_data)
        except ValidationError as err:
            return "ValidationError", err.messages


    def to_dict(self):
        return {
            "sensor_id": self.sensor_id,
            "acc_x": self.acc_x,
            "acc_y": self.acc_y,
            "gyro_x": self.gyro_x,
            "gyro_y": self.gyro_y,
            "gyro_z": self.gyro_z,
            "gps_latitude": self.gps_latitude,
            "gps_longitude": self.gps_longitude,
            "sensor_data_id": self.sensor_data_id
        }