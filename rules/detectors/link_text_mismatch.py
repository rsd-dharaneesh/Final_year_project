import re

def detect(email: dict) -> bool:
    html = email.get("body_html", "")
    return bool(re.search(r'<a[^>]+href="http[^"]+"[^>]*>[^<]*http', html, re.I))
