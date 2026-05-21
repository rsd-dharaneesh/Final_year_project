import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK = os.getenv("SLACK_WEBHOOK")

def send_alert(email: dict):
    if not WEBHOOK:
        return

    text = (
        ":rotating_light: *Phishing Detected*\n"
        f"*From:* {email.get('from')}\n"
        f"*Subject:* {email.get('subject')}\n"
        f"*Score:* {email.get('rule_score')}\n"
        f"*Rules:* {', '.join(email.get('rule_hits', []))}"
    )

    requests.post(WEBHOOK, json={"text": text})
