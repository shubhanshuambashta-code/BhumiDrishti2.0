from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project
from app.api.deps import get_current_user
from sqlalchemy import func

router = APIRouter()

@router.get('/stats/dashboard')
def dashboard_stats(db: Session = Depends(get_db), user = Depends(get_current_user)):
    total = db.query(func.count(Project.project_id)).scalar() or 0
    delayed = db.query(func.count(Project.project_id)).filter(Project.delayed == 1).scalar() or 0
    avg_prev_delay = db.query(func.avg(Project.previous_project_delay_rate)).scalar() or 0.0
    affected_families = db.query(func.sum(Project.affected_families)).scalar() or 0
    compensation_pending = db.query(func.sum(Project.compensation_pending)).scalar() or 0
    high_risk = db.query(func.count(Project.project_id)).filter(Project.delayed == 1).scalar() or 0

    return {
        'total_projects': int(total),
        'projects_delayed_count': int(delayed),
        'avg_prev_delay_rate': float(avg_prev_delay) if avg_prev_delay is not None else 0.0,
        'total_affected_families': int(affected_families),
        'compensation_pending_total': int(compensation_pending),
        'high_risk_count': int(high_risk)
    }
