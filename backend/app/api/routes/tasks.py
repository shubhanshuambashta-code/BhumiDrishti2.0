from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db import get_db
from app.api.deps import get_current_user, require_role
from app.services.tasks import create_task, list_tasks, update_task_status

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_role: str = None
    assigned_user: str = None
    priority: str = 'Medium'
    due_date: str = None

@router.post('/projects/{project_id}/tasks')
def api_create_task(project_id: str, payload: TaskCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    t = create_task(db, username=user.username, project_id=project_id, title=payload.title, description=payload.description, assigned_role=payload.assigned_role, assigned_user=payload.assigned_user, priority=payload.priority, due_date=payload.due_date)
    return {'task': {'id': t.id, 'title': t.title, 'status': t.status}}

@router.get('/projects/{project_id}/tasks')
def api_list_tasks(project_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    rows = list_tasks(db, project_id)
    return {'tasks': [ {'id': r.id, 'title': r.title, 'status': r.status, 'assigned_role': r.assigned_role, 'assigned_user': r.assigned_user, 'priority': r.priority, 'due_date': r.due_date, 'created_at': r.created_at.isoformat()} for r in rows ]}

@router.post('/tasks/{task_id}/status')
def api_update_task(task_id: int, payload: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    status = payload.get('status')
    if not status:
        raise HTTPException(status_code=400, detail='status required')
    t = update_task_status(db, username=user.username, task_id=task_id, status=status)
    if not t:
        raise HTTPException(status_code=404, detail='Task not found')
    return {'task': {'id': t.id, 'status': t.status}}
