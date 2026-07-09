# OpsTriage AI Interview Preparation Guide

This guide prepares you to discuss OpsTriage AI in AI Engineer, ML Engineer, and enterprise AI interviews.

Use these answers as starting points. The strongest interview style is natural and specific: explain what you built, why you built it, what broke, what you fixed, and what you would improve next.

## Section 1 - Elevator Pitch

### 30-Second Explanation

OpsTriage AI is an AI-powered production incident triage system. It takes an incident title and description, then predicts which enterprise support team should handle it. I built it because production support engineers often spend time manually reading tickets and routing them to teams like Claims, Membership, API Platform, Infrastructure, or Data Engineering. I fine-tuned Qwen3-1.7B with LoRA using LLaMA Factory on NVIDIA Brev, and I built the dataset preparation, validation, training configs, and documentation around it.

### 1-Minute Explanation

OpsTriage AI is a decision-support system for production incident routing. In many enterprise IT environments, especially healthcare, customer support or monitoring systems create incidents, and support engineers manually decide which team owns the issue. That first routing step is repetitive but important because wrong routing creates delays and handoffs.

For the MVP, I created a synthetic enterprise incident dataset with incident titles, descriptions, and support-team labels. I built utilities to validate the dataset, check labels, detect duplicates, create train/validation/test splits, and convert the data into ShareGPT JSON for supervised fine-tuning. Then I fine-tuned Qwen3-1.7B using LoRA through LLaMA Factory on an NVIDIA L4 GPU in Brev.

The project is not trying to replace engineers. It is meant to help them make faster, more consistent first-stage routing decisions.

### 3-Minute Explanation

OpsTriage AI is based on a real enterprise support problem I have seen in healthcare IT. Production incidents come from tools like ServiceNow, Jira, PEGA, monitoring alerts, or internal support portals. Before anyone can fix the issue, someone has to read the ticket and decide which support team owns it.

That decision is often based on experience. A senior support engineer might know that an eligibility sync issue belongs to Membership Engineering, while an API timeout belongs to API Platform, and a report mismatch may belong to Reporting & Analytics. But the ticket text can be messy. Some tickets are well-written, some have typos, some use abbreviations, and some describe symptoms instead of root causes.

I designed OpsTriage AI as a human-in-the-loop routing assistant. The input is an incident title and description. The output is a predicted support team.

I started by designing the product and architecture. Then I created the repository structure, dataset schema, label taxonomy, labeling guide, and data quality rules. After that, I generated a public-safe synthetic dataset of enterprise incidents. I wrote Python utilities to validate required columns, validate support-team labels, detect duplicates, create stratified train/validation/test splits, and convert the dataset into ShareGPT/OpenAI JSON format.

For fine-tuning, I used Qwen3-1.7B with LoRA through LLaMA Factory. I trained on NVIDIA Brev with an L4 GPU because my local Mac did not have enough memory for realistic fine-tuning. During the process I debugged LLaMA Factory dataset path issues, config compatibility issues, missing dependencies, and metric-selection issues.

The current result is a working Week 5 fine-tuning workflow with reported BLEU and ROUGE metrics. The next step is to add classification-specific evaluation like accuracy, precision, recall, macro F1, weighted F1, invalid-label rate, and confusion matrix analysis.

### 5-Minute Project Walkthrough

I would explain the project in five parts.

First, the business problem. In enterprise support teams, incidents need to be routed before they can be solved. That first triage step is repetitive, manual, and dependent on engineer experience. If an incident is routed to the wrong team, it creates delays, reassignment, and operational noise.

Second, the product goal. OpsTriage AI does not replace support engineers. It recommends the most likely support team from the incident title and description. A human engineer can accept, override, or review the recommendation.

Third, the dataset. I designed a support-team taxonomy with labels like Claims Engineering, Membership Engineering, Provider Systems, Digital Experience, API Platform, Infrastructure, Database Engineering, Security, Identity & Access, Batch Processing, DevOps, Integration Services, Reporting & Analytics, and Billing Systems. I generated 100 synthetic but realistic enterprise-style incidents. I kept the data public-safe and avoided real PHI, PII, or proprietary company data.

Fourth, the engineering pipeline. I built dataset preparation utilities in Python. The pipeline loads the CSV, validates schema, checks support-team labels, detects duplicate title-description pairs, creates stratified train/validation/test splits, converts rows into ShareGPT/OpenAI messages, and writes a data quality report. I added unit tests for the core validation and formatting logic.

