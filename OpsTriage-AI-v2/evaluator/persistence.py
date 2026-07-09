"""Report persistence utilities for security assessment artifacts."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

from evaluator.evidence import EvaluationEvidence
from evaluator.report_generator import build_security_report


DEFAULT_REPORTS_DIR = Path("reports")


@dataclass(frozen=True)
class SavedReportArtifacts:
    """Paths for persisted report artifacts."""

    markdown_path: Path
    csv_path: Path


def utc_timestamp() -> str:
    """Return a filesystem-safe UTC timestamp."""

    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def serialize_records_to_csv(records: list[EvaluationEvidence]) -> str:
    """Serialize evidence records to CSV."""

    output = StringIO()
    fieldnames = [
        "attack_id",
        "attack_name",
        "category",
        "prompt",
        "expected_safe_behavior",
        "observed_response",
        "status",
        "risk_level",
        "reasoning",
        "recommended_mitigation",
        "evaluated_at",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow(record.to_dict())
    return output.getvalue()


def build_artifact_paths(
    reports_dir: Path = DEFAULT_REPORTS_DIR,
    timestamp: str | None = None,
    prefix: str = "opstriage_v2_security_assessment",
) -> SavedReportArtifacts:
    """Build timestamped Markdown and CSV paths."""

    stamp = timestamp or utc_timestamp()
    return SavedReportArtifacts(
        markdown_path=reports_dir / f"{prefix}_{stamp}.md",
        csv_path=reports_dir / f"{prefix}_{stamp}.csv",
    )


def save_report_artifacts(
    records: list[EvaluationEvidence],
    reports_dir: Path = DEFAULT_REPORTS_DIR,
    timestamp: str | None = None,
    prefix: str = "opstriage_v2_security_assessment",
) -> SavedReportArtifacts:
    """Persist Markdown and CSV evidence artifacts."""

    paths = build_artifact_paths(reports_dir=reports_dir, timestamp=timestamp, prefix=prefix)
    paths.markdown_path.parent.mkdir(parents=True, exist_ok=True)
    paths.markdown_path.write_text(build_security_report(records), encoding="utf-8")
    paths.csv_path.write_text(serialize_records_to_csv(records), encoding="utf-8")
    return paths
