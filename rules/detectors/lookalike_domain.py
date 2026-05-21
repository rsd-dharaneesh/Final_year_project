import tldextract

def detect(email: dict) -> bool:
    from_addr = email.get("from") or ""
    domain = tldextract.extract(from_addr).domain
    return any(x in domain for x in ["paypa1", "micros0ft", "g00gle"])
