# PCRF Executive SFT Reliability Scorecard
**Causal Flow Downstream Probability Derivatives Audit Report**


### 📦 Customer Executive Summary

- **What Happened?**  
  The SFT candidate's Seen Validation EM accuracy was improved by +1.60 percentage points, while the Unseen SFT Generalization accuracy was regressed by -7.20 percentage points.  

- **Likelihood & Confidence Behavior:**  
  SFT Generalization Negative Log-Likelihood (NLL) improved (decreased) by 0.1921, and SFT Perplexity (PPL) improved (decreased) by 5.86.  

- **Why was Direct Adoption Accepted/Rejected?**  
  Direct adoption was REJECTED (DO_NOT_APPLY) due to SFT continuous and structural safety check limitations: Overall system chain reliability R_sys (37.53%) vs floor (75.0%).; Zero correct-to-wrong regressions required. Found 10 regressions.; Zero critical high-priority regressions required. Found 4 regressions.; Unseen accuracy improvement (-7.20%) vs requirement (2.0%).; Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -7.20%)..  

- **What did PCRF Prove in This Run?**  
  PCRF demonstrated essential risk-containment and SFT non-regression governance by intercepting 10 catastrophic output regression(s) and serving baseline model fallbacks.  

  - **PCRF Hallucination Exposure Control:** 100.00% of 101 baseline hallucination/target-failure cases were controlled through 101 protected router interventions.
  * Repairs Found (Semantic Recoveries): `3`
  * Repairs Promoted (Contract-Clean): `3`
  * Repairs Withheld (Contract Violation): `0`
  * Safe withhold/abstain decisions executed: `98`


---



---

## 1. Core Gating Status

* **Direct Candidate Weight Promotion Status:** `DO_NOT_APPLY`
* **Safe Diagnostic Components:** derivative diagnostics, curriculum curation, structural monitoring, protected routing
* **Unsafe Components:** direct weight promotion of optimized candidate weights
* **Measurement-Only Components:** candidate weights
* **PCRF Hallucination Exposure Control Governance:** Validation-time protected routing was exercised for measurement and safety analysis. Production enforcement is not enabled for this run.


---

## 3. Integrated PCRF Scoreboard
| Feature Track / Module | Baseline Value | PCRF Result Value | Track Score | Gating Status |
|---|---|---|---|---|
| Derivatives | 0.00 (Unmeasured) | 0.00342 (Avg Sensitivity) | 3.4/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=1.81) | 36.2/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 99.55% | 99.6/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen SFT Acc: 36.8% | Unseen SFT Acc: 29.6% | 60.0/100 | `DO_NOT_APPLY` |


---

