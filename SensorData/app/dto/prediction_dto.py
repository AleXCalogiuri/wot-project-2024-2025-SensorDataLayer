from marshmallow import Schema, fields, post_load, ValidationError
from .base_dto import BaseDTO
from ..dto.sensor_dto import SensorDTO
from flask import request

class PredictionDTO(BaseDTO):
    class Schema(Schema):
        sensor_id = fields.Str()
        sensor_model = fields.Str()
        sensor_serial = fields.Str()
        classificazione = fields.Str(required=True)
        posizione_gps_latitude = fields.Float(required=True)
        posizione_gps_longitude = fields.Float(required=True)
        via = fields.Str(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return PredictionDTO(**data)

    def __init__(self, sensor_id, sensor_model, sensor_serial, classificazione, posizione_gps_latitude, posizione_gps_longitude, via):
        self.sensor_id = sensor_id
        self.sensor_model = sensor_model
        self.sensor_serial = sensor_serial
        self.classificazione = classificazione
        self.posizione_gps_latitude = posizione_gps_latitude
        self.posizione_gps_longitude = posizione_gps_longitude
        self.via = via

    @classmethod
    def from_request(cls, json_data=None):
        if json_data is None:
            json_data = request.get_json()
        schema = cls.Schema()
        try:
            return schema.load(json_data)
        except ValidationError as err:
            return "ValidationError", err.messages

    def to_dict(self):

        return {
            # 'sensor_id': self.sensor_id
            # 'sensor_model': self.sensor_model,
            # 'sensor_serial': self.sensor_serial,
            'predilezione': self.classificazione,
            'latitudine': self.posizione_gps_latitude,
            'longitudine': self.posizione_gps_longitude,
            'via': self.via
        }