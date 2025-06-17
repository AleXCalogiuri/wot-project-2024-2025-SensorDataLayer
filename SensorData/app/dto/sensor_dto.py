from marshmallow import Schema, fields, validate, post_load, ValidationError
from .base_dto import BaseDTO
###
#Sensor {
#  sensorId: string,
#  serial: Number,
#  model: String,
#  installationDate: Timestamp,
#  lastCalibration: Timestamp,
#  status: Enum["ACTIVE", "INACTIVE", "MAINTENANCE"]
#}

class SensorDTO(BaseDTO):
    class Schema(Schema):
        sensorId = fields.Str(required=True)
        serialNumber = fields.Str(required=True,validate=validate.Length(min=5)) #giusto qualche regola per capire dove posso spingermi
        model = fields.Str(required=True, validate=validate.Length(min=6))
        installationDate = fields.DateTime(required=True)
        lastCalibrationDate = fields.DateTime()
        status = fields.Str(validate=validate.OneOf(['ACTIVE', 'INACTIVE','MAINTENANCE']))

        @post_load
        def make_object(self, data, **kwargs):
            return SensorDTO(**data)

    def __init__(self, sensorId, serialNumber, model, installationDate, lastCalibrationDate, status):
        self.sensorId = sensorId
        self.serialNumber = serialNumber
        self.model = model
        self.installationDate = installationDate
        self.lastCalibrationDate = lastCalibrationDate
        self.status = status

    @classmethod
    def from_request(cls, json_data=None):
        """Parse request data and return a validated SensorDTO instance."""
        if json_data is None:
            from flask import request
            json_data = request.get_json()
        schema = cls.Schema()
        try:
            return schema.load(json_data)  # This will call `make_object` and return SensorDTO
        except ValidationError as err:
            return "ValidationError", err.messages

    def to_dict(self):
        return {
            'sensorId': self.sensorId,
            'serialNumber': self.serialNumber,
            'model': self.model,
            'installationDate': self.installationDate.isoformat() if self.installationDate else None,
            'lastCalibrationDate': self.lastCalibrationDate.isoformat() if self.lastCalibrationDate else None,
            'status': self.status
        }

class RemoveSensorDTO(BaseDTO):
    class Schema(Schema):
        sensorId = fields.Str(required=True)
        status = fields.Str(required=True)

        @post_load
        def make_object(self, data, **kwargs):
            return RemoveSensorDTO(**data)

        def __init__(self,sensorId,status):
            self.sensorId = sensorId
            self.status = status
