def detect(email: dict) -> bool:
    body_html = email.get("body_html", "")
    return "<form" in body_html.lower()
