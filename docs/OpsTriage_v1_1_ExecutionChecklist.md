# OpsTriage AI v1.1 Execution Checklist

Goal: use the trained LoRA adapter to generate real inference outputs, classification metrics,
and a confusion matrix without committing model artifacts.

## 1. Confirm Adapter Path

Expected local adapter path:

```text
models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0
```

Confirm from the project root:

```bash
ls -la models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0
```

Expected adapter contents usually include files such as:

```text
adapter_config.json
adapter_model.safetensors
tokenizer files if exported with the adapter
```

Do not commit this directory.

## 2. Copy Adapter From NVIDIA Brev or Persistent Storage

Run these commands from the local project root.

Set local variables:

```bash
export LOCAL_PROJECT="$PWD"
export LOCAL_ADAPTER_DIR="$LOCAL_PROJECT/models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0"
mkdir -p "$LOCAL_ADAPTER_DIR"
```

If the adapter is on a Brev instance reachable by SSH:

```bash
export BREV_USER="ubuntu"
export BREV_HOST="<brev-host-or-ip>"
export BREV_ADAPTER_DIR="/home/ubuntu/OpsTriage AI/models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0"

rsync -av --progress \
  "$BREV_USER@$BREV_HOST:$BREV_ADAPTER_DIR/" \
  "$LOCAL_ADAPTER_DIR/"
```

If the adapter was saved to persistent storage on Brev, first copy it into the Brev project path,
then run the same `rsync` command.

If the adapter is already in a downloaded local folder:

```bash
rsync -av --progress \
  "/path/to/qwen3-1.7b-lora-opstriage-v0.1.0/" \
  "$LOCAL_ADAPTER_DIR/"
```

Verify the adapter arrived:

```bash
find "$LOCAL_ADAPTER_DIR" -maxdepth 2 -type f
```

## 3. Run Real Inference on the Test Split

```bash
python scripts/run_inference_on_test_set.py \
  --test-json data/processed/splits/test.json \
  --adapter-path models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0 \
  --output outputs/evaluation/model_predictions.csv
```

Expected output:

```text
Wrote outputs/evaluation/model_predictions.csv
```

## 4. Generate Classification Metrics and Confusion Matrix

```bash
python scripts/evaluate_classification.py \
  --predictions outputs/evaluation/model_predictions.csv \
  --output-dir outputs/evaluation
```

Expected outputs:

```text
outputs/evaluation/classification_report.md
outputs/evaluation/confusion_matrix.png
```

## 5. Generate Sample Predictions

```bash
python scripts/update_sample_predictions.py \
  --predictions outputs/evaluation/model_predictions.csv \
  --output src/inference/sample_predictions.md \
  --limit 5
```

Expected output:

```text
Wrote src/inference/sample_predictions.md
```

## 6. Update README Only With Real Outputs

After the previous commands succeed, update `README.md` with only real generated values:

- Actual classification metrics from `outputs/evaluation/classification_report.md`
- A short real example from `src/inference/sample_predictions.md`
- A reference to `outputs/evaluation/confusion_matrix.png`

Do not add placeholder metrics, assumed improvements, or fabricated confidence scores.

## 7. Confirm Git Ignore Safety

Verify ignored model artifacts:

```bash
git check-ignore -v models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0/adapter_model.safetensors
git check-ignore -v models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0/optimizer.pt
git check-ignore -v models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0/scheduler.pt
git check-ignore -v models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0/training_args.bin
```

Expected: each command prints the matching `.gitignore` rule.

## 8. Review Git Status Before Committing

```bash
git status --short
```

Safe to commit:

```text
app.py
README.md
requirements.txt
docs/Architecture.md
docs/BaseVsFineTuned.md
docs/Decisions.md
docs/HumanInLoop.md
docs/OpsTriage_v1_1_ExecutionChecklist.md
outputs/evaluation/classification_report.md
outputs/evaluation/confusion_matrix.png
scripts/compare_base_vs_finetuned.py
scripts/evaluate_classification.py
scripts/run_inference_on_test_set.py
scripts/update_sample_predictions.py
src/inference/__init__.py
src/inference/inference.py
src/inference/sample_predictions.md
tests/test_evaluate_classification.py
tests/test_inference.py
```

Not safe to commit:

```text
models/checkpoints/
models/merged/
*.safetensors
optimizer.pt
scheduler.pt
training_args.bin
trainer_state.json
outputs/evaluation/model_predictions.csv
```

## 9. Exact Git Commands

Check that model artifacts are ignored:

```bash
git status --ignored --short models outputs/evaluation
```

Stage only safe files:

```bash
git add \
  .gitignore \
  app.py \
  README.md \
  requirements.txt \
  docs/Architecture.md \
  docs/BaseVsFineTuned.md \
  docs/Decisions.md \
  docs/HumanInLoop.md \
  docs/OpsTriage_v1_1_ExecutionChecklist.md \
  outputs/evaluation/classification_report.md \
  outputs/evaluation/confusion_matrix.png \
  scripts/compare_base_vs_finetuned.py \
  scripts/evaluate_classification.py \
  scripts/run_inference_on_test_set.py \
  scripts/update_sample_predictions.py \
  src/inference/__init__.py \
  src/inference/inference.py \
  src/inference/sample_predictions.md \
  tests/test_evaluate_classification.py \
  tests/test_inference.py
```

If the confusion matrix is too large, unstage it:

```bash
git restore --staged outputs/evaluation/confusion_matrix.png
```

Final safety check:

```bash
git diff --cached --name-only
git status --short
```

Commit:

```bash
git commit -m "Add OpsTriage AI v1.1 inference and evaluation workflow"
```
