import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.models.log_event import LogEvent

def extract_features(db: Session, window_minutes: int = 5) -> pd.DataFrame:
    logs = db.query(LogEvent).all()
    if not logs:
        return pd.DataFrame()

    df = pd.DataFrame([{
        "id": l.id,
        "timestamp": l.timestamp,
        "service_name": l.service_name,
        "log_level": l.log_level,
    } for l in logs])

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["minute"] = df["timestamp"].dt.floor(f"{window_minutes}min")
    df["is_error"] = (df["log_level"] == "ERROR").astype(int)
    df["is_warn"] = (df["log_level"] == "WARN").astype(int)

    features = df.groupby(["service_name", "minute"]).agg(
        total_logs=("id", "count"),
        error_count=("is_error", "sum"),
        warn_count=("is_warn", "sum"),
    ).reset_index()

    features["error_rate"] = features["error_count"] / features["total_logs"]
    features["warn_rate"] = features["warn_count"] / features["total_logs"]

    return features

def get_feature_matrix(features: pd.DataFrame) -> np.ndarray:
    cols = ["total_logs", "error_count", "warn_count", "error_rate", "warn_rate"]
    return features[cols].values
