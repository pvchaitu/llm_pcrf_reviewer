# PCRF Transformer Reliability Suite — Experiment README

**Version context:** Enterprise-grade PCRF Transformer Reliability Suite with baseline reporting, full PCRF experiment execution, external CSV dataset support, dataset validation, and generated developer blueprints.

---

## 1. Purpose of This Experiment

The PCRF Transformer Reliability Suite is designed to evaluate and govern transformer model reliability using a hallucination-centered narrative rather than a raw accuracy-optimization narrative.

The experiment helps answer questions such as:

- Where does the baseline model fail to capture the expected target?
- Which failures are likely hallucination exposure risks?
- Did PCRF diagnostics identify reliability-sensitive layers or behaviors?
- Did the protected router prevent unsafe candidate behavior?
- Which PCRF components are safe to use, unsafe to promote, or measurement-only?
- Which generated blueprint markdown files can developers use for next-step implementation?

The core interpretation is:

> PCRF is primarily a reliability analyzer, hallucination exposure detector, confidence calibrator, and deployment guardrail. It should not be presented as a generic accuracy optimizer.

---

## 2. Supported Execution Modes

The updated experiment supports two execution modes.

### 2.1 Default / Full Mode

If no mode is supplied, the experiment runs in `full` mode.

```bash
python pcrf_transformer_reliability_suite.py
```

Equivalent explicit command:

```bash
python pcrf_transformer_reliability_suite.py full
```

Full mode runs the complete PCRF-enabled experiment flow, including baseline measurement, PCRF diagnostics, candidate/regularized path evaluation where enabled, protected-router analysis, executive reporting, and blueprint generation.

### 2.2 Baseline Mode

```bash
python pcrf_transformer_reliability_suite.py baseline
```

Baseline mode runs only the baseline model evaluation and generates `Baseline_Only_Report.md`. In the updated codebase, this report also includes a row-level prompt/generation hallucination audit table.

### 2.3 Important Mode Clarification

There is **no `pcrf_only` mode**.

Use:

```bash
python pcrf_transformer_reliability_suite.py full
```

or simply:

```bash
python pcrf_transformer_reliability_suite.py
```

for the PCRF-enabled/default experiment.

---

## 3. Python Virtual Environment Setup

Use a virtual environment to avoid conflicts with global Python packages.

### 3.1 Create Virtual Environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3.2 Upgrade Packaging Tools

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 3.3 Install Dependencies

Typical dependency installation:

```bash
pip install torch transformers numpy pandas scikit-learn psutil
```

If your environment requires a CUDA-specific PyTorch build, install PyTorch using the command recommended for your CUDA version from the official PyTorch selector.

### 3.4 Verify Environment

```bash
python -c "import torch, transformers, numpy; print('torch', torch.__version__); print('cuda', torch.cuda.is_available())"
```

If CUDA is unavailable, the experiment may run on CPU but will be slower.

---

## 4. Running the Experiment

### 4.1 Built-in Mock Dataset, Default Full Mode

```bash
python pcrf_transformer_reliability_suite.py
```

### 4.2 Built-in Mock Dataset, Explicit Full Mode

```bash
python pcrf_transformer_reliability_suite.py full
```

### 4.3 Built-in Mock Dataset, Baseline Mode

```bash
python pcrf_transformer_reliability_suite.py baseline
```

### 4.4 External Dataset, Default Full Mode

```bash
python pcrf_transformer_reliability_suite.py --dataset customer_prompts.csv
```

### 4.5 External Dataset, Explicit Full Mode

```bash
python pcrf_transformer_reliability_suite.py full --dataset customer_prompts.csv
```

### 4.6 External Dataset, Baseline Mode

```bash
python pcrf_transformer_reliability_suite.py baseline --dataset customer_prompts.csv
```

---

## 5. External Dataset File Support

The updated codebase supports an optional CSV dataset file using:

