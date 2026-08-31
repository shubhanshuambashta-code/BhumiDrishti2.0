from fastapi import APIRouter, HTTPException
from fastapi import Body
import pandas as pd
import os
from typing import List

from app.services.predict import predict_project

router = APIRouter()

DATA_PATH = os.path.join(os.getcwd(), "data", "projects_demo.csv")

@router.get("/projects")
def list_projects(limit: int = 50, offset: int = 0):
    """Return sample list of projects (DEMO DATA)."""
    if not os.path.exists(DATA_PATH):
        return {"message": "Demo data not found. Run ml/generate_demo.py to create data/projects_demo.csv"}
    df = pd.read_csv(DATA_PATH)
    total = len(df)
    rows = df.iloc[offset:offset+limit].to_dict(orient="records")
    # mark as demonstration data
    for r in rows:
        r["_demo_data_notice"] = "DEMONSTRATION DATA - Not official government data"
    return {"total": total, "rows": rows}

@router.get("/projects/{project_id}")
def get_project(project_id: str):
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Demo data not found")
    df = pd.read_csv(DATA_PATH)
    row = df[df["project_id"] == project_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Project not found")
    rec = row.iloc[0].to_dict()
    rec["_demo_data_notice"] = "DEMONSTRATION DATA - Not official government data"
    return rec

@router.post("/predict")
def predict(payload: dict = Body(...)):
    """Predict delay probability for a single project payload."""
    result = predict_project(payload)
    return result

@router.post("/predict/batch")
def predict_batch(payload: List[dict] = Body(...)):
    results = []
    for p in payload:
        results.append(predict_project(p))
    return {"results": results}
