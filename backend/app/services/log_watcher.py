import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.database import SessionLocal
from app.services.ingestion import ingest_log_line

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file = open(filepath, "r")
        self.file.seek(0, 2)  # seek to end of file

    def on_modified(self, event):
        if event.src_path != self.filepath:
            return
        db = SessionLocal()
        try:
            for line in self.file:
                if line.strip():
                    ingest_log_line(line, db)
                    print(f"Ingested: {line.strip()}")
        finally:
            db.close()

def start_watcher(filepath: str):
    filepath = os.path.abspath(filepath)
    print(f"Watching: {filepath}")
    handler = LogFileHandler(filepath)
    observer = Observer()
    observer.schedule(handler, path=os.path.dirname(filepath), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher("../data/sample.log")
