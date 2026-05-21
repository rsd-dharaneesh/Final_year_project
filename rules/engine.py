from ml.scorer import score as ml_score
from ml.scorer import explain as ml_explain

import yaml
# from rules.detectors import reply_to_mismatch, html_form
from rules.detectors import (
    reply_to_mismatch, html_form, lookalike_domain,
    link_text_mismatch, new_domain_age, unicode_homoglyph, attachment_urgency
    )


DETECTORS = {
    "reply_to_mismatch": reply_to_mismatch.detect,
    "html_form": html_form.detect,
    "lookalike_domain": lookalike_domain.detect,
    "link_text_mismatch": link_text_mismatch.detect,
    "new_domain_age": new_domain_age.detect,
    "unicode_homoglyph": unicode_homoglyph.detect,
    "attachment_urgency": attachment_urgency.detect,
}
with open("rules/rules.yaml") as f:
    RULE_CONFIG = yaml.safe_load(f)

def evaluate(email: dict) -> dict:
    # Apply rule-based detectors first
    hits = []
    score = 0.0

    for rule_id, detector in DETECTORS.items():
        try:
            if detector(email):
                rule_meta = RULE_CONFIG.get(rule_id, {})
                hits.append(rule_id)
                score += rule_meta.get("weight", 0.0)
        except Exception:
            # If a detector errors, skip it (detector should handle its own errors)
            continue

    score = min(score, 1.0)

    # ML score
    ml = ml_score(email)

    # Final score is the max of rule score and ML score
    final_score = max(score, ml)
    explanation = ml_explain(email)

    return {
        "rule_hits": hits,
        "rule_score": score,
        "ml_score": ml,
        "final_score": final_score,
        "verdict": "suspicious" if final_score >= 0.5 else "clean",
        "ml_explain": explanation
    }
