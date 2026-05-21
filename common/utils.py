
def explain_text(ml_explain: dict) -> str:
    if not ml_explain:
        return "No ML signal (rules-only)"

    reasons = []
    for k, v in ml_explain.items():
        if v > 0:
            reasons.append(f"{k.replace('_',' ')} increased risk")

    return "; ".join(reasons[:3])
