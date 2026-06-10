from fastapi import FastAPI
from app.database import engine, Base
from app.models import log_event
from app.api import logs

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Log Anomaly Detector",
    description="Real-time log ingestion and anomaly detection API",
    version="0.1.0"
)

app.include_router(logs.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Log Anomaly Detector is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
