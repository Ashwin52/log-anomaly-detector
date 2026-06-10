from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.log_event import LogEvent
from app.services.ingestion import ingest_log_file

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/")
def get_logs(
    level: str = Query(None),
    service: str = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    query = db.query(LogEvent)
    if level:
        query = query.filter(LogEvent.log_level == level.upper())
    if service:
        query = query.filter(LogEvent.service_name == service)
    total = query.count()
    logs = query.order_by(LogEvent.timestamp.desc()).offset(offset).limit(limit).all()
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "logs": [
            {
                "id": l.id,
                "timestamp": l.timestamp,
                "service_name": l.service_name,
                "log_level": l.log_level,
                "message": l.message,
                "anomaly_score": l.anomaly_score,
                "is_anomaly": l.is_anomaly
            } for l in logs
        ]
    }

@router.post("/ingest-file")
def ingest_file(filepath: str = Query(...), db: Session = Depends(get_db)):
    count = ingest_log_file(filepath, db)
    return {"message": f"Ingested {count} log lines", "count": count}
