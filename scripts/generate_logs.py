import random
from datetime import datetime, timedelta

services = ["auth-service", "payment-service", "inventory-service", "api-gateway", "user-service"]
levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]

messages = {
    "INFO":  ["request processed successfully", "user login successful", "cache hit", "health check ok", "db query completed"],
    "WARN":  ["response time above threshold", "retry attempt 1", "memory usage at 80%", "slow query detected", "rate limit approaching"],
    "ERROR": ["connection timeout", "database unreachable", "null pointer exception", "payment gateway failed", "service unavailable"]
}

def log_line(service, level, message, ts):
    return f"[{ts.strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {service}: {message}\n"

def generate_demo_dataset(filepath, total_lines=3000):
    lines = []
    start_time = datetime.now() - timedelta(hours=2)

    # Normal traffic baseline across all services
    for i in range(total_lines):
        ts = start_time + timedelta(seconds=i * 2)
        service = random.choice(services)
        level = random.choice(levels)
        message = random.choice(messages[level])
        lines.append(log_line(service, level, message, ts))

    # Anomaly 1: Error spike in payment-service (50 consecutive errors)
    spike_start = start_time + timedelta(minutes=40)
    for i in range(50):
        ts = spike_start + timedelta(seconds=i)
        lines.append(log_line("payment-service", "ERROR", "connection timeout", ts))

    # Anomaly 2: Silent service — auth-service goes quiet for a window then resumes
    # (represented by absence — no lines added in that window, demonstrating "too few logs" anomaly)

    # Anomaly 3: Slow degradation — inventory-service WARN flood
    degrade_start = start_time + timedelta(minutes=90)
    for i in range(40):
        ts = degrade_start + timedelta(seconds=i * 3)
        lines.append(log_line("inventory-service", "WARN", "response time above threshold", ts))

    lines.sort(key=lambda l: l[1:20])  # sort by timestamp prefix

    with open(filepath, "w") as f:
        f.writelines(lines)

    print(f"Generated {len(lines)} log lines with 3 injected anomaly patterns at {filepath}")

if __name__ == "__main__":
    generate_demo_dataset("data/sample.log", total_lines=3000)