from __future__ import annotations

from pathlib import Path

from attacks import load_attack_cases
from evaluator import SecurityEvaluator
from evaluator.persistence import build_artifact_paths, save_report_artifacts
from model_runner import MockModelRunner
from ui_helpers import save_records_to_reports


def make_records():
    attacks = load_attack_cases()[:2]
    return SecurityEvaluator(MockModelRunner()).evaluate_attacks(attacks)


def test_build_artifact_paths_uses_timestamp_and_prefix(tmp_path: Path) -> None:
    paths = build_artifact_paths(
        reports_dir=tmp_path,
        timestamp="20260707T010203Z",
        prefix="sample",
    )

    assert paths.markdown_path == tmp_path / "sample_20260707T010203Z.md"
    assert paths.csv_path == tmp_path / "sample_20260707T010203Z.csv"


def test_save_report_artifacts_writes_markdown_and_csv(tmp_path: Path) -> None:
    records = make_records()

    paths = save_report_artifacts(
        records,
        reports_dir=tmp_path,
        timestamp="20260707T010203Z",
        prefix="sample",
    )

    assert paths.markdown_path.exists()
    assert paths.csv_path.exists()
    assert "Security Validation Report" in paths.markdown_path.read_text(encoding="utf-8")
    assert "attack_id,attack_name" in paths.csv_path.read_text(encoding="utf-8")


def test_save_records_to_reports_uses_persistence(monkeypatch, tmp_path: Path) -> None:
    records = make_records()

    def fake_save_report_artifacts(records_arg):
        assert records_arg == records
        return save_report_artifacts(
            records_arg,
            reports_dir=tmp_path,
            timestamp="20260707T010203Z",
            prefix="ui",
        )

    monkeypatch.setattr("ui_helpers.save_report_artifacts", fake_save_report_artifacts)

    paths = save_records_to_reports(records)

    assert paths.markdown_path.name == "ui_20260707T010203Z.md"
    assert paths.csv_path.name == "ui_20260707T010203Z.csv"
