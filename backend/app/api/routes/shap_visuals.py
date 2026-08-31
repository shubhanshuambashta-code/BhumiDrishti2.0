from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.services.shap_service import explain_project_enhanced
from app.api.deps import get_current_user

router = APIRouter()

@router.get('/projects/{project_id}/explain-enhanced')
def explain_enhanced(project_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    p = db.query(Project).filter(Project.project_id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail='Project not found')
    row = {c.name: getattr(p, c.name) for c in p.__table__.columns}
    res = explain_project_enhanced(row)
    return res
