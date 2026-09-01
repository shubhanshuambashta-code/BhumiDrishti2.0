from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.api.deps import get_current_user
from app.services.explain import generate_shap_explanation

router = APIRouter()

@router.get('/projects/{project_id}/explain-enhanced')
def api_explain_enhanced(project_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Return a SHAP-like explanation payload (chart base64 + top contributors).
    This implementation is deterministic and lightweight (no heavy ML deps) so the UI can render visual explanations.
    """
    data = generate_shap_explanation(project_id)
    return data
