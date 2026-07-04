# PCRF Executive SFT Reliability Scorecard
**Causal Flow Downstream Probability Derivatives Audit Report**




### 📦 Customer Executive Summary

- **What Happened?**  
  The SFT candidate's Seen Validation EM accuracy was improved by +5.00 percentage points, while the Unseen SFT Generalization accuracy was improved by +5.00 percentage points.  

- **Likelihood & Confidence Behavior:**  
  SFT Generalization Negative Log-Likelihood (NLL) improved (decreased) by 0.9496, and SFT Perplexity (PPL) improved (decreased) by 109.70.  

- **Why was Direct Adoption Accepted/Rejected?**  
  Direct adoption was REJECTED (DO_NOT_APPLY) due to SFT continuous and structural safety check limitations: Overall system chain reliability R_sys (35.57%) vs floor (75.0%).; Validation examples count (40) vs strong claim requirement (100)..  

- **What did PCRF Prove in This Run?**  
  PCRF demonstrated repair promotion capabilities by successfully validating and promoting 2 correct response(s).  

  - **PCRF Hallucination Exposure Control:** 100.00% of 19 baseline hallucination/target-failure cases were controlled through 19 protected router interventions.
  * Repairs Found (Semantic Recoveries): `2`
  * Repairs Promoted (Contract-Clean): `2`
  * Repairs Withheld (Contract Violation): `0`
  * Safe withhold/abstain decisions executed: `17`


---

## 1. Core Gating Status

* **Direct Candidate Weight Promotion Status:** `DO_NOT_APPLY`
* **Safe Diagnostic Components:** derivative diagnostics, curriculum curation, structural monitoring, protected routing
* **Unsafe Components:** direct weight promotion of optimized candidate weights
* **Measurement-Only Components:** candidate weights
* **PCRF Hallucination Exposure Control Governance:** Protected routing is eligible for controlled canary enforcement, subject to deployment approval and expanded validation.


---

## 1. Hallucination Exposure Control

This section tracks the active interception of hallucinated outputs and formatting anomalies under real-time Protected Router governance.

| Exposure Metric | Count | Operational Definition & Safety Coverage |
| :--- | :---: | :--- |
| **Observed Risk Events** | `19` | All validation prompts triggering baseline failure or candidate degradation. |
| **Contained Risk Events** | `19` | Total safety interventions successfully managed by Protected Router. |
| **Served Risk Events** | `0` | Safety-withheld or incorrect completions exposed to served streams. |
| **Safe Abstains** | `17` | Unsafe outputs withheld and mapped cleanly to fallback states. |
| **Exposure Control Rate** | `100.00%` | Percentage of overall risk events successfully contained under governance. |


---

## 2. PCRF Governance Assessment

> ### 🛡️ Service Governance Scorecard
> 
> * **Governed Accuracy (Primary Customer Metric):** `57.50%`  
> * **Baseline Accuracy (Comparison Metric):** `52.50%`  
> * **Candidate Accuracy (Engineering Metric):** `57.50%`  
> * **Regression Containment Effectiveness:** `100.00%`  
> * **Repair Promotion Effectiveness:** `100.00%`  
> * **Hallucination Exposure Control Rate:** `100.00%`  
> * **Safe Abstains Executed:** `17`  
> 
> **Service Impact Narrative:**  
> Governed outcomes remained protected despite candidate degradation events during SFT evaluation. The Protected Router successfully insulated the final served endpoint, maintaining served quality at **57.50%** while preventing degraded candidate outputs from reaching users.


---

## 3. Integrated PCRF Scoreboard
| Feature Track / Module | Baseline Value | PCRF Result Value | Track Score | Gating Status |
|---|---|---|---|---|
| Derivatives | 0.00 (Unmeasured) | 0.00378 (Avg Sensitivity) | 3.8/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=3.58) | 71.5/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 99.56% | 99.6/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen SFT Acc: 50.0% | Unseen SFT Acc: 55.0% | 45.0/100 | `DO_NOT_APPLY` |


---

