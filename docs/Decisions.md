# Architecture Decision Record

This document records major product, architecture, and engineering decisions.

## ADR-001: Human-in-the-Loop Decision Support

**Status:** Accepted

**Decision:** OpsTriage AI will provide routing recommendations for human review. It will not automatically assign production incidents in Version 1.

**Rationale:** Incident routing has operational impact. Human review reduces risk while still improving triage speed and consistency.

## ADR-002: Separate AI Predictions from Business Rules

**Status:** Accepted

**Decision:** AI classification and deterministic business rules will be implemented as separate system responsibilities.

**Rationale:** Model outputs are probabilistic. Routing policies, thresholds, validation, and compliance controls should be deterministic, testable, and auditable.

## ADR-003: No Real Enterprise Incident Data in Portfolio Version

**Status:** Accepted

**Decision:** The public portfolio version will use synthetic or sanitized data only.

**Rationale:** Production incidents may contain PHI, PII, credentials, internal system names, or proprietary operational details.

