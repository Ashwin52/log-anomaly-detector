from fastapi import FastAPI

app = FastAPI(
    title="Log Anomaly Detector",
    description="Real-time log ingestion and anomaly detection API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Log Anomaly Detector is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
