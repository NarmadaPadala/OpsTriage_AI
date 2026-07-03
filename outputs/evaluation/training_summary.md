# Training Summary

OpsTriage AI Week 5 fine-tuning completed successfully.

## Run Details

| Item | Value |
|---|---|
| Model | `Qwen/Qwen3-1.7B` |
| Fine-tuning method | LoRA |
| Training environment | NVIDIA Brev |
| GPU | NVIDIA L4 |
| Adapter path | `models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0` |

## Reported Metrics

| Metric | Value |
|---|---:|
| BLEU-4 | 36.3868 |
| ROUGE-1 | 34.7179 |
| ROUGE-2 | 29.359 |
| ROUGE-L | 34.4444 |

## Notes

- The reported metrics are sequence-generation metrics from the fine-tuning workflow.
- Classification-specific evaluation is still required for production-quality model assessment.
- Model checkpoints and large artifacts are excluded from Git.

