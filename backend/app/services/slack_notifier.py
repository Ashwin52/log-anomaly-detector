import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(service_name: str, severity: str, anomaly_score: float, error_rate: float, message: str):
    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL not set — skipping Slack notification")
        return

    severity_emoji = {
        "critical": "🔴",
        "warning": "🟡",
        "info": "🔵"
    }
    emoji = severity_emoji.get(severity, "⚪")

    payload = {
        "text": (
            f"{emoji} *Anomaly Alert — {severity.upper()}*\n"
            f"*Service:* {service_name}\n"
            f"*Anomaly Score:* {anomaly_score:.3f}\n"
            f"*Error Rate:* {error_rate:.1%}\n"
            f"*Details:* {message}"
        )
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"Slack alert sent for {service_name}")
        else:
            print(f"Slack alert failed: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Slack alert error: {e}")