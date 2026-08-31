def reassign_task(db: Session, username: str, task_id: int, assigned_role: str = None, assigned_user: str = None):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        return None
    old = {'assigned_role': t.assigned_role, 'assigned_user': t.assigned_user}
    if assigned_role:
        t.assigned_role = assigned_role
    if assigned_user:
        t.assigned_user = assigned_user
    db.add(t)
    db.commit()
    db.refresh(t)
    try:
        write_audit(db, username=username, action='reassign_task', project_id=t.project_id, old_value=old, new_value={'assigned_role': t.assigned_role, 'assigned_user': t.assigned_user})
    except Exception:
        pass
    return t
