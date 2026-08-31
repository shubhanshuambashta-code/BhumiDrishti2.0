#!/usr/bin/env python3
"""
Seed the Postgres database with projects from data/projects_demo.csv
Creates tables via SQLAlchemy Base.metadata.create_all and bulk-inserts projects.
"""
import os
import csv
from sqlalchemy.exc import IntegrityError
from app.db import engine, SessionLocal, Base
from app.models import Project

DATA_PATH = os.path.join(os.getcwd(), '..', 'data', 'projects_demo.csv')


def main():
    print('Creating tables...')
    Base.metadata.create_all(bind=engine)
    if not os.path.exists(DATA_PATH):
        raise SystemExit('Demo CSV not found at %s' % DATA_PATH)
    session = SessionLocal()
    count = 0
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                proj = Project(**{k: (None if r[k]=='' else r[k]) for k in r})
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
    session.close()
    print(f'Seeded {count} projects into DB')

if __name__ == '__main__':
    main()
