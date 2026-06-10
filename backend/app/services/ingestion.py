from sqlalchemy.orm import Session
from app.models.log_event import LogEvent
from app.services.log_parser import parse_log_file, parse_log_line

def ingest_log_file(filepath: str, db: Session) -> int:
    parsed_logs = parse_log_file(filepath)
    count = 0
    for log in parsed_logs:
        event = LogEvent(
            timestamp=log["timestamp"],
            log_level=log["log_level"],
            service_name=log["service_name"],
            message=log["message"]
        )
        db.add(event)
        count += 1
    db.commit()
    return count

def ingest_log_line(line: str, db: Session) -> LogEvent | None:
    parsed = parse_log_line(line)
    if not parsed:
        return None
    event = LogEvent(
        timestamp=parsed["timestamp"],
        log_level=parsed["log_level"],
        service_name=parsed["service_name"],
        message=parsed["message"]
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
