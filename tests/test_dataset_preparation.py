from __future__ import annotations

import pytest

from config.taxonomy import APPROVED_SUPPORT_TEAMS
from preprocessing.dataset_preparation import (
    SplitConfig,
    create_stratified_splits,
    find_duplicate_title_description_pairs,
    incident_to_sharegpt,
    validate_required_columns,
    validate_support_teams,
)


def make_row(
    incident_id: str = "INC-TEST",
    title: str = "Claims API timeout",
    description: str = "Claims status API is timing out through the gateway.",
    support_team: str = "API Platform",
) -> dict[str, str]:
    return {
        "incident_id": incident_id,
        "incident_title": title,
        "incident_description": description,
        "support_team": support_team,
    }


def test_validate_required_columns_accepts_expected_schema() -> None:
    validate_required_columns(
        ["incident_id", "incident_title", "incident_description", "support_team"]
    )


def test_validate_required_columns_rejects_missing_column() -> None:
    with pytest.raises(ValueError, match="incident_description"):
        validate_required_columns(["incident_id", "incident_title", "support_team"])


def test_validate_support_teams_rejects_unknown_label() -> None:
    rows = [make_row(support_team="Unknown Team")]

    with pytest.raises(ValueError, match="Unknown Team"):
        validate_support_teams(rows)


def test_duplicate_detection_normalizes_title_and_description() -> None:
    rows = [
        make_row("INC-001", "  Claims API timeout ", "Gateway timeout on claims API."),
        make_row("INC-002", "claims api timeout", "Gateway   timeout on claims API."),
    ]

    duplicates = find_duplicate_title_description_pairs(rows)

    assert len(duplicates) == 1
    assert duplicates[0]["incident_ids"] == ["INC-001", "INC-002"]


def test_incident_to_sharegpt_uses_expected_roles_and_label() -> None:
    record = incident_to_sharegpt(make_row())

    assert [message["role"] for message in record["messages"]] == [
        "system",
        "user",
        "assistant",
    ]
    assert record["messages"][2]["content"] == "API Platform"
    assert "Incident Title: Claims API timeout" in record["messages"][1]["content"]
    assert "Approved Support Teams:" in record["messages"][1]["content"]


def test_stratified_split_keeps_each_label_in_each_split() -> None:
    rows: list[dict[str, str]] = []
    for support_team in APPROVED_SUPPORT_TEAMS[:3]:
        for index in range(6):
            rows.append(
                make_row(
                    incident_id=f"{support_team[:3]}-{index}",
                    title=f"{support_team} incident {index}",
                    description=f"Description for {support_team} incident {index}",
                    support_team=support_team,
                )
            )

    splits = create_stratified_splits(rows, SplitConfig(seed=7))

    assert len(splits["train"]) == 12
    assert len(splits["validation"]) == 3
    assert len(splits["test"]) == 3

    for support_team in APPROVED_SUPPORT_TEAMS[:3]:
        assert any(row["support_team"] == support_team for row in splits["train"])
        assert any(row["support_team"] == support_team for row in splits["validation"])
        assert any(row["support_team"] == support_team for row in splits["test"])