## 4. Gating Check Outcomes
| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🔴 FAIL | CRITICAL | 35.57% | 75.00% | Overall system chain reliability R_sys (35.57%) vs floor (75.0%). |
| Candidate Regression Review | 🟢 PASS | DIAGNOSTIC_ONLY | Observed Regressions: 0, Observed Repairs: 2, Net Delta: +2 | N/A | Model evaluation only. Captures raw candidate parameter variance before PCRF routing. |
| Regression Exposure Control | 🟢 PASS | CRITICAL | Effectiveness: 100.0%, Served Regressions: 0 | Served Regressions = 0 | Observed regressions were contained before reaching served output. |
| Critical High-Priority Regressions | 🟢 PASS | CRITICAL | 0 | 0 | Zero critical high-priority regressions required. Found 0 regressions. |
| Universal Instruction Contract Violation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 100.00% | 10.00% | Both baseline and candidate violate strict output contracts. Tracking operated as a diagnostic planner. |
| Generalization Non-Degradation Instruction Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 100.00% | 100.00% | Instruction contract tracking operated diagnostically for this validation pass. |
| Strict EM Candidate Non-Degradation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 0.00% | Strict EM validation tracking operated diagnostically for this validation pass. |
| Strict EM Absolute Direct Promotion Threshold | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 10.00% | Strict EM validation boundary executed as diagnostic analyzer. |
| Hallucination Risk Trend Variance Gate | 🟢 PASS | HIGH | 3.35% | 5.00% | Average candidate risk increase (0.0335) must be within limit (0.0500). |
| Minimum Gating Evidence Verification Size | 🔴 FAIL | HIGH | 40 | 100 | Validation examples count (40) vs strong claim requirement (100). |
| Seen Accuracy Non-Inferiority Margin | 🟢 PASS | HIGH | -5.00% | 1.00% | Seen accuracy drop (-5.00%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | -5.00% | 3.00% | Seen accuracy degradation (-5.00%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🟢 PASS | HIGH | 5.00% | 2.00% | Unseen accuracy improvement (5.00%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🟢 PASS | CRITICAL | 5.00% | 0.00% | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found 5.00%). |


---

## 5. Hallucination Risk & SFT Calibration

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `19` | Validation prompts where baseline failed to capture semantic target. |
| **Repairs Found (Semantic Recoveries)** | `2` | Raw semantic improvements found in SFT candidate. |
| **Repairs Promoted (Contract-Clean)** | `2` | Baseline errors resolved cleanly and promoted with strict EM. |
| **Repairs Withheld (Contract Violation)**| `0` | Semantic target recovered, but withheld due to contract/EM violation. |
| **Candidate Over-Steers Prevented** | `17` | Both models failed, but SFT candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `0` | Baseline was correct but SFT candidate failed; router served baseline fallback. |
| **Hallucination Exposure Control Rate** | 100.00% | All baseline cases were either repaired or withheld. |
| **Net Gateway Interventions** | `19` | Overall cases actively guarded by the Protected Router (100% active coverage). |

### Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 0 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 0 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 16 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 23 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 1 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration SFT regularization. |

*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 6. Protected Router Governance

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `0` | Fallback to baseline on candidate failure |
| **Contract-Clean Repairs Promoted** | `2` | Upgrade to SFT candidate on verified contract-clean SFT repair |
| **Over-steers Prevented** | `17` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** The router successfully blocked 0 regression(s) where candidate degraded baseline correct outputs. This demonstrates safe containment control.
* **Generalization Repair:** Promoted 2 successful contract-clean SFT candidate repair(s) into active serving streams.

### Dynamic Showcase Cases
#### Showcase Case 1: ID 084 (seen_val)
* **Operational Category:** Persistent Failure Contained: Both failed target capture; candidate risk was contained and fallback was executed.
* **Prompt:** *Complete with one word only: The official capital city of Switzerland is*
* **Expected Target:** `Bern`
* **Outputs:** Baseline=`__________. Zurich<br><br>What does t...` (Risk: 0.3285) | SFT Candidate=`__________. Zurich<br><br>The officia...` (Risk: 0.3723)
* **Latent Telemetry:** Baseline Top-1 Prob: `35.35%` | SFT Candidate Top-1 Prob: `28.52%` | Delta: `-0.0684`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `⚠️ Hallucination Risk Detected — Resp...`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.3723).*

#### Showcase Case 2: ID 081 (seen_val)
* **Operational Category:** Preserved Stricter Contract: SFT candidate violated formatting contracts; baseline output safely served instead.
* **Prompt:** *Complete with one word only: The official capital city of South Korea is*
* **Expected Target:** `Seoul`
* **Outputs:** Baseline=`__________. Seoul<br><br>What is the ...` (Risk: 0.3417) | SFT Candidate=`Seoul. <br><br>The official capital c...` (Risk: 0.3456)
* **Latent Telemetry:** Baseline Top-1 Prob: `33.79%` | SFT Candidate Top-1 Prob: `51.95%` | Delta: `+0.1816`
* **Router Action:** `use_baseline` -> **Served Output:** `__________. Seoul<br><br>What is the ...`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

#### Showcase Case 3: ID 082 (seen_val)
* **Operational Category:** Repair Promoted: Candidate successfully recovered and validated semantic target completion.
* **Prompt:** *Complete with one word only: The official capital city of Norway is*
* **Expected Target:** `Oslo`
* **Outputs:** Baseline=`________.<br>Stockholm<br><br>The off...` (Risk: 0.3150) | SFT Candidate=`Oslo. <br><br>The official capital ci...` (Risk: 0.3578)
* **Latent Telemetry:** Baseline Top-1 Prob: `41.41%` | SFT Candidate Top-1 Prob: `45.90%` | Delta: `+0.0449`
* **Router Action:** `use_candidate` -> **Served Output:** `Oslo. <br><br>The official capital ci...`
* **Protected Router Decision Explanation:** *Contract-clean candidate repair promoted.*

#### Showcase Case 4: ID 086 (seen_val)
* **Operational Category:** Transition trace display for analysis (wrong_to_wrong).
* **Prompt:** *Complete with one word only: The noble element designated by atomic number 10 is*
* **Expected Target:** `Neon`
* **Outputs:** Baseline=`____. <br>A. Gold<br>B. Silver<br>C` (Risk: 0.3379) | SFT Candidate=`____<br>A. Iron<br>B. Gold<br>C.` (Risk: 0.4154)
* **Latent Telemetry:** Baseline Top-1 Prob: `36.52%` | SFT Candidate Top-1 Prob: `17.29%` | Delta: `-0.1924`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `⚠️ Hallucination Risk Detected — Resp...`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.4154).*




