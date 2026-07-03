# Labeling Guide

This guide defines how engineers and annotators should label incidents for OpsTriage AI.

Consistent labeling is more important than large data volume. A fine-tuned model trained on inconsistent labels will learn organizational confusion instead of reliable triage behavior.

## Labeling Goal

Assign each incident to the support team that should own first-stage production triage based on the incident title and description.

The label should answer:

> Which team should receive this incident first to investigate and drive ownership?

## Approved Support Team Labels

Use only the approved support team taxonomy from [Dataset.md](Dataset.md):

- Claims Engineering
- Membership Engineering
- Provider Systems
- Digital Experience
- Billing Systems
- API Platform
- Data Engineering
- Infrastructure
- Database Engineering
- Security
- Identity & Access
- Batch Processing
- DevOps
- Integration Services
- Reporting & Analytics

Do not create new labels during annotation. If a label appears missing, mark the record as `needs_review` and document the proposed label in `annotation_notes`.

## Core Labeling Rules

1. Label the team that should own the first investigation.
2. Use the incident text, not assumptions about the reporter.
3. Prefer system ownership over symptom location when clear.
4. Do not label based only on who reported the issue.
5. Do not use final resolver information while labeling model inputs.
6. Mark ambiguous records for review instead of forcing a weak label.

## Handling Ambiguous Incidents

Ambiguous incidents occur when the title and description do not provide enough evidence to choose a single support team.

Use `label_quality = needs_review` when:

- Multiple teams are equally likely.
- The incident only says "system is down" without application context.
- The description contains symptoms but no affected system.
- The issue may be infrastructure, API, or application-level.
- The record depends on internal knowledge not present in the text.

Do not guess just to increase dataset size. Ambiguous labels are expensive because they create confusing training signals.

## Handling Multi-Application Incidents

Some incidents involve more than one application or domain.

Recommended decision order:

1. Label the team that owns the failing component, if identified.
2. If the failing component is unknown, label the team responsible for initial triage of the most specific affected business workflow.
3. If the issue is clearly caused by a shared platform, label the platform team such as API Platform, Infrastructure, Database Engineering, or Identity & Access.
4. If no ownership can be determined from text, mark `needs_review`.

Example decision pattern:

- Portal page shows a 500 error because member eligibility API is failing: API Platform if API failure is explicit.
- Portal page layout broken or button not working: Digital Experience.
- Claim status incorrect due to delayed data feed: Data Engineering or Claims Engineering depending on whether data movement failure is explicit.

## Handling Missing Information

If required context is missing, do not force a confident label.

Mark `label_quality = needs_review` when the incident lacks:

- Affected application or workflow
- Observable symptom
- Error message or failure behavior
- User population impacted
- Business domain signal

Future versions may add an explicit `needs_more_information` label or business rule, but Version 1 should not mix "missing information" with support team labels.

## Handling Incidents with Security or Access Signals

Security and access incidents require careful separation.

Use `Security` when the issue involves:

- Suspicious activity
- Potential breach
- Vulnerability exposure
- Malware or phishing indicators
- Security control failures
- Policy violations

Use `Identity & Access` when the issue involves:

- Login failure
- SSO or MFA issue
- Role or entitlement mismatch
- Access provisioning delay
- Authorization failure without security event indicators

## Handling Platform Versus Application Ownership

Use platform labels when the incident points to shared technical infrastructure.

Examples:

- API Gateway timeout: API Platform
- Database connection pool exhaustion: Database Engineering
- Kubernetes node failure: Infrastructure
- Deployment pipeline failure: DevOps
- Failed file transfer between systems: Integration Services

Use application labels when the issue is specific to a business workflow and no shared platform failure is clear.

## Annotation Workflow

Recommended enterprise workflow:

1. First annotator labels the record.
2. Second annotator reviews a sample or all high-risk records.
3. Disagreements are routed to an SME.
4. Resolved labels are added to the approved dataset version.
5. Edge cases are documented as taxonomy guidance.

## Inter-Annotator Agreement

Track agreement between labelers before training.

Recommended checks:

- Percent agreement by support team
- Disagreement rate by category
- Most common label pairs in disagreement
- Records requiring SME arbitration

Low agreement is a signal to improve the taxonomy or labeling guide before training.

## Annotation Quality Standards

A record is training-ready only when:

- The support team label is in the approved taxonomy.
- The title and description support the label.
- Sensitive information has been removed or blocked.
- The label quality is `high` or approved `medium`.
- Ambiguity is documented.
- The record is not a duplicate of another training example.

## Common Labeling Mistakes

Avoid these patterns:

- Labeling based on a keyword without reading the full description.
- Sending all login issues to Digital Experience instead of Identity & Access.
- Sending all report issues to Data Engineering instead of Reporting & Analytics.
- Sending all timeout issues to Infrastructure when the API layer is clearly named.
- Treating historical assignment group as perfect ground truth.
- Adding new labels without taxonomy review.
