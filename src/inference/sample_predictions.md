# Sample Predictions

This file documents the expected inference output shape. The trained LoRA adapter is not
stored in Git, so these examples should be regenerated after copying the adapter artifacts
to `models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0`.

## Run Command

```bash
python -m inference.inference \
  --title "Claims API returning 504 errors" \
  --description "Claims status lookups are timing out through the gateway for multiple call-center users."
```

## Output Contract

```json
{
  "predicted_team": "API Platform",
  "model_version": "qwen3-1.7b-lora-opstriage-v0.1.0",
  "inference_time_seconds": 1.2345,
  "human_review_recommendation": "Human Review Recommended - prediction is label-valid, but this local pipeline does not compute calibrated confidence.",
  "raw_model_output": "API Platform"
}
```

## Confidence Limitation

This project does not fabricate confidence scores. The current inference module validates whether
the model output is one approved support-team label, but it does not compute calibrated probability
or confidence.

In production, confidence could be implemented by capturing token-level probabilities for approved
labels, calibrating them on a held-out validation set, and setting thresholds with business owners.
Until that exists, OpsTriage AI should recommend human review even when the generated label is valid.