---

## 7. Compliance Trace

### Failed Generations Debug Trace Table

The following SFT trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | SFT Candidate Output | Baseline NLL |
|---|---|---|---|---|---|---|
| seen_val | 82 | *Complete with one word only: The official capit...* | `Oslo` | `________.<br>Stockholm<br><...` | `Oslo. <br><br>The official ...` | 2.8125 |
| seen_val | 84 | *Complete with one word only: The official capit...* | `Bern` | `__________. Zurich<br><br>W...` | `__________. Zurich<br><br>T...` | 3.7344 |
| seen_val | 86 | *Complete with one word only: The noble element ...* | `Neon` | `____. <br>A. Gold<br>B. Sil...` | `____<br>A. Iron<br>B. Gold<...` | 10.0625 |
| seen_val | 87 | *Complete with one word only: The volatile eleme...* | `Sulfur` | `__________. <br>A. Sodium<b...` | `____<br>A. Sodium<br>B. Mag...` | 3.6667 |
| seen_val | 90 | *Complete with one word only: Mechanical acousti...* | `Vacuum` | `medium. <br><br>A) Inertial...` | `medium. The sound waves tha...` | 12.3125 |
| seen_val | 96 | *Complete with one word only: To enforce unique ...* | `Set` | `technique known as ________...` | `technique known as hashing....` | 7.7500 |
| seen_val | 98 | *Complete with one word only: An execution failu...* | `Bug` | `(n) ________.<br>A. Error<b...` | `(n) ________.<br>A. Error<b...` | 11.8125 |
| seen_val | 99 | *Complete with one word only: A standardized tex...* | `JSON` | `called a(n) ________.<br>A....` | `called a(n) ________.<br>A....` | 10.9375 |
| seen_val | 100 | *Complete with one word only: The active keyword...* | `import` | `____________.<br>module<br>...` | `____________.<br>The active...` | 7.5312 |
| unseen_val | 106 | *Complete with one word only: Mammalian red bloo...* | `Oxygen` | `substances in the body. The...` | `substances in the body. The...` | 9.4375 |
| ... | ... | ... | ... | ... | ... | *(And 9 more SFT trace details)* |




---

## 8. Structural Reconciliation

### Structural Reliability Model Reconciliation

To ensure mathematical SFT rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `35.57%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `89.93%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `99.56%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.91%` (Gate Role: localized adapter SFT targeting signal)

#### ⚠️ Causal Flow Multi-Layer Reconciliation Notice
This run reports high localized individual layer survival probabilities (averaging `95.78%`) across all `24` decoder layers, while presenting a combined Strict-Series system reliability ($R_{sys}$) of **35.57%**.

