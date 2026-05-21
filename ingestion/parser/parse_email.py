import mailparser
import hashlib

def parse_email(raw: bytes) -> dict:
    mail = mailparser.parse_from_bytes(raw)

    attachments = []
    for a in mail.attachments:
        attachments.append({
            "filename": a["filename"],
            "mime_type": a["mail_content_type"],
            "size": len(a["payload"]),
            "sha256": hashlib.sha256(a["payload"]).hexdigest()
        })

    return {
        "message_id": mail.message_id,
        "from": mail.from_[0][1] if mail.from_ else None,
        "to": [x[1] for x in mail.to] if mail.to else [],
        "reply_to": mail.reply_to[0][1] if mail.reply_to else None,
        "subject": mail.subject,
        "headers": dict(mail.headers),
        "body_text": mail.text_plain[0] if mail.text_plain else "",
        "body_html": mail.text_html[0] if mail.text_html else "",
        "urls": mail.urls,
        "attachments": attachments,
        "ip_chain": mail.received
    }