```bash
--dataset <filename>
```

If `--dataset` is not provided, the experiment uses the built-in mock cloze dataset.

If `--dataset` is provided, the file is validated before model loading or experiment execution. If validation fails, the run halts early with a clear error message and a sample compliant CSV format.

---

## 6. Expected CSV Format

The dataset file must be a CSV file with this exact header:

```csv
id,prompt,target,task_type,split,is_critical,criticality_weight
```

### 6.1 Required Columns

| Column | Required | Meaning |
|---|---:|---|
| `id` | Yes | Unique integer prompt identifier. |
| `prompt` | Yes | Input prompt sent to the model. |
| `target` | Yes | Expected answer or semantic target. |
| `task_type` | Yes | Category label such as `factual_cloze`, `entity_completion`, `domain_fact`, or `ood_fact`. |
| `split` | Yes | One of `train`, `seen_val`, `unseen_val`, or `ood`. |
| `is_critical` | Yes | `0` for normal prompt, `1` for critical prompt. |
| `criticality_weight` | Yes | Numeric priority multiplier such as `1.0`, `1.5`, `2.0`, or `3.0`. |

---

## 7. Sample Compliant Dataset File

Save the following as `customer_prompts.csv`.

```csv
id,prompt,target,task_type,split,is_critical,criticality_weight
1,"The capital of France is","Paris","factual_cloze","train",0,1.0
2,"The largest planet in our solar system is","Jupiter","factual_cloze","train",0,1.0
3,"The chemical symbol for water is","H2O","factual_cloze","seen_val",0,1.0
4,"The author of Hamlet is","Shakespeare","factual_cloze","seen_val",0,1.0
5,"The currency of Japan is","Yen","factual_cloze","unseen_val",0,1.0
6,"The speed of light is measured in","meters per second","factual_cloze","unseen_val",1,1.5
7,"In quantum computing, a basic unit is called a","qubit","ood_fact","ood",1,2.0
8,"In Kubernetes, a deployable unit is called a","pod","ood_fact","ood",1,2.0
```

---

## 8. Understanding Dataset Split Types

The four split types represent different reliability objectives.

### 8.1 `train`

The `train` split contains examples available to adaptation, curriculum, regularization, or training-related parts of the full PCRF flow.

Use `train` for prompts that represent the known domain or controlled learning set.

Example:

```csv
1,"The capital of France is","Paris","factual_cloze","train",0,1.0
```

### 8.2 `seen_val`

The `seen_val` split contains validation prompts that are close to the training distribution but were not used as training examples.

Use this split to evaluate preservation of familiar patterns and to detect regressions or over-steering.

Example relationship:

- Training prompt pattern: capital-city facts.
- Seen validation prompt: another capital-city fact not used in training.

Example:

```csv
3,"The chemical symbol for water is","H2O","factual_cloze","seen_val",0,1.0
```

### 8.3 `unseen_val`

The `unseen_val` split contains in-domain prompts that differ from training examples more meaningfully than `seen_val`.

Use this split to measure generalization within the broader expected usage domain.

Example relationship:

- Training: geography facts.
- Unseen validation: currency, science, protocol, or domain facts still relevant to the customer environment.

Example:

```csv
5,"The currency of Japan is","Yen","factual_cloze","unseen_val",0,1.0
```

### 8.4 `ood`

The `ood` split means out-of-distribution.

Use this split for prompts that are harder, rarer, more specialized, or meaningfully different from the training distribution.

The OOD split is valuable for reliability and deployment-risk analysis because it helps determine whether model behavior changes when prompts are outside normal traffic patterns.

Example:

```csv
7,"In quantum computing, a basic unit is called a","qubit","ood_fact","ood",1,2.0
```

---

## 9. How to Derive Splits from Real Customer Data

### 9.1 If You Have 100 Prompts

A practical starting split:

```text
train       = 70
seen_val    = 15
unseen_val  = 10
ood         = 5
```

