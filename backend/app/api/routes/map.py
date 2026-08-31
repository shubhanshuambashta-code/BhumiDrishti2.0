from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Project

router = APIRouter()

@router.get('/projects')
def map_projects(db: Session = SessionLocal()):
    # Return GeoJSON FeatureCollection of projects
    from geoalchemy2.shape import to_shape
    features = []
    q = db.query(Project).filter(Project.latitude.isnot(None)).all()
    for p in q:
        geom = None
        try:
            if p.geom:
                shape = to_shape(p.geom)
                geom = {'type': 'Point', 'coordinates': [shape.x, shape.y]}
        except Exception:
            geom = {'type': 'Point', 'coordinates': [p.longitude or 0, p.latitude or 0]}
        props = {
            'project_id': p.project_id,
            'project_name': p.project_name,
            'district': p.district,
            'state': p.state,
            'current_stage': p.current_stage,
            'risk_category': 'DEMO'  # risk category can be computed on client or via API
        }
        features.append({'type':'Feature', 'geometry': geom, 'properties': props})
    return {'type':'FeatureCollection', 'features': features}
