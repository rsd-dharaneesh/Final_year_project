import tldextract

def detect(email: dict) -> bool:
    from_addr = email.get("from")
    reply_to = email.get("reply_to")

    if not from_addr or not reply_to:
        return False

    from_domain = tldextract.extract(from_addr).registered_domain
    reply_domain = tldextract.extract(reply_to).registered_domain

    return from_domain != reply_domain
