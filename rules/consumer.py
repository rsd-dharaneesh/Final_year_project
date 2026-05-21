from kafka import KafkaConsumer
from ingestion.producer import send
from rules.engine import evaluate
import json

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


consumer = KafkaConsumer(
    "emails.raw",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for msg in consumer:
    email = msg.value
    result = evaluate(email)
    send("emails.rules_scored", {**email, **result})
