from marshmallow import Schema, ValidationError, post_load
from flask import request, jsonify


class BaseDTO:
    """Base DTO class for request/response handling"""

    @classmethod
    def from_request(cls):
        """Create DTO from Flask request"""
        try:
            schema = cls.Schema()
            return schema.load(request.json or {})
        except ValidationError as err:
            return {'errors': err.messages}, 400

    @classmethod
    def validate_json(cls, json_data):
        """Validate JSON data"""
        try:
            schema = cls.Schema()
            return schema.load(json_data)
        except ValidationError as err:
            return {'errors': err.messages}, 400