Fifth, the fine-tuning workflow. I used LLaMA Factory to fine-tune Qwen3-1.7B with LoRA on NVIDIA Brev using an L4 GPU. I created smoke and full training configs. I debugged real issues around dataset paths, LLaMA Factory config names, YAML syntax, missing NLP dependencies, and model-selection metrics. The adapter was saved outside Git because model artifacts should not be committed.

The current project is strong as an AI engineering portfolio piece because it shows product thinking, dataset engineering, fine-tuning setup, cloud GPU workflow, debugging, and responsible AI framing. The next step is to close the evaluation loop with classification metrics and an inference demo.

## Section 2 - Business Problem

### Why did you build this?

I built it because production incident triage is a real workflow where AI can help without replacing people. In enterprise environments, a lot of time is spent reading incident descriptions and deciding which team should own the issue. That decision depends on experience and knowledge of many systems.

I wanted to build something practical that reflects how AI engineering is used in real companies: not just a chatbot, but a decision-support system with data, labels, validation, fine-tuning, evaluation, and governance.

### What real-world problem does it solve?

It helps with first-stage incident routing. When an incident comes in, someone has to decide whether it belongs to Claims Engineering, Membership, API Platform, Infrastructure, Security, Data Engineering, or another team. If the first assignment is wrong, the ticket gets bounced around.

OpsTriage AI tries to reduce that first routing delay by recommending the most likely support team from the incident text.

### Why not use traditional routing?

Traditional routing works when the rules are obvious, like a ticket explicitly saying "database backup failed." But many production incidents are not that clean. A user might say "portal is spinning," but the real issue could be a front-end bug, an API timeout, an identity problem, or infrastructure latency.

Rules are still useful, but rules alone become brittle when ticket language varies. AI can learn patterns across messy language and domain-specific phrasing.

### Why use AI?

AI is useful here because the input is unstructured text. The model can learn that different descriptions may point to the same owning team. For example, "member coverage missing," "eligibility not showing," and "new enrollment not visible downstream" may all point toward Membership Engineering.

The AI does the language understanding. Business rules still handle guardrails, confidence thresholds, and human review.

### What are the limitations?

The current dataset is synthetic and small, so I would not claim production accuracy yet. The reported BLEU and ROUGE metrics came from the fine-tuning workflow, but they are not enough for a classification system. I still need classification metrics like macro F1, precision, recall, and confusion matrix.

Also, the system does not yet have a deployed inference API, confidence scoring, monitoring, or a feedback loop. Those are planned next steps.

## Section 3 - Architecture

### How is the project architected?

The architecture starts with incident title and description. Those records go through dataset preparation, validation, stratified splitting, and conversion to ShareGPT JSON. The processed data is used by LLaMA Factory to fine-tune Qwen3-1.7B with LoRA. The output is a fine-tuned adapter that can be used later for inference and evaluation.

The larger product architecture also includes future business rules, monitoring, and human review.

### Why does each component exist?

Dataset preparation exists to make sure the data is clean before training. Validation prevents bad labels and missing fields from entering the model. Splitting lets us separate training from validation and test data. ShareGPT conversion makes the dataset compatible with LLaMA Factory. LoRA fine-tuning adapts the base model without updating all model weights. Evaluation tells us whether the model is actually useful.

### What is the dataset pipeline?

The pipeline is:

1. Load `sample_incidents.csv`.
2. Validate required columns.
3. Validate support-team labels.
4. Detect duplicate title and description pairs.
5. Create stratified train, validation, and test splits.
6. Convert each row into ShareGPT/OpenAI messages.
7. Save JSON files under `data/processed/splits/`.
8. Generate a data quality report.

### What is the training workflow?

I prepared the data locally, pushed the repo to GitHub, pulled it into NVIDIA Brev, installed the training environment, registered the dataset with LLaMA Factory, ran a smoke training job, fixed configuration issues, and then ran LoRA fine-tuning for Qwen3-1.7B.

### What is the inference workflow?

The planned inference workflow is: an engineer provides an incident title and description, the system formats that into the same prompt structure used during training, the fine-tuned model predicts one support-team label, and business rules validate the output. If the model is low confidence or outputs an unsupported label, the incident should go to human review.

### Where does human-in-the-loop fit?

