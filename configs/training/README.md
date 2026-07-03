# Training Configuration

This directory contains Sprint 3.2 fine-tuning setup artifacts for OpsTriage AI.

No training has been run from these files yet.

## Files

- `dataset_info_opstriage.json` - LLaMA Factory-style dataset registration for the processed train, validation, and test JSON files.
- `llamafactory_qwen3_1_7b_lora_sft.yaml` - Proposed LoRA supervised fine-tuning configuration for Qwen3-1.7B.
- `llamafactory_qwen3_1_7b_lora_smoke.yaml` - Tiny smoke-training configuration for environment validation only.

## Dataset Paths

- Train: `data/processed/splits/train.json`
- Validation: `data/processed/splits/validation.json`
- Test: `data/processed/splits/test.json`

## Important Notes

- Validate the config against the installed LLaMA Factory version before running.
- `eval_macro_f1` may require a custom metric hook or post-training evaluation script. If LLaMA Factory cannot select the best checkpoint by macro F1 directly, save checkpoints each epoch and select the best checkpoint using the OpsTriage evaluation pipeline.
- Do not commit downloaded base models, LoRA checkpoints, merged models, or training caches.
- Use the smoke config before running the full SFT config.

## NVIDIA Brev Workflow

OpsTriage AI will use NVIDIA Brev for GPU training because the local Mac has only 8 GB unified memory.

Recommended sequence inside Brev:

```bash
nvidia-smi
git clone https://github.com/NarmadaPadala/OpsTriage_AI.git
cd OpsTriage_AI
conda create -n opstriage python=3.11 -y
conda activate opstriage
python -m pip install --upgrade pip
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python -m pip install -r requirements.txt
python -c "import torch; print(torch.cuda.is_available())"
python3 scripts/prepare_dataset.py
```

Then register `configs/training/dataset_info_opstriage.json` with the active LLaMA Factory dataset registry and run the smoke config first:

```bash
llamafactory-cli train configs/training/llamafactory_qwen3_1_7b_lora_smoke.yaml
```

Only after smoke training succeeds:

```bash
llamafactory-cli train configs/training/llamafactory_qwen3_1_7b_lora_sft.yaml
```

See [docs/NVIDIABrevTrainingPlan.md](../../docs/NVIDIABrevTrainingPlan.md) for the full Brev runbook, artifact handling rules, and troubleshooting notes.
