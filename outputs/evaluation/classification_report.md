# Classification Evaluation Report

## Current Status

Classification evaluation code is implemented in `scripts/evaluate_classification.py`, but adapter-backed
test-set predictions have not been generated in this local checkout because model artifacts are not stored
in Git.

No accuracy, precision, recall, F1, invalid-label rate, or confusion-matrix result is claimed here.

## How to Generate Results

Create a predictions CSV with these columns:

```text
incident_title,incident_description,actual_team,predicted_team
```

Then run:

```bash
python scripts/evaluate_classification.py \
  --predictions outputs/evaluation/model_predictions.csv \
  --output-dir outputs/evaluation
```

The script writes:

- `outputs/evaluation/classification_report.md`
- `outputs/evaluation/confusion_matrix.png`

## Responsible Interpretation

The pilot dataset is intentionally small. Classification metrics are useful for pipeline validation
and error analysis, but they should not be presented as production-quality evidence without a larger
and more representative evaluation set.
