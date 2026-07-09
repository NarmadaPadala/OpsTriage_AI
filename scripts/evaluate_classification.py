"""Compute classification metrics for OpsTriage AI predictions.

Expected predictions CSV columns:

- incident_title
- incident_description
- actual_team
- predicted_team

The script intentionally requires actual predictions. It does not use labels as
predictions and does not infer improvements from generation metrics.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config.taxonomy import APPROVED_SUPPORT_TEAMS


REQUIRED_COLUMNS = ("actual_team", "predicted_team")
INVALID_LABEL = "INVALID_LABEL"


def load_prediction_rows(predictions_path: Path) -> list[dict[str, str]]:
    with predictions_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = sorted(set(REQUIRED_COLUMNS) - set(reader.fieldnames or []))
        if missing:
            raise ValueError(f"Missing required prediction columns: {', '.join(missing)}")
        return [dict(row) for row in reader]


def validate_actual_labels(rows: list[dict[str, str]]) -> None:
    invalid_actual = sorted(
        {row["actual_team"] for row in rows if row["actual_team"] not in APPROVED_SUPPORT_TEAMS}
    )
    if invalid_actual:
        raise ValueError(f"Invalid actual_team labels: {', '.join(invalid_actual)}")


def normalize_prediction(label: str) -> str:
    label = label.strip()
    return label if label in APPROVED_SUPPORT_TEAMS else INVALID_LABEL


def compute_metrics(rows: list[dict[str, str]]) -> dict[str, float]:
    y_true = [row["actual_team"] for row in rows]
    y_pred = [normalize_prediction(row["predicted_team"]) for row in rows]
    valid_y_pred = [label if label in APPROVED_SUPPORT_TEAMS else INVALID_LABEL for label in y_pred]
    metric_labels = list(APPROVED_SUPPORT_TEAMS)

    invalid_count = sum(label == INVALID_LABEL for label in valid_y_pred)
    return {
        "accuracy": accuracy_score(y_true, valid_y_pred),
        "precision_macro": precision_score(
            y_true, valid_y_pred, labels=metric_labels, average="macro", zero_division=0
        ),
        "recall_macro": recall_score(
            y_true, valid_y_pred, labels=metric_labels, average="macro", zero_division=0
        ),
        "macro_f1": f1_score(
            y_true, valid_y_pred, labels=metric_labels, average="macro", zero_division=0
        ),
        "weighted_f1": f1_score(
            y_true, valid_y_pred, labels=metric_labels, average="weighted", zero_division=0
        ),
        "invalid_label_rate": invalid_count / len(rows) if rows else 0.0,
    }


def save_confusion_matrix(rows: list[dict[str, str]], output_path: Path) -> None:
    y_true = [row["actual_team"] for row in rows]
    y_pred = [normalize_prediction(row["predicted_team"]) for row in rows]
    labels = list(APPROVED_SUPPORT_TEAMS) + [INVALID_LABEL]
    matrix = confusion_matrix(y_true, y_pred, labels=labels)

    fig, ax = plt.subplots(figsize=(12, 10))
    display = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=labels)
    display.plot(ax=ax, xticks_rotation=45, colorbar=False)
    ax.set_title("OpsTriage AI Confusion Matrix")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def build_report(rows: list[dict[str, str]], metrics: dict[str, float], predictions_path: Path) -> str:
    y_true = [row["actual_team"] for row in rows]
    y_pred = [normalize_prediction(row["predicted_team"]) for row in rows]
    labels = list(APPROVED_SUPPORT_TEAMS) + [INVALID_LABEL]
    report = classification_report(
        y_true,
        y_pred,
        labels=labels,
        zero_division=0,
    )

    lines = [
        "# Classification Evaluation Report",
        "",
        "## Source",
        "",
        f"- Predictions file: `{predictions_path}`",
        f"- Evaluated records: {len(rows)}",
        "- Metrics are computed from model predictions, not generation-only BLEU/ROUGE scores.",
        "",
        "## Summary Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Accuracy | {metrics['accuracy']:.4f} |",
        f"| Precision Macro | {metrics['precision_macro']:.4f} |",
        f"| Recall Macro | {metrics['recall_macro']:.4f} |",
        f"| Macro F1 | {metrics['macro_f1']:.4f} |",
        f"| Weighted F1 | {metrics['weighted_f1']:.4f} |",
        f"| Invalid Label Rate | {metrics['invalid_label_rate']:.4f} |",
        "",
        "## Scikit-Learn Classification Report",
        "",
        "```text",
        report,
        "```",
        "",
        "## Responsible Interpretation",
        "",
        "These metrics should be interpreted against the small pilot dataset size. They are useful",
        "for validating the evaluation pipeline and identifying label confusions, but they are not",
        "a production-readiness claim.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate OpsTriage AI classification predictions.")
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/evaluation"))
    args = parser.parse_args()

    rows = load_prediction_rows(args.predictions)
    if not rows:
        raise ValueError("Prediction file is empty.")
    validate_actual_labels(rows)

    metrics = compute_metrics(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    save_confusion_matrix(rows, args.output_dir / "confusion_matrix.png")
    report = build_report(rows, metrics, args.predictions)
    (args.output_dir / "classification_report.md").write_text(report, encoding="utf-8")

    print(f"Wrote {args.output_dir / 'classification_report.md'}")
    print(f"Wrote {args.output_dir / 'confusion_matrix.png'}")


if __name__ == "__main__":
    main()
