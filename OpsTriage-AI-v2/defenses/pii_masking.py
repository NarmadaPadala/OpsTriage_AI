"""Simple PII masking utilities."""

from __future__ import annotations

import re


SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def mask_pii(text: str) -> str:
    text = SSN_PATTERN.sub("[REDACTED_SSN]", text)
    return EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