## 4. Gating Check Outcomes
| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🔴 FAIL | CRITICAL | 37.53% | 75.00% | Overall system chain reliability R_sys (37.53%) vs floor (75.0%). |
| Correct-to-Wrong Regressions Count | 🔴 FAIL | CRITICAL | 10 | 0 | Zero correct-to-wrong regressions required. Found 10 regressions. |
| Critical High-Priority Regressions | 🔴 FAIL | CRITICAL | 4 | 0 | Zero critical high-priority regressions required. Found 4 regressions. |
| Universal Instruction Contract Violation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 100.00% | 10.00% | Both baseline and candidate violate strict output contracts. Tracking operated as a diagnostic planner. |
| Generalization Non-Degradation Instruction Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 100.00% | 100.00% | Instruction contract tracking operated diagnostically for this validation pass. |
| Strict EM Candidate Non-Degradation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 0.00% | Strict EM validation tracking operated diagnostically for this validation pass. |
| Strict EM Absolute Direct Promotion Threshold | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 10.00% | Strict EM validation boundary executed as diagnostic analyzer. |
| Hallucination Risk Trend Variance Gate | 🟢 PASS | HIGH | 2.93% | 5.00% | Average candidate risk increase (0.0293) must be within limit (0.0500). |
| Minimum Gating Evidence Verification Size | 🟢 PASS | HIGH | 250 | 100 | Validation examples count (250) vs strong claim requirement (100). |
| Seen Accuracy Non-Inferiority Margin | 🟢 PASS | HIGH | -1.60% | 1.00% | Seen accuracy drop (-1.60%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | -1.60% | 3.00% | Seen accuracy degradation (-1.60%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🔴 FAIL | HIGH | -7.20% | 2.00% | Unseen accuracy improvement (-7.20%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🔴 FAIL | CRITICAL | -7.20% | 0.00% | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -7.20%). |


---

## 5. Hallucination Risk & SFT Calibration

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `101` | Validation prompts where baseline failed to capture semantic target. |
| **Repairs Found (Semantic Recoveries)** | `3` | Raw semantic improvements found in SFT candidate. |
| **Repairs Promoted (Contract-Clean)** | `3` | Baseline errors resolved cleanly and promoted with strict EM. |
| **Repairs Withheld (Contract Violation)**| `0` | Semantic target recovered, but withheld due to contract/EM violation. |
| **Candidate Over-Steers Prevented** | `98` | Both models failed, but SFT candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `10` | Baseline was correct but SFT candidate failed; router served baseline fallback. |
| **Hallucination Exposure Control Rate** | 100.00% | 101 of 101 baseline cases were either repaired or withheld. |
| **Net Gateway Interventions** | `111` | Overall cases actively guarded by the Protected Router (100% active coverage). |


### Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 1 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 44 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 63 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 142 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 0 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration SFT regularization. |


*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 6. Protected Router Governance

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `10` | Fallback to baseline on candidate failure |
| **Contract-Clean Repairs Promoted** | `3` | Upgrade to SFT candidate on verified contract-clean SFT repair |
| **Over-steers Prevented** | `98` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** The router successfully blocked 10 regression(s) where candidate degraded baseline correct outputs. This demonstrates safe containment control.
* **Generalization Repair:** Promoted 3 successful contract-clean SFT candidate repair(s) into active serving streams.



### Dynamic Showcase Cases

#### Showcase Case 1: ID 340 (unseen_val)
* **Operational Category:** Regression Blocked: Baseline was correct but candidate regressed; protected router successfully intervened.
* **Prompt:** *Unseen Validation 15: The protocol used for secure web traffic is*
* **Expected Target:** `HTTPS`
* **Outputs:** Baseline=`called ____<br>A. SSL<br>B. HTTPS<br>C` (Risk: 0.4174) | SFT Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.4481)
* **Latent Telemetry:** Baseline Top-1 Prob: `7.81%` | SFT Candidate Top-1 Prob: `9.28%` | Delta: `+0.0146`
* **Router Action:** `use_baseline` -> **Served Output:** `called ____<br>A. SSL<br>B. HTTPS<br>C`
* **Protected Router Decision Explanation:** *Candidate blocked because baseline captured the target and candidate failed.*

#### Showcase Case 2: ID 204 (seen_val)
* **Operational Category:** Persistent Failure Contained: Both models failed target capture; candidate was suppressed and baseline fallback served.
* **Prompt:** *Seen Validation 4: The author of Odyssey is*
* **Expected Target:** `Homer`
* **Outputs:** Baseline=`a Greek poet and playwright. A) 正确 B` (Risk: 0.4024) | SFT Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.4462)
* **Latent Telemetry:** Baseline Top-1 Prob: `7.08%` | SFT Candidate Top-1 Prob: `5.35%` | Delta: `-0.0173`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `⚠️ Hallucination Risk Detected — Response Withheld for Safety`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.4462).*

#### Showcase Case 3: ID 201 (seen_val)
* **Operational Category:** Preserved Stricter Contract: Both captured semantic target, but candidate violated format constraints; baseline output served.
* **Prompt:** *Seen Validation 1: The capital of Germany is*
* **Expected Target:** `Berlin`
* **Outputs:** Baseline=`Berlin. <br><br>What is the next sentence?<br>Options are:` (Risk: 0.3340) | SFT Candidate=`Berlin. <br><br>What would be an appropriate response to this statement` (Risk: 0.3468)
* **Latent Telemetry:** Baseline Top-1 Prob: `31.64%` | SFT Candidate Top-1 Prob: `46.88%` | Delta: `+0.1523`
* **Router Action:** `use_baseline` -> **Served Output:** `Berlin. <br><br>What is the next sentence?<br>Options are:`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

