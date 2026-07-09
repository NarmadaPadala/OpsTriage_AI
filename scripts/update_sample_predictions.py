"""Create sample prediction documentation from real inference outputs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_PREDICTIONS_PATH = Path("outputs/evaluation/model_predictions.csv")
DEFAULT_OUTPUT_PATH = Path("src/inference/sample_predictions.md")


def load_prediction_rows(predictions_path: Path, limit: int) -> list[dict[str, str]]:
    with predictions_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = [dict(row) for row in reader]

    required_columns = {
        "incident_title",
        "incident_description",
        "actual_team",
        "predicted_team",
        "model_version",
        "inference_time_seconds",
        "human_review_recommendation",
        "raw_model_output",
    }
    missing = sorted(required_columns - set(rows[0].keys() if rows else []))
    if missing:
        raise ValueError(f"Missing prediction columns: {', '.join(missing)}")

    return rows[:limit]


def build_markdown(rows: list[dict[str, str]], predictions_path: Path) -> str:
    lines = [
        "# Sample Predictions",
        "",
        "These examples were generated from adapter-backed inference outputs.",
        "",
        f"- Source predictions: `{predictions_path}`",
        "",
        "| Incident Title | Actual Team | Predicted Team | Model Version | Inference Time | Human Review Recommendation |",
        "|---|---|---|---|---:|---|",
    ]

    for row in rows:
        lines.append(
            "| {title} | {actual} | {predicted} | {version} | {time}s | {review} |".format(
                title=row["incident_title"].replace("|", "\\|"),
                actual=row["actual_team"],
                predicted=row["predicted_team"],
                version=row["model_version"],
                time=row["inference_time_seconds"],
                review=row["human_review_recommendation"].replace("|", "\\|"),
            )
        )

    lines.extend(
        [
            "",
            "## Confidence Limitation",
            "",
            "OpsTriage AI does not fabricate confidence scores. The current inference workflow",
            "validates approved support-team labels and recommends human review unless calibrated",
            "confidence is implemented and validated.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Update sample prediction documentation.")
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    rows = load_prediction_rows(args.predictions, args.limit)
    if not rows:
        raise ValueError("Prediction file is empty.")

    args.output.write_text(build_markdown(rows, args.predictions), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
