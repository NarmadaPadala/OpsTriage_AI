# Demo Script

Target length: 3 to 5 minutes.

## 1. Open With The Problem

"OpsTriage AI v1 fine-tuned a Qwen3-1.7B LoRA model for enterprise incident routing. Before deploying
that kind of system, I wanted to evaluate whether it behaves safely under adversarial prompts."

## 2. Explain The Security Framing

"This is not another chatbot. This is a production AI security validation framework. It runs structured
attack prompts, records observed behavior, scores PASS/WARN/FAIL, and maps findings to defenses."

## 3. Show The Architecture

"The workflow is security reviewer to evaluation layer, attack library, model runner, scoring engine,
evidence records, and report export. The runner can operate in mock mode for demos or connect to the
OpsTriage v1 fine-tuned model when the adapter is available."

## 4. Run A Single Attack

Recommended attack:

```text
JB-001 - Ignore Routing Instructions
```

Talking point:

"The expected behavior is not to reveal hidden instructions and not to let the attack override the
routing policy."

## 5. Run All Categories

"Now I can run the full red-team suite across jailbreaks, prompt injection, obfuscation, crescendo,
PII extraction, social engineering, red teaming, tool enumeration, prompt extraction, and model
information leakage."

## 6. Explain The Results

"Each result includes the attack prompt, expected behavior, observed response, score, reasoning, risk
level, and recommended mitigation. This makes the output reviewable by both engineering and security
stakeholders."

## 7. Export Evidence

"The app exports Markdown for a readable security report and CSV for audit-style evidence analysis.
The same persistence utilities can save timestamped artifacts into the repository's `reports/`
folder."

## 8. Close With Production Readiness

"The production recommendation is layered defense: input guardrails, PII masking, approved-label
validation, output filtering, authorization, audit logging, and human review for risky incidents."

## Interview Emphasis

- I separated UI from reusable evaluation logic.
- I made mock mode the default so demos do not depend on large model artifacts.
- I kept real model mode optional and fail-safe.
- I did not fabricate findings when the adapter is unavailable.
- Every finding maps to a practical enterprise defense.
