# NVIDIA Brev Training Plan

This document defines the cloud GPU training workflow for OpsTriage AI using NVIDIA Brev.

No commands in this document have been executed locally. No model has been downloaded. No training has been started.

## Decision

OpsTriage AI will use NVIDIA Brev for Qwen3-1.7B LoRA fine-tuning because the local Mac has only 8 GB unified memory. The local machine remains the development and documentation environment. Brev becomes the GPU execution environment for smoke training, full LoRA fine-tuning, and artifact generation.

## Full Workflow

### 1. Develop Locally in VS Code

Use the local repo for:

- Product documentation
- Dataset design
- Dataset generation
- Dataset validation
- Data preparation scripts
- Training configs
- Evaluation scripts
- GitHub-ready project structure

Local development keeps the project clean and reviewable before moving compute-heavy work to the GPU environment.

### 2. Prepare Dataset Locally

Before using Brev, run the local data pipeline:

```bash
python3 scripts/prepare_dataset.py
```

Expected local outputs:

- `data/processed/splits/train.json`
- `data/processed/splits/validation.json`
- `data/processed/splits/test.json`
- `data/processed/splits/all.json`
- `outputs/data_quality/sample_incidents_report.md`

These files are small and safe to commit because they contain synthetic public-safe data.

### 3. Upload Repo or Files to NVIDIA Brev

Preferred workflow:

1. Commit and push the repository to GitHub when ready.
2. Create a Brev workspace.
3. Clone the GitHub repo inside Brev.

Alternative workflow:

- Upload only the required project files manually if GitHub push is not ready.

Recommended files to have in Brev:

- `data/sample/sample_incidents.csv`
- `data/processed/splits/*.json`
- `configs/training/*.yaml`
- `configs/training/dataset_info_opstriage.json`
- `scripts/prepare_dataset.py`
- `src/`
- `tests/`
- `docs/`

### 4. Install LLaMA Factory on Brev

Inside Brev, create an isolated Python 3.11 environment and install dependencies. Do not use the system Python directly for training.

### 5. Run Smoke Training First

Use the smoke config:

```text
configs/training/llamafactory_qwen3_1_7b_lora_smoke.yaml
```

The smoke run verifies:

- CUDA is available.
- PyTorch sees the GPU.
- LLaMA Factory is installed.
- Qwen tokenizer/model loading works.
- Dataset registration works.
- ShareGPT/OpenAI JSON format is accepted.
- LoRA attaches successfully.
- At least one tiny training flow completes.

The smoke run is not a model-quality run.

### 6. Run Full LoRA Fine-Tuning

After smoke training passes, use:

```text
configs/training/llamafactory_qwen3_1_7b_lora_sft.yaml
```

The full run should produce:

- LoRA adapter checkpoints
- Training logs
- Loss curves
- Validation metrics
- Candidate best checkpoint

Full model evaluation should still be performed using OpsTriage evaluation scripts after training. Do not rely only on training loss.

### 7. Download Only Small Artifacts Back Locally

Download and commit:

- Evaluation reports
- Confusion matrix images or CSVs
- Training summary logs
- Model card updates
- Small sample predictions
- Config changes

Do not download or commit:

- Base model weights
- LoRA adapter checkpoints
- Merged model directories
- Hugging Face cache directories
- Large training caches

Store large model artifacts separately in:

- Brev persistent storage
- Hugging Face private model repo
- Cloud object storage
- Local external storage, if needed

## Brev Setup Checklist

- [ ] Create NVIDIA Brev workspace.
- [ ] Choose a GPU instance.
- [ ] Prefer a GPU with at least 16 GB VRAM for comfortable LoRA training.
- [ ] Clone the GitHub repo.
- [ ] Create Python 3.11 environment.
- [ ] Install PyTorch with CUDA support.
- [ ] Install LLaMA Factory.
- [ ] Verify `nvidia-smi`.
- [ ] Verify PyTorch CUDA access.
- [ ] Verify dataset files exist.
- [ ] Verify LLaMA Factory can see dataset registration.
- [ ] Run dataset preparation script if processed files are missing.
- [ ] Run smoke config first.
- [ ] Review smoke logs.
- [ ] Run full LoRA config only after smoke passes.
- [ ] Save evaluation reports.
- [ ] Download only small reports and configs.

## Recommended GPU Instance

Minimum practical target:

- NVIDIA T4 16 GB or equivalent

Better options:

- NVIDIA L4
- NVIDIA A10
- NVIDIA A100, if available

For this project, Qwen3-1.7B with LoRA should be much more comfortable on a 16 GB or larger CUDA GPU than on the local 8 GB Apple Silicon machine.

## Brev Setup Commands

Run these commands inside the Brev terminal, not locally.

### 1. Inspect GPU

```bash
nvidia-smi
```

### 2. Clone Repository

Use the repo URL after the local project has been pushed:

```bash
git clone https://github.com/NarmadaPadala/OpsTriage_AI.git
cd OpsTriage_AI
```

### 3. Create Python 3.11 Environment

If Conda is available:

```bash
conda create -n opstriage python=3.11 -y
conda activate opstriage
python --version
```

If using `venv`:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install --upgrade pip
```

### 4. Install PyTorch with CUDA

Use the PyTorch command appropriate for the CUDA version available in the Brev image. A common CUDA 12.1 install command is:

```bash
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

