"""Markdown report generation for security assessment evidence."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from evaluator.evidence import EvaluationEvidence
from evaluator.summary import (
    build_assessment_summary,
    defense_priorities,
    highest_risk_attacks,
)


def deployment_recommendation(records: list[EvaluationEvidence]) -> str:
    """Return an executive deployment recommendation."""

    summary = build_assessment_summary(records)
    if summary.fail_count > 0:
        return (
            "Do not deploy to automated production routing. Resolve FAIL findings, validate "
            "defenses, and rerun the full assessment."
        )
    if summary.warn_count > 0:
        return (
            "Proceed only as human-in-the-loop decision support while WARN findings are reviewed "
            "and mitigations are validated."
        )
    return (
        "Proceed with human-in-the-loop pilot readiness review. Continue red-team regression "
        "testing before any automated routing."
    )


def build_security_report(records: list[EvaluationEvidence]) -> str:
    """Build a professional Markdown report from evaluation evidence."""

    counts = Counter(record.status.value for record in records)
    summary = build_assessment_summary(records)
    highest_risk = highest_risk_attacks(records)
    priorities = defense_priorities(records)
    lines = [
        "# OpsTriage AI v2 Security Validation Report",
        "",
        "## Executive Summary",
        "",
        "This report summarizes structured red-team testing for OpsTriage AI before production deployment.",
        "The assessment focuses on prompt-level abuse, leakage risk, unsafe routing behavior, and the",
        "defenses required for enterprise readiness.",
        "",
        f"- Total attacks: {summary.total_attacks}",
        f"- Overall Security Score: {summary.security_score}/100",
        f"- Overall Risk Level: {summary.overall_risk_level.value}",
        f"- Deployment Recommendation: {deployment_recommendation(records)}",
        "",
        "## Score Summary",
        "",
        "| Status | Count |",
        "|---|---:|",
        f"| PASS | {counts.get('PASS', 0)} |",
        f"| WARN | {counts.get('WARN', 0)} |",
        f"| FAIL | {counts.get('FAIL', 0)} |",
        "",
        "## Key Findings",
        "",
        f"- {summary.pass_count} attacks preserved the intended safety boundary.",
        f"- {summary.warn_count} attacks require manual security review.",
        f"- {summary.fail_count} attacks violated intended behavior or leaked sensitive information.",
        "- Findings are mapped to production defenses rather than treated as model-only issues.",
        "",
        "## Highest-Risk Attacks",
        "",
        "| Attack | Category | Status | Risk |",
        "|---|---|---|---|",
    ]

    for record in highest_risk:
        lines.append(
            f"| {record.attack_id}: {record.attack_name} | {record.category} | "
            f"{record.status.value} | {record.risk_level} |"
        )

    lines.extend(
        [
            "",
            "## Defense Priorities",
            "",
            "| Priority | Defense | Weighted Need |",
            "|---:|---|---:|",
        ]
    )

    for index, (defense, score) in enumerate(priorities, start=1):
        lines.append(f"| {index} | {defense} | {score} |")

    lines.extend(
        [
            "",
        "## Findings",
        "",
        ]
    )

    for record in records:
        lines.extend(
            [
                f"### {record.attack_id}: {record.attack_name}",
                "",
                f"- Category: {record.category}",
                f"- Status: {record.status.value}",
                f"- Risk Level: {record.risk_level}",
                f"- Expected Safe Behavior: {record.expected_safe_behavior}",
                f"- Observed Response: {record.observed_response}",
                f"- Reasoning: {record.reasoning}",
                f"- Recommended Mitigation: {record.recommended_mitigation}",
                "",
            ]
        )

    lines.extend(
        [
            "## Production Recommendation",
            "",
            "OpsTriage AI should remain human-in-the-loop until prompt guards, PII masking,",
            "output filtering, authorization checks, audit logging, and ongoing red-team evaluation",
            "are validated against representative production-like incidents.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_security_report(records: list[EvaluationEvidence], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_security_report(records), encoding="utf-8")
