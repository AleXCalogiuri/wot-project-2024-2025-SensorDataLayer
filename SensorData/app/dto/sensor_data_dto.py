from marshmallow import Schema, fields, ValidationError

from app.dto.base_dto import BaseDTO
from app.models.sensor_data import SensorData

"""
Sensor Data DTO Module

This module defines the Data Transfer Object (DTO) for sensor data.
It handles the serialization and deserialization of sensor data between
the application and external interfaces, including validation of input data.

The sensor data includes readings from accelerometer, gyroscope, and GPS sensors.
"""

class SensorDataDTO(BaseDTO):
    """
    Data Transfer Object for representing sensor data.

    This class handles the serialization and deserialization of sensor data,
    including validation of input data and conversion between JSON and object formats.

    Attributes:
        sensor_data_id (str): Unique identifier for the sensor data.
        timestamp (datetime): Time when the sensor data was recorded.
        accelerometer_x (float): X-axis reading from the accelerometer.
        accelerometer_y (float): Y-axis reading from the accelerometer.
        accelerometer_z (float): Z-axis reading from the accelerometer.
        gyroscope_x (float): X-axis reading from the gyroscope.
        gyroscope_y (float): Y-axis reading from the gyroscope.
        gyroscope_z (float): Z-axis reading from the gyroscope.
        gps_latitude (float): Latitude coordinate from GPS.
        gps_longitude (float): Longitude coordinate from GPS.
    """

    class Schema(Schema):
        """
        Marshmallow schema for validating and serializing SensorDataDTO objects.

        Fields:
            sensorDataId (str): Unique identifier for the sensor data.
            timestamp (datetime): Time when the sensor data was recorded.
            accelerometer_x (float): X-axis reading from the accelerometer.
            accelerometer_y (float): Y-axis reading from the accelerometer.
            accelerometer_z (float): Z-axis reading from the accelerometer.
            gyroscope_x (float): X-axis reading from the gyroscope.
            gyroscope_y (float): Y-axis reading from the gyroscope.
            gyroscope_z (float): Z-axis reading from the gyroscope.
            gps_latitude (float): Latitude coordinate from GPS.
            gps_longitude (float): Longitude coordinate from GPS.
        """
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
                 accelerometer_z, gyroscope_x, gyroscope_y, gyroscope_z,
                 gps_latitude, gps_longitude
                 ):
        """
        Initialize a new SensorDataDTO instance.

        Args:
            sensor_data_id (str): Unique identifier for the sensor data.
            timestamp (datetime): Time when the sensor data was recorded.
            accelerometer_x (float): X-axis reading from the accelerometer.
            accelerometer_y (float): Y-axis reading from the accelerometer.
            accelerometer_z (float): Z-axis reading from the accelerometer.
            gyroscope_x (float): X-axis reading from the gyroscope.
            gyroscope_y (float): Y-axis reading from the gyroscope.
            gyroscope_z (float): Z-axis reading from the gyroscope.
            gps_latitude (float): Latitude coordinate from GPS.
            gps_longitude (float): Longitude coordinate from GPS.
        """
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
    def from_request(cls, json_data=None):
        """
        Parse and validate request data to create a SensorDataDTO instance.

        This method extracts JSON data from the request if not provided,
        validates it using the Schema class, and returns a SensorDataDTO instance.

        Args:
            json_data (dict, optional): JSON data to parse. If None, data is extracted
                                       from the current Flask request. Defaults to None.

        Returns:
            SensorDataDTO: A validated instance if successful.
            tuple: ("ValidationError", error_messages) if validation fails.
        """
        if json_data is None:
            from flask import request
            json_data = request.get_json()
        schema = cls.Schema()
        try:
            return schema.load(json_data)
        except ValidationError as e:
            return "ValidationError", e.messages
