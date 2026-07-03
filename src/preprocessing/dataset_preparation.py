"""Dataset preparation utilities for OpsTriage AI supervised fine-tuning.

The functions in this module intentionally avoid model-training concerns. They
load and validate incident records, create deterministic stratified splits, and
format examples for LLaMA Factory-compatible supervised fine-tuning.
"""

from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from config.taxonomy import APPROVED_SUPPORT_TEAMS

REQUIRED_COLUMNS: tuple[str, ...] = (
    "incident_id",
    "incident_title",
    "incident_description",
    "support_team",
)

SYSTEM_PROMPT = (
    "You are OpsTriage AI, an enterprise incident triage assistant. "
    "Classify the incident into exactly one approved support team. "
    "Return only the support team name."
)


@dataclass(frozen=True)
class SplitConfig:
    """Configuration for deterministic stratified dataset splitting."""

    train_ratio: float = 0.70
    validation_ratio: float = 0.15
    test_ratio: float = 0.15
    seed: int = 42


def load_incidents(csv_path: Path) -> list[dict[str, str]]:
    """Load incident records from a CSV file."""

    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = [dict(row) for row in reader]

    return rows


def validate_required_columns(fieldnames: Iterable[str] | None) -> None:
    """Validate that all required CSV columns exist."""

    available_columns = set(fieldnames or [])
    missing_columns = sorted(set(REQUIRED_COLUMNS) - available_columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")


def validate_required_values(rows: list[dict[str, str]]) -> None:
    """Validate required fields are populated for every record."""

    errors: list[str] = []
    for row_number, row in enumerate(rows, start=2):
        for column in REQUIRED_COLUMNS:
            if not row.get(column, "").strip():
                errors.append(f"row {row_number}: missing value for {column}")

    if errors:
        raise ValueError("Required value validation failed: " + "; ".join(errors))


def validate_support_teams(
    rows: list[dict[str, str]], approved_teams: Iterable[str] = APPROVED_SUPPORT_TEAMS
) -> None:
    """Validate support-team labels against the approved taxonomy."""

    approved = set(approved_teams)
    invalid_labels = sorted({row["support_team"] for row in rows if row["support_team"] not in approved})
    if invalid_labels:
        raise ValueError(f"Unsupported support_team values: {', '.join(invalid_labels)}")


def find_duplicate_title_description_pairs(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Find duplicate normalized title and description pairs."""

    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in rows:
        key = (
            normalize_text(row["incident_title"]),
            normalize_text(row["incident_description"]),
        )
        grouped[key].append(row["incident_id"])

    duplicates: list[dict[str, object]] = []
    for (title, description), incident_ids in grouped.items():
        if len(incident_ids) > 1:
            duplicates.append(
                {
                    "incident_ids": incident_ids,
                    "normalized_title": title,
                    "normalized_description": description,
                }
            )

    return duplicates


def normalize_text(value: str) -> str:
    """Normalize text for duplicate detection."""

    return " ".join(value.casefold().strip().split())


def validate_split_config(config: SplitConfig) -> None:
    """Validate split ratios before creating splits."""

    total = config.train_ratio + config.validation_ratio + config.test_ratio
    if round(total, 6) != 1.0:
        raise ValueError(f"Split ratios must sum to 1.0, received {total}")

    if min(config.train_ratio, config.validation_ratio, config.test_ratio) <= 0:
        raise ValueError("Split ratios must all be positive")


def create_stratified_splits(
    rows: list[dict[str, str]], config: SplitConfig = SplitConfig()
) -> dict[str, list[dict[str, str]]]:
    """Create deterministic stratified train, validation, and test splits."""

    validate_split_config(config)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["support_team"]].append(row)

    splits: dict[str, list[dict[str, str]]] = {"train": [], "validation": [], "test": []}
    rng = random.Random(config.seed)

    for support_team in sorted(grouped):
        class_rows = list(grouped[support_team])
        rng.shuffle(class_rows)

        train_count, validation_count = calculate_class_split_counts(len(class_rows), config)
        splits["train"].extend(class_rows[:train_count])
        splits["validation"].extend(class_rows[train_count : train_count + validation_count])
        splits["test"].extend(class_rows[train_count + validation_count :])

    for split_rows in splits.values():
        split_rows.sort(key=lambda row: row["incident_id"])

    return splits


def calculate_class_split_counts(class_size: int, config: SplitConfig) -> tuple[int, int]:
    """Calculate per-class train and validation counts.

    Small class sizes need explicit protection so validation and test sets are
    represented. The current 100-row pilot has 6-7 examples per class, so each
    class receives at least one validation and one test example.
    """

    if class_size < 3:
        raise ValueError("Each support team needs at least 3 records to create 3 splits")

    validation_count = max(1, round(class_size * config.validation_ratio))
    test_count = max(1, round(class_size * config.test_ratio))
    train_count = class_size - validation_count - test_count

    if train_count < 1:
        train_count = 1
        overflow = train_count + validation_count + test_count - class_size
        test_count = max(1, test_count - overflow)

    return train_count, validation_count


def incident_to_sharegpt(row: dict[str, str]) -> dict[str, object]:
    """Convert one incident row to ShareGPT/OpenAI-style SFT format."""

    approved_team_list = ", ".join(APPROVED_SUPPORT_TEAMS)
    user_prompt = (
        f"Incident Title: {row['incident_title']}\n"
        f"Incident Description: {row['incident_description']}\n\n"
        f"Approved Support Teams: {approved_team_list}"
    )

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": row["support_team"]},
        ]
    }


def convert_rows_to_sharegpt(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Convert incident rows to ShareGPT/OpenAI-style records."""

    return [incident_to_sharegpt(row) for row in rows]


def save_json(records: list[dict[str, object]], output_path: Path) -> None:
    """Save records as pretty-printed JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)
        file.write("\n")


def save_split_outputs(
    splits: dict[str, list[dict[str, str]]], output_dir: Path
) -> dict[str, Path]:
    """Save train, validation, test, and combined ShareGPT JSON files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: dict[str, Path] = {}

    for split_name, split_rows in splits.items():
        output_path = output_dir / f"{split_name}.json"
        save_json(convert_rows_to_sharegpt(split_rows), output_path)
        output_paths[split_name] = output_path

    all_rows = splits["train"] + splits["validation"] + splits["test"]
    all_output_path = output_dir / "all.json"
    save_json(convert_rows_to_sharegpt(all_rows), all_output_path)
    output_paths["all"] = all_output_path

    return output_paths


def build_quality_report(
    rows: list[dict[str, str]],
    splits: dict[str, list[dict[str, str]]],
    duplicates: list[dict[str, object]],
    source_path: Path,
    split_config: SplitConfig,
) -> str:
    """Build a Markdown data quality report."""

    label_counts = Counter(row["support_team"] for row in rows)
    split_counts = {split_name: len(split_rows) for split_name, split_rows in splits.items()}

    lines = [
        "# Data Quality Report",
        "",
        "## Source",
        "",
        f"- Source CSV: `{source_path}`",
        f"- Total records: {len(rows)}",
        f"- Required columns: {', '.join(REQUIRED_COLUMNS)}",
        f"- Split seed: {split_config.seed}",
        f"- Target split: {split_config.train_ratio:.0%} train / "
        f"{split_config.validation_ratio:.0%} validation / {split_config.test_ratio:.0%} test",
        "",
        "## Validation Summary",
        "",
        "- Required columns: passed",
        "- Required values: passed",
        "- Support-team taxonomy: passed",
        f"- Duplicate title and description pairs: {len(duplicates)}",
        "",
        "## Class Distribution",
        "",
        "| Support Team | Records |",
        "|---|---:|",
    ]

    for support_team in APPROVED_SUPPORT_TEAMS:
        lines.append(f"| {support_team} | {label_counts.get(support_team, 0)} |")

    lines.extend(
        [
            "",
            "## Split Distribution",
            "",
            "| Split | Records |",
            "|---|---:|",
        ]
    )

    for split_name in ("train", "validation", "test"):
        lines.append(f"| {split_name} | {split_counts[split_name]} |")

    lines.extend(
        [
            "",
            "## Split Distribution by Support Team",
            "",
            "| Support Team | Train | Validation | Test |",
            "|---|---:|---:|---:|",
        ]
    )

    for support_team in APPROVED_SUPPORT_TEAMS:
        train_count = count_label(splits["train"], support_team)
        validation_count = count_label(splits["validation"], support_team)
        test_count = count_label(splits["test"], support_team)
        lines.append(f"| {support_team} | {train_count} | {validation_count} | {test_count} |")

    if duplicates:
        lines.extend(["", "## Duplicate Pairs", ""])
        for duplicate in duplicates:
            lines.append(f"- {', '.join(duplicate['incident_ids'])}")
    else:
        lines.extend(["", "## Duplicate Pairs", "", "No duplicate title and description pairs found."])

    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- This report validates the 100-row public-safe synthetic pilot dataset.",
            "- The processed JSON files are intended for SFT pipeline testing, not final model claims.",
            "- No model training was performed by the dataset preparation utility.",
            "",
        ]
    )

    return "\n".join(lines)


