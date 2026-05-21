import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_recall_curve
import numpy as np
import psycopg2

from ml.dataset import load_dataset

# Load data
X, y = load_dataset()

if len(X) < 20:
    raise RuntimeError("Not enough data to train ML model")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Handle imbalance
pos = sum(y_train)
neg = len(y_train) - pos
scale = neg / max(pos, 1)

# Model
model = lgb.LGBMClassifier(
    n_estimators=400,
    max_depth=8,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    scale_pos_weight=scale,
)

model.fit(X_train, y_train)


# Evaluate
preds = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, preds)
print("AUC:", auc)

# Threshold calibration
p, r, t = precision_recall_curve(y_test, preds)
f1 = (2 * p * r) / (p + r + 1e-9)
best_threshold = t[np.argmax(f1)]

print("Best threshold:", best_threshold)

# Persist metrics
conn = psycopg2.connect(
    host="localhost",
    dbname="phishguard",
    user="phishguard",
    password="phishguard"
)
cur = conn.cursor()
cur.execute(
    "INSERT INTO model_metrics (auc, threshold, samples) VALUES (%s,%s,%s)",
    (float(auc), float(best_threshold), len(X))
)
conn.commit()
conn.close()

# Save bundle
joblib.dump(
    {
        "model": model,
        "threshold": float(best_threshold),
        "features": list(X.columns),
    },
    "ml/model.joblib"
)

print("Model saved to ml/model.joblib")
