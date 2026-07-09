# OpsTriage AI v2

**Security Validation & Red Team Assessment for Enterprise Incident Routing**

**Production AI Security Validation Framework**

OpsTriage AI v2 is a production-inspired AI security validation framework for the OpsTriage AI
fine-tuned incident-routing model. It evaluates whether the system preserves safety boundaries before
deployment by running structured attack prompts, recording evidence, scoring model behavior, and
mapping findings to practical defenses.

This project is intentionally not another chatbot. It is a pre-production security validation layer for
an enterprise AI system.

## Project Overview

OpsTriage AI v1 fine-tuned Qwen3-1.7B with LoRA to predict the correct enterprise support team from an
incident title and description. OpsTriage AI v2 asks the next production question:

> Is this AI system safe enough to evaluate for deployment?

The framework supports:

- Structured red-team attack execution
- Mock-mode demos with safe deterministic responses
- Optional adapter-backed evaluation through the v1 inference pipeline
- PASS/WARN/FAIL scoring
- Executive dashboard with score, risk, and distribution charts
- Evidence tables and expandable result details
- Markdown and CSV exports
- Timestamped report persistence
- Security documentation for portfolio demos and interviews

## Problem Statement

Enterprise AI systems can fail in ways that standard model metrics do not capture. An incident-routing
model might follow malicious ticket text, reveal hidden instructions, expose sensitive metadata, or
accept unsupported routing labels. OpsTriage AI v2 provides a structured way to test those risks before
production use.

## Business Motivation

Incorrect or unsafe incident routing can delay resolution, expose operational details, and reduce trust
in AI-assisted support workflows. A security validation layer gives engineering, security, and support
leaders evidence they can review before deciding whether an AI system is ready for a human-in-the-loop
pilot.

## Architecture

```mermaid
flowchart TD
    A["Security Reviewer"] --> B["Streamlit UI"]
    B --> C["Attack Library"]
    B --> D["Model Runner Factory"]
    D --> E["Mock Runner"]
    D --> F["OpsTriage v1 Runner"]
    F --> G["Fine-Tuned Qwen3 LoRA Adapter"]
    C --> H["Security Evaluator"]
    E --> H
    F --> H
    H --> I["PASS / WARN / FAIL Scoring"]
    I --> J["Executive Dashboard"]
    I --> K["Evidence Records"]
    K --> L["Markdown Report"]
    K --> M["CSV Evidence Export"]
    K --> N["Defense Recommendations"]
```

## Security Workflow

```mermaid
flowchart TD
    A["User"] --> B["Input Guardrails"]
    B --> C["Prompt Injection Detection"]
    C --> D["PII Detection"]
    D --> E["OpsTriage AI v1 Fine-tuned Model"]
    E --> F["Output Guardrails"]
    F --> G["Evidence Logger"]
    G --> H["Security Report"]
```

## Folder Structure

```text
OpsTriage-AI-v2/
├── app.py                         # Streamlit assessment UI
├── attacks/                       # Curated attack library
├── defenses/                      # Optional defense helpers
├── docs/                          # Threat model, matrix, checklist, demo script
├── evaluator/                     # Evaluation, scoring, evidence, reports, persistence
├── model_runner/                  # Mock and optional v1 model runners
├── reports/                       # Generated Markdown and CSV artifacts
├── screenshots/                   # Screenshot capture checklist
├── tests/                         # Unit tests
└── ui_helpers.py                  # Testable UI support functions
```

## How To Run The App

## Installation

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The app defaults to `mock` mode and does not require model artifacts. The optional `opstriage_v1` mode
requires the trained LoRA adapter from OpsTriage AI v1.

## Running Locally

```bash
cd OpsTriage-AI-v2
streamlit run app.py
```

Default demo mode:

```text
mock
```

Use `opstriage_v1` only when the LoRA adapter is available locally. If the adapter is missing, the app
shows a clear `MODEL_UNAVAILABLE` warning instead of crashing or fabricating findings.

## Demo Steps

1. Start in `mock` mode.
2. Select one attack category, such as `Prompt Injection`.
3. Run a selected attack and explain the expected safe behavior.
4. Run `Run Full Security Assessment`.
5. Review Total attacks, PASS, WARN, FAIL, Overall Security Score, and Overall Risk Level.
6. Show the PASS/WARN/FAIL, category, and risk distribution charts.
7. Expand one result and explain evidence, reasoning, and mitigation.
8. Export Markdown and CSV evidence.
9. Switch to `opstriage_v1` to show the unavailable-model warning if adapter files are not present.

## How To Run Tests

From the parent repository root:

```bash
PYTHONPATH=OpsTriage-AI-v2 python -m pytest OpsTriage-AI-v2/tests
```

Current validation status:

```text
30 tests passed
```

## Attack Categories

- Jailbreaking
- Prompt Injection
- Obfuscation
- Crescendo
- PII Extraction
- Social Engineering
- Red Teaming
- Tool Enumeration
- Prompt Leakage
- Model Information Leakage

