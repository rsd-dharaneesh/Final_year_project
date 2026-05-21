import psycopg2
from datetime import date

conn = psycopg2.connect(
    host="localhost",
    dbname="phishguard",
    user="phishguard",
    password="phishguard"
)
cur = conn.cursor()

cur.execute("""
INSERT INTO verdict_metrics (bucket, clean, suspicious, alerts)
SELECT
  CURRENT_DATE,
  SUM(CASE WHEN verdict='clean' THEN 1 ELSE 0 END),
  SUM(CASE WHEN verdict='suspicious' THEN 1 ELSE 0 END),
  COUNT(*)
FROM emails
WHERE created_at::date = CURRENT_DATE
ON CONFLICT (bucket)
DO NOTHING
""")

conn.commit()
conn.close()
