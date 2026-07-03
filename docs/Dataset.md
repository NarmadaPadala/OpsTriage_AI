# Dataset Design

OpsTriage AI uses supervised training data to classify enterprise production incidents into the correct support team.

This document defines the dataset contract for future fine-tuning and evaluation work. No synthetic incidents or training data have been generated yet.

## Dataset Objective

The dataset must represent the first-stage production incident triage workflow:

- Input: incident title and incident description
- Output: owning support team

The dataset should resemble what an enterprise production support organization would maintain internally: governed labels, traceable metadata, quality controls, and clear separation between model inputs and operational metadata.

## Design Principles

- Use only synthetic, anonymized, or public-safe data in this portfolio repository.
- Treat `support_team` as the primary supervised learning label.
- Keep Version 1 classification focused on support team prediction.
- Store metadata needed for audit, quality review, and future analysis.
- Do not train directly on fields that would leak the answer, such as final resolver group, assignment group history, or manual routing notes.
- Preserve enterprise language, abbreviations, and realistic incident phrasing where safe.
- Track dataset version and label quality from the beginning.

## Canonical Dataset Schema

| Field | Data Type | Required | Used for Training | Metadata Only | Description | Why It Exists |
|---|---:|---:|---:|---:|---|---|
| `incident_id` | string | Yes | No | Yes | Unique incident identifier. | Enables traceability across labeling, evaluation, audit, and feedback loops. |
| `incident_title` | string | Yes | Yes | No | Short incident summary. | Often contains the highest-signal routing information. |
| `incident_description` | string | Yes | Yes | No | Detailed incident description. | Provides context needed to distinguish similar teams and domains. |
| `support_team` | string | Yes | Label | No | Correct owning support team. | Primary classification target for model fine-tuning and evaluation. |
| `incident_category` | string | Recommended | Optional future label | Yes | Functional issue category such as access, API, batch, billing, claims, data, infrastructure, portal, or reporting. | Supports analysis and future category prediction without expanding Version 1 scope. |
| `affected_application` | string | Recommended | No for V1 | Yes | Application, platform, or business capability believed to be impacted. | Helps diagnose routing errors and supports future application prediction. |
| `business_domain` | string | Recommended | No for V1 | Yes | Enterprise domain such as claims, provider, member, finance, data, or platform. | Useful for taxonomy validation and leadership reporting. |
| `priority` | string | Optional | No for V1 | Yes | Incident priority such as P1, P2, P3, or P4. | Enables later analysis of performance on high-impact incidents. |
| `severity` | string | Optional | No for V1 | Yes | Operational severity if distinct from priority. | Helps assess whether misclassification risk differs by incident impact. |
| `source_system` | string | Optional | No | Yes | Originating system such as ServiceNow, Jira, PEGA, monitoring, or internal portal. | Detects distribution differences across intake channels. |
| `created_channel` | string | Optional | No | Yes | Intake channel such as customer support, monitoring alert, internal user, batch process, or service desk. | Supports drift and operational workflow analysis. |
| `reported_by_role` | string | Optional | No | Yes | Role of reporter, such as customer support, provider operations, engineer, or automated monitor. | Helps analyze differences in wording and detail quality. |
| `initial_assignment_group` | string | Optional | No | Yes | First assigned group, if known. | Useful for historical analysis, but should not be used as model input because it may leak routing behavior. |
| `resolution_team` | string | Recommended when available | No | Yes | Final team that resolved the incident. | Helps validate whether `support_team` is reliable and detect historical routing mistakes. |
| `reassigned` | boolean | Optional | No | Yes | Whether the incident was reassigned after first routing. | Useful for identifying weak labels and ambiguous ownership. |
| `reassignment_count` | integer | Optional | No | Yes | Number of assignment changes. | Helps prioritize examples for label review and failure analysis. |
| `label_source` | string | Yes | No | Yes | Source of the label, such as human annotated, resolver-derived, synthetic, or SME reviewed. | Establishes confidence in the ground truth label. |
| `label_quality` | string | Yes | No | Yes | Label quality rating: high, medium, low, or needs_review. | Prevents weak labels from being treated as trusted ground truth. |
| `annotator_id` | string | Optional | No | Yes | Identifier for the person or process that labeled the incident. | Supports inter-annotator agreement and audit without exposing personal data. |
| `reviewer_id` | string | Optional | No | Yes | Identifier for SME or senior reviewer. | Supports second-pass quality control. |
| `annotation_notes` | string | Optional | No | Yes | Notes explaining label uncertainty or edge cases. | Supports future error analysis and taxonomy refinement. |
| `contains_sensitive_data` | boolean | Yes | No | Yes | Whether the original record contained sensitive information before sanitization. | Supports governance and safety checks. |
| `sanitization_status` | string | Yes | No | Yes | Sanitization state: synthetic, sanitized, reviewed, blocked. | Prevents unsafe data from entering training or public artifacts. |
| `data_source_type` | string | Yes | No | Yes | Data type: synthetic, anonymized, public-safe sample, production-derived internal. | Clarifies data origin and permitted usage. |
| `created_at` | datetime | Optional | No | Yes | Incident creation timestamp. | Enables temporal split design and drift analysis. |
| `closed_at` | datetime | Optional | No | Yes | Incident closure timestamp. | Supports future operational analytics. |
| `dataset_version` | string | Yes | No | Yes | Dataset release version, such as `dataset-v0.1.0`. | Required for reproducibility. |
| `split` | string | Yes after split | No | Yes | Dataset split: train, validation, test, or holdout. | Prevents accidental split drift between experiments. |

