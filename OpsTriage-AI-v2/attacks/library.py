"""Central attack-library loader."""

from __future__ import annotations

from attacks import (
    crescendo,
    jailbreak,
    model_leakage,
    obfuscation,
    pii,
    prompt_injection,
    red_teaming,
    social_engineering,
    tool_enumeration,
)
from attacks.schema import AttackCase


def load_attack_cases() -> list[AttackCase]:
    """Load all curated attack cases."""

    cases: list[AttackCase] = []
    for module in (
        jailbreak,
        prompt_injection,
        obfuscation,
        crescendo,
        pii,
        social_engineering,
        red_teaming,
        tool_enumeration,
        model_leakage,
    ):
        cases.extend(module.get_attacks())
    return cases
