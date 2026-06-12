import os
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from app.services.feature_extractor import extract_features, get_feature_matrix

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

def train_model(db: Session) -> IsolationForest:
    features = extract_features(db)
    if features.empty:
        raise ValueError("No data to train on")

    X = get_feature_matrix(features)
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )
    model.fit(X)
    joblib.dump(model, MODEL_PATH)
    print(f"Model trained on {len(X)} samples and saved to {MODEL_PATH}")
    return model

def load_model() -> IsolationForest | None:
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def score_logs(db: Session) -> dict:
    model = load_model()
    if not model:
        raise ValueError("Model not trained yet. Call /anomaly/train first.")

    features = extract_features(db)
    if features.empty:
        return {"scored": 0}

    X = get_feature_matrix(features)
    scores = model.score_samples(X)
    predictions = model.predict(X)

    features["anomaly_score"] = scores
    features["is_anomaly"] = (predictions == -1).astype(int)

    from app.models.log_event import LogEvent
    for _, row in features.iterrows():
        db.query(LogEvent).filter(
            LogEvent.service_name == row["service_name"],
            LogEvent.timestamp >= row["minute"]
        ).update({
            "anomaly_score": float(row["anomaly_score"]),
            "is_anomaly": int(row["is_anomaly"])
        })
    db.commit()

    anomalies = features[features["is_anomaly"] == 1]
    return {
        "scored": len(features),
        "anomalies_found": len(anomalies),
        "anomalies": anomalies[["service_name", "minute", "error_rate", "anomaly_score"]].to_dict(orient="records")
    }