### 9.2 If You Have 1,000 Prompts

A practical starting split:

```text
train       = 750
seen_val    = 125
unseen_val  = 75
ood         = 50
```

### 9.3 If You Have a Very Small Dataset

Use at least one row per split. For demonstration runs, use at least two examples per split for readability.

```text
train       = 2+
seen_val    = 2+
unseen_val  = 2+
ood         = 2+
```

### 9.4 Recommended Split Assignment Method

1. Collect source Q&A / prompt-target records.
2. Remove duplicates and near duplicates.
3. Group prompts by business domain or task type.
4. Assign majority known-domain examples to `train`.
5. Hold out similar but unused examples as `seen_val`.
6. Assign in-domain but more varied examples to `unseen_val`.
7. Assign rare, difficult, edge-case, or cross-domain examples to `ood`.
8. Review criticality labels before running the experiment.

---

## 10. Assigning `is_critical`

`is_critical` indicates whether a wrong answer carries elevated operational, business, safety, legal, compliance, financial, or customer-impacting risk.

Allowed values:

```text
0 = normal prompt
1 = critical prompt
```

### 10.1 Use `is_critical = 0` When

A wrong answer is undesirable but not operationally dangerous.

Examples:

```csv
"The capital of France is","Paris",...,0,1.0
"The author of Hamlet is","Shakespeare",...,0,1.0
```

### 10.2 Use `is_critical = 1` When

A wrong answer could affect:

- security
- compliance
- legal obligations
- financial decisions
- production operations
- customer commitments
- safety-sensitive workflows
- executive reporting
- data privacy
- medical or regulated processes

Examples:

```csv
"The default HTTPS port is","443","technology_fact","unseen_val",1,1.5
"Kubernetes schedules workloads using","kube-scheduler","ood_fact","ood",1,2.0
```

---

## 11. Assigning `criticality_weight`

`criticality_weight` is a numeric multiplier representing the relative importance of the prompt.

It does not replace correctness checking. It helps the suite prioritize or interpret failures where business impact is higher.

### 11.1 Recommended Scale

| Prompt Type | `is_critical` | Recommended Weight | Intuition |
|---|---:|---:|---|
| Normal informational prompt | 0 | 1.0 | Standard evaluation importance. |
| Important business prompt | 1 | 1.5 | Wrong answer can create customer or operational friction. |
| High-risk prompt | 1 | 2.0 | Wrong answer may affect compliance, security, customer trust, or production operations. |
| Mission-critical prompt | 1 | 3.0 | Wrong answer could cause severe business, safety, legal, or regulatory impact. Use sparingly. |

### 11.2 Safe Default

If unsure, start with:

```csv
is_critical = 0
criticality_weight = 1.0
```

Then increase values only for prompts where wrong answers have higher impact.

### 11.3 Practical Assignment Examples

| Prompt Example | Suggested `is_critical` | Suggested Weight | Reason |
|---|---:|---:|---|
| General geography fact | 0 | 1.0 | Low operational risk. |
| Internal product feature description | 0 or 1 | 1.0–1.5 | Depends on customer-facing impact. |
| Security control or protocol fact | 1 | 1.5–2.0 | Security misinformation can be risky. |
| Regulatory retention requirement | 1 | 2.0–3.0 | Compliance failure risk. |
| Production outage procedure | 1 | 2.0–3.0 | Operational risk is high. |

---

## 12. Dataset Validation Behavior

When `--dataset` is supplied, validation should occur before model loading.

The run should halt if:

- file does not exist
- extension is not `.csv`
- required columns are missing
- required fields are blank
- `id` is not an integer
- `id` values are duplicated
- `split` is not one of `train`, `seen_val`, `unseen_val`, `ood`
- any required split is missing
- `is_critical` is not `0` or `1`
- `criticality_weight` is not numeric
- `prompt` or `target` is empty

