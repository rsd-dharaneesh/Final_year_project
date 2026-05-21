from dotenv import load_dotenv
load_dotenv()

import os
import json
import secrets
import logging
import psycopg2

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ---------------- AUTH ----------------
security = HTTPBasic()
SOC_USER = "soc"
SOC_PASS = "soc123"

def auth(creds: HTTPBasicCredentials = Depends(security)):
    if not (
        secrets.compare_digest(creds.username, SOC_USER)
        and secrets.compare_digest(creds.password, SOC_PASS)
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

# ---------------- DB ----------------
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
    )

# ---------------- APP ----------------
app = FastAPI()

# ---------------- DASHBOARD ----------------
@app.get("/", response_class=HTMLResponse, dependencies=[Depends(auth)])
def dashboard():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT message_id, sender, subject, verdict, rule_hits, ml_explain, created_at
        FROM emails
        ORDER BY created_at DESC
        LIMIT 50
    """)
    rows = cur.fetchall()
    conn.close()

    html = """
    <html>
    <head>
      <title>PhishGuard SOC</title>
      <style>
        body { font-family: Arial; background:#0f172a; color:#e5e7eb; }
        table { width:100%; border-collapse: collapse; }
        th, td { padding:8px; border-bottom:1px solid #334155; }
        .bad { color:#ef4444; font-weight:bold; }
        .ok { color:#22c55e; }
        button { margin-right:5px; }
      </style>
    </head>
    <body>
      <h2>PhishGuard SOC Dashboard</h2>
      <table>
        <tr>
          <th>Sender</th>
          <th>Subject</th>
          <th>Verdict</th>
          <th>Rules</th>
          <th>ML Reason</th>
          <th>Time</th>
          <th>Feedback</th>
        </tr>
    """

    for msg_id, sender, subject, verdict, rules, ml_explain, created in rows:
        ml_text = json.dumps(ml_explain) if ml_explain is not None else ''
        html += f"""
        <tr>
          <td>{sender}</td>
          <td>{subject}</td>
          <td class=\"{'bad' if verdict=='suspicious' else 'ok'}\">{verdict}</td>
          <td>{json.dumps(rules)}</td>
          <td>{ml_text}</td>
          <td>{created}</td>
          <td>
            <button onclick="sendFeedback('{msg_id}','phish')">Phish</button>
            <button onclick="sendFeedback('{msg_id}','clean')">Clean</button>
          </td>
        </tr>
        """

    html += """
      </table>

      <script>
        function sendFeedback(id, label) {
          fetch("/feedback", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
              message_id: id,
              label: label
            })
          }).then(() => alert("Feedback saved"));
        }
      </script>
    </body>
    </html>
    """

    return html

# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------- FEEDBACK API ----------------
@app.post("/feedback")
async def feedback(request: Request):
    data = await request.json()
    message_id = data["message_id"]
    label = data["label"]  # 'phish' or 'clean'

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO feedback (message_id, label)
        VALUES (%s,%s)
        ON CONFLICT (message_id)
        DO UPDATE SET label = EXCLUDED.label
    """, (message_id, label))
    conn.commit()
    conn.close()

    logging.info(f"Feedback recorded: {message_id} → {label}")
    return {"status": "ok"}
