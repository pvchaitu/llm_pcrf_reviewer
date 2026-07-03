# PCRF Transformer Reliability Executive Report
**Causal Reliability Flow & Derivative-Weighted Diagnostics Dashboard**

---


### 📦 Customer Executive Summary

- **What Happened?**  
  The candidate model's Seen Validation exact-match accuracy was regressed by -1.60 percentage points, while the Unseen Validation Generalization accuracy was regressed by -1.60 percentage points.  

- **Likelihood & Confidence Behavior:**  
  Generalization Negative Log-Likelihood (NLL) improved (decreased) by 0.1463, and Perplexity (PPL) improved (decreased) by 4.47.  

- **Why was Direct Adoption Accepted/Rejected?**  
  Direct adoption was REJECTED (DO_NOT_PROMOTE_WEIGHTS) due to active safety and performance gate failures: Overall system chain reliability R_sys (37.45%) vs floor (75.0%).; Zero correct-to-wrong regressions required. Found 26 regressions.; Zero critical high-priority regressions required. Found 8 regressions.; Candidate instruction-contract violation rate (100.00%) must be below ceiling (10.0%).; Candidate strict EM (0.00%) must be above minimal floor (10.0%).; Seen accuracy drop (1.60%) vs non-inferiority margin (1.0%).; Unseen accuracy improvement (-1.60%) vs requirement (2.0%).; Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -1.60%)..  

- **What did PCRF Prove in This Run?**  
  PCRF demonstrated essential risk-containment and non-regression governance by intercepting 26 catastrophic output regression(s) and serving safe baseline fallbacks.  

  - **PCRF Hallucination Exposure Control:** 100.00% of 91 baseline hallucination/target-failure cases were controlled through 91 protected router interventions.
  * Semantic target recoveries observed: `22`
  * Contract-clean repairs promoted to customer-facing output: `0`
  * Semantic recoveries withheld due to instruction-contract violations: `22`
  * Safe withhold/abstain decisions executed: `91`


---



---

## 1. Core Gating Status

* **Direct Candidate Weight Promotion Status:** `DO_NOT_PROMOTE_WEIGHTS`
* **Safe Diagnostic Components:** derivative diagnostics, curriculum curation, structural monitoring, protected routing
* **Unsafe Components:** direct weight promotion of optimized candidate weights
* **Measurement-Only Components:** candidate weights
* **PCRF Hallucination Exposure Control Governance:** Validation-time protected routing was exercised for measurement and safety analysis. Production enforcement is not enabled for this run.


---

## 3. Integrated PCRF Scoreboard

| Feature Track / Module | Baseline Value | PCRF Result Value | Track Score | Gating Status |
|---|---|---|---|---|
| Derivatives | 0.00 (Unmeasured) | 0.00769 (Avg Sensitivity) | 7.7/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=2.31) | 46.3/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 99.55% | 99.6/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen Acc: 39.2% | Unseen Acc: 37.6% | 52.0/100 | `DO_NOT_PROMOTE_WEIGHTS` |


---

## 4. Promotion Decision Evidence (Scoreboard Component Breakdown)

| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🔴 FAIL | CRITICAL | 37.45% | 75.00% | Overall system chain reliability R_sys (37.45%) vs floor (75.0%). |
| Correct-to-Wrong Regressions Count | 🔴 FAIL | CRITICAL | 26 | 0 | Zero correct-to-wrong regressions required. Found 26 regressions. |
| Critical High-Priority Regressions | 🔴 FAIL | CRITICAL | 8 | 0 | Zero critical high-priority regressions required. Found 8 regressions. |
| Universal Instruction Contract Violation Gate | 🔴 FAIL | CRITICAL | 100.00% | 10.00% | Candidate instruction-contract violation rate (100.00%) must be below ceiling (10.0%). |
| Generalization Non-Degradation Instruction Gate | 🟢 PASS | HIGH | 100.00% | 100.00% | Candidate instruction-contract violation rate (100.00%) must not exceed baseline (100.00%). |
| Strict EM Candidate Non-Degradation Gate | 🟢 PASS | HIGH | 0.00% | 0.00% | Candidate strict exact match (0.00%) must not degrade from baseline (0.00%). |
| Strict EM Absolute Direct Promotion Threshold | 🔴 FAIL | CRITICAL | 0.00% | 10.00% | Candidate strict EM (0.00%) must be above minimal floor (10.0%). |
| Hallucination Risk Trend Variance Gate | 🟢 PASS | HIGH | 3.24% | 5.00% | Average candidate risk increase (0.0324) must be within limit (0.0500). |
| Minimum Gating Evidence Verification Size | 🟢 PASS | HIGH | 250 | 100 | Validation examples count (250) vs strong claim requirement (100). |
| Seen Accuracy Non-Inferiority Margin | 🔴 FAIL | HIGH | 1.60% | 1.00% | Seen accuracy drop (1.60%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | 1.60% | 3.00% | Seen accuracy degradation (1.60%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🔴 FAIL | HIGH | -1.60% | 2.00% | Unseen accuracy improvement (-1.60%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🔴 FAIL | CRITICAL | -1.60% | 0.00% | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -1.60%). |


---

## 5. Hallucination Risk & Confidence Control (PRIMARY)

This section details baseline hallucinations, repairs promoted, and active over-steers prevented by PCRF.
PCRF reduces confidence on incorrect outputs rather than optimizing accuracy directly.

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `91` | Validation prompts where baseline failed to capture semantic target. |
| **Active Semantic Target Recoveries** | `22` | Raw semantic improvements found in the SFT candidate. |
| **Active Contract-Clean Repairs Promoted** | `0` | Baseline errors resolved cleanly and promoted with strict EM. |
| **Semantic Recoveries Withheld (Contract)**| `22` | Semantic target recovered, but withheld due to contract/EM violation. |
| **Candidate Over-Steers Prevented** | `69` | Both models failed, but candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `26` | Baseline was correct but candidate failed; router served baseline fallback. |
| **Hallucination Exposure Control Rate** | 100.00% | 91 of 91 baseline cases were either repaired by candidate or withheld. |
| **Net Gateway Interventions** | `117` | Overall cases actively guarded by the Protected Router (100% active coverage). |


---

### Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 0 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 42 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 53 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 155 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 0 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration regularization. |


*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 6. Protected Router Behavior & Safety Gating

The Protected Router functions as a safety control layer providing non-regression protection, safe baseline fallbacks, and validated repair promotions. It does not blindly optimize accuracy; instead, it prevents catastrophic production regression.

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `26` | Fallback to baseline on candidate failure |
| **Contract-Clean Repairs Promoted** | `0` | Upgrade to candidate on verified contract-clean repair |
| **Over-steers Prevented** | `69` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** The router successfully blocked 26 regression(s) where candidate degraded baseline correct outputs. This demonstrates safe containment control.
* **Generalization Repair:** No clean semantic repairs were promoted in this run.



---

### Dynamic Showcase Cases

#### Showcase Case 1: ID 303 (seen_val)
* **Operational Category:** Regression Blocked: Baseline was correct but candidate regressed; protected router successfully intervened.
* **Prompt:** *Seen Validation 103: The largest ocean is*
* **Expected Target:** `Pacific`
* **Outputs:** Baseline=`the Pacific Ocean, which covers about 7.8%` (Risk: 0.4157) | Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.4510)
* **Latent Telemetry:** Baseline Top-1 Prob: `17.19%` | Candidate Top-1 Prob: `16.50%` | Delta: `-0.0068`
* **Router Action:** `use_baseline` -> **Served Output:** `the Pacific Ocean, which covers about 7.8%`
* **Protected Router Decision Explanation:** *Candidate blocked because baseline captured the target and candidate failed.*

#### Showcase Case 2: ID 205 (seen_val)
* **Operational Category:** Persistent Failure Contained: Both models failed target capture; candidate was suppressed and baseline fallback served.
* **Prompt:** *Seen Validation 5: The author of Odyssey is*
* **Expected Target:** `Homer`
* **Outputs:** Baseline=`a Greek poet and playwright. A) True B) False` (Risk: 0.4007) | Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.4370)
* **Latent Telemetry:** Baseline Top-1 Prob: `8.25%` | Candidate Top-1 Prob: `6.54%` | Delta: `-0.0171`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `⚠️ Hallucination Risk Detected — Response Withheld for Safety`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.4370).*

