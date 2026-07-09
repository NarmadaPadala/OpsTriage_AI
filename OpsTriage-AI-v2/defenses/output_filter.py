"""Output filters for sensitive information disclosure."""

SENSITIVE_OUTPUT_PATTERNS = (
    "system prompt",
    "developer message",
    "api key",
    "password",
    "adapter_model.safetensors",
)


def contains_sensitive_output(text: str) -> bool:
    normalized = text.casefold()
    return any(pattern in normalized for pattern in SENSITIVE_OUTPUT_PATTERNS)
