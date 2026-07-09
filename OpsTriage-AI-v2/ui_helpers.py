"""Reusable helpers for the Streamlit security assessment UI."""

from __future__ import annotations

from attacks.schema import AttackCase
from evaluator import EvaluationEvidence, SecurityEvaluator, build_assessment_summary
from evaluator.persistence import save_report_artifacts, serialize_records_to_csv
from evaluator.report_generator import build_security_report, deployment_recommendation
from evaluator.summary import category_distribution, risk_distribution, status_distribution
from model_runner import create_model_runner


ALL_CATEGORIES_LABEL = "All Categories"


def category_options(attacks: list[AttackCase]) -> list[str]:
    """Return category labels for UI selection."""

    categories = sorted({attack.category.value for attack in attacks})
    return [ALL_CATEGORIES_LABEL] + categories


def attacks_for_category(attacks: list[AttackCase], category: str) -> list[AttackCase]:
    """Filter attack cases by category label."""

    if category == ALL_CATEGORIES_LABEL:
        return attacks

    return [attack for attack in attacks if attack.category.value == category]


def attack_name_options(attacks: list[AttackCase]) -> list[str]:
    """Return stable attack names for a selectbox."""

    return [f"{attack.attack_id} - {attack.name}" for attack in attacks]


def find_attack_by_option(attacks: list[AttackCase], option: str) -> AttackCase:
    """Resolve a selectbox option back to an attack case."""

    attack_id = option.split(" - ", 1)[0]
    for attack in attacks:
        if attack.attack_id == attack_id:
            return attack

    raise ValueError(f"Unknown attack option: {option}")


def run_attacks(attacks: list[AttackCase], runner_mode: str) -> list[EvaluationEvidence]:
    """Run selected attacks with a configured model runner."""

    runner = create_model_runner(runner_mode)
    evaluator = SecurityEvaluator(runner)
    return evaluator.evaluate_attacks(attacks)


def evidence_table_rows(records: list[EvaluationEvidence]) -> list[dict[str, str]]:
    """Convert evidence records into UI table rows."""

    return [
        {
            "attack name": record.attack_name,
            "category": record.category,
            "prompt": record.prompt,
            "observed response": record.observed_response,
            "score": record.status.value,
            "reasoning": record.reasoning,
            "recommended mitigation": record.recommended_mitigation,
        }
        for record in records
    ]


def dashboard_metrics(records: list[EvaluationEvidence]) -> dict[str, str | int]:
    """Return executive dashboard metrics for the UI."""

    summary = build_assessment_summary(records)
    return {
        "Total attacks": summary.total_attacks,
        "PASS": summary.pass_count,
        "WARN": summary.warn_count,
        "FAIL": summary.fail_count,
        "Overall Security Score": f"{summary.security_score}/100",
        "Overall Risk Level": summary.overall_risk_level.value,
    }


def dashboard_deployment_recommendation(records: list[EvaluationEvidence]) -> str:
    """Return the deployment recommendation for dashboard display."""

    return deployment_recommendation(records)


def distribution_chart_rows(distribution: dict[str, int]) -> list[dict[str, str | int]]:
    """Convert a distribution dictionary to Streamlit-friendly chart rows."""

    return [{"label": label, "count": count} for label, count in distribution.items()]


def dashboard_distributions(records: list[EvaluationEvidence]) -> dict[str, list[dict[str, str | int]]]:
    """Return all dashboard chart distributions."""

    return {
        "PASS/WARN/FAIL Distribution": distribution_chart_rows(status_distribution(records)),
        "Attack Category Distribution": distribution_chart_rows(category_distribution(records)),
        "Risk Level Distribution": distribution_chart_rows(risk_distribution(records)),
    }


def records_to_csv(records: list[EvaluationEvidence]) -> str:
    """Serialize evidence records to CSV."""

    return serialize_records_to_csv(records)


def records_to_markdown(records: list[EvaluationEvidence]) -> str:
    """Serialize evidence records to Markdown."""

    return build_security_report(records)


def has_model_unavailable(records: list[EvaluationEvidence]) -> bool:
    """Return whether any v1 model-backed run failed gracefully."""

    return any(record.observed_response.startswith("MODEL_UNAVAILABLE") for record in records)


def save_records_to_reports(records: list[EvaluationEvidence]):
    """Save Markdown and CSV artifacts to the reports directory."""

    return save_report_artifacts(records)
