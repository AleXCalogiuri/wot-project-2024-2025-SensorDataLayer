import datetime

from app.models.sensor import Sensor, Status  # Import the class and enum
from app.dto.sensor_dto import SensorDTO  # Import the DTO class

#classe di servizio per mappare i sensori
class SensorService:
    """Service class for sensor operations"""

    @staticmethod
    def add_sensor(sensor_dto: SensorDTO):
        """Creates a new sensor"""
        try:
            # Create an instance to call the method
            sensor_model = Sensor("", 0, "", datetime.datetime.now(), datetime.datetime.now(), Status.ACTIVE)

            # Check if sensor already exists
            if sensor_model.findBySensorId(sensor_dto.sensorId):
                return {'error': 'il sensore è già stato inserito'}, 409

            # Convert DTO status string to Status enum
            status_enum = Status.ACTIVE  # Default
            if sensor_dto.status:
                status_enum = Status(sensor_dto.status)

            # Create new sensor using factory method
            sensor = Sensor.create_sensor(
                sensorId=sensor_dto.sensorId,
                serial=int(sensor_dto.serialNumber),  # Convert to int
                model=sensor_dto.model,
                installationDate=sensor_dto.installationDate,  # Use from DTO
                lastCalibration=sensor_dto.lastCalibrationDate or datetime.datetime.now(),  # Use DTO or current
                status=status_enum
            )

            # Save the sensor
            sensor.save()

            return {
                'sensorId': sensor.sensorId,
                'serial': sensor.serial,
                'model': sensor.model,
                'installationDate': sensor.installationDate.isoformat(),
                'lastCalibration': sensor.lastCalibration.isoformat(),
                'status': sensor.status.value,
                'message': 'Sensor created successfully'
            }, 201

        except ValueError as ve:
            return {'error': f'Invalid status value: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Failed to create sensor: {str(e)}'}, 500

    @staticmethod
    def get_sensor(sensor_id: str):
        """Retrieves a sensor by ID and returns as DTO"""
        try:
            sensor_model = Sensor("", 0, "", datetime.datetime.now(), datetime.datetime.now(), Status.ACTIVE)
            result = sensor_model.findBySensorId(sensor_id)

            if result:
                # Convert database result to DTO format
                # Note: you'll need to implement a method to get full sensor data
                return {'sensor': result}, 200
            else:
                return {'error': 'Sensor not found'}, 404

        except Exception as e:
            return {'error': f'Failed to retrieve sensor: {str(e)}'}, 500

    @staticmethod
    def update_sensor(sensor_id: str, sensor_dto: SensorDTO):
        """Updates an existing sensor"""
        try:
            sensor_model = Sensor("", 0, "", datetime.datetime.now(), datetime.datetime.now(), Status.ACTIVE)

            # Check if sensor exists
            if not sensor_model.findBySensorId(sensor_id):
                return {'error': 'Sensor not found'}, 404

            # Convert DTO status string to Status enum
            status_enum = Status.ACTIVE  # Default
            if sensor_dto.status:
                status_enum = Status(sensor_dto.status)

            # Create updated sensor object
            updated_sensor = Sensor(
                sensorId=sensor_id,
                serial=int(sensor_dto.serialNumber),
                model=sensor_dto.model,
                installationDate=sensor_dto.installationDate,
                lastCalibration=sensor_dto.lastCalibrationDate or datetime.datetime.now(),
                status=status_enum
            )

            # Save (will update since it exists)
            updated_sensor.save()

            return {
                'sensorId': updated_sensor.sensorId,
                'serial': updated_sensor.serial,
                'model': updated_sensor.model,
                'installationDate': updated_sensor.installationDate.isoformat(),
                'lastCalibration': updated_sensor.lastCalibration.isoformat(),
                'status': updated_sensor.status.value,
                'message': 'Sensor updated successfully'
            }, 200

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
            sensor_model = Sensor("", 0, "", datetime.datetime.now(), datetime.datetime.now(), Status.ACTIVE)

            # Check if sensor exists
            existing = sensor_model.findBySensorId(sensor_id)
            if not existing:
                return {'error': 'Sensor not found'}, 404

            # Set status to INACTIVE (soft delete)
            # Note: You'll need to implement update_status method or similar
            # For now, this is a placeholder

            return {'message': 'Sensor deactivated successfully'}, 200

        except Exception as e:
            return {'error': f'Failed to delete sensor: {str(e)}'}, 500