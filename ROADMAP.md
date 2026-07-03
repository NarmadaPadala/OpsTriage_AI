# Product Roadmap

This roadmap describes the intended product evolution for OpsTriage AI. The sequence is designed to demonstrate enterprise AI Engineering maturity: start with a measurable classification problem, add deterministic governance, then expand toward richer operational intelligence.

## Version 1: Fine-Tuned Incident Classification

Build the core supervised classification capability.

Primary outcome:

- Predict the correct support team from incident title and description.

Key capabilities:

- Label taxonomy
- Dataset schema
- Baseline comparison
- Fine-tuned open-source model
- Evaluation report
- Model card

## Version 2: Business Rules Engine

Add deterministic policy controls around AI output.

Primary outcome:

- Convert raw model predictions into governed decision support.

Key capabilities:

- Confidence thresholds
- Human-review routing
- Required field validation
- Unsupported or deprecated team handling
- Low-information incident handling
- Rule auditability

## Version 3: Application Prediction

Predict the affected application or platform in addition to support team.

Primary outcome:

- Improve routing clarity by identifying the likely impacted system.

Key capabilities:

- Application label taxonomy
- Multi-label or multi-task design
- Application-level evaluation
- Error analysis by application family

## Version 4: Incident Category Prediction

Classify incidents by operational category.

Primary outcome:

- Identify whether an incident is related to access, claims, billing, data, API, infrastructure, portal, or other defined categories.

Key capabilities:

- Category taxonomy
- Category-specific metrics
- Team and category confusion analysis

## Version 5: RAG

Add retrieval-augmented support context.

Primary outcome:

- Use support ownership documentation, runbooks, and routing policies to improve recommendations.

Key capabilities:

- Document ingestion
- Retrieval index
- Source citation
- Routing-policy grounding
- RAG evaluation

## Version 6: Knowledge Article Recommendation

Recommend relevant knowledge articles, runbooks, or troubleshooting guides.

Primary outcome:

- Help engineers start investigation faster after routing.

Key capabilities:

- Knowledge article retrieval
- Article ranking
- Relevance evaluation
- Human feedback capture

## Version 7: Multi-Agent Investigation

Introduce specialized investigation agents for advanced workflows.

Primary outcome:

- Coordinate domain-specific reasoning across logs, runbooks, service metadata, and incident history.

Key capabilities:

- Triage agent
- Retrieval agent
- Evidence summarization agent
- Escalation recommendation agent
- Guardrails and orchestration policy

## Version 8: REST API

Expose prediction and evaluation capabilities through a service interface.

Primary outcome:

- Make OpsTriage AI integration-ready for enterprise tools.

Key capabilities:

- FastAPI service
- Prediction endpoint
- Health endpoint
- Version endpoint
- Request validation
- Structured response contract

## Version 9: Streamlit Dashboard

Build an enterprise-friendly demo and analysis dashboard.

Primary outcome:

- Provide an interactive interface for incident prediction and model evaluation.

Key capabilities:

- Incident prediction form
- Confidence and explanation display
- Evaluation metrics page
- Confusion matrix view
- Error analysis view

## Version 10: Continuous Learning

Design a feedback and retraining loop.

Primary outcome:

- Improve model quality over time using reviewed incidents and engineer feedback.

Key capabilities:

- Feedback capture
- Accepted versus overridden recommendation tracking
- Drift monitoring
- Retraining candidate selection
- Model promotion workflow
- Evaluation gate before deployment

