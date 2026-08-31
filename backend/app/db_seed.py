#!/usr/bin/env python3
"""
Seed the Postgres database with projects from data/projects_demo.csv
Creates tables via SQLAlchemy Base.metadata.create_all and bulk-inserts projects.
Also seeds demo users for quick access.
"""
import os
import csv
from sqlalchemy.exc import IntegrityError
from app.db import engine, SessionLocal, Base
from app.models import Project, User
from app.core.security import hash_password

DATA_PATH = os.path.join(os.getcwd(), '..', 'data', 'projects_demo.csv')

DEMO_USERS = [
    {'username': 'superadmin', 'password': 'demoPass123', 'role': 'superadmin'},
    {'username': 'state_admin', 'password': 'demoPass123', 'role': 'state_admin'},
    {'username': 'district_officer', 'password': 'demoPass123', 'role': 'district_admin'},
    {'username': 'project_officer', 'password': 'demoPass123', 'role': 'project_officer'},
    {'username': 'viewer', 'password': 'demoPass123', 'role': 'viewer'}
]


def seed_projects(session):
    if not os.path.exists(DATA_PATH):
        raise SystemExit('Demo CSV not found at %s' % DATA_PATH)
    count = 0
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                # convert numeric fields to appropriate types
                proj_data = {k: (None if r[k]=='' else r[k]) for k in r}
                # SQLAlchemy will try to coerce types; keep strings and let DB handle casting where possible
                proj = Project(**proj_data)
                # set geom if lat/lon
                try:
                    lat = float(r.get('latitude') or 0)
                    lon = float(r.get('longitude') or 0)
                    if lat and lon:
                        proj.geom = f'SRID=4326;POINT({lon} {lat})'
                except Exception:
                    pass
                session.merge(proj)
                count += 1
                if count % 200 == 0:
                    session.commit()
            except IntegrityError:
                session.rollback()
    session.commit()
    print(f'Seeded {count} projects into DB')


def seed_users(session):
    count = 0
    for u in DEMO_USERS:
        try:
            existing = session.query(User).filter(User.username == u['username']).first()
            if existing:
                continue
            hashed = hash_password(u['password'])
            user = User(username=u['username'], hashed_password=hashed, role=u['role'])
            session.add(user)
            count += 1
        except Exception:
            session.rollback()
    session.commit()
    print(f'Seeded {count} demo users into DB')


def main():
    print('Creating tables...')
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    seed_projects(session)
    seed_users(session)
    session.close()

if __name__ == '__main__':
    main()
