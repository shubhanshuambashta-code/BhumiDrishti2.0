from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db import get_db
from app.api.deps import get_current_user, require_role
from app.services.alerts import list_alerts, acknowledge_alert

router = APIRouter()

@router.get('/')
def get_alerts(project_id: Optional[str] = None, unread_only: bool = False, limit: int = 50, offset: int = 0, db: Session = Depends(get_db), user = Depends(get_current_user)):
    total, rows = list_alerts(db, project_id=project_id, unread_only=unread_only, limit=limit, offset=offset)
    return {'total': total, 'rows': [ { 'id': r.id, 'project_id': r.project_id, 'alert_type': r.alert_type, 'message': r.message, 'severity': r.severity, 'created_at': r.created_at.isoformat(), 'read': r.read, 'meta': r.meta } for r in rows ]}

@router.post('/{alert_id}/ack')
def ack_alert(alert_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    a = acknowledge_alert(db, alert_id)
    if not a:
        raise HTTPException(status_code=404, detail='Alert not found')
    # audit logging will be handled by caller or can be added here
    return {'status':'ok', 'alert': {'id': a.id, 'read': a.read}}