The model should not automatically assign production incidents. It should recommend a support team, and the engineer should accept or override it. The override should be captured as feedback for future evaluation and retraining.

### Why use cloud GPU?

My local Mac has only 8 GB unified memory, which is not a good environment for fine-tuning a 1.7B parameter model. NVIDIA Brev gave me access to an L4 GPU, which was much more appropriate for LoRA fine-tuning.

### How is the repo structured?

The repo separates product docs, dataset files, training configs, preprocessing code, test code, and output reports. That separation makes the project easier to review and closer to how an AI team would organize a real project.

## Section 4 - Dataset Engineering

### How did you design the dataset?

I designed the dataset around the minimum useful input and output for the MVP. The inputs are `incident_title` and `incident_description`. The label is `support_team`. I also designed a broader schema in the docs for future metadata like affected application, source system, priority, label quality, and dataset version.

### Why synthetic data?

Because real enterprise incidents can contain PHI, PII, internal system names, customer information, and proprietary operational details. For a public portfolio project, synthetic data is safer. The key was to make it realistic enough to represent actual support tickets without exposing sensitive information.

### How did you create the label taxonomy?

I chose realistic enterprise support teams such as Claims Engineering, Membership Engineering, Provider Systems, Digital Experience, API Platform, Infrastructure, Database Engineering, Security, Identity & Access, Batch Processing, DevOps, Integration Services, Reporting & Analytics, Billing Systems, and Data Engineering.

The labels are broad enough to cover common enterprise incidents but not so granular that the model would have too many classes for a small dataset.

### How did you handle duplicates?

I implemented duplicate detection using normalized title and description pairs. The logic lowercases text, strips extra whitespace, and groups records by normalized title-description pairs. If multiple incidents have the same pair, the pipeline flags them.

### How did you validate the data?

The pipeline validates required columns, required values, approved support-team labels, duplicate title-description pairs, and split distribution. It also creates a Markdown data quality report so the dataset can be reviewed before training.

### How did you split the data?

I used a stratified 70/15/15 split. Stratification matters because each support team needs representation in train, validation, and test sets. With a small dataset, I also made sure every class gets at least one validation and one test example.

### Why convert to ShareGPT format?

LLaMA Factory expects supervised fine-tuning data in a conversational format. Each example becomes a list of messages: a system instruction, a user message containing the incident title and description, and an assistant message containing the correct support-team label.

### What were the dataset challenges?

The biggest challenge was balancing realism with safety. Real tickets are messy, but public data cannot contain sensitive details. Another challenge was avoiding repetitive examples. If synthetic data is too templated, the model learns shallow patterns instead of useful routing signals.

## Section 5 - Fine-Tuning

### Why Qwen3-1.7B?

I chose Qwen3-1.7B because it is small enough for practical LoRA fine-tuning while still being a modern open-source language model. For a portfolio project, it is a good balance between capability, cost, and training feasibility.

### Why LoRA?

LoRA lets me fine-tune a small number of adapter weights instead of updating the full model. That makes training cheaper, faster, and easier to manage. It also keeps the adapter separate from the base model, which is better for artifact management.

### Why PEFT?

PEFT stands for parameter-efficient fine-tuning. The idea is that I do not need to update every weight in a large model to adapt it to a domain task. I can train a small adapter that captures the task-specific behavior.

### Why not full fine-tuning?

Full fine-tuning would require much more compute, memory, storage, and careful training management. For this task and dataset size, full fine-tuning would be unnecessary and more risky. LoRA is a better engineering choice.

### Why LLaMA Factory?

LLaMA Factory gives a practical fine-tuning workflow for open-source models. It supports LoRA, dataset registration, model templates, training configs, and GPU execution. It let me focus on dataset quality and configuration rather than writing a full trainer from scratch.

### What training configuration did you use?

The main configuration used Qwen3-1.7B, LoRA, supervised fine-tuning, sequence length 1024, learning rate `1e-4`, 4 epochs, LoRA rank 16, LoRA alpha 32, and dropout 0.05. I also had a smoke config with smaller settings to validate the environment before full training.

### Why those hyperparameters?

I chose conservative hyperparameters because the dataset is small. A high learning rate or too many epochs could overfit quickly. LoRA rank 16 gives some adaptation capacity without making the adapter too large. Dropout helps reduce overfitting risk.

