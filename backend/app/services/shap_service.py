import joblib
import os
import numpy as np
import pandas as pd
import shap
from app.core.config import settings

_model = None
_pipeline = None
_feat_names = None


def _load():
    global _model, _pipeline, _feat_names
    model_path = settings.MODEL_PATH
    if not os.path.exists(model_path):
        return False
    artifact = joblib.load(model_path)
    if isinstance(artifact, dict):
        _model = artifact.get('model')
        _pipeline = artifact.get('pipeline')
    else:
        _model = artifact
    # attempt to get feature names
    try:
        num_features = []
        cat_features = []
        if hasattr(_pipeline, 'transformers_'):
            # ColumnTransformer
            for name, trans, cols in _pipeline.transformers_:
                if name == 'num':
                    num_features = list(cols)
                if name == 'cat':
                    # obtain ohe
                    ohe = trans.named_steps.get('ohe')
                    cats = ohe.get_feature_names_out(cols)
                    cat_features = list(cats)
        _feat_names = num_features + cat_features
    except Exception:
        _feat_names = None
    return True


def explain_project_shap(row: dict, top_k: int = 8):
    if _model is None:
        _load()
    if _model is None:
        return {'error': 'Model not available for SHAP explanations. Train model first.'}

    df = pd.DataFrame([row])
    # ensure required columns exist
    # select the same columns used during training
    try:
        X = df
        X_t = _pipeline.transform(X)
        # Use TreeExplainer for XGBoost
        explainer = shap.TreeExplainer(_model)
        shap_values = explainer.shap_values(X_t)
        # shap_values is array (n_classes?) For binary, shap_values shape may be (n_features,)
        # For XGBoost binary: shap_values is array of shape (n_samples, n_features)
        sv = shap_values[0] if isinstance(shap_values, list) else shap_values[0]
        # map to feature names
        if _feat_names is None:
            # fallback names
            names = [f'f{i}' for i in range(len(sv))]
        else:
            names = _feat_names
        contribs = list(zip(names, sv))
        # sort by absolute contribution
        contribs_sorted = sorted(contribs, key=lambda x: abs(x[1]), reverse=True)[:top_k]
        positive = [(n, float(v)) for n, v in contribs_sorted if v > 0]
        negative = [(n, float(v)) for n, v in contribs_sorted if v <= 0]
        return {
            'top_positive_contributors': positive,
            'top_negative_contributors': negative,
            'feature_names': names
        }
    except Exception as e:
        return {'error': 'SHAP explain failed', 'details': str(e)}