### 12.1 Expected Invalid Dataset Error Shape

```text
ERROR: Invalid dataset file format.

Reason:
- Missing required column: target

Expected CSV format:
id,prompt,target,task_type,split,is_critical,criticality_weight

Sample compliant dataset:
<8-row sample CSV>

Why this format is required:
train is used for adaptation or training-related paths; seen_val measures preservation on familiar validation patterns; unseen_val measures generalization within the expected domain; ood measures broader deployment risk under harder or different prompts.

Execution halted before model loading or experiment execution.
```

---

## 13. Baseline-Only Report

The baseline-only report is generated when running:

```bash
python pcrf_transformer_reliability_suite.py baseline
```

or:

```bash
python pcrf_transformer_reliability_suite.py baseline --dataset customer_prompts.csv
```

### 13.1 Expected Sections

The updated baseline report should include:

1. Execution Mode
2. Dataset Source
3. Dataset Partition Counts
4. Baseline Metrics
5. Baseline Prompt / Generation Hallucination Audit

### 13.2 Baseline Prompt / Generation Hallucination Audit

This table exposes row-level baseline behavior.

Expected columns:

```markdown
| ID | Split | Prompt | Baseline Generation | Expected Value | Actual Value | Match? | Hallucinated? |
```

### 13.3 Hallucination Rule for Baseline Report

For baseline-only reporting:

```text
Hallucinated = YES when generated output does not semantically match the expected target.
```

In code terms:

```python
evaluate_semantic_match(generated_output, expected_target) == False
```

This makes the baseline report useful as a pre-PCRF exposure view:

> “Before PCRF governance, these were the prompts where the baseline generated an actual value that did not match the expected target.”

---

## 14. Executive Report Overview

The full experiment generates an executive report intended for customer-facing and patent-review-safe interpretation.

The executive report should be read as a reliability-governance report, not only as a model-performance report.

### 14.1 How to Read the Executive Report

Read it in this order:

1. Customer Executive Summary Box
2. Core Gating Status
3. Hallucination Risk and Exposure Control Section
4. Metrics at a Glance
5. Promotion Decision Evidence
6. Protected Router Benefit Accounting
7. Transition Analysis
8. Failure Taxonomy
9. Metric Confidence / Sample Size Context
10. Blueprint Files / Developer Next Steps

This ordering keeps the narrative focused on hallucination detection, safe routing, confidence calibration, and deployment governance.

---

## 15. Executive Report Metrics — Intuition and Usage

### 15.1 Seen Validation Accuracy

Measures correctness on validation examples close to the training distribution.

How to interpret:

- Stable seen accuracy suggests no major loss on familiar patterns.
- Drop in seen accuracy may indicate over-steering, forgetting, or unsafe adaptation.
- Improvement is useful but should not be the primary PCRF claim.

How to use:

- Use as a non-regression indicator.
- Do not use alone to justify production promotion.

### 15.2 Unseen Validation Accuracy

Measures correctness on in-domain examples not used during training.

How to interpret:

- Improvement can suggest better generalization.
- Drop can signal poor transfer or overfitting.
- Stable but low unseen accuracy may indicate the model still needs training data or better domain grounding.

How to use:

- Use with hallucination exposure metrics and NLL/PPL.
- Avoid claiming broad generalization if sample size is small.

### 15.3 Negative Log-Likelihood (NLL)

NLL measures how much probability the model assigns to the expected target sequence. Lower is better.

Intuition:

- Lower NLL means the model finds the expected target more probable.
- Higher NLL means the model struggles to assign probability mass to the target.

How to use:

- If accuracy is unchanged but NLL improves, the model may be becoming more confident toward the correct target even before exact-match improvements appear.
- If NLL worsens while accuracy improves, inspect for overconfidence, formatting artifacts, or shortcut learning.

### 15.4 Perplexity (PPL)

Perplexity is derived from NLL and is also lower-is-better.

