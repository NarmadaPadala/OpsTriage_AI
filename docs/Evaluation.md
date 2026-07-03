# Evaluation

OpsTriage AI will be evaluated as a supervised classification system.

The detailed evaluation strategy is maintained in [EvaluationStrategy.md](EvaluationStrategy.md).

## Planned Metrics

- Accuracy
- Precision
- Recall
- F1 score
- Confusion matrix
- Per-class support team metrics

## Evaluation Principle

The fine-tuned model must be compared against simpler baselines before being considered justified.

Potential baselines:

- Deterministic keyword baseline
- Traditional machine learning baseline
- Fine-tuned open-source language model

No evaluation pipeline has been implemented yet.
