import psycopg2
import pandas as pd
from ml.features import extract_features

def load_dataset():
    conn = psycopg2.connect(
        host="localhost",
        dbname="phishguard",
        user="phishguard",
        password="phishguard"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT sender, subject, body_html, verdict
        FROM emails
    """)
    cur.execute("""
        SELECT e.sender, e.subject, e.body_html,
        COALESCE(f.label, e.verdict) AS label
        FROM emails e
        LEFT JOIN feedback f ON e.message_id = f.message_id
    """)

    rows = cur.fetchall()
    conn.close()

    X = []
    y = []

    for sender, subject, body_html, label in rows:
        email = {
            "from": sender,
            "subject": subject,
            "body_html": body_html,
        }
        X.append(extract_features(email))
        # y.append(1 if verdict == "suspicious" else 0)
        y.append(1 if label in ("phish", "suspicious") else 0)


    return pd.DataFrame(X).fillna(0), y
