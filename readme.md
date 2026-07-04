# PCRF Transformer Reliability Suite — Experiment README

**Version context:** Enterprise-grade PCRF Transformer Reliability Suite with baseline reporting, full PCRF experiment execution, external CSV dataset support, dataset validation, multi-tier structural reliability reconciliation, and generated developer blueprints.

---

## 1. Purpose of This Experiment

The PCRF (Parameter Causal Reliability Flow) Transformer Reliability Suite is designed to evaluate, regularize, and govern transformer model reliability during Supervised Fine-Tuning (SFT). Unlike traditional fine-tuning scripts that focus entirely on raw accuracy optimization, the PCRF Suite establishes a **hallucination-centered and representation-safety narrative**. 

The suite treats the deep latent space of the transformer as a series-connected causal system of message passing. By perturbing specific hidden states, checking activation drift, and setting routing boundaries, the suite answers several critical questions:

- **Where does the baseline model fail to capture semantic targets?** It maps pre-training baseline vulnerability before SFT updates are applied.
- **Which SFT modifications introduce representation drift?** It tracks how parameter changes during SFT degrade hidden representation boundaries.
- **Did PCRF diagnostics isolate critical bottleneck blocks?** It solves downstream probability derivatives using PyTorch autograd and Birnbaum structural importance metrics to isolate the exact layers responsible for accuracy decay.
- **Did the Protected Router prevent unsafe candidate behavior?** It tests a dual-path inference routing architecture to verify if regressions are blocked and repairs are safely served.
- **Which SFT optimizations are approved for weight promotion?** It acts as a safety gatekeeper, declaring weights `SAFE_TO_APPLY`, `MEASUREMENT_ONLY`, or `DO_NOT_APPLY`.
- **How can developers apply these findings to subsequent SFT training cycles?** It programmatically generates code-ready blueprint markdown files based on verified safe tracks.

### 🧠 Core Interpretation

> **PCRF is primarily a reliability analyzer, hallucination exposure detector, confidence calibrator, and deployment guardrail. It should not be presented as a generic accuracy optimizer.** It serves to insulate served endpoints from SFT representation drift while maximizing repair recovery.

---

## 2. Modular File Architecture & Core Rules

The PCRF suite is structured as a professional, production-grade modular codebase consisting of six key files:

```text
├── run_experiment.py       # Command Line Interface (CLI) & experiment orchestrator
├── pcrf_core.py            # Core reliability math, Autograd DAG calculations, and Birnbaum indices
├── pcrf_dataset.py         # QA Cloze Dataset, text normalization, and CSV validation
├── pcrf_governance.py      # SafePCRFController gating check logic and ProtectedRouter
├── pcrf_modeling.py        # Hook management, EvaluatorPlus CLM metrics, SFT regularizer & CDL v2
└── pcrf_reporting.py       # Markdown Executive Report and Developer Debug Log generators
```

### ⚠️ Crucial Architectural Rules

1. **Comparison Baseline Outputs Are Never Masked:** For audit integrity and diagnostic traceability, baseline outputs must never be masked in developer or customer reports. If a baseline output failed target capture, its raw text must be exposed so developers can inspect what went wrong.
2. **Unresolved Candidate Hallucinations Are Masked:** Candidate outputs and final served outputs (when safety-withheld) must be strictly masked using the safe template string: `⚠️ Hallucination Risk Detected — Response Withheld for Safety` to prevent unsafe exposure in customer artifacts.
3. **Small-Model Relaxation Rule:** If a lightweight model (such as a `0.5B` parameter profile or `GPT-2`) is evaluated, strict formatting and instruction contract gates are bypassed. If the lightweight candidate captures the semantic target, it is safely treated as a repair, and contract violations are captured purely as diagnostic observations. For standard models, formatting and contract compliance are strictly enforced.

---

## 3. Supported Execution Modes

The runner is orchestrated via the CLI script: `run_experiment.py`. It supports two principal execution modes.

### 3.1 Default / Full Mode

If no mode is supplied (or `full` is explicitly passed), the suite runs the complete PCRF pipeline. This includes running baseline evaluations, standalone derivative estimation, curriculum dataset curation, structural residual-depth profiling, SFT CdL v2 optimization training, Protected Router routing, MD report generation, and programmatic conditional blueprints.

```bash
python run_experiment.py
```

*Equivalent explicit command:*

```bash
python run_experiment.py full
```

### 3.2 Baseline Mode

