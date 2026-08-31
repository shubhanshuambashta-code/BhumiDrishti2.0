from sqlalchemy.orm import Session
from app.models import Task
from app.services.audit import write_audit


def create_task(db: Session, username: str, project_id: str, title: str, description: str, assigned_role: str = None, assigned_user: str = None, priority: str = 'Medium', due_date: str = None, meta: dict = None):
    t = Task(project_id=project_id, title=title, description=description, assigned_role=assigned_role, assigned_user=assigned_user, priority=priority, due_date=due_date, status='Open', meta=meta or {})
    db.add(t)
    db.commit()
    db.refresh(t)
    try:
        write_audit(db, username=username, action='create_task', project_id=project_id, old_value={}, new_value={'task_id': t.id, 'title': title, 'assigned': assigned_user or assigned_role})
    except Exception:
        pass
    return t


def list_tasks(db: Session, project_id: str):
    return db.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at.desc()).all()


def update_task_status(db: Session, username: str, task_id: int, status: str):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        return None
    old = {'status': t.status}
    t.status = status
    t.updated_at = t.updated_at
    db.add(t)
    db.commit()
    db.refresh(t)
    try:
        write_audit(db, username=username, action='update_task', project_id=t.project_id, old_value=old, new_value={'status': status})
    except Exception:
        pass
    return t


def claim_task(db: Session, username: str, task_id: int):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        return None
    old = {'assigned_user': t.assigned_user, 'status': t.status}
    t.assigned_user = username
    t.status = 'In Progress'
    db.add(t)
    db.commit()
    db.refresh(t)
    try:
        write_audit(db, username=username, action='claim_task', project_id=t.project_id, old_value=old, new_value={'assigned_user': username, 'status': t.status})
    except Exception:
        pass
    return t


def tasks_for_inbox(db: Session, username: str, role: str):
    # tasks assigned to the user or to the user's role
    q = db.query(Task).filter((Task.assigned_user == username) | (Task.assigned_role == role)).order_by(Task.created_at.desc())
    return q.all()
