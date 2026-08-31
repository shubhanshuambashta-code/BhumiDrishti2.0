from sqlalchemy.orm import Session
from app.db import get_db
from app.models import AuditLog
from datetime import datetime


def write_audit(db: Session, username: str, action: str, project_id: str = None, old_value: dict = None, new_value: dict = None, meta: dict = None):
    a = AuditLog(username=username, action=action, project_id=project_id, old_value=old_value or {}, new_value=new_value or {}, timestamp=datetime.utcnow(), meta=meta or {})
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def list_audits(db: Session, project_id: str = None, username: str = None, limit: int = 100, offset: int = 0):
    q = db.query(AuditLog)
    if project_id:
        q = q.filter(AuditLog.project_id == project_id)
    if username:
        q = q.filter(AuditLog.username == username)
    total = q.count()
    rows = q.order_by(AuditLog.timestamp.desc()).limit(limit).offset(offset).all()
    return total, rows
