from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.anomaly_detector import train_model, score_logs

router = APIRouter(prefix="/anomaly", tags=["anomaly"])

@router.post("/train")
def train(db: Session = Depends(get_db)):
    model = train_model(db)
    return {"message": "Model trained successfully", "model": str(model)}

@router.post("/score")
def score(db: Session = Depends(get_db)):
    result = score_logs(db)
    return result