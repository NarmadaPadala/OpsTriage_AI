# Evaluation Strategy

OpsTriage AI should be evaluated as an enterprise supervised classification system, not as a demo-only LLM application.

The model must prove that it improves incident triage quality while remaining transparent about failure modes.

## Evaluation Objectives

Evaluation should answer:

- How often does the model predict the correct support team?
- Which teams does the model route well?
- Which teams are frequently confused?
- Does the model perform acceptably on smaller classes?
- How often should low-confidence predictions be sent to human review?
- Does fine-tuning outperform simpler baselines?
- Are errors operationally acceptable?

## Recommended Dataset Split

Initial recommended split:

- Training: 70 percent
- Validation: 15 percent
- Test: 15 percent

Why this split:

- Training needs enough examples for fine-tuning.
- Validation is needed for model selection, threshold tuning, and prompt or configuration choices.
- Test must remain untouched until final evaluation.

For larger datasets, an 80/10/10 split may be acceptable. For smaller datasets, keep enough test examples per class to support meaningful per-team metrics.

## Split Strategy

Use stratified splitting by `support_team` so each class is represented across train, validation, and test sets.

When timestamps are available, consider:

- Train on older incidents.
- Validate on more recent incidents.
- Test on the newest holdout period.

Temporal testing better reflects production drift, but it requires enough examples across all classes.

## Leakage Prevention

Do not allow the same or near-duplicate incident scenario to appear in multiple splits.

Keep these groups together:

- Duplicate incidents
- Reopened incidents
- Same incident thread
- Generated variants of the same synthetic scenario
- Incidents copied from the same source text

## Baseline Requirement

The fine-tuned model should be compared against simpler baselines:

1. Majority-class baseline
2. Keyword or rules baseline
3. Traditional ML baseline such as TF-IDF plus classifier
4. Fine-tuned open-source language model

Fine-tuning is justified only if it improves enough to offset added complexity, cost, latency, and maintenance.

## Metrics

### Accuracy

Accuracy measures the percentage of incidents where the predicted support team equals the true label.

Why it matters:

- Simple executive-level performance indicator.
- Useful when classes are reasonably balanced.

Limitation:

- Can hide poor performance on smaller support teams.

### Precision

Precision answers:

> When the model predicts a team, how often is it correct?

Why it matters:

- High precision reduces incorrect assignments to a team.
- Important for teams that receive expensive or high-risk incidents.

Example concern:

- If many non-security incidents are routed to Security, that team may waste time on false positives.

### Recall

Recall answers:

> Of all incidents that truly belong to a team, how many did the model find?

Why it matters:

- High recall reduces missed incidents for a team.
- Important for critical domains such as claims, access, infrastructure, and security.

Example concern:

- Low recall for Identity & Access may cause access incidents to be misrouted to application teams.

### F1 Score

F1 balances precision and recall.

Why it matters:

- Useful when both false positives and false negatives matter.
- Better than accuracy when class distribution is uneven.

### Macro F1

Macro F1 calculates F1 independently for each class and averages all classes equally.

Why it matters:

- Protects smaller teams from being hidden by larger classes.
- Strong signal for enterprise routing fairness across support teams.

Recommended use:

- Primary model selection metric for early versions.

### Weighted F1

Weighted F1 averages class F1 scores based on class frequency.

Why it matters:

- Reflects overall production distribution.
- Useful for operational volume planning.

Limitation:

- Can understate poor performance on rare but important teams.

### Confusion Matrix

A confusion matrix shows true labels versus predicted labels.

Why it matters:

- Identifies common misrouting patterns.
- Reveals overlapping team ownership.
- Helps improve taxonomy, labeling, business rules, and training data.

High-value confusion pairs might include:

- Digital Experience versus API Platform
- Claims Engineering versus Billing Systems
- Data Engineering versus Reporting & Analytics
- Infrastructure versus Database Engineering
- Security versus Identity & Access
- Batch Processing versus Integration Services

## Per-Class Reporting

Every evaluation report should include:

- Support team
- Example count
- Precision
- Recall
- F1
- Top confused-with labels

Do not report only aggregate accuracy.

## Confidence and Threshold Evaluation

If the model returns confidence scores, evaluate:

- Accuracy by confidence bucket
- Coverage at different confidence thresholds
- Human-review rate at each threshold
- Error rate for high-confidence predictions

Enterprise decision support systems should know when not to be confident.

## Failure Analysis

After training, wrong predictions should be reviewed systematically.

Recommended failure categories:

- Ambiguous incident text
- Missing application or workflow context
- Multi-team incident
- Taxonomy overlap
- Incorrect or noisy label
- Insufficient training examples
- Abbreviation or enterprise terminology gap
- Typo or spelling robustness issue
- Platform versus application confusion
- Security versus access confusion
- Data pipeline versus reporting confusion
- Low-quality synthetic scenario

## Failure Analysis Dashboards

Create dashboards or reports for:

- Confusion matrix by model version
- Per-class precision, recall, and F1
- Error examples by support team
- High-confidence wrong predictions
- Low-confidence correct predictions
- Failure category counts
- Performance by incident category
- Performance by text length bucket
- Performance by source system
- Performance by label quality
- Drift in incident language over time

## Human Review Analysis

For production readiness, track:

- AI recommendation accepted
- AI recommendation overridden
- Final assigned team
- Override reason
- Confidence score
- Reviewer notes

This feedback should become part of future dataset growth after quality review.

## Future Dataset Growth

New incidents should enter the dataset through a governed workflow:

1. Collect candidate incidents.
2. Remove or block sensitive information.
3. Normalize schema.
4. Assign initial label.
5. Review ambiguous or high-risk records.
6. Run duplicate and leakage checks.
7. Add approved records to a candidate dataset version.
8. Evaluate before promoting the dataset version.

## Engineer Feedback Loop

Engineer feedback should improve the dataset only after review.

Useful feedback:

- Accepted recommendation
- Overridden recommendation
- Corrected support team
- Missing information reason
- Explanation of why the AI was wrong
- New taxonomy edge case

Do not automatically train on every correction. Human corrections can also be noisy.

## Dataset Versioning

Use semantic-style dataset versions:

- `dataset-v0.1.0`: Initial design or sample candidate
- `dataset-v0.2.0`: Expanded label coverage
- `dataset-v1.0.0`: First stable training dataset

Each dataset version should include:

- Creation date
- Source description
- Number of records
- Label distribution
- Quality checks passed
- Known limitations
- Split strategy
- Related model versions

Model evaluation must always identify the dataset version used.
