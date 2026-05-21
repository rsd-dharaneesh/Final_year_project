import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    dbname="phishguard",
    user="phishguard",
    password="phishguard"
)

df = pd.read_sql("""
SELECT subject, created_at
FROM emails
WHERE created_at > NOW() - INTERVAL '7 days'
""", conn)

avg_len = df["subject"].str.len().mean()

if avg_len > 120:
    print("⚠️ Drift warning: unusually long subjects")

conn.close()
