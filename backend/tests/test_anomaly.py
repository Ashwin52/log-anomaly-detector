from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_logs():
    response = client.get("/logs/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "logs" in data
    assert "total" in data
    assert len(data["logs"]) <= 5

def test_get_logs_filter_by_level():
    response = client.get("/logs/?level=ERROR&limit=5")
    assert response.status_code == 200
    data = response.json()
    for log in data["logs"]:
        assert log["log_level"] == "ERROR"

def test_train_model():
    response = client.post("/anomaly/train")
    assert response.status_code == 200
    assert "message" in response.json()

def test_score_logs():
    response = client.post("/anomaly/score")
    assert response.status_code == 200
    data = response.json()
    assert "scored" in data
    assert "anomalies_found" in data