import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    dbname="phishguard",
    user="phishguard",
    password="phishguard"
)
cur = conn.cursor()

PHISH_SUBJECTS = [
    "URGENT verify account",
    "Action required immediately",
    "Your account is limited",
    "Security alert",
]

CLEAN_SUBJECTS = [
    "Meeting agenda",
    "Invoice attached",
    "Weekly update",
    "Project discussion",
]

for _ in range(30):
    is_phish = random.random() > 0.5
    subject = random.choice(PHISH_SUBJECTS if is_phish else CLEAN_SUBJECTS)

    cur.execute(
        "INSERT INTO emails (sender, subject, verdict) VALUES (%s,%s,%s)",
        (
            "alerts@paypa1-secure.com" if is_phish else "hr@company.com",
            subject,
            "suspicious" if is_phish else "clean",
        )
    )

conn.commit()
conn.close()
print("Bootstrap data inserted")