Baseline-only mode is selected when skipping downstream training, regularization, and routing tasks. It profiles only the pre-training model on all dataset splits and generates a baseline-only compliance trace.

```bash
python run_experiment.py baseline
```

---

## 4. Python Virtual Environment Setup

Always execute the suite inside a virtual environment to prevent package version drift.

### 4.1 Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4.2 Upgrade Packaging Tools & Install Dependencies

```bash
python -m pip install --upgrade pip setuptools wheel
pip install torch transformers numpy psutil scikit-learn
```

### 4.3 Verify CUDA Context

```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available())"
```

---

## 5. CLI Execution & Argument Routing

### 5.1 Default Execution (Built-In Dataset)

Runs default `full` mode using the built-in mock cloze dataset (130 balanced examples spanning scientific, cs, and factual domains):

```bash
python run_experiment.py
```

### 5.2 Baseline Execution (Built-In Dataset)

```bash
python run_experiment.py baseline
```

### 5.3 External Dataset Execution (Full Mode)

Pass your validated CSV dataset file using the `--dataset` argument:

```bash
python run_experiment.py full --dataset customer_prompts.csv
```

### 5.4 External Dataset Execution (Baseline Mode)

```bash
python run_experiment.py baseline --dataset customer_prompts.csv
```

---

## 6. External Dataset Verification

When `--dataset` is supplied, the suite executes a strict validation pass via `validate_external_dataset_file` before loading the model. If errors are found, the run halts immediately to prevent out-of-memory errors on corrupt files.

### 6.1 Expected CSV Header Schema

The dataset file must be a CSV file with this exact header:

```csv
id,prompt,target,task_type,split,is_critical,criticality_weight
```

### 6.2 Schema Column Types & Specifications

| Column | Type | Validation Constraint | Meaning |
| :--- | :---: | :--- | :--- |
| `id` | Integer | Must be a unique integer across all rows. | Unique prompt identifier. |
| `prompt` | String | Cannot be empty or whitespace-only. | Input text prompt sent to the model. |
| `target` | String | Cannot be empty. Represented as a clean target. | Expected answer or semantic target. |
| `task_type` | String | String label (e.g., `factual_cloze`, `cs_cloze`). | Category label used for taxonomical failure groupings. |
| `split` | String | Must be one of: `train`, `seen_val`, `unseen_val`, `ood`. | Partitions dataset for the validation engine. |
| `is_critical` | Integer | Must be `0` or `1`. | Identifies high-risk business prompts. |
| `criticality_weight` | Float | Must be a positive numeric value. | Optimization and priority loss multiplier. |

---

## 7. Sample Compliant Dataset File

The following 8-row sample dataset represents a fully compliant schema. You can save this as `customer_prompts.csv` to verify system behavior:

```csv
id,prompt,target,task_type,split,is_critical,criticality_weight
1,"Complete with one word only: The capital of France is","Paris","factual_cloze","train",0,1.0
2,"Complete with one word only: The largest planet is","Jupiter","factual_cloze","train",0,1.0
3,"Complete with one word only: The chemical symbol for water is","H2O","factual_cloze","seen_val",0,1.0
4,"Complete with one word only: The author of Hamlet is","Shakespeare","factual_cloze","seen_val",0,1.0
5,"Complete with one word only: The currency of Japan is","Yen","factual_cloze","unseen_val",0,1.0
6,"Complete with one word only: The speed of light is measured in","meters per second","factual_cloze","unseen_val",1,1.5
7,"Complete with one word only: In quantum computing, a basic unit is called a","qubit","ood_fact","ood",1,2.0
8,"Complete with one word only: In Kubernetes, a deployable unit is called a","pod","ood_fact","ood",1,2.0
```

---

## 8. Split Type Intuitions

To properly evaluate SFT model reliability, customer dataset rows must be mapped to specific splits, each representing a distinct validation objective:

### 8.1 `train`
Used to fit standard weights, build priority sampling distributions, or regularize parameter drift paths. Prompts assigned to `train` should represent your baseline learning objectives.

### 8.2 `seen_val`
Prompts in `seen_val` represent patterns and formats extremely close to the training set (e.g., similar tasks but different entities). Use this split to measure overfitting, over-steering, and to confirm that the candidate preserves base capabilities.

### 8.3 `unseen_val`
Prompts in `unseen_val` differ meaningfully from training samples while remaining within the expected business domain. Use this split to measure SFT generalization and verify if fine-tuning is successfully transferring to unseen topics.