Intuition:

- Lower PPL indicates the expected output is less surprising to the model.
- High PPL suggests uncertainty or poor alignment with expected target text.

How to use:

- Use PPL as a readability-friendly view of NLL.
- Do not treat PPL alone as a hallucination metric.

### 15.5 Strict Exact Match

Checks whether the generated answer exactly matches the expected target after strict normalization.

Intuition:

- Useful for cloze-style tasks where only the target answer should be generated.
- Penalizes extra words, formatting leakage, or over-generation.

How to use:

- Use to evaluate instruction compliance.
- If semantic capture is high but strict EM is low, the model may know the answer but violates the output contract.

### 15.6 First-Token Match

Checks whether the first generated token or first answer unit aligns with the expected target.

Intuition:

- Useful when early-token behavior matters.
- Helps identify whether the model starts correctly but then over-generates.

How to use:

- Combine with strict EM and instruction violation metrics.
- Strong first-token match with poor strict EM usually means formatting or continuation control issues.

### 15.7 Semantic Capture

Checks whether the expected target is semantically captured in the generated output.

Intuition:

- More relaxed than strict exact match.
- Useful for determining whether the model got the core answer right.

How to use:

- If semantic capture is good but strict EM is poor, prioritize output contract enforcement.
- If semantic capture is poor, treat it as target failure or hallucination exposure.

### 15.8 Instruction Violation

Detects whether output violates the expected answer format, such as producing multiple words when only one target is expected.

Intuition:

- The answer may contain the target but still be unusable in production because it violates the contract.

How to use:

- High instruction violation means developers should focus on decoding constraints, prompt contracts, output parsers, or contrastive formatting suppression.

### 15.9 Hallucination Exposure Control Rate

Measures the percentage of baseline hallucination cases that were controlled through repair, withholding, abstention, or safe routing.

Intuition:

- This is one of the most important PCRF narrative metrics.
- It reflects exposure control rather than raw accuracy improvement.

How to use:

- Use this in customer messaging to explain governance value.
- Avoid phrasing it as “accuracy improved by X%.”
- Prefer: “X% of baseline hallucination exposures were controlled through safe routing or withholding.”

### 15.10 Total Baseline Hallucinations Found

Counts baseline validation cases where baseline failed to capture the expected semantic target.

Intuition:

- Establishes the pre-PCRF exposure surface.

How to use:

- Use as the denominator for hallucination exposure control.
- Review row-level examples to understand failure pattern.

### 15.11 Active Semantic Target Recoveries

Counts cases where the candidate recovered the expected target when baseline failed.

Intuition:

- Indicates potential repair opportunities.

How to use:

- Do not automatically treat all recoveries as production-safe.
- Check strict EM and instruction contract first.

### 15.12 Contract-Clean Repairs Promoted

Counts baseline failures repaired by candidate where the candidate output also satisfied strict contract requirements.

Intuition:

- This is stronger than semantic recovery.
- It means the candidate produced a usable target-aligned answer under output constraints.

How to use:

- These are the safest repair examples to showcase.
- Still validate sample size and domain coverage before broad claims.

### 15.13 Semantic Recoveries Withheld for Contract

Counts cases where candidate captured the answer but violated format or strict output requirements.

Intuition:

- The model may know the target but is not deployment-safe for strict answer contracts.

How to use:

- Developers should inspect prompt formatting, decoder constraints, and output validation.

### 15.14 Candidate Over-Steers Prevented

Counts cases where candidate behavior was worse or riskier and the router prevented unsafe promotion.

Intuition:

- Shows non-regression protection.

How to use:

- Use this to explain why PCRF should be a protected governance layer rather than blind model replacement.

### 15.15 Catastrophic Regressions Blocked

Counts cases where baseline was correct but candidate failed and protected routing avoided serving the candidate.

Intuition:

- Strong safety indicator.

How to use:

