# Defense Recommendations

| Finding Type | Recommended Defense | Production Rationale |
|---|---|---|
| Prompt Injection | Input Guardrails | Prevent untrusted incident text from becoming instructions |
| Jailbreaking | Prompt Guard + Output Guardrails | Preserve policy boundaries |
| PII Extraction | PII masking | Reduce data exposure before inference |
| Social Engineering | Authorization | User claims should not override workflow policy |
| Prompt Leakage | Output Guardrails | Block hidden instruction disclosure |
| Tool Enumeration | Tool Allowlist | Prevent disclosure or invention of internal capabilities |
| Crescendo | Conversation-level risk detection | Detect risk that accumulates across turns |
| Unsupported Label | Approved-label validation | Protect downstream routing systems |
