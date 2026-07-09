from __future__ import annotations

import pytest

from inference.inference import (
    build_human_review_recommendation,
    build_incident_prompt,
    extract_approved_label,
)


def test_build_incident_prompt_includes_inputs_and_taxonomy() -> None:
    prompt = build_incident_prompt(
        "Provider portal timeout",
        "Authorization tab spins for provider users.",
    )

    assert "Incident Title: Provider portal timeout" in prompt
    assert "Incident Description: Authorization tab spins for provider users." in prompt
    assert "Approved Support Teams:" in prompt
    assert "Provider Systems" in prompt


def test_extract_approved_label_accepts_exact_label() -> None:
    assert extract_approved_label("API Platform") == "API Platform"


def test_extract_approved_label_extracts_single_embedded_label() -> None:
    assert extract_approved_label("The correct team is Billing Systems.") == "Billing Systems"


def test_extract_approved_label_rejects_ambiguous_output() -> None:
    assert extract_approved_label("API Platform or Integration Services") is None


def test_extract_approved_label_rejects_unknown_output() -> None:
    assert extract_approved_label("Customer Support") is None


@pytest.mark.parametrize(
    ("predicted_team", "expected_phrase"),
    [
        ("Claims Engineering", "Human Review Recommended"),
        (None, "Human Review Required"),
    ],
)
def test_human_review_recommendation_is_confidence_honest(
    predicted_team: str | None, expected_phrase: str
) -> None:
    recommendation = build_human_review_recommendation(predicted_team)

    assert expected_phrase in recommendation
