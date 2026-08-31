#!/usr/bin/env bash
set -e

# Usage: ./scripts/seed.sh
python3 -m venv .venv || true
source .venv/bin/activate
pip install -r backend/requirements.txt
python ml/generate_demo.py --n 2000 --out data/projects_demo.csv
python ml/train.py --data data/projects_demo.csv --out ml/models/model_v1.joblib

echo "Seed completed. Start backend: uvicorn backend.app.main:app --reload --port 8000"
