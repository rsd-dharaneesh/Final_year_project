Here’s a **senior-engineer-level README**: concise, architectural, no fluff, signals taste and judgment.
You can paste this **as-is** into `README.md`.

---

# PhishGuard 🛡️

**Enterprise-grade Email Phishing Detection Pipeline**

PhishGuard is an end-to-end phishing detection system designed with **real enterprise security architecture** in mind.
It combines **rule-based detection, machine learning, analyst feedback, explainability, and monitoring** into a single cohesive pipeline.

This is **not a demo toy**. It mirrors how commercial email security products are built.

---

## Architecture Overview

```
SMTP Ingest
   ↓
Kafka (raw emails)
   ↓
Rules Engine  ─────┐
                    ├─ Final Score & Verdict
ML Scoring  ────────┘
   ↓
PostgreSQL (audit log)
   ↓
SOC UI (FastAPI)
   ↓
Alerts (Slack)
```

### Design principles

* **Rules-first safety**: ML never overrides strong deterministic signals
* **Fail-safe defaults**: ML unavailable → rules only
* **Explainability over black-box scores**
* **Human-in-the-loop learning**
* **Observability by default**

---

## Core Features

### 🔍 Detection

* Deterministic phishing rules:

  * Reply-To mismatch
  * HTML credential forms
  * Lookalike domains
  * IP-based URLs
  * Urgency language
* ML-based scoring (LightGBM)
* Safe score fusion:

  ```
  final_score = max(rule_score, ml_score)
  ```

---

### 🧠 Machine Learning

* Feature engineering (lexical, structural, entropy-based)
* Class-imbalance handling
* Threshold calibration (precision/recall optimized)
* Cold-start safe (rules-only fallback)
* Active learning from analyst feedback

---

### 🧑‍💻 SOC Operations

* Web-based SOC dashboard (FastAPI)
* Basic Auth protected
* Per-email:

  * Verdict
  * Fired rules
  * ML explanation
  * Timestamp
* Analyst feedback:

  * Mark **Phish / Clean**
  * Overrides rule labels for training

---

### 🔎 Explainability (Confidence)

* Per-email ML feature attribution
* Top contributing signals shown inline
* Fully auditable decisions
* SOC2 / compliance-friendly design

---

### 🚨 Alerts

* Real-time Slack alerts
* Deduplication (one alert per email)
* Alert audit trail stored in DB

---

### 📊 Monitoring

* AUC tracked per retrain
* Training sample counts
* Verdict volume trends
* Drift detection hooks

---

## Tech Stack

| Layer       | Technology           |
| ----------- | -------------------- |
| Ingestion   | SMTP (aiosmtpd)      |
| Messaging   | Kafka                |
| Backend API | FastAPI              |
| Database    | PostgreSQL           |
| ML          | LightGBM, sklearn    |
| UI          | Server-rendered HTML |
| Alerts      | Slack Webhooks       |
| Runtime     | Python 3.11          |
| Infra       | Docker Compose       |

---

## Quick Start

### 1. Clone & setup

```bash
git clone <repo>
cd phishguard
```

### 2. Start infrastructure

```bash
docker compose up -d
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start services

```powershell
.\run_all.ps1
```

### 5. Open SOC UI

```
http://127.0.0.1:8000
```

---

## Environment Configuration

Create `.env` from the example:

```env
DB_HOST=localhost
DB_NAME=phishguard
DB_USER=phishguard
DB_PASS=phishguard

KAFKA_BOOTSTRAP=localhost:9092
SLACK_WEBHOOK=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

---

## Testing the Pipeline

Send a phishing test email:

```bash
python send_phish_test.py
```

Expected results:

* Email ingested via SMTP
* Rules + ML scoring applied
* Stored in Postgres
* Visible in SOC UI
* Slack alert fired (once)
* Analyst feedback accepted

---

## Active Learning Workflow

1. Email flagged as suspicious
2. Analyst marks **Phish** or **Clean**
3. Feedback stored as ground truth
4. Weekly retraining
5. ML accuracy improves over time

This is how **real SOC systems evolve**.

---

## Why This Project Matters

This project demonstrates:

* Distributed system design
* ML lifecycle awareness
* Security-first thinking
* Observability and explainability
* Human-in-the-loop ML
* Production-safe engineering choices

It intentionally avoids:

* Black-box ML decisions
* Overfitting demos
* Fragile pipelines
* Unobservable systems

---

## Future Work

* URL reputation enrichment
* Multi-tenant isolation
* RBAC for SOC UI
* SIEM export (Elastic/Splunk)
* Cloud-native deployment (K8s)

---

## Final Note

PhishGuard is built to answer a simple but hard question:

> *Can we trust this system in a real SOC?*

Every architectural choice is made with that question in mind.

---

