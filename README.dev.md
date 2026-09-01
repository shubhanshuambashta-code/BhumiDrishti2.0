# Development README additions

## Local development using docker-compose

I included a docker-compose.yml that starts Redis, ClamAV, the backend (Python), and the frontend (Node). To start the stack:

1. Ensure Docker and docker-compose (v2) are installed
2. From the repository root run:

   chmod +x scripts/start-dev.sh
   ./scripts/start-dev.sh

3. After services are up:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000

4. Seed sample data (optional):
   ./scripts/seed.sh

Notes
- The backend will install Python deps from backend/requirements.txt on container start; this may take a minute the first time.
- Environment variables:
  - REDIS_URL (set in compose to redis://redis:6379/0)
  - CLAMD_HOST/CLAMD_PORT (compose sets to clamav:3310)
  - EXPLAIN_CACHE_TTL (defaults to 3600)