#### Showcase Case 3: ID 201 (seen_val)
* **Operational Category:** Preserved Stricter Contract: Both captured semantic target, but candidate violated format constraints; baseline output served.
* **Prompt:** *Seen Validation 1: The capital of Germany is*
* **Expected Target:** `Berlin`
* **Outputs:** Baseline=`Berlin. <br><br>What is the next sentence?<br>Options are:` (Risk: 0.3342) | Candidate=`Berlin. <br><br>What would be an appropriate response to this statement` (Risk: 0.3456)
* **Latent Telemetry:** Baseline Top-1 Prob: `31.64%` | Candidate Top-1 Prob: `44.53%` | Delta: `+0.1289`
* **Router Action:** `use_baseline` -> **Served Output:** `Berlin. <br><br>What is the next sentence?<br>Options are:`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

#### Showcase Case 4: ID 215 (seen_val)
* **Operational Category:** Transition trace display for analysis (wrong_to_wrong).
* **Prompt:** *Seen Validation 15: The author of Odyssey is*
* **Expected Target:** `Homer`
* **Outputs:** Baseline=`a Greek poet and playwright. He was born in Athens,` (Risk: 0.4064) | Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.4426)
* **Latent Telemetry:** Baseline Top-1 Prob: `7.86%` | Candidate Top-1 Prob: `6.10%` | Delta: `-0.0176`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `⚠️ Hallucination Risk Detected — Response Withheld for Safety`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.4426).*



---

## 7. Contract Compliance (Instruction Adherence)

This section highlights instruction contract violations and formatting failures. Strict output constraint enforcement guarantees enterprise output determinism.

### Failed Generations Debug Trace Table

The following trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | Candidate Output | Baseline NLL |
|---|---|---|---|---|---|---|
| seen_val | 205 | *Seen Validation 5: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.4375 |
| seen_val | 215 | *Seen Validation 15: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.4844 |
| seen_val | 235 | *Seen Validation 35: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 4.0938 |
| seen_val | 255 | *Seen Validation 55: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 4.1875 |
| seen_val | 265 | *Seen Validation 65: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 4.7500 |
| seen_val | 270 | *Seen Validation 70: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 5.0312 |
| seen_val | 275 | *Seen Validation 75: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 4.6562 |
| seen_val | 280 | *Seen Validation 80: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 5.2812 |
| seen_val | 285 | *Seen Validation 85: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 4.6875 |
| seen_val | 290 | *Seen Validation 90: The author of Odyssey is* | `Homer` | `a man who has been in the b...` | `⚠️ Hallucination Risk Detec...` | 5.4062 |
| ... | ... | ... | ... | ... | ... | *(And 107 more trace details)* |



---

## 8. Structural Reliability (PCRF Structural / CREW)

### Structural Reliability Model Reconciliation

To ensure mathematical rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `37.45%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `89.84%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `99.55%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.87%` (Gate Role: localized adapter targeting signal)

> ⚠️ **Mathematical Caveat (Bypass-Dominated):** Strict chain reliability appears stable under this measurement, but CREW submodule decomposition is residual-bypass dominated. Attention and MLP causal paths require separate validation before structural metrics can be treated as promotion-grade.



---