### 8.4 `ood` (Out-of-Distribution)
Contains prompts representing edge cases, rare tasks, specialized jargon, or highly complex conditions. Use this split to measure transfer limits and establish model stability when exposed to raw production anomalies.

---

## 9. How to Derive Splits from Real Customer Data

### 9.1 Small Datasets (e.g., 100 Prompts)
```text
train       = 70 prompts (for localized calibration)
seen_val    = 15 prompts (to monitor familiar validation preservation)
unseen_val  = 10 prompts (to evaluate generalization within expected domain)
ood         = 5 prompts  (to assess out-of-distribution transfer limits)
```

### 9.2 Larger Datasets (e.g., 1,000 Prompts)
```text
train       = 750 prompts
seen_val    = 125 prompts
unseen_val  = 75 prompts
ood         = 50 prompts
```

### 9.3 General Recommendation Workflow
1. Remove identical prompts or near-duplicates.
2. Group remaining prompts by business task.
3. Assign standard, high-frequency prompts to `train`.
4. Hold out similar but distinct prompts to `seen_val`.
5. Hold out slightly more diverse prompts within the same task domain to `unseen_val`.
6. Reserve highly complex, long-sequence, or edge-case questions to `ood`.

---

## 10. Assigning `is_critical` & `criticality_weight`

### 10.1 `is_critical` (Binary: `0` or `1`)
Indicates whether a wrong answer carries catastrophic downstream consequences (e.g., security breaches, legal non-compliance, system outages). 
- Use `is_critical = 0` for informational queries where errors are inconvenient but operationally safe.
- Use `is_critical = 1` for API tokens, permission rules, financial calculations, encryption parameters, or system configurations.

### 10.2 `criticality_weight` (Numeric Multiplier)
Used by the CDL v2 regularizer and curriculum planners to scale priority scores during SFT optimization. 

| Operational Criticality | `is_critical` | Weight Multiplier | Rationale |
| :--- | :---: | :---: | :--- |
| Standard Informational | 0 | `1.0` | Baseline baseline importance. |
| High Priority | 1 | `1.5` | Errors introduce moderate business friction. |
| Highly Sensitive / Security | 1 | `2.0` | Errors compromise security, privacy, or customer trust. |
| Mission Critical | 1 | `3.0` | Errors cause direct regulatory penalties, data loss, or physical outages. |

---

## 11. Dataset Validation Behavior

If `--dataset` is provided, validation occurs first. If any rule is violated, execution stops with a detailed error format:

```text
==========================================================================================
ERROR: Invalid dataset file format.

Reason(s):
 - [Row 12] Column 'target' is blank.
 - Missing rows for splits: ['ood']. Each split category must have at least one row.

Expected CSV format:
id,prompt,target,task_type,split,is_critical,criticality_weight

Sample compliant dataset:
id,prompt,target,task_type,split,is_critical,criticality_weight
1,"The capital of France is","Paris","factual_cloze","train",0,1.0
...

Why this format is required:
 - train: Used for fitting, adaptation, or regularization paths...
 - seen_val: Used to measure preservation on validation prompts...
 - unseen_val: Used to measure generalization on validation prompts...
 - ood: Used to measure out-of-distribution transfer behavior...
==========================================================================================
Execution halted before model loading or experiment execution.
```

---

## 12. Baseline-Only Report

When running `python run_experiment.py baseline`, the suite bypasses all training, regularization, and routing diagnostics to output `Baseline_Only_Report.md` inside your output directory. 

### 12.1 Report Schema & Table

This report includes a full prompt/generation audit table displaying baseline completions over *all* splits (train, validation, and OOD):

```markdown
| ID | Split | Prompt | Baseline Generation | Expected Value | Actual Value | Match? | Hallucinated? |
|---|---|---|---|---|---|---|---|
| 001 | seen_val | *Complete...* | `Paris` | `Paris` | `Paris` | YES | NO |
| 002 | unseen_val| *Complete...* | `Washington` | `New York` | `Washington` | NO | YES |
```

### 12.2 Hallucination Attribution Rule
In baseline-only reporting, a baseline output is classified as `Hallucinated? = YES` **if and only if** its generated text fails exact semantic capture vs. target (`evaluate_semantic_match == False`). Since baseline outputs must never be masked for audit integrity, this table exposes exactly where pre-training vulnerabilities lie prior to fine-tuning.

---

## 13. Executive Report Overview

