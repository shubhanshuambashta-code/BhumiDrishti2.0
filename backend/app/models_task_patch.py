class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    assigned_role = Column(String, nullable=True)
    assigned_user = Column(String, nullable=True)
    priority = Column(String, default='Medium')
    due_date = Column(String, nullable=True)
    status = Column(String, default='Open')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSONB)
