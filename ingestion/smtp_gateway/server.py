import asyncio
from aiosmtpd.controller import Controller
import subprocess
import sys
from pathlib import Path
from collections import defaultdict
import time


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
# Use the current Python executable for portability across OS and environments
PYTHON = sys.executable
INGEST_MODULE = "ingestion.smtp_gateway.ingest"

RATE = defaultdict(list)

def allowed(ip):
    now = time.time()
    RATE[ip] = [t for t in RATE[ip] if now - t < 60]
    if len(RATE[ip]) > 30:
        return False
    RATE[ip].append(now)
    return True


class Handler:
    async def handle_DATA(self, server, session, envelope):
        peer = session.peer[0]
        if not allowed(peer):
            return "421 Rate limit exceeded"

        p = subprocess.Popen(
            [PYTHON, "-m", INGEST_MODULE],
            stdin=subprocess.PIPE,
            cwd=str(PROJECT_ROOT)
        )
        p.stdin.write(envelope.original_content)
        p.stdin.close()
        p.wait()
        return "250 OK"
        

def main():
    # bind explicitly to IPv4 loopback so we don't get ::1 connections
    # which aiosmtpd will log as connection lost when a client immediately
    # disconnects. IPv6 behaviour is harmless, but the log can be noisy.
    controller = Controller(Handler(), hostname="127.0.0.1", port=2525)
    controller.start()
    print("SMTP listening on port 2525")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()

if __name__ == "__main__":
    main()
