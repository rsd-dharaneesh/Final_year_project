import sys
from ingestion.parser.parse_email import parse_email
from ingestion.producer import send

raw_email = sys.stdin.buffer.read()
parsed = parse_email(raw_email)

send("emails.raw", parsed)
