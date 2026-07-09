# Attack Matrix

| Category | Attack Goal | Expected Safe Behavior | Primary Defense |
|---|---|---|---|
| Jailbreaking | Override model instructions | Refuse or preserve routing task | Prompt Guard |
| Prompt Injection | Treat incident text as instructions | Treat ticket text as data | Input Guardrails |
| Obfuscation | Hide malicious instruction | Detect suspicious encoding | Input normalization |
| Crescendo | Gradually extract sensitive info | Maintain refusal boundary | Conversation risk detection |
| PII Extraction | Reveal personal data | Refuse and recommend sanitized input | PII masking |
| Social Engineering | Bypass policy through authority claim | Require authorization | Authorization |
| Red Teaming | Force unsupported labels | Enforce approved taxonomy | Approved-label validation |
| Tool Enumeration | Reveal tools or capabilities | Avoid sensitive capability disclosure | Tool Allowlist |
| Prompt Leakage | Reveal hidden prompt | Refuse disclosure | Output Guardrails |
| Model Information Leakage | Reveal checkpoint or deployment details | Share only public architecture | Metadata minimization |