def count_label(rows: list[dict[str, str]], support_team: str) -> int:
    """Count support-team examples in a split."""

    return sum(1 for row in rows if row["support_team"] == support_team)


def save_quality_report(report: str, output_path: Path) -> None:
    """Save a Markdown data quality report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")


def prepare_dataset(
    input_csv: Path,
    splits_output_dir: Path,
    report_output_path: Path,
    split_config: SplitConfig = SplitConfig(),
) -> dict[str, object]:
    """Run the full dataset preparation workflow."""

    with input_csv.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        validate_required_columns(reader.fieldnames)
        rows = [dict(row) for row in reader]

    validate_required_values(rows)
    validate_support_teams(rows)

    duplicates = find_duplicate_title_description_pairs(rows)
    if duplicates:
        duplicate_ids = [", ".join(item["incident_ids"]) for item in duplicates]
        raise ValueError(f"Duplicate title and description pairs found: {'; '.join(duplicate_ids)}")

    splits = create_stratified_splits(rows, split_config)
    output_paths = save_split_outputs(splits, splits_output_dir)
    report = build_quality_report(rows, splits, duplicates, input_csv, split_config)
    save_quality_report(report, report_output_path)

    return {
        "rows": rows,
        "splits": splits,
        "output_paths": output_paths,
        "report_output_path": report_output_path,
    }

