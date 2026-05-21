import os
import joblib
from ml.features import extract_features

MODEL_PATH = "ml/model.joblib"

_bundle = None
if os.path.exists(MODEL_PATH):
    _bundle = joblib.load(MODEL_PATH)

def score(email: dict) -> float:
    if _bundle is None:
        return 0.0

    model = _bundle["model"]
    feats = extract_features(email)
    X = [[feats[k] for k in _bundle["features"]]]

    return float(model.predict_proba(X)[0][1])

def is_phish(email: dict) -> bool:
    if _bundle is None:
        return False

    threshold = _bundle.get("threshold", 0.5)
    return score(email) >= threshold

def explain(email: dict) -> dict:
    if _bundle is None:
        return {}

    model = _bundle["model"]
    feats = extract_features(email)
    X = [[feats[k] for k in _bundle["features"]]]

    contrib = model.predict(X, pred_contrib=True)[0]
    names = _bundle["features"]

    explanation = sorted(
        zip(names, contrib[:-1]),  # last value = bias
        key=lambda x: abs(x[1]),
        reverse=True
    )[:5]

    return {k: round(v, 4) for k, v in explanation}

