from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.api.deps import require_role, get_current_user
from app.services.audit import list_audits

router = APIRouter()

@router.get('/')
def get_audit_logs(project_id: str = None, username: str = None, limit: int = 50, offset: int = 0, db: Session = Depends(get_db), user = Depends(require_role('superadmin'))):
    total, rows = list_audits(db, project_id=project_id, username=username, limit=limit, offset=offset)
    return {'total': total, 'rows': [ { 'id': r.id, 'username': r.username, 'action': r.action, 'project_id': r.project_id, 'old_value': r.old_value, 'new_value': r.new_value, 'timestamp': r.timestamp.isoformat(), 'meta': r.meta } for r in rows ]}
