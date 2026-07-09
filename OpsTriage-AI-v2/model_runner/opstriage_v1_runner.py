"""Runner that calls the existing OpsTriage AI v1 inference pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

from model_runner.base import BaseModelRunner


PROJECT_ROOT = Path(__file__).resolve().parents[2]
V1_SRC_DIR = PROJECT_ROOT / "src"
DEFAULT_ADAPTER_PATH = PROJECT_ROOT / "models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0"


class OpsTriageV1Runner(BaseModelRunner):
    """Optional adapter-backed runner for the fine-tuned OpsTriage v1 model."""

    name = "opstriage_v1"

    def __init__(self, adapter_path: Path = DEFAULT_ADAPTER_PATH) -> None:
        self.adapter_path = adapter_path
        self._router = None
        self._configuration_error: str | None = None

    def run(self, prompt: str) -> str:
        """Run the attack prompt through the v1 incident router.

        The security prompt is wrapped as an incident description because v1 is a routing model,
        not a chat model. If model artifacts are unavailable, this returns a clear non-model-backed
        response rather than raising through the UI or report pipeline.
        """

        if not self.adapter_path.exists():
            return self._unavailable_response(
                f"LoRA adapter not found at {self.adapter_path}."
            )

        try:
            router = self._get_router()
            prediction = router.predict(
                title="Security red-team evaluation",
                description=prompt,
            )
        except Exception as exc:  # pragma: no cover - exercised with real model environment
            return self._unavailable_response(str(exc))

        return (
            f"Predicted Support Team: {prediction.predicted_team}\n"
            f"Model Version: {prediction.model_version}\n"
            f"Human Review Recommendation: {prediction.human_review_recommendation}\n"
            f"Raw Model Output: {prediction.raw_model_output}"
        )

    def _get_router(self):
        if self._router is not None:
            return self._router

        if str(V1_SRC_DIR) not in sys.path:
            sys.path.insert(0, str(V1_SRC_DIR))

        try:
            from inference.inference import QwenLoRAIncidentRouter
        except ImportError as exc:
            raise RuntimeError(
                "Could not import OpsTriage v1 inference pipeline from src/inference."
            ) from exc

        self._router = QwenLoRAIncidentRouter(adapter_path=self.adapter_path)
        return self._router

    @staticmethod
    def _unavailable_response(reason: str) -> str:
        return (
            "MODEL_UNAVAILABLE: OpsTriage v1 adapter-backed inference could not run. "
            f"Reason: {reason} No model-backed security finding is claimed from this response."
        )
