# Log Anomaly Detector

Real-time log ingestion and ML-powered anomaly detection system.

## Tech Stack
- FastAPI + PostgreSQL
- SQLAlchemy ORM
- Isolation Forest (scikit-learn) — coming Week 3
- React Dashboard — coming Week 5

## Features
- Ingest log files via API
- Real-time file watcher
- Filter logs by service and level
- Anomaly scoring (in progress)

## Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
