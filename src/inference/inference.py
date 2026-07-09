"""Production-inspired inference pipeline for OpsTriage AI.

This module is intentionally small and explicit. It loads the fine-tuned LoRA
adapter when model artifacts are available, asks the model for exactly one
approved support-team label, validates the generated label, and returns routing
metadata that can be shown in a UI or captured by an evaluation script.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config.taxonomy import APPROVED_SUPPORT_TEAMS
from preprocessing.dataset_preparation import SYSTEM_PROMPT

DEFAULT_BASE_MODEL = "Qwen/Qwen3-1.7B"
DEFAULT_ADAPTER_PATH = Path("models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0")
MODEL_VERSION = "qwen3-1.7b-lora-opstriage-v0.1.0"
MAX_NEW_TOKENS = 32


class InferenceConfigurationError(RuntimeError):
    """Raised when inference cannot run because local model setup is incomplete."""


@dataclass(frozen=True)
class IncidentPrediction:
    """Structured inference response returned by the routing pipeline."""

    predicted_team: str
    model_version: str
    inference_time_seconds: float
    human_review_recommendation: str
    raw_model_output: str


def build_incident_prompt(title: str, description: str) -> str:
    """Build the user prompt used during fine-tuning and inference."""

    approved_team_list = ", ".join(APPROVED_SUPPORT_TEAMS)
    return (
        f"Incident Title: {title.strip()}\n"
        f"Incident Description: {description.strip()}\n\n"
        f"Approved Support Teams: {approved_team_list}"
    )


def extract_approved_label(model_output: str) -> str | None:
    """Extract exactly one approved support team from model text.

    The model was trained to return only the label. In production, this parser
    protects downstream systems from malformed generations or unsupported teams.
    """

    normalized_output = " ".join(model_output.strip().split())
    if normalized_output in APPROVED_SUPPORT_TEAMS:
        return normalized_output

    matches = [team for team in APPROVED_SUPPORT_TEAMS if team in normalized_output]
    if len(matches) == 1:
        return matches[0]

    return None


def build_human_review_recommendation(predicted_team: str | None) -> str:
    """Return a responsible routing recommendation without fabricating confidence."""

    if predicted_team is None:
        return "Human Review Required - model output was not an approved support-team label."

    return (
        "Human Review Recommended - prediction is label-valid, but this local pipeline "
        "does not compute calibrated confidence."
    )


class QwenLoRAIncidentRouter:
    """Adapter-backed incident router for the fine-tuned Qwen model."""

    def __init__(
        self,
        base_model_name: str = DEFAULT_BASE_MODEL,
        adapter_path: Path = DEFAULT_ADAPTER_PATH,
        model_version: str = MODEL_VERSION,
        device_map: str = "auto",
    ) -> None:
        self.base_model_name = base_model_name
        self.adapter_path = adapter_path
        self.model_version = model_version
        self.device_map = device_map
        self._tokenizer: Any | None = None
        self._model: Any | None = None

    def load(self) -> None:
        """Load tokenizer, base model, and LoRA adapter.

        Adapter files are intentionally excluded from Git. If they are not
        present, the caller receives an actionable setup error instead of a
        silent fallback prediction.
        """

        if not self.adapter_path.exists():
            raise InferenceConfigurationError(
                "LoRA adapter not found at "
                f"{self.adapter_path}. Copy the trained adapter artifacts into this "
                "path or pass --adapter-path to a local checkpoint before running inference."
            )

        try:
            import torch
            from peft import PeftModel
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise InferenceConfigurationError(
                "Missing inference dependencies. Install requirements.txt, including "
                "torch, transformers, and peft, before running adapter-backed inference."
            ) from exc

        tokenizer = AutoTokenizer.from_pretrained(self.base_model_name, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map=self.device_map,
            trust_remote_code=True,
        )
        model = PeftModel.from_pretrained(base_model, str(self.adapter_path))
        model.eval()

        self._tokenizer = tokenizer
        self._model = model

    def predict(self, title: str, description: str) -> IncidentPrediction:
        """Predict one approved support team for an incident."""

        if not title.strip() or not description.strip():
            raise ValueError("Incident title and description are required.")

        if self._model is None or self._tokenizer is None:
            self.load()

        assert self._model is not None
        assert self._tokenizer is not None

        start_time = time.perf_counter()
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_incident_prompt(title, description)},
        ]
        prompt = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)

        generated_ids = self._model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=self._tokenizer.eos_token_id,
        )
        new_tokens = generated_ids[0][inputs["input_ids"].shape[-1] :]
        raw_output = self._tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        elapsed = time.perf_counter() - start_time

        predicted_team = extract_approved_label(raw_output)
        return IncidentPrediction(
            predicted_team=predicted_team or "INVALID_LABEL",
            model_version=self.model_version,
            inference_time_seconds=round(elapsed, 4),
            human_review_recommendation=build_human_review_recommendation(predicted_team),
            raw_model_output=raw_output,
        )


def predict_incident(
    title: str,
    description: str,
    adapter_path: Path = DEFAULT_ADAPTER_PATH,
    base_model_name: str = DEFAULT_BASE_MODEL,
) -> IncidentPrediction:
    """Convenience function for one-off adapter-backed predictions."""

    router = QwenLoRAIncidentRouter(base_model_name=base_model_name, adapter_path=adapter_path)
    return router.predict(title, description)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OpsTriage AI adapter-backed inference.")
    parser.add_argument("--title", required=True, help="Incident title")
    parser.add_argument("--description", required=True, help="Incident description")
    parser.add_argument("--adapter-path", type=Path, default=DEFAULT_ADAPTER_PATH)
    parser.add_argument("--base-model", default=DEFAULT_BASE_MODEL)
    args = parser.parse_args()

    result = predict_incident(args.title, args.description, args.adapter_path, args.base_model)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