### Why NVIDIA L4?

The L4 GPU is a practical cloud GPU for this kind of fine-tuning. It is much more suitable than my local Mac for loading the model and running LoRA training. I did not need a huge A100-style setup for this stage.

### What was the checkpoint strategy?

The adapter was saved under `models/checkpoints/qwen3-1.7b-lora-opstriage-v0.1.0`, but checkpoint files are excluded from Git. The repo stores configs and reports, not large model artifacts.

## Section 6 - Debugging

### What was the dataset path issue?

LLaMA Factory resolves dataset file paths relative to the `data/` directory. I originally had paths like `data/processed/splits/train.json`, so LLaMA Factory looked for `data/data/processed/splits/train.json`. The fix was to change the dataset registry paths to `processed/splits/train.json`.

### What was the LLaMA Factory compatibility issue?

The version I used was LLaMA Factory v0.9.5. Some config fields did not match that version. For example, `generation_max_new_tokens` needed to be changed to `max_new_tokens`.

### What happened with `generation_max_new_tokens`?

That field was not accepted by the installed LLaMA Factory version. The minimal fix was to use the supported field name, `max_new_tokens`, instead of trying to work around it elsewhere.

### What happened with missing `jieba`?

`jieba` is used by some metric/evaluation tooling, especially around text segmentation. When it was missing, the fix was to install the dependency in the Brev environment rather than changing the project logic.

### What happened with missing `nltk`?

`nltk` was also needed for evaluation-related metrics. The fix was similar: install the missing dependency in the training environment and keep the repo configs clean.

### What happened with `metric_for_best_model`?

The config referenced `eval_macro_f1`, but the current LLaMA Factory generation workflow does not automatically produce macro F1. That exposed a design gap: classification-specific evaluation should be a separate pipeline. I documented that instead of pretending BLEU and ROUGE are classification metrics.

### What was the YAML syntax issue?

Training configs are strict. A small syntax or unsupported-field issue can stop training before it starts. I used smoke training to catch those issues early before running the full job.

### Why run smoke training?

Smoke training validates the environment, model loading, dataset registration, tokenizer, LoRA setup, and output paths with a tiny job. It is much cheaper to fail early on a smoke run than halfway through full training.

### What did you learn from cloud GPU setup?

I learned that cloud training is not just "run the model." You have to manage Python versions, CUDA, PyTorch, dependencies, dataset paths, config compatibility, and artifact handling. Most of the engineering work is making the run reproducible and debuggable.

## Section 7 - Evaluation

### What are BLEU and ROUGE?

BLEU and ROUGE are text-generation metrics. BLEU measures overlap with reference text, often used in translation. ROUGE measures overlap too, often used in summarization. In this project, they were reported by the fine-tuning workflow.

### Why did those metrics appear?

Because the model was trained in a generative supervised fine-tuning setup. The assistant response is the support-team label, so LLaMA Factory reported generation-style metrics.

### Are BLEU and ROUGE enough?

No. They are not enough for this task. This is a classification problem, so the more important metrics are accuracy, precision, recall, macro F1, weighted F1, invalid-label rate, and confusion matrix.

### Why is macro F1 important?

Macro F1 treats each support team equally. That matters because smaller teams should not be ignored just because larger classes have more examples.

### Why precision?

Precision tells us: when the model predicts a team, how often is it correct? It matters because false assignments waste team time.

### Why recall?

Recall tells us: of all incidents that truly belong to a team, how many did the model catch? It matters because missed incidents create routing delays.

### Why confusion matrix?

A confusion matrix shows which teams the model confuses. That is very useful for this project because some teams naturally overlap, like Digital Experience vs API Platform or Security vs Identity & Access.

### How would you compare base vs fine-tuned model?

I would run the same test set through the base Qwen model and the fine-tuned adapter using the same prompt. Then I would compare exact-label accuracy, macro F1, weighted F1, invalid-label rate, and confusion matrix.

### What future evaluation improvements would you add?

I would add an evaluation script that loads predictions, normalizes labels, rejects unsupported labels, computes classification metrics, and exports confusion matrix and error examples.

## Section 8 - Production AI

### How would you productionize this?

I would wrap the model behind an inference API, add input validation, return the top predicted support team plus confidence, and apply business rules before showing the recommendation to an engineer. I would also log predictions, overrides, and final assignments for monitoring and retraining.

