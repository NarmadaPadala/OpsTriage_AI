# Contributing Guide

OpsTriage AI is structured as a professional AI Engineering repository. Contributions should preserve a clear separation between product documentation, data assets, model experiments, application code, evaluation, and operational concerns.

## Folder Conventions

Use folders according to their intended ownership:

- `docs/` - Product, architecture, dataset, evaluation, roadmap, and decision documents.
- `data/raw/` - Original datasets. Do not commit sensitive or large raw data.
- `data/processed/` - Cleaned or transformed datasets. Do not commit large generated artifacts.
- `data/sample/` - Small public-safe samples for demos and documentation.
- `notebooks/` - Exploratory analysis only. Production logic should move into `src/`.
- `src/ingestion/` - Data loading and source-system ingestion code.
- `src/preprocessing/` - Text preparation and feature preparation code.
- `src/training/` - Model training and experiment entry points.
- `src/inference/` - Prediction-time model loading and inference code.
- `src/evaluation/` - Metrics, reports, and evaluation workflows.
- `src/business_rules/` - Deterministic rules and routing policies.
- `src/api/` - API service code.
- `src/utils/` - Shared utilities with limited, well-defined scope.
- `src/config/` - Configuration helpers and constants.
- `models/` - Local model artifacts. Large artifacts should not be committed.
- `app/` - User-facing application code.
- `tests/` - Unit and integration tests.
- `outputs/` - Generated reports, charts, and evaluation artifacts.
- `assets/` - Static assets such as diagrams and images.

## Naming Conventions

- Use lowercase snake_case for Python files and modules.
- Use PascalCase only for Python classes.
- Use UPPER_SNAKE_CASE for constants.
- Use descriptive file names such as `dataset_schema.md`, `model_card.md`, or `test_business_rules.py`.
- Avoid vague names such as `helper.py`, `final.py`, `new_model.py`, or `test2.py`.

## Formatting Standards

- Target Python 3.10 or newer.
- Keep line length at 100 characters.
- Format Python code with Black-compatible style.
- Sort imports consistently.
- Keep notebooks clean before committing.
- Do not commit generated cache files, local logs, model binaries, or sensitive data.

## Commit Message Standards

Use concise, meaningful commit messages.

Recommended format:

```text
type(scope): short summary
```

Examples:

```text
docs(prd): add incident triage product requirements
chore(repo): initialize project foundation
feat(evaluation): add confusion matrix report
test(rules): validate low confidence fallback
```

Common commit types:

- `docs` - Documentation changes
- `chore` - Repository maintenance or configuration
- `feat` - New user-facing or system capability
- `fix` - Bug fix
- `test` - Test additions or updates
- `refactor` - Internal restructuring without behavior change
- `perf` - Performance improvement

## Branch Naming

Use short branch names that describe the work:

```text
docs/product-foundation
feature/dataset-schema
feature/evaluation-pipeline
fix/business-rule-threshold
chore/project-config
```

## Data and Security Rules

- Do not commit PHI, PII, credentials, secrets, proprietary logs, or real enterprise incidents.
- Use synthetic or sanitized data for portfolio work.
- Keep large datasets and model artifacts outside Git unless explicitly approved.
- Document dataset origin and version whenever data is added.

## Review Expectations

Before opening a pull request or making a release:

- Confirm the change matches the current sprint scope.
- Run available tests.
- Update relevant documentation.
- Avoid unrelated refactors.
- Include evaluation evidence for model or metrics changes.

