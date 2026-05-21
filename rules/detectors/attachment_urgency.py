def detect(email: dict) -> bool:
    urgent = any(w in (email.get("subject","").lower()) for w in ["urgent","immediate","action"])
    return urgent and len(email.get("attachments", [])) > 0
