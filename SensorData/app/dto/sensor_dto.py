from marshmallow import Schema, fields, validate, post_load, ValidationError
from .base_dto import BaseDTO

"""
Sensor DTO Module

This module defines Data Transfer Objects (DTOs) for sensor-related operations.
It handles the serialization and deserialization of sensor data between
the application and external interfaces, including validation of input data.

The module contains two main DTOs:
1. SensorDTO: Represents a sensor with its properties
2. RemoveSensorDTO: Used for sensor removal operations
"""

class SensorDTO(BaseDTO):
    """
    Data Transfer Object for representing a sensor.

    This class handles the serialization and deserialization of sensor data,
    including validation of input data and conversion between JSON and object formats.

    Attributes:
        sensorId (str): Unique identifier for the sensor.
        serialNumber (str): Serial number of the sensor (minimum length: 5).
        model (str): Model of the sensor (minimum length: 6).
        installationDate (datetime): Date and time when the sensor was installed.
        lastCalibrationDate (datetime): Date and time of the last calibration.
        status (str): Current status of the sensor, one of ["ACTIVE", "INACTIVE", "MAINTENANCE"].
    """

    class Schema(Schema):
        """
        Marshmallow schema for validating and serializing SensorDTO objects.

        Fields:
            sensorId (str): Unique identifier for the sensor (required).
            serialNumber (str): Serial number of the sensor (required, min length: 5).
            model (str): Model of the sensor (required, min length: 6).
            installationDate (datetime): Date and time when the sensor was installed (required).
            lastCalibrationDate (datetime): Date and time of the last calibration.
            status (str): Current status of the sensor, one of ["ACTIVE", "INACTIVE", "MAINTENANCE"].
        """
        sensorId = fields.Str(required=False)
        serialNumber = fields.Str(required=True, validate=validate.Length(min=5))
        model = fields.Str(required=True, validate=validate.Length(min=6))
        installationDate = fields.DateTime(required=True)
        lastCalibrationDate = fields.DateTime()
        status = fields.Str(validate=validate.OneOf(['ACTIVE', 'INACTIVE', 'MAINTENANCE']))

        @post_load
        def make_object(self, data, **kwargs):
            """
            Create a SensorDTO instance from validated data.

            Args:
                data (dict): The validated data dictionary.
                **kwargs: Additional keyword arguments.

            Returns:
                SensorDTO: A new instance with the provided data.
            """
            return SensorDTO(**data)

    def __init__(self, sensorId, serialNumber, model, installationDate, lastCalibrationDate, status):
        """
        Initialize a new SensorDTO instance.

        Args:
            sensorId (str): Unique identifier for the sensor.
            serialNumber (str): Serial number of the sensor.
            model (str): Model of the sensor.
            installationDate (datetime): Date and time when the sensor was installed.
            lastCalibrationDate (datetime): Date and time of the last calibration.
            status (str): Current status of the sensor.
        """
        self.sensorId = sensorId
        self.serialNumber = serialNumber
        self.model = model
        self.installationDate = installationDate
        self.lastCalibrationDate = lastCalibrationDate
        self.status = status

    @classmethod
    def from_request(cls, json_data=None):
        """
        Parse and validate request data to create a SensorDTO instance.

        This method extracts JSON data from the request if not provided,
        validates it using the Schema class, and returns a SensorDTO instance.

        Args:
            json_data (dict, optional): JSON data to parse. If None, data is extracted
                                       from the current Flask request. Defaults to None.

        Returns:
            SensorDTO: A validated instance if successful.
            tuple: ("ValidationError", error_messages) if validation fails.
        """
        if json_data is None:
            from flask import request
            json_data = request.get_json()
        schema = cls.Schema()
        try:
            return schema.load(json_data)  # This will call `make_object` and return SensorDTO
        except ValidationError as err:
            return "ValidationError", err.messages

    def to_dict(self):
        """
        Convert the SensorDTO instance to a dictionary representation.

        This method serializes the SensorDTO object to a dictionary format
        suitable for JSON conversion, ensuring datetime objects are properly
        formatted as ISO 8601 strings.

        Returns:
            dict: A dictionary containing the sensor data with keys corresponding to attributes.
        """
        return {
            'sensorId': self.sensorId,
            'serialNumber': self.serialNumber,
            'model': self.model,
            'installationDate': self.installationDate.isoformat() if self.installationDate else None,
            'lastCalibrationDate': self.lastCalibrationDate.isoformat() if self.lastCalibrationDate else None,
            'status': self.status
        }

class RemoveSensorDTO(BaseDTO):
    """
    Data Transfer Object for sensor removal operations.

    This class handles the serialization and deserialization of data needed
    for removing or changing the status of a sensor.

    Attributes:
        sensorId (str): Unique identifier for the sensor to be removed/updated.
        status (str): The new status to be applied to the sensor.
    """

    class Schema(Schema):
        """
        Marshmallow schema for validating and serializing RemoveSensorDTO objects.

        Fields:
            sensorId (str): Unique identifier for the sensor (required).
            status (str): The new status to be applied to the sensor (required).
        """
        sensorId = fields.Str(required=True)
        status = fields.Str(required=True)

        @post_load
        def make_object(self, data, **kwargs):
            """
            Create a RemoveSensorDTO instance from validated data.

            Args:
                data (dict): The validated data dictionary.
                **kwargs: Additional keyword arguments.

            Returns:
                RemoveSensorDTO: A new instance with the provided data.
            """
            return RemoveSensorDTO(**data)

    def __init__(self, sensorId, status):
        """
        Initialize a new RemoveSensorDTO instance.

        Args:
            sensorId (str): Unique identifier for the sensor to be removed/updated.
            status (str): The new status to be applied to the sensor.
        """
        self.sensorId = sensorId
        self.status = status
