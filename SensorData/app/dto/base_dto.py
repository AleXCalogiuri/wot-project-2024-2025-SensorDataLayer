from marshmallow import Schema, ValidationError, post_load
from flask import request, jsonify

"""
Base DTO Module

This module defines the base Data Transfer Object (DTO) class that provides common
functionality for all DTOs in the application. It handles JSON validation and
request data processing, serving as a foundation for more specific DTO classes.
"""

class BaseDTO:
    """
    Base Data Transfer Object class for request/response handling.

    This abstract base class provides common functionality for all DTOs in the application,
    including methods for creating DTOs from HTTP requests and validating JSON data.
    Subclasses should implement their own Schema inner class for validation rules.
    """

    @classmethod
    def from_request(cls):
        """
        Create a DTO instance from the current Flask request.

        This method extracts JSON data from the current request, validates it using
        the class's Schema, and returns either a valid DTO instance or an error response.

        Returns:
            object: An instance of the DTO class if validation succeeds.
            tuple: A tuple containing an error dictionary and HTTP status code (400) if validation fails.

        Raises:
            ValidationError: Handled internally to return appropriate error responses.
        """
        try:
            schema = cls.Schema()
            return schema.load(request.json or {})
        except ValidationError as err:
            return {'errors': err.messages}, 400

    @classmethod
    def validate_json(cls, json_data):
        """
        Validate JSON data against the class's Schema.

        Args:
            json_data (dict): The JSON data to validate.

        Returns:
            object: An instance of the DTO class if validation succeeds.
            tuple: A tuple containing an error dictionary and HTTP status code (400) if validation fails.

        Raises:
            ValidationError: Handled internally to return appropriate error responses.
        """
        try:
            schema = cls.Schema()
            return schema.load(json_data)
        except ValidationError as err:
            return {'errors': err.messages}, 400
