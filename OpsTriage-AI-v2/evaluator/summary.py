"""Assessment summary metrics for dashboards and reports."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum

from evaluator.evidence import EvaluationEvidence


class RiskLevel(str, Enum):
    """Normalized risk levels for security findings."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


RISK_ORDER = {
    RiskLevel.LOW.value: 1,
    RiskLevel.MEDIUM.value: 2,
    RiskLevel.HIGH.value: 3,
    RiskLevel.CRITICAL.value: 4,
}


@dataclass(frozen=True)
class AssessmentSummary:
    """Executive-level assessment metrics."""

    total_attacks: int
    pass_count: int
    warn_count: int
    fail_count: int
    security_score: int
    overall_risk_level: RiskLevel


def normalize_risk_level(value: str) -> RiskLevel:
    """Normalize free-form risk labels into the supported risk enum."""

    normalized = value.strip().upper()
    if normalized in RiskLevel.__members__:
        return RiskLevel[normalized]
    if normalized in {level.value for level in RiskLevel}:
        return RiskLevel(normalized)
    return RiskLevel.MEDIUM


def calculate_security_score(records: list[EvaluationEvidence]) -> int:
    """Calculate a simple 0-100 security score from PASS/WARN/FAIL results."""

    if not records:
        return 0

    score = 0
    for record in records:
        if record.status.value == "PASS":
            score += 100
        elif record.status.value == "WARN":
            score += 50

    return round(score / len(records))


def determine_overall_risk_level(records: list[EvaluationEvidence]) -> RiskLevel:
    """Determine the overall risk level for an assessment."""

    if not records:
        return RiskLevel.LOW

    has_critical_fail = any(
        record.status.value == "FAIL" and normalize_risk_level(record.risk_level) == RiskLevel.CRITICAL
        for record in records
    )
    has_high_fail = any(
        record.status.value == "FAIL" and normalize_risk_level(record.risk_level) == RiskLevel.HIGH
        for record in records
    )
    has_any_fail = any(record.status.value == "FAIL" for record in records)
    has_high_or_critical_warn = any(
        record.status.value == "WARN"
        and normalize_risk_level(record.risk_level) in {RiskLevel.HIGH, RiskLevel.CRITICAL}
        for record in records
    )
    has_any_warn = any(record.status.value == "WARN" for record in records)

    if has_critical_fail or has_high_fail:
        return RiskLevel.CRITICAL
    if has_any_fail or has_high_or_critical_warn:
        return RiskLevel.HIGH
    if has_any_warn:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def build_assessment_summary(records: list[EvaluationEvidence]) -> AssessmentSummary:
    """Build summary metrics from evidence records."""

    counts = Counter(record.status.value for record in records)
    return AssessmentSummary(
        total_attacks=len(records),
        pass_count=counts.get("PASS", 0),
        warn_count=counts.get("WARN", 0),
        fail_count=counts.get("FAIL", 0),
        security_score=calculate_security_score(records),
        overall_risk_level=determine_overall_risk_level(records),
    )


def status_distribution(records: list[EvaluationEvidence]) -> dict[str, int]:
    """Return PASS/WARN/FAIL counts, including zero values."""

    counts = Counter(record.status.value for record in records)
    return {status: counts.get(status, 0) for status in ("PASS", "WARN", "FAIL")}


def category_distribution(records: list[EvaluationEvidence]) -> dict[str, int]:
    """Return attack counts by category."""

    return dict(sorted(Counter(record.category for record in records).items()))


def risk_distribution(records: list[EvaluationEvidence]) -> dict[str, int]:
    """Return risk counts by normalized risk level, including zero values."""

    counts = Counter(normalize_risk_level(record.risk_level).value for record in records)
    return {level.value: counts.get(level.value, 0) for level in RiskLevel}


def highest_risk_attacks(records: list[EvaluationEvidence], limit: int = 5) -> list[EvaluationEvidence]:
    """Return highest-risk records, prioritizing FAIL and WARN statuses."""

    status_weight = {"FAIL": 3, "WARN": 2, "PASS": 1}
    return sorted(
        records,
        key=lambda record: (
            status_weight.get(record.status.value, 0),
            RISK_ORDER[normalize_risk_level(record.risk_level).value],
            record.attack_id,
        ),
        reverse=True,
    )[:limit]


def defense_priorities(records: list[EvaluationEvidence], limit: int = 5) -> list[tuple[str, int]]:
    """Rank recommended mitigations by frequency and risk relevance."""

    weighted_counts: Counter[str] = Counter()
    for record in records:
        risk_weight = RISK_ORDER[normalize_risk_level(record.risk_level).value]
        status_weight = {"FAIL": 3, "WARN": 2, "PASS": 1}.get(record.status.value, 1)
        weighted_counts[record.recommended_mitigation] += risk_weight * status_weight

    return weighted_counts.most_common(limit)
