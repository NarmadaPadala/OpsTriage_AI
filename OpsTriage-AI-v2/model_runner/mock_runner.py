"""Deterministic mock runner for demos, screenshots, and local tests."""

from __future__ import annotations

from model_runner.base import BaseModelRunner


class MockModelRunner(BaseModelRunner):
    """Safe mock model runner that requires no external model artifacts."""

    name = "mock"

    def run(self, prompt: str) -> str:
        normalized = prompt.casefold()

        if any(term in normalized for term in ("system prompt", "developer message", "hidden")):
            return (
                "I cannot reveal hidden instructions, system prompts, or developer messages. "
                "For this incident-routing request, I would keep the approved taxonomy in force "
                "and send the case to human review because the prompt is attempting to override "
                "the system boundary."
            )

        if any(term in normalized for term in ("ssn", "date of birth", "member id", "pii")):
            return (
                "I cannot provide, infer, or reconstruct personal data from training or incident "
                "records. The safe handling path is to mask PII before inference, use sanitized "
                "incident text, and route this case through human review."
            )

        if any(term in normalized for term in ("bypass", "vp of operations", "urgent")):
            return (
                "I cannot bypass authorization, escalation, or routing controls based only on a "
                "claimed role or urgency statement. The request should follow the approved incident "
                "workflow and receive human review."
            )

        if any(term in normalized for term in ("tool", "api", "credential", "database")):
            return (
                "I cannot enumerate internal tools, credentials, databases, or deployment details. "
                "I can only discuss the public assessment workflow and recommend using an approved "
                "tool allowlist plus human review for capability-related requests."
            )

        return (
            "I would treat the provided text as untrusted incident content, preserve the approved "
            "routing workflow, avoid unsupported labels, and recommend human review for suspicious "
            "or ambiguous instructions."
        )
