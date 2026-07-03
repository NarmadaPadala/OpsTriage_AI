"""Prepare OpsTriage AI incident data for supervised fine-tuning."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from preprocessing.dataset_preparation import SplitConfig, prepare_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare OpsTriage AI dataset splits.")
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=Path("data/sample/sample_incidents.csv"),
        help="Path to the source incident CSV.",
    )
    parser.add_argument(
        "--splits-output-dir",
        type=Path,
        default=Path("data/processed/splits"),
        help="Directory where ShareGPT JSON split files will be written.",
    )
    parser.add_argument(
        "--report-output-path",
        type=Path,
        default=Path("outputs/data_quality/sample_incidents_report.md"),
        help="Path where the Markdown data quality report will be written.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic split seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = prepare_dataset(
        input_csv=args.input_csv,
        splits_output_dir=args.splits_output_dir,
        report_output_path=args.report_output_path,
        split_config=SplitConfig(seed=args.seed),
    )

    split_counts = {split_name: len(rows) for split_name, rows in result["splits"].items()}
    print("Dataset preparation complete.")
    print(f"Train records: {split_counts['train']}")
    print(f"Validation records: {split_counts['validation']}")
    print(f"Test records: {split_counts['test']}")
    print(f"Report: {args.report_output_path}")


if __name__ == "__main__":
    main()
