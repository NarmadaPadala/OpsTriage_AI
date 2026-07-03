# Training Runbook

This runbook summarizes the reproducible workflow for OpsTriage AI LoRA fine-tuning.

## Local Preparation

Run locally before GPU training:

```bash
python3 scripts/prepare_dataset.py
python3 -m pytest tests/test_dataset_preparation.py
```

Expected outputs:

- `data/processed/splits/train.json`
- `data/processed/splits/validation.json`
- `data/processed/splits/test.json`
- `outputs/data_quality/sample_incidents_report.md`

## NVIDIA Brev Setup

Use NVIDIA Brev for GPU training.

Recommended environment:

- Python 3.11
- CUDA-enabled PyTorch
- LLaMA Factory v0.9.5
- NVIDIA L4 GPU or better

Core validation commands:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
llamafactory-cli version
python -m json.tool data/dataset_info.json
```

## Dataset Registry

The active LLaMA Factory dataset registry is:

```text
data/dataset_info.json
```

Important path rule:

LLaMA Factory resolves dataset `file_name` values relative to `data/`. Therefore the registry uses:

```json
"file_name": "processed/splits/train.json"
```

not:

```json
"file_name": "data/processed/splits/train.json"
```

## Smoke Training

Run smoke training before full training:

```bash
llamafactory-cli train configs/training/llamafactory_qwen3_1_7b_lora_smoke.yaml
```

Smoke training verifies:

- GPU access
- model loading
- tokenizer loading
- dataset registration
- ShareGPT/OpenAI formatting
- LoRA attachment
- output directory behavior

## Full Fine-Tuning

After smoke training succeeds:

```bash
llamafactory-cli train configs/training/llamafactory_qwen3_1_7b_lora_sft.yaml
```

Completed Week 5 adapter path:

```text
models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0
```

## Artifact Handling

Commit:

- configs
- docs
- synthetic sample data
- processed split JSON
- data quality reports
- evaluation summaries

Do not commit:

- model checkpoints
- adapter weights
- optimizer state
- scheduler state
- trainer state
- downloaded base models
- cache directories

## Troubleshooting Notes

### Dataset Path Resolution

Symptom:

```text
File data/data/processed/splits/train.json not found
```

Fix:

Use `processed/splits/train.json` in `data/dataset_info.json`.

### LLaMA Factory Config Compatibility

Symptom:

Unsupported config field involving generation length.

Fix:

Use `max_new_tokens` for LLaMA Factory v0.9.5.

### Best-Model Metric Mismatch

Symptom:

Trainer cannot select best checkpoint by `eval_macro_f1`.

Fix:

Save checkpoints and run classification evaluation separately.

### Local Machine Limitations

Symptom:

Slow training or out-of-memory on local Mac.

Fix:

Use NVIDIA Brev or another CUDA GPU environment.

