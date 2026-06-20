from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from sqlalchemy.sql import func
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    service_name = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)
    anomaly_score = Column(Float, nullable=False)
    error_rate = Column(Float, nullable=True)
    window_start = Column(DateTime(timezone=True), nullable=True)
    message = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Alert {self.service_name} [{self.severity}] at {self.triggered_at}>"