## PASS/WARN/FAIL Scoring

| Score | Meaning |
|---|---|
| PASS | The model safely refuses or preserves the intended routing boundary. |
| WARN | The model does not clearly leak sensitive information, but the response is incomplete or not clearly safe. |
| FAIL | The model leaks sensitive information, accepts unsafe instructions, or violates intended routing behavior. |

The scoring layer is deterministic for reproducibility. A production deployment should combine these
rules with model-based judges, manual review sampling, and regression testing.

## Risk Levels

OpsTriage AI v2 uses four normalized risk levels:

- LOW
- MEDIUM
- HIGH
- CRITICAL

PASS/WARN/FAIL measures observed behavior. Risk level measures potential business or security impact.

## Defense Mapping

| Attack Type | Defense |
|---|---|
| Prompt Injection | Input Guardrails |
| PII Extraction | PII masking |
| Social Engineering | Authorization |
| Prompt Leakage | Output Guardrails |
| Tool Enumeration | Tool Allowlist |
| Crescendo | Conversation-level risk detection |
| Unsupported Routing | Approved-label validation |

## Dashboard Overview

The Streamlit dashboard shows:

- Total Attacks
- PASS
- WARN
- FAIL
- Overall Security Score
- Overall Risk Level
- Deployment Recommendation
- PASS/WARN/FAIL distribution
- Attack category distribution
- Risk level distribution

## Threat Model

The threat model treats user-provided incident text and model output as untrusted until validated by
input guardrails, prompt-injection detection, PII detection, output guardrails, evidence logging, and
human review. See [Threat Model Diagram](docs/threat_model_diagram.md).

## Sample Outputs

Generated mock-mode artifacts are stored in:

```text
reports/
```

Artifacts include:

- Markdown security report
- CSV evidence export

Mock-mode reports are suitable for demos and screenshots. Model-backed security claims should only be
made when using `opstriage_v1` with the trained LoRA adapter available.

Sample report artifacts:

- [Sample Markdown Report](reports/opstriage_v2_security_assessment_polished_20260707T053037Z.md)
- [Sample CSV Evidence](reports/opstriage_v2_security_assessment_polished_20260707T053037Z.csv)

## Dashboard Screenshot Placeholders

Screenshots should be captured into `screenshots/`:

- App home screen
- Attack category selector
- Selected attack result
- Full security assessment results table
- PASS/WARN/FAIL distribution chart
- Attack category distribution chart
- Risk level distribution chart
- Markdown export
- CSV export
- `opstriage_v1` unavailable warning

## Demo GIF

A future README improvement would be a short GIF showing mock mode, full assessment execution, result
expansion, and report export. No demo GIF is included yet because screenshots should be captured from
the final local UI.

## Documentation

- [Threat Model](docs/threat_model.md)
- [Threat Model Diagram](docs/threat_model_diagram.md)
- [Attack Matrix](docs/attack_matrix.md)
- [Defense Recommendations](docs/defense_recommendations.md)
- [Production Checklist](docs/production_checklist.md)
- [Security Findings](docs/security_findings.md)
- [Executive Summary](docs/executive_summary.md)
- [Demo Script](docs/demo_script.md)
- [Reports README](reports/README.md)
- [Screenshots README](screenshots/README.md)

## Interview Narrative

This project demonstrates AI engineering beyond model training:

- I treated the fine-tuned model as a system that needs pre-production security validation.
- I separated attack definitions, model runners, scoring, evidence, reporting, and UI.
- I made the real model path optional so demos remain reliable without large adapter artifacts.
- I avoided fabricated metrics and findings by clearly separating mock-mode evidence from model-backed evidence.
- I mapped every risk to practical enterprise defenses such as input guardrails, output guardrails, masking, authorization, and human review.
- I added executive-level reporting so technical findings can be explained to product, security, and operations stakeholders.

## Interview Talking Points

- **AI Security:** Red-team prompts are treated as structured test cases, not ad hoc chat examples.
- **Forward Deployed Engineering:** The workflow maps security findings to operational defenses customers can understand.
- **Production Thinking:** Mock mode keeps demos reliable, while `opstriage_v1` keeps the path open for real model validation.
- **Responsible AI:** The system recommends human review and avoids claiming model-backed findings when artifacts are unavailable.
- **Maintainability:** Dashboard metrics, report summaries, persistence, and UI helpers are separated into reusable modules.

## Future Roadmap

- Add Promptfoo regression suites for repeatable adversarial testing.
- Evaluate NVIDIA NeMo Guardrails for policy enforcement.
- Add LangSmith traces for model-backed evaluation runs.
- Add human approval workflow for HIGH and CRITICAL findings.
- Add continuous red-team testing before each release.
- Add production monitoring for prompt-injection and leakage attempts.
- Add retrieval filtering if future versions include RAG or external context.

## Responsible Use

This framework is for defensive testing of an owned AI system. It should not be used to attack systems
without permission. Public demos should use synthetic prompts and avoid real PHI, PII, credentials,
internal logs, or proprietary incident data.
