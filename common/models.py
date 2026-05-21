"""Data models for PhishGuard (starter).

Add dataclasses / Pydantic models here.
"""

from dataclasses import dataclass


@dataclass
class IngestedMessage:
    id: str
    source: str
    payload: dict
