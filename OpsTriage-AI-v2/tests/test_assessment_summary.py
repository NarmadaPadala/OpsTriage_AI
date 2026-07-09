from __future__ import annotations

from attacks import load_attack_cases
from attacks.schema import AttackCategory
from evaluator import SecurityEvaluator
from evaluator.evidence import EvaluationEvidence
from evaluator.scoring import EvaluationStatus
from evaluator.summary import (
    RiskLevel,
    build_assessment_summary,
    category_distribution,
    determine_overall_risk_level,
    risk_distribution,
    status_distribution,
)
from model_runner import MockModelRunner
from ui_helpers import dashboard_distributions, dashboard_metrics


def make_record(status: EvaluationStatus, risk_level: str) -> EvaluationEvidence:
    attack = load_attack_cases()[0]
    return EvaluationEvidence(
        attack_id=attack.attack_id,
        attack_name=attack.name,
        category=AttackCategory.JAILBREAKING.value,
        prompt=attack.prompt,
        expected_safe_behavior=attack.expected_safe_behavior,
        observed_response="Synthetic test response",
        status=status,
        risk_level=risk_level,
        reasoning="Synthetic test reasoning",
        recommended_mitigation=attack.recommended_mitigation,
        evaluated_at="2026-07-07T00:00:00+00:00",
    )


def test_assessment_summary_calculates_score_and_counts() -> None:
    records = [
        make_record(EvaluationStatus.PASS, "LOW"),
        make_record(EvaluationStatus.WARN, "MEDIUM"),
        make_record(EvaluationStatus.FAIL, "HIGH"),
    ]

    summary = build_assessment_summary(records)

    assert summary.total_attacks == 3
    assert summary.pass_count == 1
    assert summary.warn_count == 1
    assert summary.fail_count == 1
    assert summary.security_score == 50
    assert summary.overall_risk_level == RiskLevel.CRITICAL


def test_overall_risk_low_when_all_mock_attacks_pass() -> None:
    records = SecurityEvaluator(MockModelRunner()).evaluate_attacks(load_attack_cases())

    assert determine_overall_risk_level(records) == RiskLevel.LOW


def test_distributions_include_expected_labels() -> None:
    records = SecurityEvaluator(MockModelRunner()).evaluate_attacks(load_attack_cases())

    assert status_distribution(records)["PASS"] == len(records)
    assert "Prompt Injection" in category_distribution(records)
    assert set(risk_distribution(records)) == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_dashboard_helpers_return_metrics_and_chart_rows() -> None:
    records = SecurityEvaluator(MockModelRunner()).evaluate_attacks(load_attack_cases())

    metrics = dashboard_metrics(records)
    distributions = dashboard_distributions(records)

    assert metrics["Total attacks"] == len(records)
    assert metrics["Overall Security Score"] == "100/100"
    assert distributions["PASS/WARN/FAIL Distribution"][0] == {"label": "PASS", "count": len(records)}
