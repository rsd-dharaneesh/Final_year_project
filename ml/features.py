import re
import math
from collections import Counter
import tldextract

# ---------- helpers ----------

def entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = Counter(s)
    total = len(s)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

# ---------- main feature extractor ----------

def extract_features(email: dict) -> dict:
    features = {}

    sender = email.get("from") or ""
    subject = email.get("subject") or ""
    html = email.get("body_html") or ""
    urls = email.get("urls") or []
    headers = email.get("headers") or {}

    # ---- Subject features ----
    features["subject_len"] = len(subject)
    features["subject_has_urgent"] = int(
        any(w in subject.lower() for w in ["urgent", "verify", "action", "immediately"])
    )
    features["subject_has_digits"] = int(any(c.isdigit() for c in subject))

    # ---- Sender domain features ----
    ext = tldextract.extract(sender)
    domain = ext.domain or ""
    features["sender_domain_len"] = len(domain)
    features["sender_domain_digits"] = int(any(c.isdigit() for c in domain))
    features["sender_domain_entropy"] = entropy(domain)

    # ---- HTML features ----
    features["has_html_form"] = int("<form" in html.lower())
    features["has_password_input"] = int("type=\"password\"" in html.lower())
    features["anchor_mismatch"] = int(
        "<a" in html.lower() and "http" in html.lower()
    )

    # ---- URL features ----
    features["url_count"] = len(urls)
    features["url_long_count"] = sum(1 for u in urls if len(u) > 60)
    features["url_has_ip"] = int(any(re.search(r"https?://\d+\.\d+", u) for u in urls))
    features["url_has_at"] = int(any("@" in u for u in urls))

    shorteners = ("bit.ly", "t.co", "tinyurl", "goo.gl", "is.gd")
    features["url_shortener"] = int(any(s in u for u in urls for s in shorteners))

    features["url_entropy_max"] = max(
        [entropy(u) for u in urls], default=0.0
    )

    # ---- Header signals ----
    headers_str = str(headers).lower()
    features["spf_fail"] = int("spf=fail" in headers_str)
    features["dkim_fail"] = int("dkim=fail" in headers_str)

    return features
