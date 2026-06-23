from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import engine, Base, SessionLocal
from app.models import log_event, alert
from app.api import logs, anomaly, alerts
from app.services.anomaly_detector import score_logs, load_model

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Log Anomaly Detector",
    description="Real-time log ingestion and anomaly detection API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs.router)
app.include_router(anomaly.router)
app.include_router(alerts.router)

scheduler = BackgroundScheduler()

def scheduled_scoring():
    if load_model() is None:
        print("Skipping scheduled scoring — model not trained yet")
        return
    db = SessionLocal()
    try:
        result = score_logs(db)
        print(f"Scheduled scoring: {result['scored']} windows, {result['anomalies_found']} anomalies found")
    except Exception as e:
        print(f"Scheduled scoring failed: {e}")
    finally:
        db.close()


@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(
        scheduled_scoring,
        "interval",
        seconds=60,
        id="anomaly_scoring",
        misfire_grace_time=30,
        max_instances=1
    )
    scheduler.start()
    print("Background scheduler started — scoring every 60 seconds")

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()

@app.get("/")
def root():
    return {"status": "ok", "message": "Log Anomaly Detector is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}