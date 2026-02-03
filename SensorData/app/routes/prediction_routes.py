from flask import Blueprint, jsonify, request

from ..services.prediction_service import PredictionService
from ..ml_model.model_loader import model,model_info


predict_bp = Blueprint('predict', __name__)

#depency injection della classe di servizio

service = PredictionService(model, model_info)

@predict_bp.route('/model', methods=['POST'])
def  classifica():
    json_data = request.json  # Ottiene i dati JSON come dizionario
    result, status = PredictionService.validate_json_request(json_data,service)
    return jsonify(result),status