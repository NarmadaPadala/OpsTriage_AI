"""Compare base Qwen and fine-tuned Qwen predictions on unseen incidents."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from inference.inference import (
    DEFAULT_ADAPTER_PATH,
    DEFAULT_BASE_MODEL,
    MODEL_VERSION,
    QwenLoRAIncidentRouter,
    build_human_review_recommendation,
    extract_approved_label,
)


@dataclass(frozen=True)
class IncidentExample:
    title: str
    description: str


DEFAULT_EXAMPLES = [
    IncidentExample(
        "Provider roster sync failed for external directory",
        "The nightly provider roster file reached the vendor SFTP folder, but the vendor rejected it because required network affiliation fields were blank.",
    ),
    IncidentExample(
        "Members cannot download ID card PDF",
        "The member portal loads plan details, but clicking download ID card returns a blank PDF for multiple users.",
    ),
    IncidentExample(
        "Claim status API latency after deployment",
        "Client applications report 20 second response times from the claim status endpoint after the latest gateway deployment.",
    ),
]


class BaseQwenRouter(QwenLoRAIncidentRouter):
    """Use the same generation contract without applying a LoRA adapter."""

    def load(self) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "Missing dependencies. Install torch and transformers before comparison."
            ) from exc

        tokenizer = AutoTokenizer.from_pretrained(self.base_model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map=self.device_map,
            trust_remote_code=True,
        )
        model.eval()

        self._tokenizer = tokenizer
        self._model = model


def load_examples(path: Path | None) -> list[IncidentExample]:
    if path is None:
        return DEFAULT_EXAMPLES

    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [
            IncidentExample(row["incident_title"], row["incident_description"])
            for row in reader
        ]


def build_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Base Qwen vs Fine-Tuned Qwen",
        "",
        "This comparison is designed to be factual: it records the raw prediction from the",
        "base model and the fine-tuned LoRA model without inventing improvements.",
        "",
        f"- Base model: `{DEFAULT_BASE_MODEL}`",
        f"- Fine-tuned model version: `{MODEL_VERSION}`",
        f"- Adapter path: `{DEFAULT_ADAPTER_PATH}`",
        "",
        "| Incident | Base Qwen Prediction | Fine-Tuned Qwen Prediction | Difference | Commentary |",
        "|---|---|---|---|---|",
    ]

    for row in rows:
        lines.append(
            "| {incident} | {base} | {fine_tuned} | {difference} | {commentary} |".format(
                incident=row["incident"].replace("|", "\\|"),
                base=row["base_prediction"],
                fine_tuned=row["fine_tuned_prediction"],
                difference=row["difference"],
                commentary=row["commentary"].replace("|", "\\|"),
            )
        )

    lines.extend(
        [
            "",
            "## Confidence Limitation",
            "",
            "This workflow does not report confidence scores. A production version should compute",
            "and calibrate label probabilities before allowing auto-route recommendations.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare base and fine-tuned Qwen routing.")
    parser.add_argument("--examples", type=Path)
    parser.add_argument("--output", type=Path, default=Path("docs/BaseVsFineTuned.md"))
    parser.add_argument("--adapter-path", type=Path, default=DEFAULT_ADAPTER_PATH)
    args = parser.parse_args()

    examples = load_examples(args.examples)
    base_router = BaseQwenRouter()
    tuned_router = QwenLoRAIncidentRouter(adapter_path=args.adapter_path)

    rows: list[dict[str, str]] = []
    for example in examples:
        base_result = base_router.predict(example.title, example.description)
        tuned_result = tuned_router.predict(example.title, example.description)
        base_label = extract_approved_label(base_result.raw_model_output) or "INVALID_LABEL"
        tuned_label = extract_approved_label(tuned_result.raw_model_output) or "INVALID_LABEL"
        difference = "Same" if base_label == tuned_label else "Different"
        commentary = build_human_review_recommendation(tuned_label if tuned_label != "INVALID_LABEL" else None)
        rows.append(
            {
                "incident": example.title,
                "base_prediction": base_label,
                "fine_tuned_prediction": tuned_label,
                "difference": difference,
                "commentary": commentary,
            }
        )

    args.output.write_text(build_markdown(rows), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