- High count means direct candidate promotion is risky.
- Router or measurement-only deployment may be safer.

### 15.16 Transition Types

The transition table usually includes:

| Transition | Meaning |
|---|---|
| Correct → Correct | Baseline and candidate both captured target. |
| Correct → Wrong | Candidate regressed from a correct baseline. |
| Wrong → Correct | Candidate repaired a baseline failure. |
| Wrong → Wrong | Persistent failure across both paths. |

How to use:

- `Wrong → Correct` supports repair potential.
- `Correct → Wrong` supports router protection need.
- `Wrong → Wrong` supports abstain/safe fallback narrative.
- `Correct → Correct` supports non-regression stability.

### 15.17 Structural Reliability Metrics

Structural reliability metrics estimate representation stability across layers or modules.

Common interpretations:

- Lower reliability may indicate fragile or drift-prone layers.
- High layer sensitivity may indicate intervention risk.
- Bottleneck layers may require careful damping or guarded adaptation.

How to use:

- Do not use structural metrics alone to claim model quality.
- Use them to guide safe developer interventions, layer selection, and blueprint usage.

### 15.18 Birnbaum / Layer Sensitivity Metrics

Layer sensitivity metrics identify components whose perturbation has higher downstream effect.

Intuition:

- Sensitive layers can have large impact if modified.
- They may be candidates for careful intervention or for protection from aggressive updates.

How to use:

- Use for parameter-group learning-rate damping.
- Use for adapter placement decisions.
- Use for safe regularization planning.

### 15.19 Promotion Decision Evidence

This section explains whether direct candidate model adoption is safe, unsafe, or measurement-only.

How to interpret:

- Passing one metric is not enough.
- Promotion depends on non-regression, hallucination control, NLL/PPL behavior, contract compliance, and sample-size confidence.

How to use:

- If direct promotion fails, use safe components only.
- If measurement-only, do not deploy direct weights; use diagnostics, reports, or router insights.

### 15.20 Metric Confidence / Sample Size Context

This section calibrates how strong the claims can be.

Intuition:

- Small validation datasets can show directional evidence but not strong statistical proof.

How to use:

- For customer or patent-facing claims, keep wording calibrated.
- Use larger validation sets for stronger conclusions.

---

## 16. Understanding Safe, Unsafe, and Measurement-Only Components

The executive report may classify components into categories.

### 16.1 Safe Diagnostic Components

These can typically be used for analysis, reporting, and developer guidance.

Examples may include:

- hallucination risk scoring
- row-level failure taxonomy
- structural diagnostics
- confidence calibration analysis
- router outcome analysis

Use these to understand model behavior and plan improvements.

### 16.2 Unsafe Components

Unsafe components should not be directly promoted or deployed without more validation.

Examples may include:

- candidate weights that regress on seen validation
- interventions that increase hallucination exposure
- outputs that violate strict instruction contracts

Use these as warnings and investigation priorities.

### 16.3 Measurement-Only Components

Measurement-only means the component is useful for diagnostics but not approved for production enforcement in the current run.

Use these for:

- analysis
- research evidence
- future experiment planning
- controlled canary design

Do not present measurement-only components as production-enabled.

---

## 17. Blueprint Markdown Files

The experiment may generate blueprint markdown files that help developers act on safe areas identified by the executive report.

These blueprints are intended as next-step engineering guides, not automatic deployment approvals.

### 17.1 Parameter-Scale / Learning-Rate Damping Blueprint

Use when the executive report shows sensitive layers, unstable structural reliability, or high empirical derivative impact.

Purpose:

- create layer-wise parameter groups
- damp learning rates for sensitive layers
- reduce representation drift
- avoid over-steering

How developers should use it:

1. Open the blueprint markdown.
2. Identify the referenced CSV or layer sensitivity source.
3. Review selected bottleneck layers.
4. Apply damping logic in a controlled training branch.
5. Re-run full experiment.
6. Confirm no increase in regressions or hallucination exposure.

