# Fine-Tuning Results

OpsTriage AI Week 5 fine-tuning completed successfully on NVIDIA Brev.

## Run Summary

| Item | Value |
|---|---|
| Project | OpsTriage AI |
| Model | `Qwen/Qwen3-1.7B` |
| Method | LoRA fine-tuning |
| Framework | LLaMA Factory |
| Environment | NVIDIA Brev |
| GPU | NVIDIA L4 |
| Adapter path | `models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0` |
| Task | Enterprise production incident support-team classification |

## Reported Metrics

| Metric | Value |
|---|---:|
| BLEU-4 | 36.3868 |
| ROUGE-1 | 34.7179 |
| ROUGE-2 | 29.359 |
| ROUGE-L | 34.4444 |

These metrics were reported by the fine-tuning workflow. They should not be presented as classification accuracy. Future evaluation should add task-specific classification metrics.

## Engineering Challenges Solved

- Dataset registry paths were corrected from `data/processed/splits/*.json` to `processed/splits/*.json` because LLaMA Factory resolves paths relative to `data/`.
- LLaMA Factory v0.9.5 config compatibility was fixed by using `max_new_tokens`.
- Missing local ML dependencies were avoided by moving training to NVIDIA Brev.
- Best-model metric mismatch was identified because macro F1 requires a classification evaluation layer, not only generation metrics.
- YAML syntax and field compatibility issues were corrected before the successful run.
- Local Mac memory limits were avoided by using an NVIDIA L4 GPU.

## Artifact Policy

The LoRA adapter and checkpoint files are intentionally not committed to Git.

Excluded artifacts include:

- `models/checkpoints/`
- `adapter_model.safetensors`
- `optimizer.pt`
- `scheduler.pt`
- `training_args.bin`
- `trainer_state.json`
- Large model or cache files

## Next Evaluation Work

Add a classification evaluation pipeline that computes:

- Accuracy
- Precision
- Recall
- Macro F1
- Weighted F1
- Invalid-label rate
- Confusion matrix
- Error analysis examples

