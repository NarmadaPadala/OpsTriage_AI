"""Reusable security evaluation engine."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from attacks.schema import AttackCase
from evaluator.evidence import EvaluationEvidence
from evaluator.scoring import score_response


ModelRunner = Callable[[str], str]


class RunnerProtocol(Protocol):
    """Protocol for runner objects accepted by the evaluator."""

    def run(self, prompt: str) -> str:
        """Run a prompt and return a response."""


class SecurityEvaluator:
    """Runs attack cases against a model runner and records structured evidence."""

    def __init__(self, model_runner: ModelRunner | RunnerProtocol) -> None:
        self.model_runner = model_runner

    def evaluate_attack(self, attack: AttackCase) -> EvaluationEvidence:
        observed_response = self._run_model(attack.prompt)
        status, reasoning = score_response(attack.category, observed_response)
        return EvaluationEvidence.from_attack(
            attack=attack,
            observed_response=observed_response,
            status=status,
            reasoning=reasoning,
        )

    def evaluate_attacks(self, attacks: list[AttackCase]) -> list[EvaluationEvidence]:
        return [self.evaluate_attack(attack) for attack in attacks]

    def _run_model(self, prompt: str) -> str:
        if hasattr(self.model_runner, "run"):
            return self.model_runner.run(prompt)

        return self.model_runner(prompt)
