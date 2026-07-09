"""Generate adapter-backed predictions for the held-out test split."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from inference.inference import DEFAULT_ADAPTER_PATH, QwenLoRAIncidentRouter


def extract_test_rows(test_json_path: Path) -> list[dict[str, str]]:
    records = json.loads(test_json_path.read_text(encoding="utf-8"))
    rows: list[dict[str, str]] = []
    for record in records:
        messages = record["messages"]
        user_content = messages[1]["content"]
        title = user_content.split("Incident Title:", 1)[1].split("\n", 1)[0].strip()
        description = (
            user_content.split("Incident Description:", 1)[1]
            .split("\n\nApproved Support Teams:", 1)[0]
            .strip()
        )
        rows.append(
            {
                "incident_title": title,
                "incident_description": description,
                "actual_team": messages[2]["content"].strip(),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OpsTriage inference on the test split.")
    parser.add_argument("--test-json", type=Path, default=Path("data/processed/splits/test.json"))
    parser.add_argument("--adapter-path", type=Path, default=DEFAULT_ADAPTER_PATH)
    parser.add_argument("--output", type=Path, default=Path("outputs/evaluation/model_predictions.csv"))
    args = parser.parse_args()

    router = QwenLoRAIncidentRouter(adapter_path=args.adapter_path)
    rows = extract_test_rows(args.test_json)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "incident_title",
            "incident_description",
            "actual_team",
            "predicted_team",
            "model_version",
            "inference_time_seconds",
            "human_review_recommendation",
            "raw_model_output",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            prediction = router.predict(row["incident_title"], row["incident_description"])
            writer.writerow(
                {
                    **row,
                    "predicted_team": prediction.predicted_team,
                    "model_version": prediction.model_version,
                    "inference_time_seconds": prediction.inference_time_seconds,
                    "human_review_recommendation": prediction.human_review_recommendation,
                    "raw_model_output": prediction.raw_model_output,
                }
            )

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
