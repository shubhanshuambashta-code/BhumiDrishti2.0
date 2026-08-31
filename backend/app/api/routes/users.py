from fastapi import APIRouter, Depends
from app.api.deps import require_role
from app.db import get_db
from sqlalchemy.orm import Session
from app.models import User

router = APIRouter()

@router.get('/')
def list_users(db: Session = Depends(get_db), current=Depends(require_role('superadmin'))):
    rows = db.query(User).all()
    return [{'username': r.username, 'role': r.role, 'full_name': r.full_name, 'email': r.email} for r in rows]