The full PCRF experiment generates a comprehensive executive scorecard (`PCRF_Executive_Reliability_Report.md`) inside the output folder. This report is written in highly professional, calibrated, and customer-safe language, strictly prioritizing sections to establish a clear reliability narrative:

### 13.1 Ordered Sections

1. **Section 2: PCRF Governance Assessment Box:** Houses the primary customer metrics (Governed served accuracy vs. candidate accuracy and baseline accuracy).
2. **Section 1: Hallucination Exposure Control:** Tracks overall active safety interventions and exposure rates.
3. **Section 3: Served Accuracy Framework:** Clear conceptual breakdown of how the Protected Router operates.
4. **Section 4: Regression Containment Metrics:** Tabulates how effectively routing loops block candidate regressions.
5. **Section 5: Repair Promotion Metrics:** Shows how many semantic repairs were identified, validated, and promoted.
6. **Section 6: SFT Candidate Quality vs. Governance Outcomes:** Contrasts un-routed candidate parameter quality with actual routed system outcomes.
7. **Section 7: Transition Analysis Matrix:** Full statistical breakdown of model transitions.
8. **Section 8: Technical Debug & Advanced Analytics:** Detailed discussion on Likelihood-Semantic Divergences and Regression Detection Coverages.
9. **Section 9: Protected Router Case Showcases:** Dynamic examples displaying real-time routing decisions.
10. **Section 10: Gating Check Outcomes:** Displays every safety check from `SafePCRFController`.
11. **Section 11: Integrated PCRF Scoreboard:** Scorecard detailing performance across the four standalone scenario plugins.
12. **Section 12: Structural Reconciliation:** Resolves sequential series product decay vs. CREW residual-depth formulas.
13. **Section 13: Compliance Trace & Debug Table:** Compiles prompts where targets were missed.
14. **Section 14: Customer-Safe Report Masking Audit:** Confirms that candidate outputs were masked to prevent exposure.

---

## 14. Executive Report Metrics — Intuition and Usage

### 14.1 Seen Exact-Match Accuracy
- **Intuition:** measures correctness on validation prompts close to training. A decrease indicates representation over-steering or forgetting.
- **Usage:** Serves as a primary SFT non-degradation indicator.

### 14.2 Unseen Generalization Accuracy
- **Intuition:** measures correctness on out-of-training domain prompts. Measures whether SFT updates successfully generalized or overfit.
- **Usage:** Critical for proving candidate model quality.

### 14.3 Negative Log-Likelihood (NLL)
- **Intuition:** measures cross-entropy loss over expected targets. Lower is better. Worsening NLL despite flat accuracy suggests the model is growing unstable.
- **Usage:** Primary continuous metric for regularization.

### 14.4 Perplexity (PPL)
- **Intuition:** Exponential mapping of NLL ($e^{NLL}$). Higher perplexity means the expected target text is highly "surprising" to the candidate.
- **Usage:** Intuitive representation of model uncertainty.

### 14.5 Strict Exact Match
- **Intuition:** Checks if the decoded string exactly matches the target after simple lowercase stripping. Strongly penalizes instruction-contract violations (e.g. over-generation).
- **Usage:** Gates candidate promotion on formatting compliance.

### 14.6 First-Token Match
- **Intuition:** Evaluates if the very first decoded token is correct. Helpful for understanding if the model started correctly before over-generating.
- **Usage:** Isolates semantic knowledge from formatting drift.

### 14.7 Semantic Capture
- **Intuition:** Evaluates if the expected target is captured anywhere inside the decoded boundaries.
- **Usage:** Measures raw knowledge retrieval.

### 14.8 Instruction Violation Rate
- **Intuition:** Tracks how often the candidate generated extra text, blank lines, or template choices instead of the target word.
- **Usage:** Indicates whether decoding parameters or custom formatting suppression is required.

### 14.9 Hallucination Exposure Control Rate
- **Intuition:** The percentage of overall baseline risks and candidate regressions that were successfully contained by the Protected Router.
- **Usage:** High rate demonstrates that router governance is successfully insulating served environments.

### 14.10 Total Baseline Hallucinations Found
- **Intuition:** The exact count of validation prompts where the baseline failed. This forms the baseline exposure surface.
- **Usage:** Denominator for repair and exposure metrics.

### 14.11 Active Semantic Target Recoveries
- **Intuition:** Baseline failed, but candidate captured the semantic target. This represents potential candidate repairs.
- **Usage:** Diagnostic measurement of SFT capability improvement.

