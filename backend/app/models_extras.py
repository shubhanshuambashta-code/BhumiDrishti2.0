from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from app.db import Base
from datetime import datetime

class TaskComment(Base):
    __tablename__ = 'task_comments'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False, index=True)
    username = Column(String, nullable=False)
    comment = Column(Text)
    parent_id = Column(Integer, ForeignKey('task_comments.id'), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TaskAttachment(Base):
    __tablename__ = 'task_attachments'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False, index=True)
    filename = Column(String)
    original_name = Column(String)
    uploaded_by = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSONB)
