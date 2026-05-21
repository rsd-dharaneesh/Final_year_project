import os
import sys

# Ensure repo root is on sys.path so sibling packages (like `alerts`) are
# importable when running this file directly (e.g. `python soc\\consumer.py`).
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from kafka import KafkaConsumer
import psycopg2
import json
from alerts.slack import send_alert


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


conn = psycopg2.connect(
    dbname="phishguard",
    user="phishguard",
    password="phishguard",
    host="localhost"
)
cur = conn.cursor()

consumer = KafkaConsumer(
    "emails.rules_scored",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True, 
    group_id="soc-writer",
    value_deserializer=lambda x: json.loads(x.decode())
)

for msg in consumer:
    e = msg.value
    cur.execute(
        "INSERT INTO emails (message_id, sender, subject, rule_hits, rule_score, verdict, ml_explain) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (
            e.get("message_id"),
            e.get("from"),
            e.get("subject"),
            json.dumps(e.get("rule_hits")),
            e.get("rule_score"),
            e.get("verdict"),
            json.dumps(e.get("ml_explain", {})),
        )
    )
    conn.commit()
    if e.get("verdict") == "suspicious":
        cur.execute(
            "SELECT 1 FROM alerts_sent WHERE message_id=%s",
            (e.get("message_id"),)
        )
        if not cur.fetchone():
            send_alert(e)
            cur.execute(
                "INSERT INTO alerts_sent (message_id) VALUES (%s)",
                (e.get("message_id"),)
            )
            conn.commit()

