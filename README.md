# BHUMIDRISHTI

AI-Powered Predictive Land Acquisition Risk & Decision Support Platform

This repository is a working prototype for the Smart India Hackathon 2026. It implements a multi-service web application with a FastAPI backend, ML pipeline (XGBoost), and a Next.js frontend (skeleton). The dataset used is synthetic DEMONSTRATION data and clearly marked as such.

Phase 1: Repository skeleton, demo data generator, ML training pipeline, FastAPI skeleton, Docker Compose.

Quick start (development):

1. Copy environment variables from .env.example to .env and edit as needed.
2. Generate demo data and train a starter model:
   - python3 -m venv .venv && source .venv/bin/activate
   - pip install -r backend/requirements.txt
   - python ml/generate_demo.py --n 2000 --out data/projects_demo.csv
   - python ml/train.py --data data/projects_demo.csv --out ml/models/model_v1.joblib
3. Run backend locally:
   - cd backend
   - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Or with Docker Compose:

  docker compose up --build

Note: This is Phase 1. Additional features (frontend, PostGIS, full authentication, RBAC, Redis/Celery, SHAP explainability, GIS map, etc.) will be implemented in subsequent phases.

DEMONSTRATION DATA NOTICE: data/projects_demo.csv is synthetic demonstration data for the prototype only. Not official government data.
