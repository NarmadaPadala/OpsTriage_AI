# Data Quality Rules

This document defines data quality controls for OpsTriage AI training and evaluation datasets.

High-quality incident classification depends on clean inputs, reliable labels, and strict handling of sensitive information.

## Quality Gate Summary

A record should be excluded from training if it fails any critical gate:

- Missing required input fields
- Missing support team label
- Label outside approved taxonomy
- Contains unresolved sensitive information
- Duplicate of another record in the same split
- Label quality marked `needs_review`
- Text too short to support the label

## Required Field Validation

Required fields:

- `incident_id`
- `incident_title`
- `incident_description`
- `support_team`
- `label_source`
- `label_quality`
- `contains_sensitive_data`
- `sanitization_status`
- `data_source_type`
- `dataset_version`

Validation rules:

- Required fields must not be null.
- Text fields must not be whitespace only.
- `support_team` must match the approved taxonomy exactly.
- `dataset_version` must be present before training or evaluation.

## Duplicate Detection

Duplicate incidents can inflate model performance if similar examples appear across train, validation, and test splits.

Recommended duplicate checks:

- Exact match on normalized title and description.
- Near-duplicate detection using text similarity.
- Same incident title with minor punctuation or casing differences.
- Same description reused across multiple generated or copied records.
- Same `incident_id` appearing more than once.

Recommended action:

- Keep one canonical record.
- Preserve the highest quality label.
- Do not allow near-duplicates to cross train, validation, and test splits.

## Very Short Incidents

Very short incidents often lack enough information for reliable labeling.

Examples:

- "App down"
- "Not working"
- "Claims issue"
- "Login problem"

Recommended rule:

- Flag records below a minimum text length for review.
- Do not automatically discard all short incidents because real enterprise tickets can be brief.
- Use short records for evaluation only if the label is SME-confirmed and the ambiguity is intentional.

## Noisy Incidents

Incident text may contain signatures, copied emails, stack traces, chat history, screenshots converted to text, or ticket boilerplate.

Recommended handling:

- Remove irrelevant boilerplate.
- Preserve meaningful error messages.
- Preserve application names when public-safe or synthetic.
- Preserve domain-specific abbreviations.
- Avoid over-cleaning text in ways that remove real routing signals.

## Spelling Mistakes

Spelling mistakes should not be automatically corrected in the canonical raw text.

Recommended approach:

- Preserve realistic spelling mistakes in training examples.
- Track obvious misspellings for analysis.
- Use preprocessing later if it improves evaluation.
- Include typo-heavy cases in validation and test sets to measure robustness.

## Abbreviations

Enterprise incidents often use abbreviations such as SSO, MFA, API, EDI, ETL, DB, UI, SLA, P1, batch, prod, and auth.

Recommended handling:

- Preserve common operational abbreviations.
- Maintain an abbreviation glossary in future documentation.
- Do not expand abbreviations inconsistently across records.
- Ensure annotators understand domain-specific abbreviations before labeling.

## Sensitive Information

The dataset must not include unresolved sensitive data.

Sensitive information includes:

- PHI
- PII
- Member IDs
- Provider IDs when traceable
- Claim numbers when traceable
- Account numbers
- Email addresses
- Phone numbers
- Social Security numbers
- Access tokens
- API keys
- Passwords
- Internal hostnames if proprietary
- Real customer names
- Real employee names
- Confidential system details

Recommended action:

- Replace sensitive values with safe placeholders only when allowed.
- Block records that cannot be safely sanitized.
- Mark `contains_sensitive_data = true` if sensitive information existed before sanitization.
- Mark `sanitization_status = reviewed` only after safety review.

## PII and PHI Removal

For public portfolio use, prefer synthetic examples over sanitized real records.

If sanitization is used internally:

- Replace names with generic role-based placeholders.
- Replace IDs with non-real placeholders.
- Remove or generalize addresses, dates of birth, and contact details.
- Avoid preserving unique combinations that could re-identify a person.
- Document the sanitization method.

## Label Quality Checks

Before training:

- Verify label distribution by support team.
- Identify classes with too few examples.
- Review examples with reassignment history.
- Review examples with annotator disagreement.
- Review common confusion pairs.
- Exclude `needs_review` examples.

## Split Leakage Checks

Before evaluation:

- Ensure duplicate and near-duplicate examples do not appear across splits.
- Ensure incidents from the same original ticket thread stay in one split.
- Ensure generated variants of the same scenario stay in one split.
- Prefer temporal holdout for final evaluation when real timestamped data exists.

## Class Balance

Support teams should have enough examples for reliable evaluation.

Recommended early target:

- Minimum viable experimentation: at least 50 examples per class.
- Stronger evaluation: at least 100 to 200 examples per class.
- Production-grade evaluation: enough examples per class to support stable confidence intervals.

Do not oversample weak examples just to balance classes. Quality matters more than symmetry.

## Data Quality Dashboard

Future dashboards should track:

- Record count by dataset version
- Record count by support team
- Label quality distribution
- Missing field rates
- Duplicate count
- Sensitive-data block count
- Average title and description length
- Short incident count
- Annotator disagreement rate
- Split distribution

