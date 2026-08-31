import os
import joblib
import numpy as np
import pandas as pd
from app.core.config import settings

_model = None
_pipeline = None

def _load_model_and_pipeline():
    global _model, _pipeline
    model_path = settings.MODEL_PATH
    if os.path.exists(model_path):
        try:
            obj = joblib.load(model_path)
            # obj can be a dict with keys 'model' and 'pipeline'
            if isinstance(obj, dict):
                _pipeline = obj.get('pipeline')
                _model = obj.get('model')
            else:
                _model = obj
            return True
        except Exception as e:
            print("Failed to load model:", e)
            return False
    return False


def predict_project(project: dict):
    """Return prediction with probability and risk score. If trained model not found, fall back to heuristic."""
    if _model is None:
        _load_model_and_pipeline()
    # convert single record to DataFrame
    df = pd.DataFrame([project])
    # basic preprocessing for required numeric fields
    numeric_cols = [
        'pending_approvals', 'legal_disputes', 'compensation_pending_percentage',
        'possession_percentage', 'affected_families', 'elapsed_days', 'r_and_r_pending_families'
    ]
    for c in numeric_cols:
        if c not in df.columns:
            df[c] = 0
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    # If model loaded, use pipeline
    if _model is not None:
        try:
            X = df if _pipeline is None else _pipeline.transform(df)
            proba = _model.predict_proba(X)[:, 1][0]
        except Exception as e:
            print("Model prediction failed, falling back to heuristic:", e)
            proba = _heuristic_proba(df.iloc[0])
    else:
        proba = _heuristic_proba(df.iloc[0])

    # calibrate to risk score
    risk_score = int(round(proba * 100))
    if risk_score < 30:
        category = 'LOW'
    elif risk_score < 60:
        category = 'MODERATE'
    elif risk_score < 80:
        category = 'HIGH'
    else:
        category = 'CRITICAL'

    return {
        'delay_probability': float(round(proba, 4)),
        'risk_score': risk_score,
        'risk_category': category,
        'note': 'DEMONSTRATION PREDICTION - For demo only. Replace model with production model for official use.'
    }


def _heuristic_proba(row):
    # simple weighted heuristic as fallback
    score = 0.0
    score += min(row.get('pending_approvals', 0) / 10.0, 1.0) * 0.25
    score += min(row.get('legal_disputes', 0) / 5.0, 1.0) * 0.2
    score += (row.get('compensation_pending_percentage', 0)/100.0) * 0.2
    score += (1 - row.get('possession_percentage', 0)/100.0) * 0.15
    score += min(row.get('elapsed_days', 0)/365.0, 1.0) * 0.2
    return float(min(score, 0.9999))
