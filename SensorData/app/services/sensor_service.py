import datetime
from ..models.sensor import Sensor,Status
from ..dto.sensor_dto import SensorDTO  # Import the DTO class
from ..utils.sensor_utl import SensorUTL

#classe di servizio per mappare i sensori
class SensorService:
    """Service class for sensor operations"""

    @staticmethod
    def add_sensor(sensor_dto: SensorDTO):
        """Creates a new sensor"""
        try:
            # Create an instance to call the method
            sensor_model = SensorUTL.to_model(sensor_dto)

            # Convert DTO status string to Status enum
            status_enum = Status.ACTIVE  # Default
            if sensor_dto.status:
                status_enum = Status(sensor_dto.status)

            # Create a new sensor using factory method
            sensor_model.status = status_enum
            # Save the sensor
            added_sensor_id = sensor_model.save()

            result = SensorDTO(added_sensor_id,sensor_dto.serialNumber,sensor_dto.model,sensor_dto.status)
            return result.to_dict(), 201

        except ValueError as ve:
            return {'error': f'Invalid status value: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Failed to create sensor: {str(e)}'}, 500

    @staticmethod
    def get_sensor(sensor_id: str):
        """Retrieves a sensor by ID and returns as DTO"""
        try:
            sensor_founded = Sensor.find_by_sensor_id(sensor_id)

            if sensor_founded:
                # Convert database result to DTO format
                result = SensorUTL.to_dto(sensor_founded)
                # Note: you'll need to implement a method to get full sensor data
                return result.to_dict(), 200
            else:
                return {'error': 'Sensor not found'}, 404

        except Exception as e:
            return {'error': f'Failed to retrieve sensor: {str(e)}'}, 500



    @staticmethod
    def update_sensor_status(id,status):
        """Updates an existing sensor"""
        try:
            # Check if sensor exists
            sensor_model = Sensor.find_by_sensor_id(id)
            if not sensor_model or sensor_model is None:
                return {'error': 'Sensor not found'}, 404

            # Convert DTO status string to Status enum
            status_enum = Status.ACTIVE  # Default
            if sensor_model.status:
                status_enum = Status(sensor_model.status)

            # Create updated sensor object
            sensor_model.status = status_enum


            # Save (will update since it exists)
            sensor_model.save()
            result = SensorUTL.to_dto(sensor_model)
            return result, 200

        except ValueError as ve:
            return {'error': f'Invalid status value: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Failed to update sensor: {str(e)}'}, 500

    @staticmethod
    def validate_and_create_sensor(json_data):
        """Validates JSON data and creates sensor if valid"""
        # Use DTO validation
        result = SensorDTO.from_request(json_data)

        if isinstance(result, tuple) and result[0] == "ValidationError":
            return {'error': 'Validation failed', 'details': result[1]}, 400

        # If validation passed, result is a SensorDTO
        return SensorService.add_sensor(result)

    @staticmethod
    def delete_sensor(sensor_id: str):
        """Deletes a sensor (sets status to INACTIVE)"""
        try:

            # Check if sensor exists
            existing = Sensor.find_by_sensor_id(sensor_id)
            if not existing or existing is None:
                return {'error': 'Sensor not found'}, 404


            return {'message': 'Sensor deactivated successfully'}, 200

        except Exception as e:
            return {'error': f'Failed to delete sensor: {str(e)}'}, 500


    @classmethod
    def get_all_sensors(cls):
        row_dto_list = []
        records = Sensor.find_all()
        for row in records:

            row_dto = SensorUTL.to_dto(row)
            row_dto_list.append(row_dto.to_dict())  # to_dict() qui, non prima

        return row_dto_list,200


    #attenzione perché qui restituisce un dict, quindi il dato trattalo come tale
    @classmethod
    def get_dati_sensore(cls, sensor_id):
        row_tuple = Sensor.find_by_sensor_id(sensor_id)
        result = SensorUTL.to_dto(row_tuple)
        if not result or result is None:
            return {'error': 'Sensor not found'}, 404

        return result.to_dict(),200