## Bottleneck Selection & Layer Causal Flow Matrix

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 1, 2, 3, 21, 22, 23`
* **Highest Empirical Sensitivity Layer:** Layer `0` (Empirical Delta: `0.03759`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `23` (Birnbaum Index: `0.65759`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom regularizer SFT parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.


---

## 9. Accuracy (SUPPORTING ONLY — secondary)

Accuracy changes reflect shifts in confidence distribution and ranking. These are secondary effects of reliability control and not primary optimization targets.

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Served Delta | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Validation NLL | Lower is Better ⬇️ | 3.1941 | 2.8972 | 3.1941 | -0.2969 | +0.0000 | Candidate: Candidate shifted confidence distribution (Lower) (-0.2969), Served: Unchanged (+0.0000). |
| Unseen Validation NLL | Lower is Better ⬇️ | 3.4913 | 3.3450 | 3.4913 | -0.1463 | +0.0000 | Candidate: Candidate shifted confidence distribution (Lower) (-0.1463), Served: Unchanged (+0.0000). |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 32.8272 | 28.3604 | 32.8272 | -4.4669 | +0.0000 | Candidate: Candidate shifted confidence distribution (Lower) (-4.4669), Served: Unchanged (+0.0000). |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 3.3427 | 3.1211 | 3.3427 | -0.2216 | +0.0000 | Candidate: Candidate shifted confidence distribution (Lower) (-0.2216), Served: Unchanged (+0.0000). |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | +0.00% | Candidate: Unchanged (+0.0000%), Served: Unchanged (+0.0000%). |
| Semantic Target Capture | Higher is Better ⬆️ | 63.60% | 62.00% | 63.60% | -1.60% | +0.00% | Candidate: Candidate shifted confidence distribution (Lower) (-0.0160%), Served: Unchanged (+0.0000%). |
| First-Token Target Match | Higher is Better ⬆️ | 30.00% | 30.00% | 30.00% | +0.00% | +0.00% | Candidate: Unchanged (+0.0000%), Served: Unchanged (+0.0000%). |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | +0.00% | Candidate: Confidence profile stable (+0.0000%), Served: Confidence profile stable (+0.0000%). |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 88.00% | 86.40% | 88.00% | -1.60% | +0.00% | Candidate: Observed ranking sensitivity under calibration (-0.0160%), Served: Confidence profile stable (+0.0000%). |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 39.20% | 37.60% | 39.20% | -1.60% | +0.00% | Candidate: Observed ranking sensitivity under calibration (-0.0160%), Served: Confidence profile stable (+0.0000%). |


---

| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `133` | `53.2%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `26` | `10.4%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `22` | `8.8%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `69` | `27.6%` | Persistent target failure across both configurations |


---

### Metric Confidence & Validation Sample Size Limits

* **Train Split Partition Count:** `200`
* **Seen Validation Split Count:** `125`
* **Unseen Validation Split Count:** `125`
* **Total Combined Validation Count:** `250`


### Paired Significance Context:
With smaller validation sets, discrete accuracy deltas must be interpreted as directional evidence rather than definitive proof of generalization. 
Enterprise deployments should scale validation spaces to larger evaluation corpuses to perform paired statistical tests.


---

### Dynamic Executive AI Governance Conclusion

Based on evidence compiled in this evaluation cycle, we draw the following conclusions:

* **Demonstrated Capabilities:** The candidate model demonstrated improved continuous likelihood metrics (NLL) but failed discrete accuracy non-inferiority or structural safety thresholds. Direct promotion of current weights is not safe.
* **Repairs Promoted:** No clean hallucination repairs were promoted in this run.
* **Router Safety:** The Protected Router successfully preserved baseline served accuracy by blocking 26 regressions.


---

### Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*
PASSED

⚠️ **Warning: Raw Hallucinated Output Leaks Detected in Report!**

* Raw baseline output for row 205 leaked: 'a Greek poet and playwright. A) True B) False'
* Raw baseline output for row 215 leaked: 'a Greek poet and playwright. He was born in Athens,'
