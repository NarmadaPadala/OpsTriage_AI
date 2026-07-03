# Training Environment

This document records the Sprint 3.3 local environment inspection for OpsTriage AI fine-tuning.

No model was downloaded. No training was started. No checkpoints were created.

## Environment Snapshot

| Item | Observed Value |
|---|---|
| Python executable | `/opt/anaconda3/bin/python3` |
| Python version | `3.13.5` |
| OS | `macOS 26.5.1` |
| Kernel | `Darwin 25.5.0` |
| Architecture | `arm64` |
| CPU | Apple M2 |
| CPU cores | 8 |
| Unified memory | 8 GB |
| Available disk at repo path | Approximately 193 GiB |
| PyTorch installed | No |
| LLaMA Factory installed | No |
| Transformers installed | No |
| Datasets installed | No |

## Accelerator Status

The machine is Apple Silicon, so PyTorch can often use Metal Performance Shaders through `mps` when a compatible PyTorch build is installed.

Current status:

- CUDA: not applicable on this Mac.
- MPS: hardware likely supports it, but PyTorch is not installed, so runtime support is not currently available.
- CPU: available, but CPU-only LLM fine-tuning would be very slow.

## LLaMA Factory Status

LLaMA Factory is not installed in the current Python environment.

The current Python version is also a risk. LLaMA Factory documentation lists Python 3.11 as the mandatory minimum and recommended baseline, along with PyTorch, Transformers, Datasets, Accelerate, PEFT, and TRL dependencies.

Reference:

- LLaMA Factory README: https://github.com/hiyouga/LLaMA-Factory

## Recommended Local Setup

Do not install directly into the current Anaconda Python 3.13 environment.

Recommended approach:

1. Create a Python 3.11 virtual environment.
2. Install PyTorch for macOS.
3. Install LLaMA Factory and metrics dependencies.
4. Validate `mps` availability.
5. Run only a tiny smoke training job first.

Exact commands to run after approval:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch torchvision torchaudio
python -m pip install -r requirements.txt
python -m pip install "llamafactory[metrics]"
python -c "import torch; print('mps available:', torch.backends.mps.is_available())"
python -c "import llamafactory; print('llamafactory import ok')"
```

If `python3.11` is not installed:

```bash
brew install python@3.11
```

These commands have not been executed.

## Feasibility Assessment

### Local Full Training

Local full LoRA training of `Qwen/Qwen3-1.7B` on this Mac is high risk.

Reasons:

- 8 GB unified memory is tight for 1.7B parameter training.
- LLaMA Factory's estimated hardware table lists 16-bit LoRA memory for 7B models at approximately 16 GB and 4-bit QLoRA at approximately 6 GB. A 1.7B model is smaller, but the local machine must still hold model weights, activations, optimizer state, LoRA adapters, tokenizer buffers, and OS memory.
- Apple MPS support is useful but not equivalent to CUDA training support.
- Some LLaMA Factory optimizations, such as bitsandbytes QLoRA, are primarily CUDA-oriented and may not behave the same way on macOS.

Expected outcome:

- A tiny smoke run may be possible after installing a compatible environment.
- Full training may be slow, memory constrained, or unstable locally.

### Cloud Training

Recommended for serious fine-tuning:

- Google Colab with a T4, L4, or A100 GPU
- Kaggle GPU notebook
- RunPod, Lambda, Paperspace, or similar GPU cloud
- University or enterprise GPU environment

Cloud training is better for:

- Faster iteration
- CUDA support
- Better LLaMA Factory compatibility
- Cleaner reproducibility
- Lower risk of local memory failures

## Expected Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Python 3.13 incompatibility | Package install failures | Use Python 3.11 virtual environment. |
| 8 GB memory limit | Out-of-memory during training | Use tiny smoke run locally; use cloud GPU for full training. |
| MPS limitations | Training instability or unsupported ops | Validate with a tiny run before any full job. |
| Slow CPU fallback | Training may take impractically long | Do not run CPU-only full training. |
| LLaMA Factory config drift | YAML field differences by version | Validate config after installation. |
| Metric selection mismatch | Macro F1 may not be available inside trainer | Save epoch checkpoints and run external evaluation. |

## Fallback Plan

If local smoke training fails:

1. Keep local environment for dataset prep, validation, and documentation.
2. Move fine-tuning to Colab, Kaggle, or GPU cloud.
3. Upload only the safe processed dataset files.
4. Run LLaMA Factory training in the GPU environment.
5. Download only compact artifacts needed for reporting, such as metrics and confusion matrices.
6. Keep large checkpoints out of GitHub.

## Recommendation

Use this Mac for:

- Dataset preparation
- Validation
- Documentation
- Evaluation report development
- Very small smoke tests only

Use Colab, Kaggle, or GPU cloud for:

- Real Qwen3-1.7B LoRA training
- Adapter checkpoint creation
- Model evaluation at meaningful scale

