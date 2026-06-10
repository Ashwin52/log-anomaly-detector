from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class LogEvent(Base):
    __tablename__ = "log_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    service_name = Column(String(100), nullable=False, index=True)
    log_level = Column(String(20), nullable=False, index=True)
    message = Column(Text, nullable=False)
    anomaly_score = Column(Float, nullable=True)
    is_anomaly = Column(Integer, default=0)

    def __repr__(self):
        return f"<LogEvent {self.service_name} [{self.log_level}] at {self.timestamp}>"
