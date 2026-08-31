from sqlalchemy.orm import Session
from app.models import Alert
from datetime import datetime


def create_alert(db: Session, project_id: str, alert_type: str, message: str, severity: str = 'High', meta: dict = None, assigned_role: str = None, assigned_user: str = None):
    a = Alert(project_id=project_id, alert_type=alert_type, message=message, severity=severity, created_at=datetime.utcnow(), read=False, meta=meta or {}, assigned_role=assigned_role, assigned_user=assigned_user)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def list_alerts(db: Session, project_id: str = None, unread_only: bool = False, assigned_to: str = None, limit: int = 100, offset: int = 0):
    q = db.query(Alert)
    if project_id:
        q = q.filter(Alert.project_id == project_id)
    if unread_only:
        q = q.filter(Alert.read == False)
    if assigned_to:
        # assigned_to can be a role (e.g., 'project_officer') or username; match either
        q = q.filter((Alert.assigned_role == assigned_to) | (Alert.assigned_user == assigned_to))
    total = q.count()
    rows = q.order_by(Alert.created_at.desc()).limit(limit).offset(offset).all()
    return total, rows


def acknowledge_alert(db: Session, alert_id: int):
    a = db.query(Alert).filter(Alert.id == alert_id).first()
    if not a:
        return None
    a.read = True
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def assign_alert(db: Session, alert_id: int, assigned_role: str = None, assigned_user: str = None):
    a = db.query(Alert).filter(Alert.id == alert_id).first()
    if not a:
        return None
    if assigned_role:
        a.assigned_role = assigned_role
    if assigned_user:
        a.assigned_user = assigned_user
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
