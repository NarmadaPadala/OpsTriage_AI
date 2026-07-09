"""Factory for selecting security-evaluation model runners."""

from __future__ import annotations

from pathlib import Path

from model_runner.base import BaseModelRunner
from model_runner.mock_runner import MockModelRunner
from model_runner.opstriage_v1_runner import OpsTriageV1Runner


SUPPORTED_RUNNER_MODES = ("mock", "opstriage_v1")


def create_model_runner(mode: str = "mock", adapter_path: Path | None = None) -> BaseModelRunner:
    """Create a model runner by mode."""

    normalized_mode = mode.strip().casefold()

    if normalized_mode == "mock":
        return MockModelRunner()

    if normalized_mode == "opstriage_v1":
        return OpsTriageV1Runner(adapter_path=adapter_path) if adapter_path else OpsTriageV1Runner()

    raise ValueError(
        f"Unsupported model runner mode '{mode}'. Supported modes: "
        + ", ".join(SUPPORTED_RUNNER_MODES)
    )