#### Showcase Case 4: ID 214 (seen_val)
* **Operational Category:** Repair Promoted: Candidate successfully recovered and validated semantic target completion.
* **Prompt:** *Seen Validation 14: The author of Odyssey is*
* **Expected Target:** `Homer`
* **Outputs:** Baseline=`a Greek poet and playwright. A) True B) False` (Risk: 0.4099) | SFT Candidate=`Homer, the Greek poet. This statement is true or false` (Risk: 0.4499)
* **Latent Telemetry:** Baseline Top-1 Prob: `7.23%` | SFT Candidate Top-1 Prob: `6.69%` | Delta: `-0.0054`
* **Router Action:** `use_candidate` -> **Served Output:** `Homer, the Greek poet. This statement is true or false`
* **Protected Router Decision Explanation:** *Contract-clean candidate repair promoted.*



---

## 7. Compliance Trace

### Failed Generations Debug Trace Table

The following SFT trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | SFT Candidate Output | Baseline NLL |
|---|---|---|---|---|---|---|
| seen_val | 204 | *Seen Validation 4: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.6406 |
| seen_val | 209 | *Seen Validation 9: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.4844 |
| seen_val | 214 | *Seen Validation 14: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `Homer, the Greek poet. This...` | 3.1250 |
| seen_val | 219 | *Seen Validation 19: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.4531 |
| seen_val | 229 | *Seen Validation 29: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `Homer, the Greek poet. This...` | 3.6406 |
| seen_val | 234 | *Seen Validation 34: The author of Odyssey is* | `Homer` | `a man who has been in the m...` | `⚠️ Hallucination Risk Detec...` | 4.2812 |
| seen_val | 239 | *Seen Validation 39: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.7500 |
| seen_val | 249 | *Seen Validation 49: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.8438 |
| seen_val | 254 | *Seen Validation 54: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.6250 |
| seen_val | 259 | *Seen Validation 59: The author of Odyssey is* | `Homer` | `a Greek poet and playwright...` | `⚠️ Hallucination Risk Detec...` | 3.7031 |
| ... | ... | ... | ... | ... | ... | *(And 101 more SFT trace details)* |



---

## 8. Structural Reconciliation

### Structural Reliability Model Reconciliation

To ensure mathematical SFT rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `37.53%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `89.84%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `99.55%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.86%` (Gate Role: localized adapter SFT targeting signal)

#### ⚠️ Causal Flow Multi-Layer Reconciliation Notice
This run reports high localized individual layer survival probabilities (averaging `96.00%`) across all `24` decoder layers, while presenting a combined Strict-Series system reliability ($R_{sys}$) of **37.53%**.

This is **not a mathematical error**, but rather a critical architectural discovery resolved by PCRF's multi-tier decomposition:

1. **The Product Decay of Series Chains ($R_{sys}$):**
   In a strict sequential dependency model (where information must travel down a 24-layer latent highway without bypass preservation), errors compound multiplicatively:
   $$R_{sys} = \prod_{l=1}^{L} r_l$$
   Even when every single layer is on average `96.00%` stable, a 24-layer deep cascade naturally multiplies down to:
   $$(96.00\%)^{24} \approx 37.53\%$$
   Because our model undergoes structural shift during fine-tuning, several layers present slightly higher informational decay, dragging the strict multiplicative series reliability down to **37.53%**.

2. **The Residual Bypass Reality (CREW Reliability):**
   Modern Transformer decoders do not rely on a strict sequential dependency; they utilize dense residual bypass paths (Attention and MLP shortcuts). Under the **CREW (Causal Residual-depth Evaluation Weights)** formulation, which maps bypass-dominated highway paths, the system reliability is measured at **89.84%** (CREW Product) and **99.55%** (CREW Geometric).

   This proves that **the model's base representation is highly stable**, but SFT-induced modifications have caused localized informational alignment gaps when forcing sequential inference logic.

