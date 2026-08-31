from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.services.predict import predict_project
from app.services.recommendation import recommend_for_project
from app.api.deps import get_current_user

router = APIRouter()

@router.post('/projects/{project_id}/intervene')
def intervene(project_id: str, adjustments: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(Project).filter(Project.project_id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail='Project not found')
    # merge adjustments into project dict
    proj_dict = {c.name: getattr(p, c.name) for c in p.__table__.columns}
    proj_dict.update(adjustments)
    # run prediction before and after
    before = predict_project(proj_dict)
    after = predict_project(proj_dict)
    # Note: predict_project uses provided fields; adjustments should alter risk
    return {'before': before, 'after': after, 'delta_score': before['risk_score'] - after['risk_score']}

@router.get('/projects/{project_id}/recommend')
def recommend(project_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.query(Project).filter(Project.project_id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail='Project not found')
    proj_dict = {c.name: getattr(p, c.name) for c in p.__table__.columns}
    recs = recommend_for_project(proj_dict)
    return {'recommendations': recs}
