# Fine-Tuning Plan

OpsTriage AI will fine-tune an open-source language model to classify enterprise production incidents into the correct support team.

This document summarizes the Sprint 3 fine-tuning setup. No model training has been run yet.

## Objective

Given:

- Incident title
- Incident description

Predict:

- One approved support-team label

The model is a decision-support component. It does not automatically assign incidents or replace human review.

## Model Choice

Selected model:

- `Qwen/Qwen3-1.7B`

Why this model:

- Small enough for practical LoRA fine-tuning.
- Strong instruction-following family.
- Suitable for structured classification prompts.
- Reasonable portfolio model for demonstrating open-source fine-tuning.

Important note:

Qwen3 supports thinking and non-thinking behavior. For this classification task, the model should return only the final support-team label. We should avoid training chain-of-thought or verbose explanations in Version 1.

## Fine-Tuning Approach

Method:

- LoRA supervised fine-tuning

Why LoRA:

- Updates a small adapter instead of all model weights.
- Reduces compute and storage requirements.
- Makes experiments easier to version and compare.
- Fits the portfolio goal without creating very large artifacts.

## Dataset Version

Current dataset:

- Source CSV: `data/sample/sample_incidents.csv`
- Processed train split: `data/processed/splits/train.json`
- Processed validation split: `data/processed/splits/validation.json`
- Processed test split: `data/processed/splits/test.json`
- Quality report: `outputs/data_quality/sample_incidents_report.md`

Current dataset size:

- Train: 70
- Validation: 15
- Test: 15
- Total: 100

This 100-row dataset is appropriate for pipeline validation and smoke testing. It is not large enough for strong final model claims. Before final fine-tuning claims, expand toward the planned 500-record dataset.

## Training Parameters

| Parameter | Value | Rationale |
|---|---:|---|
| Base model | `Qwen/Qwen3-1.7B` | Practical open-source model for LoRA fine-tuning. |
| Training stage | Supervised fine-tuning | The task has labeled input-output examples. |
| Fine-tuning method | LoRA | Efficient adapter tuning. |
| Max sequence length | `1024` | Incident title and description are short; longer context is unnecessary. |
| Learning rate | `1e-4` | Conservative starting point for a small domain dataset. |
| Epochs | `4` | Enough passes for domain adaptation while watching overfitting. |
| Effective batch size | `16` | Achieved with small per-device batch and gradient accumulation. |
| LoRA rank | `16` | Good balance between capacity and overfitting risk. |
| LoRA alpha | `32` | Common scaling choice for rank 16. |
| LoRA dropout | `0.05` | Adds regularization for a small dataset. |
| Optimizer | AdamW | Standard optimizer for adapter fine-tuning. |
| Scheduler | Cosine | Smooth decay after warmup. |
| Evaluation | Each epoch | Allows checkpoint comparison and overfitting detection. |

## Expected Outputs

Training should eventually produce:

- LoRA adapter checkpoint
- Training logs
- Validation metrics by epoch
- Test metrics for the selected checkpoint
- Confusion matrix
- Error analysis report
- Optional merged model artifact
- Model card update

Recommended paths:

- Checkpoints: `models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0/`
- Merged model: `models/merged/qwen3-1.7b-opstriage-v0.1.0/`
- Training logs: `outputs/training_logs/qwen3-1.7b-lora-opstriage-v0.1.0/`
- Evaluation reports: `outputs/evaluation/`

Large artifacts should not be committed to GitHub.

## Evaluation Plan

Compare:

- Base Qwen3-1.7B
- Fine-tuned LoRA adapter
- Merged model, if created

Metrics:

- Accuracy
- Precision
- Recall
- Macro F1
- Weighted F1
- Confusion matrix
- Invalid-label rate

Primary model-selection metric:

- Macro F1

Why:

All support teams matter. Weighted F1 can hide weak performance on smaller classes.

## Risks

### Dataset Size

The current 100-row dataset is too small for strong final performance claims.

Mitigation:

- Treat current training as a smoke test only.
- Expand toward 500 examples before final evaluation.

### Overfitting

The model may memorize small synthetic examples.

Mitigation:

- Track validation metrics each epoch.
- Use dropout.
- Compare train and validation loss.
- Add more varied incidents before final training.

### Invalid Labels

The model may output labels outside the approved taxonomy.

Mitigation:

- Use exact-label prompts.
- Validate outputs against taxonomy.
- Consider constrained label scoring during inference.

### Similar-Team Confusion

Likely confusion pairs:

- Digital Experience vs API Platform
- Data Engineering vs Reporting & Analytics
- Security vs Identity & Access
- Infrastructure vs Database Engineering
- Batch Processing vs Integration Services

Mitigation:

- Add more contrastive examples.
- Improve annotation guidelines.
- Use confusion matrix analysis after each run.

### Notebook Drift

The Week 5 notebook may use tutorial assumptions that are not production-ready.

Mitigation:

- Reuse the workflow structure.
- Replace data, prompt, metrics, outputs, and artifact naming with OpsTriage-specific versions.

## Current Status

Sprint 3.2 creates configuration and documentation only.

Not performed:

- No model download
- No LLaMA Factory install or execution
- No LoRA training
- No checkpoint creation
- No merged model creation