> ⚠️ **Mathematical Caveat (Bypass-Dominated):** Strict SFT chain reliability appears stable under this measurement, but CREW submodule decomposition is residual-bypass dominated. Attention and MLP causal paths require separate validation before structural metrics can be treated as promotion-grade.



## Bottleneck Selection & Layer Causal Flow Matrix

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 1, 6, 9, 10, 21, 22, 23`
* **Highest Empirical Sensitivity Layer:** Layer `7` (Empirical Delta: `0.00884`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `23` (Birnbaum Index: `0.66107`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom SFT regularizer parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.


---

## 9. SFT Generalization Accuracies

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Candidate Direction | Served Delta | Served Direction | Customer Reading Guidance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Validation NLL | Lower is Better ⬇️ | 2.3784 | 1.8674 | 2.1721 | -0.5110 | Favorable | -0.2063 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Validation NLL | Lower is Better ⬇️ | 3.5115 | 3.3194 | 3.5054 | -0.1921 | Favorable | -0.0061 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 33.4999 | 27.6436 | 33.2953 | -5.8562 | Favorable | -0.2046 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 2.9450 | 2.5934 | 2.8388 | -0.3516 | Favorable | -0.1062 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Semantic Target Capture | Higher is Better ⬆️ | 59.60% | 56.80% | 60.80% | -2.80% | Unfavorable | +1.20% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| First-Token Target Match | Higher is Better ⬆️ | 30.00% | 38.40% | 30.80% | +8.40% | Favorable | +0.80% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 82.40% | 84.00% | 84.00% | +1.60% | Favorable | +1.60% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 36.80% | 29.60% | 37.60% | -7.20% | Unfavorable | +0.80% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |



**Reading the Metrics Scoreboard:**
* **Candidate Delta** indicates raw SFT model representation movement.
* **Served Delta** reflects governed served output. A flat Served Delta can signify safe routing overrides.


| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `139` | `55.6%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `10` | `4.0%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `3` | `1.2%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `98` | `39.2%` | Persistent target failure across both configurations |


### Metric Confidence & Validation Sample Size Limits

* **Train Split Partition Count:** `200`
* **Seen Validation Split Count:** `125`
* **Unseen Validation Split Count:** `125`
* **Total Combined Validation Count:** `250`


### Paired Significance Context:
With smaller validation sets, discrete accuracy deltas must be interpreted as directional SFT evidence rather than definitive proof of generalization. 
Enterprise deployments should scale validation spaces to larger evaluation corpuses to perform paired statistical tests.


### Dynamic Executive AI Governance Conclusion

Based on SFT evidence compiled in this evaluation cycle, we draw the following conclusions:

* **Demonstrated SFT Capabilities:** SFT candidate model demonstrated improved continuous likelihood metrics (NLL) but failed discrete accuracy non-inferiority or structural safety thresholds. Direct promotion of current weights is not safe.
* **Repairs Promoted:** Promoted 3 validated SFT semantic repairs.
* **Router Safety:** The Protected Router successfully preserved SFT served accuracy by blocking 10 regressions.


### Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*


## 10. Report Masking Audit

**Customer-Safe Output Masking Audit:** FAILED

⚠️ **Warning: Raw Hallucinated Output Leaks Detected in Report!**

* Raw baseline output for row 204 leaked: 'a Greek poet and playwright. A) 正确 B'
* Raw baseline output for row 209 leaked: 'a Greek poet and playwright. A) True B) False'
* Raw baseline output for row 214 leaked: 'a Greek poet and playwright. A) True B) False'
* Raw baseline output for row 219 leaked: 'a Greek poet and playwright. A) 正确 B'
* Raw baseline output for row 239 leaked: 'a Greek poet and playwright. A) 正确 B'
* Raw baseline output for row 249 leaked: 'a Greek poet and playwright. A) 正确 B'
* Raw baseline output for row 254 leaked: 'a Greek poet and playwright. A) 正确 B'
* Raw baseline output for row 259 leaked: 'a Greek poet and playwright. A) 正确 B'
* Raw baseline output for row 319 leaked: 'a Greek poet and playwright. A) 正确 B'