### What monitoring would you add?

I would monitor prediction volume, invalid-label rate, confidence distribution, override rate, latency, error rate, and performance by support team. Over time, I would also monitor drift in incident language.

### What observability would you add?

Each prediction should include model version, dataset version, timestamp, input length, predicted label, confidence, fallback status, and whether the engineer accepted or overrode the recommendation.

### How would feedback work?

If an engineer changes the predicted team, that override should be captured with the corrected label and reason. But I would not automatically retrain on every override. I would review feedback quality first.

### How would retraining work?

I would collect reviewed incidents, run data quality checks, create a new dataset version, train a candidate model, compare it against the current model, and only promote it if it passes evaluation gates.

### How would confidence scores work?

For production, I would prefer scoring the fixed label set instead of trusting free-form generated confidence. The system should know when to say "needs human review."

### What security concerns exist?

Incident text can contain PHI, PII, credentials, internal hostnames, or proprietary details. The system needs redaction, access controls, secure logging, and clear policies around what data can be used for training.

### How would it scale?

The inference service could be stateless behind an API. For high volume, we could batch requests or use a hosted inference endpoint. The dataset and model registry would track versions.

## Section 9 - AI Engineering Concepts

### What is an LLM?

An LLM is a language model trained to predict and generate text. In this project, I used an LLM because incident descriptions are unstructured language.

### What is a transformer?

A transformer is the architecture behind most modern LLMs. It uses attention to understand relationships between tokens in text.

### What are embeddings?

Embeddings are numeric representations of text. Similar text usually has similar embedding vectors. They are useful for search, clustering, and retrieval.

### What is fine-tuning?

Fine-tuning means taking a pre-trained model and training it further on task-specific examples. In this project, the task is mapping incident text to support-team labels.

### What is prompt engineering?

Prompt engineering is designing the input instruction so the model understands the task. Here, the prompt tells the model to classify the incident into exactly one approved support team.

### What is inference?

Inference is using the trained model to make predictions on new inputs.

### What is tokenization?

Tokenization breaks text into pieces the model can process. The model does not read raw words exactly like humans do; it reads tokens.

### What are adapters?

Adapters are small trainable modules added to a base model. They let us adapt the model without changing all its weights.

### What is quantization?

Quantization reduces the precision of model weights to save memory and speed up inference or training. For example, using 4-bit weights instead of 16-bit weights.

### What is LoRA?

LoRA is a parameter-efficient fine-tuning method. It trains small low-rank matrices instead of updating the full model.

### What is QLoRA?

QLoRA combines quantization with LoRA. It loads the base model in lower precision and trains adapters, which reduces memory needs.

### What is PEFT?

PEFT means parameter-efficient fine-tuning. LoRA is one PEFT method.

### What is RAG?

RAG means retrieval-augmented generation. It retrieves relevant documents and gives them to the model as context. For OpsTriage AI, future RAG could use support ownership docs or runbooks.

### What is MCP?

MCP, or Model Context Protocol, is a standard for connecting AI systems to tools and data sources. In a future enterprise version, it could help connect the model to incident systems, knowledge bases, or observability tools.

### What is agentic AI?

Agentic AI means a system can plan steps, use tools, and coordinate actions. For this project, I would be careful with agents. I would not let an agent auto-remediate production incidents without strong controls.

## Section 10 - Behavioral Questions

### Tell me about this project.

I built OpsTriage AI to solve a real production support problem: routing incidents to the right team. I designed the product, dataset, taxonomy, preprocessing pipeline, LLaMA Factory configs, cloud GPU training workflow, and documentation. The project helped me practice end-to-end AI engineering, not just model usage.

### What was the biggest challenge?

The biggest challenge was debugging the training workflow across local and cloud environments. The model training itself was only one part. I had to fix dataset path resolution, config compatibility, missing dependencies, and metric-selection issues.

### What was your biggest learning?

My biggest learning was that AI engineering is mostly system engineering around the model. Dataset quality, config management, reproducibility, evaluation, and artifact handling matter as much as the fine-tuning command.

### What would you improve?

I would add classification-specific evaluation, compare base vs fine-tuned model, add inference examples, expand the dataset, and build a small API or dashboard.

### Why are you transitioning into AI Engineering?

I enjoy working at the intersection of software, data, and real business workflows. My background helps me understand operational problems, and AI engineering gives me the tools to build systems that make those workflows smarter and faster.

