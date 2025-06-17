from flask import Blueprint, jsonify, request
from app.dto.sensor_dto import SensorDTO
from app.services.sensor_service import SensorService

sensor_bp = Blueprint('sensors', __name__)



@sensor_bp.route('/sensors', methods=['POST'])
def create_sensor():
    # Opzione 1: Validazione automatica
    result, status_code = SensorService.validate_and_create_sensor(request.json)
    return jsonify(result), status_code


@sensor_bp.route('/sensors/<id>', methods=['GET'])
def get_sensor(id):
    '''get sensor by id'''
    result, status_code = SensorService.get_sensor(id)
    return jsonify(result), status_code


@sensor_bp.route('/sensors', methods=['GET'])
def get_all_sensors():
    '''get all sensors'''
    result, status_code = SensorService.get_all_sensors()
    return jsonify(result), status_code

@sensor_bp.route('/sensors/<id>', methods=['DELETE'])
def remove_sensor(id):
    '''remove sensor by id'''
    result, status_code = SensorService.remove_sensor(id)
    return jsonify(result), status_code

@sensor_bp.route('/sensors/<id>', methods=['POST'])
def update_sensor(id):
    '''update sensor by id'''
    result, status_code = SensorService.update_sensor(request.json)
    return jsonify(result), status_code

