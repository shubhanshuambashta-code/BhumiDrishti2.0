from pydantic import BaseModel
from typing import Optional, Any

class ProjectBase(BaseModel):
    project_id: str
    project_name: Optional[str]

class ProjectOut(ProjectBase):
    project_type: Optional[str]
    department: Optional[str]
    state: Optional[str]
    district: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    delayed: Optional[int]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = 'viewer'

class UserOut(BaseModel):
    username: str
    role: str

