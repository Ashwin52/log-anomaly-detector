from sqlalchemy.orm import Session
from app.models.alert import Alert
from datetime import timedelta

def get_severity(anomaly_score: float) -> str:
    if anomaly_score < -0.6:
        return "critical"
    elif anomaly_score < -0.4:
        return "warning"
    else:
        return "info"

def alert_already_exists(db: Session, service_name: str, window_start) -> bool:
    existing = db.query(Alert).filter(
        Alert.service_name == service_name,
        Alert.window_start == window_start
    ).first()
    return existing is not None

def create_alerts_from_anomalies(db: Session, anomalies: list[dict]) -> list[Alert]:
    created = []
    for anomaly in anomalies:
        if alert_already_exists(db, anomaly["service_name"], anomaly["minute"]):
            continue
        severity = get_severity(anomaly["anomaly_score"])
        alert = Alert(
            service_name=anomaly["service_name"],
            severity=severity,
            anomaly_score=anomaly["anomaly_score"],
            error_rate=anomaly.get("error_rate"),
            window_start=anomaly["minute"],
            message=f"Anomaly detected in {anomaly['service_name']} — error rate {anomaly.get('error_rate', 0):.1%}"
        )
        db.add(alert)
        created.append(alert)
    db.commit()
    for alert in created:
        db.refresh(alert)
    return created