## Version 1 Model Inputs

Only these fields should be used as direct model input in Version 1:

- `incident_title`
- `incident_description`

The training prompt or classification input may concatenate these fields in a consistent format. The exact prompt format should be defined later during modeling design.

## Version 1 Label

The primary label is:

- `support_team`

This label represents the team that should own the incident after first-stage triage.

## Fields Excluded from Training

The following fields should not be used as model inputs in Version 1:

- `initial_assignment_group`
- `resolution_team`
- `reassigned`
- `reassignment_count`
- `label_quality`
- `annotation_notes`
- `dataset_version`
- `split`
- `source_system`

Some of these fields may be useful for analysis, but using them during training can leak process information that would not be available at prediction time.

## Support Team Taxonomy

The initial taxonomy should be broad enough to represent enterprise production support ownership while remaining small enough for reliable fine-tuning and evaluation.

| Support Team | Description | Why This Team Exists |
|---|---|---|
| Claims Engineering | Owns claims intake, adjudication, claim status, claim edits, and claims workflow issues. | Claims systems are complex, high-volume, and business-critical in healthcare operations. |
| Membership Engineering | Owns member enrollment, eligibility, coverage, demographic updates, and member profile issues. | Membership data drives access, billing, claims, and digital experiences. |
| Provider Systems | Owns provider directory, provider profile, network, credentialing, and provider portal back-end issues. | Provider data and workflows are distinct from member-facing and claims workflows. |
| Digital Experience | Owns web and mobile user experience issues, login-adjacent UI flows, front-end errors, and customer-facing portal behavior. | Digital incidents often present as user-facing defects even when downstream services are involved. |
| Billing Systems | Owns premium billing, invoices, payments, refunds, notices, autopay, and account ledger issues. | Billing incidents affect financial operations and require separate ownership from claims and membership teams. |
| API Platform | Owns shared APIs, gateway behavior, service contracts, rate limits, API errors, and integration endpoints. | API ownership must be separated from business applications to avoid misrouting platform incidents. |
| Data Engineering | Owns data pipelines, data quality, ETL jobs, ingestion, lakehouse feeds, and downstream data availability. | Production incidents often involve missing, delayed, duplicated, or incorrect data movement. |
| Infrastructure | Owns servers, compute, network, storage, load balancers, and platform availability issues. | Infrastructure issues can affect many applications and need platform-level triage. |
| Database Engineering | Owns database performance, connectivity, replication, locks, backups, and query-level database incidents. | Database issues require specialized ownership and should not be buried under application teams. |
| Security | Owns security events, suspicious activity, vulnerability exposure, policy violations, and security control failures. | Security incidents have different escalation paths, evidence handling, and risk requirements. |
| Identity & Access | Owns authentication, authorization, SSO, MFA, access provisioning, role mapping, and entitlement issues. | Access issues are common and often cross multiple applications. |
| Batch Processing | Owns scheduled jobs, nightly cycles, file processing, failed batches, and delayed operational runs. | Batch incidents have unique timing, dependency, and restart patterns. |
| DevOps | Owns CI/CD failures, deployment issues, release automation, environment configuration, and build pipeline incidents. | Deployment and environment failures are operationally distinct from application defects. |
| Integration Services | Owns enterprise interfaces, message queues, file transfers, EDI, HL7-like exchanges, and partner integrations. | Integration failures often involve external systems and middleware ownership. |
| Reporting & Analytics | Owns dashboards, reports, semantic layers, extracts, metric discrepancies, and analytics data products. | Reporting incidents may be data-related but often have separate business intelligence ownership. |

## Taxonomy Design Guidance

Do not create too many labels too early. A label should exist only when:

- It has clear ownership.
- It has enough examples for training and evaluation.
- Engineers can consistently distinguish it from neighboring labels.
- It maps to a real routing decision.

If two teams are frequently confused by humans, the issue may be taxonomy design rather than model performance.

## Label Quality Levels

Use these levels to decide whether a record is eligible for training:

- `high`: Labeled by SME or final resolver with clear ownership.
- `medium`: Label appears reliable but lacks SME review.
- `low`: Historical label may be noisy or ambiguous.
- `needs_review`: Should not be used for training until resolved.

Recommended rule: train only on `high` and carefully reviewed `medium` examples for early model versions.

## Dataset Readiness Checklist

Before any model training:

- Required fields are populated.
- Support team labels match the approved taxonomy.
- Sensitive information is removed or blocked.
- Duplicates are identified.
- Label quality is assigned.
- Train, validation, and test splits are frozen.
- Dataset version is recorded.
- Known limitations are documented.
