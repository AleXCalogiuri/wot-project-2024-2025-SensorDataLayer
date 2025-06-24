#questa classe carica il modello nel progetto

from joblib import load

model = load('model_multiclass_road_condition.pkl')
model_info = load('model_multiclass_info.pkl')
