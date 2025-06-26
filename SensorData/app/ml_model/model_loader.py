#questa classe carica il modello nel progetto

from joblib import load
import os
# Ottieni il percorso della directory corrente del file
current_dir = os.path.dirname(os.path.abspath(__file__))
model_info = os.path.join(current_dir, '..', 'ml_model', 'model_multiclass_road_condition.pkl')
model = load(model_info)

# Oppure, se il file è nella stessa directory:
model_info = os.path.join(current_dir, 'model_multiclass_road_condition.pkl')
model = load(model_info)