from __future__ import annotations

from attacks import load_attack_cases
from evaluator import SecurityEvaluator
from model_runner import MockModelRunner, OpsTriageV1Runner
from ui_helpers import (
    ALL_CATEGORIES_LABEL,
    attack_name_options,
    attacks_for_category,
    category_options,
    dashboard_deployment_recommendation,
    evidence_table_rows,
    find_attack_by_option,
    has_model_unavailable,
    records_to_csv,
    records_to_markdown,
    run_attacks,
)


def test_category_options_include_all_categories_label() -> None:
    options = category_options(load_attack_cases())

    assert options[0] == ALL_CATEGORIES_LABEL
    assert "Prompt Injection" in options


def test_attacks_for_category_filters_cases() -> None:
    attacks = load_attack_cases()
    filtered = attacks_for_category(attacks, "Prompt Injection")

    assert filtered
    assert {attack.category.value for attack in filtered} == {"Prompt Injection"}


def test_find_attack_by_option_returns_matching_case() -> None:
    attacks = load_attack_cases()
    option = attack_name_options(attacks)[0]

    attack = find_attack_by_option(attacks, option)

    assert option.startswith(attack.attack_id)


def test_run_attacks_uses_mock_runner() -> None:
    attack = load_attack_cases()[0]
    records = run_attacks([attack], "mock")

    assert len(records) == 1
    assert records[0].attack_id == attack.attack_id


def test_evidence_table_rows_use_required_columns() -> None:
    attack = load_attack_cases()[0]
    record = SecurityEvaluator(MockModelRunner()).evaluate_attack(attack)

    rows = evidence_table_rows([record])

    assert rows[0]["attack name"] == attack.name
    assert rows[0]["score"] in {"PASS", "WARN", "FAIL"}
    assert "recommended mitigation" in rows[0]


def test_export_serializers_include_evidence() -> None:
    attack = load_attack_cases()[0]
    record = SecurityEvaluator(MockModelRunner()).evaluate_attack(attack)

    csv_output = records_to_csv([record])
    markdown_output = records_to_markdown([record])

    assert "attack_id,attack_name" in csv_output
    assert attack.attack_id in csv_output
    assert "Security Validation Report" in markdown_output
    assert attack.attack_id in markdown_output


def test_dashboard_deployment_recommendation_is_present() -> None:
    attack = load_attack_cases()[0]
    record = SecurityEvaluator(MockModelRunner()).evaluate_attack(attack)

    recommendation = dashboard_deployment_recommendation([record])

    assert "human-in-the-loop" in recommendation


def test_has_model_unavailable_detects_missing_v1_adapter(tmp_path) -> None:
    runner = OpsTriageV1Runner(adapter_path=tmp_path / "missing-adapter")
    attack = load_attack_cases()[0]
    record = SecurityEvaluator(runner).evaluate_attack(attack)

    assert has_model_unavailable([record])
