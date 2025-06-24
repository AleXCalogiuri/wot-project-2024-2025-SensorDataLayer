from flask import Flask
from joblib import load
from app.services.prediction_service import PredictionService

app = Flask(__name__)

#carica i modelli all'avvio in modo da non doverli ricaricare ogni volta
model = load('model_multiclass_road_condition.pkl')
model_info = load('model_multiclass_info.pkl')

#Depency injection
prediction_service = PredictionService(model, model_info)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
