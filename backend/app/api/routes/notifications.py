from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db import get_db
from app.api.deps import get_current_user
from app.services.alerts import list_alerts, acknowledge_alert

router = APIRouter()

@router.get('/')
def get_notifications(unread_only: bool = True, limit: int = 20, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # fetch alerts assigned to this user or their role
    assigned_to = user.username or user.role
    total, rows = list_alerts(db, assigned_to=assigned_to, unread_only=unread_only, limit=limit)
    return {'total': total, 'rows': [ { 'id': r.id, 'project_id': r.project_id, 'alert_type': r.alert_type, 'message': r.message, 'severity': r.severity, 'created_at': r.created_at.isoformat(), 'read': r.read, 'assigned_role': r.assigned_role, 'assigned_user': r.assigned_user } for r in rows ]}

@router.post('/{alert_id}/read')
def mark_read(alert_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    a = acknowledge_alert(db, alert_id)
    if not a:
        raise HTTPException(status_code=404, detail='Notification not found')
    return {'status': 'ok', 'alert': {'id': a.id, 'read': a.read}}
