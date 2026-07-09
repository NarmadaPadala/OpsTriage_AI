"""Shared attack-case schema for the security evaluation framework."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AttackCategory(str, Enum):
    """Supported AI security attack categories."""

    JAILBREAKING = "Jailbreaking"
    PROMPT_INJECTION = "Prompt Injection"
    OBFUSCATION = "Obfuscation"
    CRESCENDO = "Crescendo"
    PII_EXTRACTION = "PII Extraction"
    SOCIAL_ENGINEERING = "Social Engineering"
    RED_TEAMING = "Red Teaming"
    TOOL_ENUMERATION = "Tool Enumeration"
    SYSTEM_PROMPT_EXTRACTION = "Prompt Leakage"
    MODEL_INFORMATION_LEAKAGE = "Model Information Leakage"


@dataclass(frozen=True)
class AttackCase:
    """One structured red-team test case."""

    attack_id: str
    name: str
    category: AttackCategory
    prompt: str
    expected_safe_behavior: str
    risk_level: str
    recommended_mitigation: str
