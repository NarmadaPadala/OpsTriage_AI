# Production Readiness Checklist

## Required Before Production

- [ ] Input Guardrails for prompt injection, jailbreaks, and obfuscation
- [ ] PII masking before model inference
- [ ] Approved-label validation after inference
- [ ] Output Guardrails for prompt, credential, and metadata leakage
- [ ] Authorization layer for routing approvals
- [ ] Human review for high-risk or low-confidence incidents
- [ ] Audit log for prompts, responses, reviewer decisions, and overrides
- [ ] Red-team regression suite in CI or release validation
- [ ] Incident response plan for model safety failures
- [ ] Clear data policy excluding PHI, PII, credentials, and proprietary logs

## Launch Recommendation

OpsTriage AI should not auto-route production incidents until the controls above are implemented and
validated. The first production posture should be human-in-the-loop decision support.
