# Threat Model Diagram

```mermaid
flowchart TD
    A["User"] --> B["Input Guardrails"]
    B --> C["Prompt Injection Detection"]
    C --> D["PII Detection"]
    D --> E["OpsTriage AI v1<br/>Fine-tuned Model"]
    E --> F["Output Guardrails"]
    F --> G["Evidence Logger"]
    G --> H["Security Report"]

    classDef user fill:#eff6ff,stroke:#2563eb,color:#0f172a;
    classDef guardrail fill:#ecfeff,stroke:#0891b2,color:#0f172a;
    classDef model fill:#f5f3ff,stroke:#7c3aed,color:#0f172a;
    classDef evidence fill:#f8fafc,stroke:#475569,color:#0f172a;

    class A user;
    class B,C,D,F guardrail;
    class E model;
    class G,H evidence;
```

## Purpose

This threat model frames OpsTriage AI v2 as a pre-production security validation layer. The core
principle is that incident text and model output are both untrusted until guardrails, validation,
evidence logging, and human review controls are applied.
