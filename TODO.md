# Engineering Backlog

This backlog is organized by sprint. It is intentionally written as an engineering planning artifact, not a tutorial checklist.

## Sprint 0: Product and Architecture Foundation

- [x] Define product vision and enterprise use case.
- [x] Define primary user personas.
- [x] Define current-state and future-state workflows.
- [x] Define AI responsibilities.
- [x] Define deterministic business rules responsibilities.
- [x] Define initial support team taxonomy.
- [x] Define success metrics.
- [x] Define non-goals for Version 1.

## Sprint 1: Repository and Engineering Foundation

- [x] Initialize repository structure.
- [x] Add README.
- [x] Add MIT license.
- [x] Add Python and ML `.gitignore`.
- [x] Add minimal dependency list.
- [x] Add project configuration.
- [x] Add changelog.
- [x] Add roadmap.
- [x] Add contributing standards.
- [x] Initialize Git repository.
- [ ] Create first commit.
- [x] Add architecture diagram.
- [x] Add screenshot capture checklist when UI exists.

## Sprint 2: Dataset Design and Label Taxonomy

- [x] Finalize support team definitions.
- [x] Create dataset data dictionary.
- [x] Define required and optional dataset fields.
- [x] Define label quality standards.
- [ ] Define synthetic data generation strategy.
- [x] Define train, validation, and test split policy.
- [x] Add data governance notes.

## Sprint 3: Synthetic Dataset Creation

- [ ] Generate synthetic incidents using the approved schema.
- [ ] Review incidents for label consistency.
- [ ] Check class balance across support teams.
- [ ] Add data validation rules.
- [ ] Create dataset version notes.
- [ ] Store sample data only if safe for public repository use.

## Sprint 4: Baseline Modeling

- [x] Add dataset preparation utilities.
- [x] Validate required dataset columns.
- [x] Validate support-team taxonomy.
- [x] Detect duplicate title and description pairs.
- [x] Create stratified train, validation, and test splits.
- [x] Convert incident rows to ShareGPT/OpenAI JSON format.
- [x] Generate data quality report.
- [ ] Implement deterministic keyword baseline.
- [ ] Implement traditional ML baseline.
- [ ] Evaluate baseline models.
- [ ] Produce baseline metrics report.
- [ ] Analyze confusion matrix.
- [ ] Identify classes requiring more data or clearer labels.

## Sprint 5: Fine-Tuned Incident Classification

- [x] Select open-source model candidate.
- [x] Configure LLaMA Factory experiment.
- [x] Document Week 5 notebook adaptation plan.
- [x] Document fine-tuning plan.
- [x] Inspect local training environment.
- [x] Document smoke training plan.
- [x] Document NVIDIA Brev training workflow.
- [ ] Create NVIDIA Brev workspace.
- [ ] Clone GitHub repo inside Brev.
- [ ] Create Python 3.11 training environment in Brev.
- [ ] Install CUDA-compatible PyTorch in Brev.
- [ ] Install LLaMA Factory in Brev.
- [ ] Verify GPU access in Brev.
- [ ] Register OpsTriage dataset in LLaMA Factory.
- [ ] Run Brev smoke training config.
- [ ] Review smoke training logs.
- [ ] Fine-tune support team classifier.
- [ ] Evaluate against test set.
- [ ] Compare against baselines.
- [ ] Create model card.
- [ ] Decide whether fine-tuned model is justified.

## Sprint 5.5: Training Documentation and Evaluation Artifacts

- [x] Document Week 5 fine-tuning results.
- [x] Add training runbook.
- [x] Add training summary artifact.
- [x] Update README with training environment and reported metrics.
- [x] Document engineering challenges solved.
- [x] Confirm checkpoint and large model artifacts are excluded from Git.

## Sprint 6: Business Rules Engine

- [ ] Define confidence thresholds.
- [ ] Define human-review fallback behavior.
- [ ] Define unsupported input handling.
- [ ] Define insufficient-information detection.
- [ ] Add rule-level tests.
- [ ] Document rule ownership and change process.

## Sprint 7: Inference Contract and API Design

- [ ] Define prediction request schema.
- [ ] Define prediction response schema.
- [ ] Define model version metadata.
- [ ] Define error response format.
- [ ] Design FastAPI endpoints.
- [ ] Add API contract tests.

## Sprint 8: Streamlit Dashboard

- [ ] Build incident prediction form.
- [ ] Display recommended support team.
- [ ] Display confidence and alternatives.
- [ ] Display explanation signals.
- [ ] Add evaluation summary page.
- [ ] Add screenshots for README.

## Sprint 9: Evaluation and Observability

- [ ] Add reusable evaluation pipeline.
- [ ] Add per-class metrics.
- [ ] Add confusion matrix output.
- [ ] Add error analysis report.
- [ ] Add prediction logging design.
- [ ] Add model version tracking.

## Sprint 10: Portfolio Release

- [ ] Polish README.
- [ ] Add architecture diagram.
- [ ] Add final screenshots.
- [ ] Add demo script.
- [ ] Add limitations section.
- [ ] Add future roadmap.
- [ ] Prepare GitHub release.
