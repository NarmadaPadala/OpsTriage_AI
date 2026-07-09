# Base Qwen vs Fine-Tuned Qwen

This workflow is implemented in `scripts/compare_base_vs_finetuned.py`.

## Current Status

The comparison has not been executed in this local checkout because the trained LoRA adapter files
are intentionally excluded from Git. This document is therefore a reproducibility note, not a claim
that the fine-tuned model improved over the base model.

## How to Run

```bash
python scripts/compare_base_vs_finetuned.py
```

The script runs several unseen incidents through:

1. Base `Qwen/Qwen3-1.7B`
2. Fine-tuned `Qwen/Qwen3-1.7B` with the OpsTriage LoRA adapter

It writes this document with:

- Prediction
- Difference
- Commentary

## Interpretation Rules

- Do not claim the fine-tuned model is better unless the comparison output supports it.
- Treat invalid or ambiguous generations as evaluation findings, not errors to hide.
- Keep the commentary focused on routing behavior and enterprise risk.