### 14.12 Contract-Clean SFT Repairs Promoted
- **Intuition:** SFT candidate successfully repaired a baseline failure *and* met all instruction and exact-match contract rules.
- **Usage:** Safer repair cases promoted into served environments.

### 14.13 Semantic Recoveries Withheld for Contract
- **Intuition:** Candidate retrieved the correct answer but violated formatting contracts.
- **Usage:** Direct warning that decoding boundaries or instruction tuning is fragile.

### 14.14 Candidate Over-Steers Prevented
- **Intuition:** Both baseline and candidate failed, but candidate presented a higher risk score. The router safely fallback-selected the lower-risk baseline output.
- **Usage:** Proof of risk-mitigation gating.

### 14.15 Catastrophic Regressions Blocked
- **Intuition:** Baseline was correct, but candidate failed. The router blocked the candidate and served the baseline fallback.
- **Usage:** Measures regression-containment performance.

### 14.16 Model Transitions
- **Correct ➔ Correct:** Stability preserved across both models.
- **Correct ➔ Wrong:** Catastrophic regression. Must be blocked by the router.
- **Wrong ➔ Correct:** Repair opportunity. If clean, promoted; if dirty, withheld.
- **Wrong ➔ Wrong:** Persistent failure. Handled via abstention/fallback.

### 14.17 Structural Reliability ($R_{sys}$)
- **Intuition:** Multi-layer sequential probability chain indicating representation stability. 
- **Usage:** Multiplicative product of layer-wise survival rates.

### 14.18 Birnbaum Sensitivity Index ($D_R$)
- **Intuition:** Analytical derivative indicating which decoder layers have the largest downstream impact on model reliability.
- **Usage:** Guides parameter-group optimizer damping and SFT regularization targets.

### 14.19 Gating check Outcomes
- **Intuition:** Multi-gate system checks on accuracy, risk drift, sample sizes, and structural reliability.
- **Usage:** Establishes direct promotional boundaries.

### 14.20 Metric Confidence Section
- **Intuition:** Flags if validation sample sizes are too small to support strong claims.
- **Usage:** Calibrates claims to prevent overclaiming.

---

## 15. Safe, Unsafe, and Measurement-Only Components

To protect SFT deployments, the suite organizes candidate features into three operational categories:

### 15.1 Safe Diagnostic Components
These components present high stability and are approved for immediate use. Typically includes standalone derivatives, curriculum plans, and Protected Router inference gating.

### 15.2 Unsafe Components
These components present immediate risk (e.g., candidate weights that degrade unseen validation accuracy or cause risk drift). They are blocked from weight promotion.

### 15.3 Measurement-Only Components
Approved for monitoring, auditing, and logging, but blocked from production enforcement. Helpful for collecting canary data before committing to weight updates.

---

## 16. Blueprint Markdown Files

When the experiment is executed in `full` mode, the suite evaluates which scenario tracks achieved stable scores. For every track deemed `SAFE_TO_APPLY`, the reporting engine programmatically generates a visual implementation blueprint file. 

These are located in the output folder and contain ready-to-use Python implementations:

### 16.1 Parameter Sensitivity-Damped Optimization Blueprint
*File Name:* `PCRF_Implementation_Blueprint_Derivatives_<MODEL_NAME>.md`
- **When generated:** When the derivatives track is verified as safe.
- **Developer action:** Copy the code block to configure SFT optimizers to adapt learning rates scaled inversely by layer sensitivity coordinates.

### 16.2 Curriculum Sampling Curation Blueprint
*File Name:* `PCRF_Implementation_Blueprint_Curriculum_<MODEL_NAME>.md`
- **When generated:** When curriculum curation is verified as safe.
- **Developer action:** Use the generated dataloader script to sample SFT examples based on normalized priority scores and oversampling bounds.

### 16.3 Real-Time Structural Drift Alarm Blueprint
*File Name:* `PCRF_Implementation_Blueprint_Structural_<MODEL_NAME>.md`
- **When generated:** When the structural monitor is verified as safe.
- **Developer action:** Copy the code block to construct a runtime monitor that computes real-time activation cosine similarity and raises alerts on drift.

### 16.4 Advanced CDL v2 SFT Regularization Blueprint
*File Name:* `PCRF_Implementation_Blueprint_Regularization_<MODEL_NAME>.md`
- **When generated:** When SFT regularization is verified as safe.
- **Developer action:** Integrate the CDL v2 SFT loss formulation (comprising cross-entropy, KL divergence, hinge margin, and confidence penalties) into your training code.

