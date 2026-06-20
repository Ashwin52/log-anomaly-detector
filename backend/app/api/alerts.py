from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/")
def get_alerts(
    severity: str = Query(None),
    service: str = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity.lower())
    if service:
        query = query.filter(Alert.service_name == service)
    total = query.count()
    alerts = query.order_by(Alert.triggered_at.desc()).offset(offset).limit(limit).all()
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "alerts": [
            {
                "id": a.id,
                "triggered_at": a.triggered_at,
                "service_name": a.service_name,
                "severity": a.severity,
                "anomaly_score": a.anomaly_score,
                "error_rate": a.error_rate,
                "message": a.message
            } for a in alerts
        ]
    }