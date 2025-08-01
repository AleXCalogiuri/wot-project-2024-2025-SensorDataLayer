from marshmallow import Schema, fields, post_load, ValidationError
from .base_dto import BaseDTO
from ..dto.sensor_dto import SensorDTO

"""
PredictionDTO Module

This module defines the Data Transfer Object (DTO) for prediction data.
It handles the serialization and deserialization of prediction data between
the application and external interfaces.

Structure:
    PredictionDTO: {
        sensor_productor: SensorDTO,
        classificazione: String representing one of ["Good & Paved", "Good & Unpaved", "Bad & Paved", "Bad & Unpaved"]
    }
"""
class PredictionDTO(BaseDTO):
    """
    Data Transfer Object for representing a prediction.

    This class handles the serialization and deserialization of prediction data,
    including validation of input data and conversion between JSON and object formats.
    """

    class Schema(Schema):
        """
        Marshmallow schema for validating and serializing PredictionDTO objects.
        """

        timestampRilevazione= fields.DateTime()
        classificazione = fields.Str(required=True)
        posizione_gps_latitude = fields.Float(required=True)
        posizione_gps_longitude = fields.Float(required=True)
        strada_rilevamento = fields.Str(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        """
        Create a PredictionDTO instance from validated data.

        Args:
            data (dict): The validated data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            PredictionDTO: A new instance with the provided data.
        """
        return PredictionDTO(**data)

    def __init__(self, classificazione, posizione_gps_latitude, posizione_gps_longitude,strada_rilevamento):
        """
        Initialize a new PredictionDTO instance.


        """
        self.classificazione = classificazione
        self.posizione_gps_latitude = posizione_gps_latitude
        self.posizione_gps_longitude = posizione_gps_longitude
        self.strada_rilevamento = strada_rilevamento

    @classmethod
    def from_request(cls, json_data=None):
        """
        Parse and validate request data to create a PredictionDTO instance.

        This method extracts JSON data from the request if not provided,
        validates it using the Schema class, and returns a PredictionDTO instance.

        Args:
            json_data (dict, optional): JSON data to parse. If None, data is extracted
                                       from the current Flask request. Defaults to None.

        Returns:
            PredictionDTO: A validated instance if successful.
            tuple: ("ValidationError", error_messages) if validation fails.
        """
        if json_data is None:
            from flask import request
            json_data = request.get_json()
        schema = cls.Schema()
        try:
            return schema.load(json_data)
        except ValidationError as err:
            return "ValidationError", err.messages

    def to_dict(self):
        """
        Convert the PredictionDTO instance to a dictionary representation.

        This method serializes the PredictionDTO object to a dictionary format
        suitable for JSON conversion, ensuring nested objects are also properly
        serialized.

        Returns:
            dict: A dictionary containing the prediction data with keys:
                  - 'sensor_productor': The serialized sensor data
                  - 'classificazione': The classification result
        """
        return {
            'classificazione': self.classificazione,
            'gps_latitude': self.posizione_gps_latitude,
            'gps_longitude': self.posizione_gps_longitude,
            'strada_rilevamento': self.strada_rilevamento
        }
