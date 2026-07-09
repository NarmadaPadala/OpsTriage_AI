"""Evidence records produced by security evaluations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from attacks.schema import AttackCase
from evaluator.scoring import EvaluationStatus


@dataclass(frozen=True)
class EvaluationEvidence:
    """One completed attack evaluation record."""

    attack_id: str
    attack_name: str
    category: str
    prompt: str
    expected_safe_behavior: str
    observed_response: str
    status: EvaluationStatus
    risk_level: str
    reasoning: str
    recommended_mitigation: str
    evaluated_at: str

    @classmethod
    def from_attack(
        cls,
        attack: AttackCase,
        observed_response: str,
        status: EvaluationStatus,
        reasoning: str,
    ) -> "EvaluationEvidence":
        return cls(
            attack_id=attack.attack_id,
            attack_name=attack.name,
            category=attack.category.value,
            prompt=attack.prompt,
            expected_safe_behavior=attack.expected_safe_behavior,
            observed_response=observed_response,
            status=status,
            risk_level=attack.risk_level,
            reasoning=reasoning,
            recommended_mitigation=attack.recommended_mitigation,
            evaluated_at=datetime.now(UTC).isoformat(),
        )

    def to_dict(self) -> dict[str, str]:
        record = asdict(self)
        record["status"] = self.status.value
        return record
