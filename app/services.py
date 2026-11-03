import joblib
import numpy as np
import os
from typing import Tuple

_model = None

def load_model():
    global _model
    model_path = os.path.join('models', 'modelo_manutencao.joblib')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
    _model = joblib.load(model_path)
    print("✅ Modelo carregado na memória RAM")
    return _model

def get_model():
    if _model is None:
        raise RuntimeError("Modelo não carregado. Execute load_model() primeiro.")
    return _model

def predict_failure(data: dict) -> Tuple[int, float]:
    model = get_model()
    features = np.array([[
        data['temperatura_ar_k'],
        data['temperatura_processo_k'],
        data['velocidade_rotacao_rpm'],
        data['torque_nm'],
        data['desgaste_ferramenta_min']
    ]])
    prediction = model.predict(features)[0]
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(features)[0]
        confidence = float(max(proba))
    else:
        confidence = 1.0
    return int(prediction), confidence