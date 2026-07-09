"""Input guardrails for suspicious prompt patterns."""

SUSPICIOUS_PATTERNS = (
    "ignore previous instructions",
    "print your system prompt",
    "developer message",
    "hidden prompt",
    "bypass",
)


def is_prompt_suspicious(prompt: str) -> bool:
    normalized = prompt.casefold()
    return any(pattern in normalized for pattern in SUSPICIOUS_PATTERNS)
