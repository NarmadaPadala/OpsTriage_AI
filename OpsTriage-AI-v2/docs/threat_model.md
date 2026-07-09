# Threat Model

## System Under Assessment

OpsTriage AI predicts an enterprise support team from an incident title and description. In production,
the model would assist incident routing and should remain governed by validation, authorization, and
human review controls.

## Security Objectives

- Prevent leakage of hidden prompts, model metadata, credentials, and deployment details.
- Prevent extraction or generation of PII.
- Prevent untrusted incident text from overriding system policy.
- Prevent unsupported routing labels from entering downstream systems.
- Preserve human review for high-risk, ambiguous, or suspicious incidents.

## Trust Boundaries

- Incident text is untrusted input.
- Model output is untrusted until validated.
- User role claims are untrusted until authorized.
- Adapter files and deployment metadata are sensitive operational assets.

## Primary Risks

| Risk | Impact | Example Defense |
|---|---|---|
| Prompt injection | Model follows malicious ticket text | Input Guardrails |
| PII extraction | Sensitive data exposure | PII masking |
| Prompt Leakage | System instructions exposed | Output Guardrails |
| Unsupported routing | Bad downstream assignment | Approved-label validation |
| Social engineering | Unauthorized workflow override | Authorization |
| Crescendo attack | Multi-turn boundary erosion | Conversation-level risk detection |

## Security Principle

The model recommends. Deterministic controls govern. Humans remain accountable for production routing.
