import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] ([\w-]+): (.+)'
)

def parse_log_line(line: str) -> dict | None:
    line = line.strip()
    if not line:
        return None
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    timestamp_str, level, service, message = match.groups()
    return {
        "timestamp": datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"),
        "log_level": level,
        "service_name": service,
        "message": message
    }

def parse_log_file(filepath: str) -> list[dict]:
    parsed = []
    with open(filepath, "r") as f:
        for line in f:
            result = parse_log_line(line)
            if result:
                parsed.append(result)
    return parsed

if __name__ == "__main__":
    results = parse_log_file("../data/sample.log")
    print(f"Parsed {len(results)} log lines")
    print("Sample:", results[0])
    print("Sample:", results[-1])
