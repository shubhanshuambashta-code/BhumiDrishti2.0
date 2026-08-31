from sqlalchemy.orm import Session
from app.models import Alert
from datetime import datetime


def create_alert(db: Session, project_id: str, alert_type: str, message: str, severity: str = 'High', meta: dict = None):
    a = Alert(project_id=project_id, alert_type=alert_type, message=message, severity=severity, created_at=datetime.utcnow(), read=False, meta=meta or {})
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def list_alerts(db: Session, project_id: str = None, unread_only: bool = False, limit: int = 100, offset: int = 0):
    q = db.query(Alert)
    if project_id:
        q = q.filter(Alert.project_id == project_id)
    if unread_only:
        q = q.filter(Alert.read == False)
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