If the Brev image uses a different CUDA version, use the matching PyTorch install command from the PyTorch selector.

### 5. Install Project Dependencies

```bash
python -m pip install -r requirements.txt
```

If the `llamafactory` package in `requirements.txt` does not install cleanly, install from source:

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git external/LLaMA-Factory
cd external/LLaMA-Factory
python -m pip install -e .
python -m pip install -r requirements/metrics.txt
cd ../..
```

### 6. Verify Runtime

```bash
python -c "import torch; print('cuda available:', torch.cuda.is_available()); print('gpu:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')"
python -c "import transformers, datasets, accelerate; print('hf stack ok')"
python -c "import llamafactory; print('llamafactory ok')"
```

### 7. Verify Dataset Files

```bash
ls -lh data/processed/splits/
python3 scripts/prepare_dataset.py
```

Expected files:

```text
train.json
validation.json
test.json
all.json
```

### 8. Register Dataset with LLaMA Factory

If using the LLaMA Factory source repo, merge the OpsTriage dataset registration into its `data/dataset_info.json`.

Conceptual command:

```bash
cp configs/training/dataset_info_opstriage.json external/LLaMA-Factory/data/dataset_info_opstriage.json
```

Depending on the installed version, either:

- merge entries into `external/LLaMA-Factory/data/dataset_info.json`, or
- use the supported dataset directory/config option from the active LLaMA Factory CLI.

Validate this step before training.

### 9. Run Smoke Training

From the project root, after dataset registration is confirmed:

```bash
llamafactory-cli train configs/training/llamafactory_qwen3_1_7b_lora_smoke.yaml
```

If using the source checkout directly:

```bash
cd external/LLaMA-Factory
llamafactory-cli train ../../configs/training/llamafactory_qwen3_1_7b_lora_smoke.yaml
cd ../..
```

### 10. Run Full LoRA Fine-Tuning

Run this only after smoke passes:

```bash
llamafactory-cli train configs/training/llamafactory_qwen3_1_7b_lora_sft.yaml
```

## Artifact Handling

Commit to GitHub:

- Training configs
- Dataset preparation scripts
- Synthetic sample dataset
- Processed JSON splits
- Data quality reports
- Evaluation reports
- Confusion matrix reports
- Small sample prediction outputs
- Model card
- Documentation

Do not commit:

- `models/checkpoints/`
- `models/merged/`
- Hugging Face cache
- LLaMA Factory cache
- Downloaded base model weights
- Adapter checkpoints
- Optimizer states
- TensorBoard event logs if large

Large artifacts should be stored separately and referenced from documentation.

## Troubleshooting Notes

### CUDA Issues

Symptoms:

- `torch.cuda.is_available()` returns `False`.
- `nvidia-smi` works but PyTorch cannot see CUDA.
- CUDA runtime version mismatch errors.

Actions:

- Confirm the Brev instance has a GPU attached.
- Run `nvidia-smi`.
- Install the PyTorch build matching the CUDA runtime.
- Recreate the environment if CUDA packages are mixed.

### Out-of-Memory Errors

Symptoms:

- CUDA OOM during model load or first training step.
- Process killed during tokenization or training.

Actions:

- Use the smoke config first.
- Reduce `per_device_train_batch_size` to `1`.
- Increase `gradient_accumulation_steps`.
- Reduce `cutoff_len`.
- Disable unnecessary evaluation generation.
- Use a larger GPU instance.
- Consider QLoRA if supported cleanly in the Brev CUDA environment.

### Hugging Face Login

Symptoms:

- Model download requires authentication.
- Rate limit or gated model error.

Actions:

```bash
huggingface-cli login
```

Use a Hugging Face token with appropriate read access. Do not hard-code tokens in scripts or commit them.

### Dataset Path Issues

Symptoms:

- LLaMA Factory cannot find `opstriage_train`.
- File-not-found errors for `data/processed/splits/train.json`.
- Dataset loads zero examples.

Actions:

- Confirm current working directory.
- Confirm processed files exist.
- Confirm dataset registration was merged into the active LLaMA Factory registry.
- Use absolute paths temporarily to debug.

### LLaMA Factory Config Mismatch

Symptoms:

- YAML field not recognized.
- `eval_strategy` or metric-related config errors.
- Dataset format tags not accepted.

Actions:

- Check installed LLaMA Factory version.
- Compare config with examples in that installed version.
- Remove unsupported fields for smoke testing.
- Use external OpsTriage evaluation for macro F1 if trainer does not support it directly.

## Final Brev Execution Sequence

Run these steps inside NVIDIA Brev:

1. Open Brev workspace terminal.
2. Run `nvidia-smi`.
3. Clone `https://github.com/NarmadaPadala/OpsTriage_AI.git`.
4. Enter the repo directory.
5. Create and activate Python 3.11 environment.
6. Install CUDA-compatible PyTorch.
7. Install project dependencies.
8. Install LLaMA Factory.
9. Verify CUDA, Hugging Face stack, and LLaMA Factory imports.
10. Run `python3 scripts/prepare_dataset.py`.
11. Confirm processed split files exist.
12. Register OpsTriage dataset with LLaMA Factory.
13. Run the smoke training config.
14. Review smoke logs.
15. Run full LoRA fine-tuning config only if smoke succeeds.
16. Run evaluation.
17. Download only reports, metrics, and small sample outputs.
18. Keep checkpoints and merged models outside Git.

