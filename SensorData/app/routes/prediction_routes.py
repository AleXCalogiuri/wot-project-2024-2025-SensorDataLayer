from flask import Blueprint, jsonify, request
from app.dto.prediction_request_dto import PredictRequestDTO
from app.services.prediction_service import PredictionService

sensor_bp = Blueprint('predict', __name__)

@sensor_bp.route('/model', methods=['POST'])
def  classifica():

    result,status = PredictionService.send_prediction(request.json)
    return jsonify(result),status