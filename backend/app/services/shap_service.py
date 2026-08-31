import joblib
import os
import numpy as np
import pandas as pd
import shap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
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


def _get_shap_values(X_df):
    if _model is None:
        _load()
    if _model is None:
        raise RuntimeError('Model artifact not available')
    X_t = _pipeline.transform(X_df) if _pipeline is not None else X_df.values
    # Use TreeExplainer for tree models
    explainer = shap.TreeExplainer(_model)
    shap_values = explainer.shap_values(X_t)
    # shap_values could be list (for multi-class) or array
    if isinstance(shap_values, list):
        # for binary classifier, shap returns [neg, pos] arrays sometimes; choose the explanation for class 1
        try:
            sv = shap_values[1][0]
        except Exception:
            sv = shap_values[0][0]
    else:
        # array-like
        sv = shap_values[0] if shap_values.ndim == 2 else shap_values
    return sv, X_t


def explain_project_enhanced(row: dict, top_k: int = 8):
    """Return enhanced SHAP explanation and a small PNG chart (base64) for a single project dict."""
    if _model is None or _pipeline is None or _feat_names is None:
        _load()
    if _model is None:
        return {'error': 'Model not available for SHAP explanations. Train model first.'}

    df = pd.DataFrame([row])
    # Ensure columns expected by pipeline exist (best-effort)
    try:
        sv, X_t = _get_shap_values(df)
    except Exception as e:
        return {'error': 'SHAP computation failed', 'details': str(e)}

    # Map coefficients to feature names
    if _feat_names is None:
        names = [f'f{i}' for i in range(len(sv))]
    else:
        names = _feat_names

    contribs = list(zip(names, sv))
    contribs_sorted = sorted(contribs, key=lambda x: abs(x[1]), reverse=True)[:top_k]
    positive = [{'feature': n, 'contribution': float(v)} for n, v in contribs_sorted if v > 0]
    negative = [{'feature': n, 'contribution': float(v)} for n, v in contribs_sorted if v <= 0]

    # Create a simple bar chart for top contributors
    labels = [c[0] for c in contribs_sorted]
    values = [c[1] for c in contribs_sorted]

    fig, ax = plt.subplots(figsize=(6, 3))
    colors = ['#d6336c' if v > 0 else '#198754' for v in values]
    ax.barh(range(len(values)), values, color=colors)
    ax.set_yticks(range(len(values)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel('SHAP contribution')
    ax.set_title('Top feature contributions (positive increases risk)')
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    img_data = f"data:image/png;base64,{img_b64}"

    # Try to compute approximate percent contributions relative to absolute sum
    abs_sum = sum(abs(v) for _, v in contribs_sorted) or 1.0
    contributors = []
    for n, v in contribs_sorted:
        contributors.append({'feature': n, 'contribution': float(v), 'pct_of_top': float(round(abs(v)/abs_sum*100,2))})

    return {
        'top_positive_contributors': positive,
        'top_negative_contributors': negative,
        'contributors': contributors,
        'chart_base64': img_data
    }
