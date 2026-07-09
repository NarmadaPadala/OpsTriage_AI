# Reports

This folder stores generated OpsTriage AI v2 security assessment artifacts.

## Artifact Types

- `*.md` files are Markdown executive/security reports.
- `*.csv` files are structured evidence exports for review, filtering, or spreadsheet analysis.

## Filename Pattern

Generated reports use timestamped filenames:

```text
opstriage_v2_security_assessment_YYYYMMDDTHHMMSSZ.md
opstriage_v2_security_assessment_YYYYMMDDTHHMMSSZ.csv
```

Polished demo samples may include `_polished_` in the filename.

## Demo Artifacts

The sample files in this folder are generated in `mock` mode. They are useful for GitHub review,
LinkedIn screenshots, and interview walkthroughs, but they are not claims about the real LoRA adapter
unless the runner mode is explicitly `opstriage_v1`.

## Production Evidence Standard

For production readiness, reports should clearly identify:

- model runner mode
- attack set used
- evidence timestamp
- PASS/WARN/FAIL counts
- observed model responses
- recommended mitigations
- whether findings are mock-mode or model-backed