---

## 17. SFT Action Mapping

Use the following mapping to guide your next engineering steps based on report signals:

| Executive Report Signal | Diagnostic Root Cause | Recommended Next Step | Active Blueprint Target |
| :--- | :--- | :--- | :--- |
| **High `Correct ➔ Wrong` Transitions** | Candidate over-steering during SFT. | Reject direct weight promotion. Deploy Protected Router to intercept regressions. | API Guard / CDL Regularization |
| **High `Wrong ➔ Correct` (Dirty Repairs)** | Model has knowledge but violates formatting. | Enhance instruction tuning, enforce stricter stop tokens, or apply margin loss. | CDL Regularization |
| **High `Wrong ➔ Wrong` (Persistent Failure)** | Knowledge gap in baseline model. | Supplement training data or use retrieval-augmented generation (RAG). | Curriculum Curation |
| **High Instruction Violations** | Decode template leakage or continuation drift. | Enforce one-token generation modes or contrastive formatting penalties. | CDL Regularization |
| **Low Structural Reliability $R_{sys}$** | Representational drift compounded across blocks. | Damp SFT optimization on sensitive layers or increase weight penalties. | Parameter Damping |
| **Low Validation Sample Size Warning** | Validation partition size is too small. | Scale validation dataset to meet statistical confidence boundaries. | Dataset Filtration |

---

## 18. Recommended Workflow for Developers

### Step 1 — Benchmark Baseline Exposure
Run the experiment in baseline mode on your customer-aligned dataset to establish baseline vulnerabilities:
```bash
python run_experiment.py baseline --dataset customer_prompts.csv
```
Review `Baseline_Only_Report.md` to identify failed prompts, critical targets, and hallucination rates.

### Step 2 — Run Full PCRF Experiment
Train, profile, and evaluate the candidate model using full mode:
```bash
python run_experiment.py full --dataset customer_prompts.csv
```

### Step 3 — Review the Executive Summary & Gating Status
Open `PCRF_Executive_Reliability_Report.md`. Check Section 1 and Section 2 to confirm whether direct candidate weight promotion was approved or rejected.

### Step 4 — Inspect Critical Failure & Success Traces
If direct promotion was rejected, open `critical_failure.txt` to examine row-level failures. Open `governance_success_trace.txt` to see how Protected Router prevented exposure.

### Step 5 — Implement Blueprint Code
Open the generated blueprint markdown files for safe diagnostic tracks. Integrate the provided code blocks into your training pipeline to resolve the identified vulnerabilities.

### Step 6 — Re-run and Validate
Re-run baseline and full modes on your calibrated training pipeline until all critical gates pass and weights are declared `SAFE_TO_APPLY`.

---

## 19. Common Mistakes to Avoid

1. **Treating PCRF as a Generic Accuracy Optimizer:** PCRF must be framed as a reliability, safety, and risk containment engine.
2. **Masking Baseline Outputs:** Baseline outputs must remain unmasked for compliance audit trailing.
3. **Evaluating with Trivial Prompts:** If validation prompts are too easy, representational drift and regression risks will not trigger.
4. **Duplicate Prompts Across Splits:** Ensure no prompt is duplicated between `train` and validation partitions.
5. **Marking All Prompts as Critical:** If every row is critical, the prioritization signal is diluted.
6. **Deploying Candidates with Regressions:** Direct adoption of candidates with any regressions must be blocked.
7. **Overclaiming Small-Sample Results:** Keep executive findings calibrated using sample size confidence gates.

---

## 20. Troubleshooting

### 20.1 Dataset Fails Validation Pass
Confirm your file is a valid CSV with the correct headers. Check for blank fields, non-integer IDs, duplicate IDs, invalid splits, or non-numeric criticality weights.

### 20.2 No Row-Level Table in Baseline Report
Ensure you are running the runner in baseline mode (`python run_experiment.py baseline`) and that the dataset path is parsed correctly.

### 20.3 Full Mode Runs on Default Execution
This is expected behavior. If no command is provided, `run_experiment.py` defaults to full mode.

### 20.4 External Dataset is Ignored
Ensure you pass `--dataset <filename.csv>` directly to the CLI entry point.

### 20.5 Audit Masking Flags a Failure
Ensure candidate outputs are strictly masked using `SAFETY_WITHHELD_RESPONSE` on hallucination. Do not mask correct baseline outputs.