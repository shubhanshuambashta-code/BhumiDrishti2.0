from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UserCreate, Token
from app.core.security import hash_password, create_access_token, verify_password
from app import models
from datetime import timedelta

router = APIRouter()

# NOTE: For demo, create simple in-DB user table via SQLAlchemy's Base? We'll simulate a minimal user store in-memory for now.
_USERS = {}

@router.post('/register', response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.username in _USERS:
        raise HTTPException(status_code=400, detail='User exists')
    _USERS[user.username] = {'username': user.username, 'password': hash_password(user.password), 'role': user.role}
    return {'username': user.username, 'role': user.role}

@router.post('/login', response_model=Token)
def login(form_data: UserCreate):
    u = _USERS.get(form_data.username)
    if not u or not verify_password(form_data.password, u['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    access_token = create_access_token(data={"sub": form_data.username, "role": u['role']})
    return {"access_token": access_token, "token_type": "bearer"}
