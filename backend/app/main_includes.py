from app.api.routes import projects
from app.api.routes import auth as auth_routes
from app.api.routes import interventions
from app.api.routes import alerts as alerts_routes
from app.api.routes import audit as audit_routes
from app.api.routes import map as map_routes

app.include_router(auth_routes.router, prefix="/api/auth")
app.include_router(projects.router, prefix="/api")
app.include_router(interventions.router, prefix="/api")
app.include_router(alerts_routes.router, prefix="/api/alerts")
app.include_router(audit_routes.router, prefix="/api/audit-logs")
app.include_router(map_routes.router, prefix="/api/map")
