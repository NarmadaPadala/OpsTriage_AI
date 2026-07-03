# OpsTriage AI

**AI-powered production incident decision support for enterprise support teams.**

OpsTriage AI is a portfolio-grade AI Engineering project designed like an enterprise product. The system will help production support teams classify incoming incidents and recommend the correct owning support team using a fine-tuned open-source language model, deterministic business rules, and measurable evaluation workflows.

This repository is intentionally structured as a production-oriented AI project, not a tutorial or throwaway prototype.

## Project Overview

Enterprise incident support teams receive production issues from systems such as ServiceNow, Jira, PEGA, Service Marketplace, monitoring tools, and internal support portals. Before an incident can be resolved, a support engineer must determine which application, domain, or engineering team should own the issue.

OpsTriage AI focuses on the first stage of that workflow: incident triage.

Given an incident title and description, the system will recommend the most likely support team and provide supporting decision context for human review.

Example support teams include:

- Claims Engineering
- Digital Experience
- Provider Systems
- Membership Systems
- Billing Systems
- Data Engineering
- Infrastructure
- API Platform

## Business Problem

Manual incident routing is repetitive, time-consuming, and heavily dependent on experienced engineers. Incorrect routing can create delays, increase reassignment volume, and slow down production incident resolution.

The goal of OpsTriage AI is not to replace support engineers. The goal is to accelerate first-stage triage by providing a high-quality recommendation that engineers can accept, override, or use as decision support.

## Why This Project Exists

This project demonstrates how an AI Engineering team would approach a real enterprise workflow:

- Understand the operational problem before building models
- Define clear product and system boundaries
- Separate AI responsibilities from deterministic business rules
- Use measurable evaluation instead of subjective demos
- Design for observability, explainability, and human review
- Treat datasets, labels, and model versions as governed assets

## High-Level Architecture

The planned system architecture includes:

1. **Incident Intake Layer**  
   Accepts incident title and description from a UI, batch file, or future API integration.

2. **Input Validation Layer**  
   Validates required fields and guards against incomplete or unsafe inputs.

3. **Preprocessing Layer**  
   Prepares incident text for model inference while preserving domain-specific signals.

4. **AI Classification Layer**  
   Uses a fine-tuned open-source language model to predict the most likely support team.

5. **Business Rules Layer**  
   Applies deterministic routing policies, confidence thresholds, and human-review rules.

6. **Evaluation Layer**  
   Measures model performance using accuracy, precision, recall, F1 score, and confusion matrix analysis.

7. **Application Layer**  
   Provides an interface for entering incidents, reviewing recommendations, and viewing outputs.

8. **Observability and Audit Layer**  
   Tracks prediction metadata, model versions, evaluation results, and decision outcomes.

## Technologies

Planned technology areas:

- Python
- pandas
- scikit-learn
- Hugging Face Transformers
- Hugging Face Datasets
- LLaMA Factory
- FastAPI
- Streamlit
- Evaluation tooling
- Versioned datasets and model artifacts

The repository starts with a minimal dependency list. Additional packages should be added only when a sprint requires them.

## Planned Features

- Incident title and description intake
- Support team classification
- Confidence-aware recommendations
- Top alternative support teams
- Business-rule-based review routing
- Evaluation reports
- Confusion matrix analysis
- Model card and risk documentation
- Human-in-the-loop feedback design
- Future API and dashboard interfaces

## Screenshots

Screenshots will be added as the product interface evolves.

Placeholder:

```text
docs/Screenshots/
```

## Current Status

**Version:** v0.1.0  
**Status:** Project foundation initialized  
**Current Sprint:** Sprint 1 - Repository and engineering foundation  

No AI models, datasets, training code, or business logic have been implemented yet.

## Future Roadmap

The long-term roadmap includes:

- Fine-tuned incident classification
- Business rules engine
- Application-level prediction workflow
- Incident category prediction
- Retrieval-augmented generation
- Knowledge article recommendation
- Multi-agent investigation support
- REST API
- Streamlit dashboard
- Continuous learning workflow

See [ROADMAP.md](ROADMAP.md) for the product roadmap and [TODO.md](TODO.md) for the engineering backlog.

## Responsible AI Positioning

OpsTriage AI is designed as a decision support system. Human engineers remain accountable for final routing decisions, especially when incidents are ambiguous, low-confidence, high-severity, or operationally sensitive.

The system should not process real PHI, PII, credentials, proprietary logs, or confidential enterprise incidents in this public portfolio version.

