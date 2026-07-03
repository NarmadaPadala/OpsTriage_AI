# Smoke Training Plan

This plan defines the smallest safe training test for OpsTriage AI before any full fine-tuning run.

No smoke training has been executed yet.

## Objective

Verify that the environment, dataset registration, tokenizer, model loading, LoRA configuration, and output paths work end-to-end.

The smoke run is not intended to produce a useful model.

## Non-Goals

The smoke run should not:

- Claim model quality
- Produce final checkpoints
- Merge adapters
- Run full evaluation
- Replace the base-vs-fine-tuned comparison
- Use the full 100-row pilot dataset

## Dataset Scope

Use a tiny subset only:

- Maximum training samples: 12
- Maximum validation samples: 6
- Sequence length: 512 for smoke only
- Epochs: 1

The full training config remains:

- Sequence length: 1024
- Epochs: 4

## Pre-Run Checklist

Before running smoke training:

- Python 3.11 virtual environment exists.
- PyTorch imports successfully.
- `torch.backends.mps.is_available()` has been checked on Mac.
- LLaMA Factory imports successfully.
- `data/processed/splits/train.json` exists.
- `data/processed/splits/validation.json` exists.
- Dataset registration has been copied or linked into the active LLaMA Factory dataset registry.
- No large model artifacts are committed to Git.

## Smoke Run Configuration

Use:

```text
configs/training/llamafactory_qwen3_1_7b_lora_smoke.yaml
```

Expected behavior:

- Model and tokenizer load.
- LLaMA Factory accepts the dataset registration.
- A tiny LoRA training run starts and finishes.
- A small smoke output directory is created locally.
- Any checkpoint created during smoke testing remains local and uncommitted.

## Smoke Success Criteria

The smoke run passes if:

- Training starts without dataset-format errors.
- Tokenization completes.
- LoRA modules are attached.
- At least one training step completes.
- Evaluation step runs or is intentionally skipped for smoke.
- Output path is created without crashing.

The smoke run does not need high accuracy.

## Smoke Failure Criteria

Stop and troubleshoot if:

- Python package incompatibility occurs.
- LLaMA Factory cannot read the ShareGPT format.
- Qwen tokenizer template fails.
- MPS unsupported operation appears.
- Memory pressure terminates the process.
- The model produces invalid output formatting during smoke inference.

## After Smoke Training

If smoke passes locally:

1. Delete or ignore smoke checkpoints.
2. Run base-model classification benchmark.
3. Expand to a larger dataset if approved.
4. Decide whether full training should run locally or in cloud.

If smoke fails locally:

1. Do not spend time forcing full local training.
2. Move training to Colab, Kaggle, or GPU cloud.
3. Reuse the same dataset files and configs.