### 17.2 Curriculum / Dataset Filtration Blueprint

Use when failures cluster around certain prompts, task types, critical prompts, or hallucination categories.

Purpose:

- prioritize difficult examples
- oversample high-risk prompts
- build replay buffers
- strengthen validation around failure modes

How developers should use it:

1. Inspect failure taxonomy and row-level trace.
2. Identify repeated failure categories.
3. Use criticality-weighted sampling if appropriate.
4. Add targeted examples to train or validation splits.
5. Keep seen/unseen/OOD separation intact.
6. Re-run baseline and full modes.

### 17.3 API Guard / Representation Tracking Blueprint

Use when the executive report suggests the router or representation monitoring is safer than direct model promotion.

Purpose:

- inspect hidden-space stability
- detect high-risk inputs
- route or abstain when reliability is low
- prevent unsafe generated answers from being served

How developers should use it:

1. Treat it as a canary or guardrail design.
2. Integrate only in non-production or controlled environments first.
3. Define thresholds from validation runs, not guesses.
4. Log abstentions and withheld outputs.
5. Re-evaluate on larger datasets.

### 17.4 CDL / Regularization Blueprint

Use when the report indicates candidate improvement potential but also shows drift or regression risk.

Purpose:

- anchor candidate model to reference baseline
- penalize risky drift
- apply reliability-weighted training constraints
- reduce catastrophic regressions

How developers should use it:

1. Confirm the executive report does not approve direct blind promotion.
2. Use CDL as a controlled training strategy.
3. Apply small learning rates and drift penalties.
4. Validate against seen, unseen, and OOD splits.
5. Promote only if gating evidence improves.

---

## 18. How to Decide Developer Next Steps from Executive Report

Use this mapping:

| Executive Report Signal | Developer Next Step |
|---|---|
| High baseline hallucination count | Improve dataset coverage and enable baseline exposure reporting. |
| High hallucination exposure control rate | Consider router/abstain workflow as governance value. |
| Many wrong → correct transitions | Investigate candidate repair potential. |
| Many correct → wrong transitions | Do not directly promote candidate; use router or further regularization. |
| Many wrong → wrong transitions | Use abstain/safe fallback; add training data or retrieval grounding. |
| High instruction violation | Improve output contract, decoding, prompt format, or parser. |
| High layer sensitivity | Use learning-rate damping or adapter placement blueprint. |
| Weak sample confidence | Increase validation set size before strong customer claims. |
| Measurement-only recommendation | Use diagnostics, not production enforcement. |
| Unsafe component listed | Block promotion until issue is resolved and revalidated. |

---

## 19. Recommended Customer-Facing Interpretation

Use neutral, evidence-bound wording.

Preferred language:

> The run identified baseline hallucination exposure cases and measured how PCRF governance components controlled, withheld, routed, or diagnosed those risks.

Avoid:

> PCRF improves accuracy by X%.

Preferred:

> PCRF provided hallucination exposure visibility and guarded routing behavior under the measured validation conditions.

Avoid:

> The model is now safe for all production use.

Preferred:

> The artifacts identify safe diagnostic components and any components requiring further validation before production use.

---

## 20. Recommended Workflow for Developers

### Step 1 — Run Baseline

```bash
python pcrf_transformer_reliability_suite.py baseline --dataset customer_prompts.csv
```

Review:

- baseline metrics
- row-level hallucination audit table
- mismatch cases
- critical prompt failures

### Step 2 — Run Full PCRF Experiment

```bash
python pcrf_transformer_reliability_suite.py full --dataset customer_prompts.csv
```

Review:

- executive summary
- hallucination exposure control
- transition analysis
- promotion decision evidence
- blueprint files

### Step 3 — Compare Baseline vs Full

Ask:

