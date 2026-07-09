from __future__ import annotations

from scripts.evaluate_classification import compute_metrics, normalize_prediction


def test_normalize_prediction_marks_unknown_labels_invalid() -> None:
    assert normalize_prediction("Customer Support") == "INVALID_LABEL"


def test_compute_metrics_includes_invalid_label_rate() -> None:
    rows = [
        {"actual_team": "API Platform", "predicted_team": "API Platform"},
        {"actual_team": "Billing Systems", "predicted_team": "Customer Support"},
    ]

    metrics = compute_metrics(rows)

    assert metrics["accuracy"] == 0.5
    assert metrics["invalid_label_rate"] == 0.5
