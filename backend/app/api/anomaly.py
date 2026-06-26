from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.anomaly_detector import train_model, score_logs
from app.models.log_event import LogEvent

router = APIRouter(prefix="/anomaly", tags=["anomaly"])

@router.post("/train")
def train(db: Session = Depends(get_db)):
    model = train_model(db)
    return {"message": "Model trained successfully", "model": str(model)}

@router.post("/score")
def score(db: Session = Depends(get_db)):
    result = score_logs(db)
    return result

@router.get("/history")
def anomaly_history(db: Session = Depends(get_db)):
    logs = db.query(LogEvent).filter(
        LogEvent.anomaly_score.isnot(None)
    ).order_by(LogEvent.timestamp.asc()).limit(200).all()

    return [
        {
            "timestamp": log.timestamp,
            "service_name": log.service_name,
            "anomaly_score": log.anomaly_score,
            "is_anomaly": log.is_anomaly
        }
        for log in logs
    ]