- Which baseline hallucinations were detected?
- Which were repaired?
- Which were withheld?
- Which remained unresolved?
- Did candidate introduce regressions?
- Did router prevent regressions?

### Step 4 — Apply Blueprint Guidance

Use only safe or measurement-approved blueprints.

Do not deploy unsafe components.

### Step 5 — Increase Validation Strength

For customer or patent-facing claims:

- increase validation dataset size
- include more critical prompts
- include realistic OOD prompts
- preserve train/seen/unseen/OOD separation
- compare repeated runs if stochastic behavior is enabled

---

## 21. Common Mistakes to Avoid

### Mistake 1 — Treating PCRF as Pure Accuracy Tuning

PCRF should be framed as reliability governance, not generic accuracy optimization.

### Mistake 2 — Using Only Easy Validation Prompts

If validation prompts are too easy, hallucination exposure may be underestimated.

### Mistake 3 — Mixing Train and Validation Rows

Do not duplicate the same prompt across train and validation splits.

### Mistake 4 — Marking Everything Critical

If every row is critical, the criticality signal loses prioritization value.

### Mistake 5 — Ignoring Contract Violations

A semantically correct answer can still be unusable if it violates strict output requirements.

### Mistake 6 — Promoting Candidate Weights Despite Regressions

If `correct → wrong` cases exist, direct promotion requires strong caution.

### Mistake 7 — Overstating Small-Sample Findings

Small validation sets support directional findings, not broad statistical proof.

---

## 22. Troubleshooting

### 22.1 Dataset Fails Validation

Check:

- exact header spelling
- `.csv` extension
- non-empty prompt and target
- unique integer IDs
- valid split values
- at least one row per split
- `is_critical` is 0 or 1
- `criticality_weight` is numeric

### 22.2 Baseline Report Has No Row-Level Table

Confirm that you are using the updated codebase and running:

```bash
python pcrf_transformer_reliability_suite.py baseline
```

or:

```bash
python pcrf_transformer_reliability_suite.py baseline --dataset customer_prompts.csv
```

### 22.3 Full Mode Runs When No Mode Is Supplied

This is expected.

```bash
python pcrf_transformer_reliability_suite.py
```

is equivalent to:

```bash
python pcrf_transformer_reliability_suite.py full
```

### 22.4 External Dataset Is Ignored

Confirm that you passed:

```bash
--dataset customer_prompts.csv
```

and that the file passed validation.

### 22.5 Output Claims Look Too Strong

Use the metric confidence and promotion decision evidence sections to calibrate language. Avoid broad production claims from small validation samples.

---

## 23. Minimal Customer Dataset Template

```csv
id,prompt,target,task_type,split,is_critical,criticality_weight
101,"<customer prompt>","<expected answer>","<category>","train",0,1.0
102,"<customer prompt>","<expected answer>","<category>","train",0,1.0
201,"<customer prompt>","<expected answer>","<category>","seen_val",0,1.0
202,"<customer prompt>","<expected answer>","<category>","seen_val",0,1.0
301,"<customer prompt>","<expected answer>","<category>","unseen_val",1,1.5
302,"<customer prompt>","<expected answer>","<category>","unseen_val",1,1.5
401,"<customer prompt>","<expected answer>","<category>","ood",1,2.0
402,"<customer prompt>","<expected answer>","<category>","ood",1,2.0
```

---

## 24. Summary

This experiment should be used as a reliability-governance workflow:

1. Establish baseline hallucination exposure.
2. Run full PCRF diagnostics and governed routing.
3. Interpret executive metrics as safety and reliability evidence.
4. Use blueprint markdown files for developer next steps.
5. Avoid overstated accuracy claims.
6. Scale validation before customer-wide or production-wide claims.

The strongest customer narrative is:

> The PCRF suite identifies baseline hallucination exposure, measures reliability-sensitive failure modes, prevents unsafe candidate regressions through guarded routing, and generates actionable blueprints for safe engineering follow-up.
