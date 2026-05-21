def detect(email: dict) -> bool:
    return any(ord(c) > 127 for c in (email.get("from") or ""))