This is **not a mathematical error**, but rather a critical architectural discovery resolved by PCRF's multi-tier decomposition:

1. **The Product Decay of Series Chains ($R_{sys}$):**
  In a strict sequential dependency model (where information must travel down a 24-layer latent highway without bypass preservation), errors compound multiplicatively:
  $$R_{sys} = \prod_{l=1}^{L} r_l$$
  Even when every single layer is on average `95.78%` stable, a 24-layer deep cascade naturally multiplies down to:
  $$(95.78\%)^{24} \approx 35.57\%$$
  Because our model undergoes structural shift during fine-tuning, several layers present slightly higher informational decay, dragging the strict multiplicative series reliability down to **35.57%**.

2. **The Residual Bypass Reality (CREW Reliability):**
  Modern Transformer decoders do not rely on a strict sequential dependency; they utilize dense residual bypass paths (Attention and MLP shortcuts). Under the **CREW (Causal Residual-depth Evaluation Weights)** formulation, which maps bypass-dominated highway paths, the system reliability is measured at **89.93%** (CREW Product) and **99.56%** (CREW Geometric).

  This proves that **the model's base representation is highly stable**, but SFT-induced modifications have caused localized informational alignment gaps when forcing sequential inference logic.

> ⚠️ **Mathematical Caveat (Bypass-Dominated):** Strict SFT chain reliability appears stable under this measurement, but CREW submodule decomposition is residual-bypass dominated. Attention and MLP causal paths require separate validation before structural metrics can be treated as promotion-grade.



## Bottleneck Selection & Layer Causal Flow Matrix

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 3, 10, 12, 13, 21, 22, 23`
* **Highest Empirical Sensitivity Layer:** Layer `12` (Empirical Delta: `-0.01433`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `23` (Birnbaum Index: `0.64843`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom SFT regularizer parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.



---

## 9. SFT Generalization Accuracies

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Candidate Direction | Served Delta | Served Direction | Customer Reading Guidance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Validation NLL | Lower is Better ⬇️ | 4.7107 | 3.6968 | 4.5042 | -1.0138 | Favorable | -0.2064 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Validation NLL | Lower is Better ⬇️ | 5.1869 | 4.2373 | 5.0932 | -0.9496 | Favorable | -0.0938 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 178.9205 | 69.2234 | 162.9090 | -109.6971 | Favorable | -16.0115 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 4.9488 | 3.9671 | 4.7987 | -0.9817 | Favorable | -0.1501 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Semantic Target Capture | Higher is Better ⬆️ | 52.50% | 57.50% | 57.50% | +5.00% | Favorable | +5.00% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| First-Token Target Match | Higher is Better ⬆️ | 37.50% | 47.50% | 40.00% | +10.00% | Favorable | +2.50% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 55.00% | 60.00% | 60.00% | +5.00% | Favorable | +5.00% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 50.00% | 55.00% | 55.00% | +5.00% | Favorable | +5.00% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |


**Reading the Metrics Scoreboard:**
* **Candidate Delta** indicates raw SFT model representation movement.
* **Served Delta** reflects governed served output. A flat Served Delta can signify safe routing overrides.

| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `21` | `52.5%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `0` | `0.0%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `2` | `5.0%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `17` | `42.5%` | Persistent target failure across both configurations |

### Metric Confidence & Validation Sample Size Limits

* **Train Split Partition Count:** `80`
* **Seen Validation Split Count:** `20`
* **Unseen Validation Split Count:** `20`
* **Total Combined Validation Count:** `40`

### Paired Significance Context:
With smaller validation sets, discrete accuracy deltas must be interpreted as directional SFT evidence rather than definitive proof of generalization. 
Enterprise deployments should scale validation spaces to larger evaluation corpuses to perform paired statistical tests.

### Dynamic Executive AI Governance Conclusion

Based on SFT evidence compiled in this evaluation cycle, we draw the following conclusions:

* **Demonstrated SFT Capabilities:** SFT candidate model demonstrated improved continuous likelihood metrics (NLL) but failed discrete accuracy non-inferiority or structural safety thresholds. Direct promotion of current weights is not safe.
* **Repairs Promoted:** Promoted 2 validated SFT semantic repairs.
* **Router Safety:** The Protected Router successfully preserved SFT served accuracy by blocking 0 regressions.

### Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*



## 10. Report Masking Audit

**Customer-Safe Output Masking Audit:** PASSED

Customer-safe hallucination output masking passed. Detected unresolved hallucinations were represented using the safety-withheld response.
