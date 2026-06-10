import random
import time
from datetime import datetime

services = ["auth-service", "payment-service", "inventory-service", "api-gateway", "user-service"]
levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]  # weighted — more INFO than errors

messages = {
    "INFO":  ["request processed successfully", "user login successful", "cache hit", "health check ok", "db query completed"],
    "WARN":  ["response time above threshold", "retry attempt 1", "memory usage at 80%", "slow query detected", "rate limit approaching"],
    "ERROR": ["connection timeout", "database unreachable", "null pointer exception", "payment gateway failed", "service unavailable"]
}

def generate_log_line():
    service = random.choice(services)
    level = random.choice(levels)
    message = random.choice(messages[level])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{level}] {service}: {message}\n"

def generate_normal_logs(filepath, count=1000):
    with open(filepath, "w") as f:
        for _ in range(count):
            f.write(generate_log_line())
    print(f"Generated {count} normal log lines at {filepath}")

def inject_anomaly(filepath, count=50):
    with open(filepath, "a") as f:
        service = "payment-service"
        for _ in range(count):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] [ERROR] {service}: connection timeout\n")
    print(f"Injected {count} anomalous log lines")

if __name__ == "__main__":
    filepath = "data/sample.log"
    generate_normal_logs(filepath, 1000)
    inject_anomaly(filepath, 50)
    print("Done! Check data/sample.log")