### Why should we hire you?

I can take an ambiguous business problem and turn it into a structured AI project. I care about the full lifecycle: requirements, data, model, evaluation, deployment path, documentation, and responsible use. This project shows that I can learn quickly, debug real issues, and build with an enterprise mindset.

## Section 11 - Follow-Up Technical Questions

1. Why did you choose fine-tuning instead of prompt-only classification?
2. Why did you choose Qwen3-1.7B?
3. How would you evaluate whether fine-tuning helped?
4. What would a baseline model look like?
5. How would TF-IDF plus logistic regression compare?
6. Why is macro F1 important here?
7. How would you handle class imbalance?
8. How would you prevent hallucinated labels?
9. How would you constrain outputs to approved teams?
10. What is the difference between validation and test data?
11. Why did you use stratified splitting?
12. What happens if a class has too few examples?
13. How would you detect duplicates?
14. How would you detect near duplicates?
15. How would you handle ambiguous incidents?
16. How would you handle multi-team incidents?
17. How would you expand the dataset?
18. How would you validate synthetic data quality?
19. What are the risks of synthetic data?
20. How would you incorporate real data safely?
21. How would you remove PHI or PII?
22. What is LoRA rank?
23. What is LoRA alpha?
24. What does LoRA dropout do?
25. What would happen if the learning rate is too high?
26. What would happen if you train too many epochs?
27. How would you detect overfitting?
28. Why use a smoke training run?
29. What broke during LLaMA Factory setup?
30. What did the `data/data/...` error mean?
31. Why did `generation_max_new_tokens` fail?
32. Why are BLEU and ROUGE not enough?
33. How would you compute invalid-label rate?
34. How would you create a confusion matrix?
35. What confusion pairs do you expect?
36. How would you compare base vs fine-tuned model?
37. How would you package the adapter?
38. Why not commit model artifacts?
39. Where would you store checkpoints?
40. How would inference work?
41. How would you compute confidence?
42. What should happen below confidence threshold?
43. How would human feedback improve the model?
44. How would retraining be triggered?
45. How would you monitor drift?
46. How would you deploy this as an API?
47. What would the request and response schema be?
48. What security controls are needed?
49. How would you handle audit logging?
50. How would you convince a support team to trust it?
51. What is the role of business rules?
52. What would you do differently with more time?
53. What if the model performs worse than a baseline?
54. How would you debug bad predictions?
55. How would you explain this project to a non-technical manager?

## Section 12 - Recruiter Questions

### What is OpsTriage AI?

It is an AI project that classifies production incidents into support teams using a fine-tuned open-source language model.

### Why is this project relevant to AI engineering?

It includes dataset design, preprocessing, fine-tuning, cloud GPU training, evaluation documentation, and responsible AI design.

### What technologies did you use?

Python, LLaMA Factory, Qwen3-1.7B, LoRA, NVIDIA Brev, GitHub, and Markdown documentation.

### Is this a deployed product?

Not yet. It is currently a fine-tuning and AI engineering portfolio project. The next step would be inference and evaluation.

### What role did you personally play?

I built the project end to end: product framing, dataset design, preprocessing, configs, training workflow, debugging, and documentation.

### What is the strongest part of the project?

The strongest part is that it is structured like a real AI engineering project, not just a demo. It has data design, validation, training configs, debugging notes, and artifact governance.

## Section 13 - Hiring Manager Questions

### How would this fit into an enterprise support organization?

It would sit between incident intake and assignment. The model would recommend a support team, then a human support engineer would review and confirm or override the recommendation.

### How would you measure business impact?

I would measure first-assignment accuracy, triage time reduction, reassignment rate, engineer override rate, and SLA impact.

### What would make this production-ready?

It needs a larger dataset, classification-specific evaluation, baseline comparison, inference API, confidence handling, observability, security controls, and a human feedback loop.

### How would you manage risk?

I would keep human approval in the loop, block auto-assignment for low-confidence predictions, monitor invalid outputs, audit decisions, and avoid training on sensitive data.

### Why should a team trust this system?

Trust would come from transparent evaluation, clear confidence thresholds, easy override, audit logs, and evidence that it reduces routing errors without removing human control.

### What would you build next?

I would build the classification evaluation pipeline first, then add inference examples, then build a small API or dashboard. After that I would add business rules and feedback capture.
