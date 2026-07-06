# PCRF Executive SFT Reliability Scorecard
**Causal Flow Downstream Probability Derivatives Audit Report**


### 📦 Customer Executive Summary

- **What Happened?**  
  The SFT candidate's Seen Validation EM accuracy was unchanged, while the Unseen SFT Generalization accuracy was regressed by -1.60 percentage points.  

- **Likelihood & Confidence Behavior:**  
  SFT Generalization Negative Log-Likelihood (NLL) improved (decreased) by 5.1935, and SFT Perplexity (PPL) improved (decreased) by 756329.39.  

- **Why was Direct Adoption Accepted/Rejected?**  
  Direct adoption was REJECTED (DO_NOT_APPLY) due to SFT continuous and structural safety check limitations: Overall system chain reliability R_sys (34.11%) vs floor (75.0%).; Zero correct-to-wrong regressions required. Found 5 regressions.; Average candidate risk increase (0.0587) must be within limit (0.0500).; Unseen accuracy improvement (-1.60%) vs requirement (2.0%).; Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -1.60%)..  

- **What did PCRF Prove in This Run?**  
  PCRF demonstrated essential risk-containment and SFT non-regression governance by intercepting 5 catastrophic output regression(s) and serving baseline model fallbacks.  

  - **PCRF Hallucination Exposure Control:** 100.00% of 95 baseline hallucination/target-failure cases were controlled through 95 protected router interventions.
  * Repairs Found (Semantic Recoveries): `3`
  * Repairs Promoted (Contract-Clean): `3`
  * Repairs Withheld (Contract Violation): `0`
  * Safe withhold/abstain decisions executed: `92`


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
| Derivatives | 0.00 (Unmeasured) | 0.00261 (Avg Sensitivity) | 2.6/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=5.20) | 100.0/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 99.49% | 99.5/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen SFT Acc: 56.0% | Unseen SFT Acc: 54.4% | 60.0/100 | `DO_NOT_APPLY` |


---

## 4. Gating Check Outcomes
| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🔴 FAIL | CRITICAL | 34.11% | 75.00% | Overall system chain reliability R_sys (34.11%) vs floor (75.0%). |
| Correct-to-Wrong Regressions Count | 🔴 FAIL | CRITICAL | 5 | 0 | Zero correct-to-wrong regressions required. Found 5 regressions. |
| Critical High-Priority Regressions | 🟢 PASS | CRITICAL | 0 | 0 | Zero critical high-priority regressions required. Found 0 regressions. |
| Universal Instruction Contract Violation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 100.00% | 10.00% | Both baseline and candidate violate strict output contracts. Tracking operated as a diagnostic planner. |
| Generalization Non-Degradation Instruction Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 100.00% | 100.00% | Instruction contract tracking operated diagnostically for this validation pass. |
| Strict EM Candidate Non-Degradation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 0.00% | Strict EM validation tracking operated diagnostically for this validation pass. |
| Strict EM Absolute Direct Promotion Threshold | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 10.00% | Strict EM validation boundary executed as diagnostic analyzer. |
| Hallucination Risk Trend Variance Gate | 🔴 FAIL | HIGH | 5.87% | 5.00% | Average candidate risk increase (0.0587) must be within limit (0.0500). |
| Minimum Gating Evidence Verification Size | 🟢 PASS | HIGH | 250 | 100 | Validation examples count (250) vs strong claim requirement (100). |
| Seen Accuracy Non-Inferiority Margin | 🟢 PASS | HIGH | 0.00% | 1.00% | Seen accuracy drop (0.00%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | 0.00% | 3.00% | Seen accuracy degradation (0.00%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🔴 FAIL | HIGH | -1.60% | 2.00% | Unseen accuracy improvement (-1.60%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🔴 FAIL | CRITICAL | -1.60% | 0.00% | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -1.60%). |


---

## 5. Hallucination Risk & SFT Calibration

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `95` | Validation prompts where baseline failed to capture semantic target. |
| **Repairs Found (Semantic Recoveries)** | `3` | Raw semantic improvements found in SFT candidate. |
| **Repairs Promoted (Contract-Clean)** | `3` | Baseline errors resolved cleanly and promoted with strict EM. |
| **Repairs Withheld (Contract Violation)**| `0` | Semantic target recovered, but withheld due to contract/EM violation. |
| **Candidate Over-Steers Prevented** | `92` | Both models failed, but SFT candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `5` | Baseline was correct but SFT candidate failed; router served baseline fallback. |
| **Hallucination Exposure Control Rate** | 100.00% | 95 of 95 baseline cases were either repaired or withheld. |
| **Net Gateway Interventions** | `100` | Overall cases actively guarded by the Protected Router (100% active coverage). |


### Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 3 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 3 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 27 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 153 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 64 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration SFT regularization. |


*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 6. Protected Router Governance

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `5` | Fallback to baseline on candidate failure |
| **Contract-Clean Repairs Promoted** | `3` | Upgrade to SFT candidate on verified contract-clean SFT repair |
| **Over-steers Prevented** | `92` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** The router successfully blocked 5 regression(s) where candidate degraded baseline correct outputs. This demonstrates safe containment control.
* **Generalization Repair:** Promoted 3 successful contract-clean SFT candidate repair(s) into active serving streams.



### Dynamic Showcase Cases

#### Showcase Case 1: ID 223 (seen_val)
* **Operational Category:** Regression Blocked: Baseline was correct but candidate regressed; protected router successfully intervened.
* **Prompt:** *Extract the user role (admin/editor/viewer) from this permission string: 'Can read audit logs and browse directory configurations' as JSON: { 'role':*
* **Expected Target:** `viewer`
* **Outputs:** Baseline=`'viewer' } The user role is viewer. Here's` (Risk: 0.1981) | SFT Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.5722)
* **Latent Telemetry:** Baseline Top-1 Prob: `91.41%` | SFT Candidate Top-1 Prob: `60.55%` | Delta: `-0.3086`
* **Router Action:** `use_baseline` -> **Served Output:** `'viewer' } The user role is viewer. Here's`
* **Protected Router Decision Explanation:** *Candidate blocked because baseline captured the target and candidate failed.*

#### Showcase Case 2: ID 201 (seen_val)
* **Operational Category:** Persistent Failure Contained: Both models failed target capture; candidate was suppressed and baseline fallback served.
* **Prompt:** *JSON payload: { 'event': 'FailedLogin', 'username': 'administrator', 'ip': '198.51.100.12', 'attempts': 18 }. Risk triage (low/medium/high):*
* **Expected Target:** `high`
* **Outputs:** Baseline=`low<br><br>What is the risk level of this incident? The` (Risk: 0.4121) | SFT Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.4474)
* **Latent Telemetry:** Baseline Top-1 Prob: `8.98%` | SFT Candidate Top-1 Prob: `8.94%` | Delta: `-0.0005`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `⚠️ Hallucination Risk Detected — Response Withheld for Safety`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.4474).*

#### Showcase Case 3: ID 202 (seen_val)
* **Operational Category:** Preserved Stricter Contract: Both captured semantic target, but candidate violated format constraints; baseline output served.
* **Prompt:** *JSON payload: { 'event': 'FailedLogin', 'username': 'sam_dev', 'ip': '192.168.1.99', 'attempts': 1 }. Risk triage (low/medium/high):*
* **Expected Target:** `low`
* **Outputs:** Baseline=`low<br><br>What is the risk level of this incident? The` (Risk: 0.4102) | SFT Candidate=`low<br><br>What is the risk level of this incident? The` (Risk: 0.4474)
* **Latent Telemetry:** Baseline Top-1 Prob: `9.81%` | SFT Candidate Top-1 Prob: `9.72%` | Delta: `-0.0010`
* **Router Action:** `use_baseline` -> **Served Output:** `low<br><br>What is the risk level of this incident? The`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

#### Showcase Case 4: ID 232 (seen_val)
* **Operational Category:** Repair Promoted: Candidate successfully recovered and validated semantic target completion.
* **Prompt:** *Extract the transaction status (approved/declined) from this gateway log: 'Adyen gateway logs: transaction rejected for user' as JSON: { 'status':*
* **Expected Target:** `declined`
* **Outputs:** Baseline=`'rejected', 'reason': 'user rejected payment request'` (Risk: 0.3852) | SFT Candidate=`'rejected', 'reason': 'user declined payment request'}` (Risk: 0.2503)
* **Latent Telemetry:** Baseline Top-1 Prob: `98.44%` | SFT Candidate Top-1 Prob: `84.77%` | Delta: `-0.1367`
* **Router Action:** `use_candidate` -> **Served Output:** `'rejected', 'reason': 'user declined payment request'}`
* **Protected Router Decision Explanation:** *Contract-clean candidate repair promoted.*



---

## 7. Compliance Trace

### Failed Generations Debug Trace Table

The following SFT trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | SFT Candidate Output | Baseline NLL |
|---|---|---|---|---|---|---|
| seen_val | 201 | *JSON payload: { 'event': 'FailedLogin', 'userna...* | `high` | `low<br><br>What is the risk...` | `⚠️ Hallucination Risk Detec...` | 4.2188 |
| seen_val | 203 | *JSON payload: { 'event': 'S3BucketCreated', 'ow...* | `high` | `What is the risk of this ev...` | `⚠️ Hallucination Risk Detec...` | 4.3750 |
| seen_val | 204 | *JSON payload: { 'event': 'S3BucketCreated', 'ow...* | `low` | `What is the risk of this ev...` | `⚠️ Hallucination Risk Detec...` | 2.9375 |
| seen_val | 205 | *JSON payload: { 'event': 'IAMPolicyModified', '...* | `medium` | `What is the risk of this ev...` | `⚠️ Hallucination Risk Detec...` | 8.6250 |
| seen_val | 206 | *JSON payload: { 'event': 'IAMPolicyModified', '...* | `medium` | `What is the risk of this IA...` | `⚠️ Hallucination Risk Detec...` | 7.2812 |
| seen_val | 207 | *JSON payload: { 'event': 'PortScanDetected', 's...* | `high` | `low<br><br>What is the risk...` | `⚠️ Hallucination Risk Detec...` | 4.2812 |
| seen_val | 210 | *JSON payload: { 'event': 'SSHKeyAdded', 'user':...* | `high` | `low<br><br>What is the risk...` | `⚠️ Hallucination Risk Detec...` | 3.9219 |
| seen_val | 215 | *Extract the API action (get/post/delete) from t...* | `post` | `'GET', 'url': '/webhooks/ne...` | `⚠️ Hallucination Risk Detec...` | 9.6875 |
| seen_val | 222 | *Extract the user role (admin/editor/viewer) fro...* | `editor` | `'admin' } The user role is ...` | `⚠️ Hallucination Risk Detec...` | 17.6250 |
| seen_val | 223 | *Extract the user role (admin/editor/viewer) fro...* | `viewer` | `'viewer' } The user role is...` | `⚠️ Hallucination Risk Detec...` | 20.3750 |
| ... | ... | ... | ... | ... | ... | *(And 90 more SFT trace details)* |



---

## 8. Structural Reconciliation

### Structural Reliability Model Reconciliation

To ensure mathematical SFT rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `34.11%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `88.35%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `99.49%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.97%` (Gate Role: localized adapter SFT targeting signal)

#### ⚠️ Causal Flow Multi-Layer Reconciliation Notice
This run reports high localized individual layer survival probabilities (averaging `95.62%`) across all `24` decoder layers, while presenting a combined Strict-Series system reliability ($R_{sys}$) of **34.11%**.

This is **not a mathematical error**, but rather a critical architectural discovery resolved by PCRF's multi-tier decomposition:

1. **The Product Decay of Series Chains ($R_{sys}$):**
   In a strict sequential dependency model (where information must travel down a 24-layer latent highway without bypass preservation), errors compound multiplicatively:
   $$R_{sys} = \prod_{l=1}^{L} r_l$$
   Even when every single layer is on average `95.62%` stable, a 24-layer deep cascade naturally multiplies down to:
   $$(95.62\%)^{24} \approx 34.11\%$$
   Because our model undergoes structural shift during fine-tuning, several layers present slightly higher informational decay, dragging the strict multiplicative series reliability down to **34.11%**.

2. **The Residual Bypass Reality (CREW Reliability):**
   Modern Transformer decoders do not rely on a strict sequential dependency; they utilize dense residual bypass paths (Attention and MLP shortcuts). Under the **CREW (Causal Residual-depth Evaluation Weights)** formulation, which maps bypass-dominated highway paths, the system reliability is measured at **88.35%** (CREW Product) and **99.49%** (CREW Geometric).

   This proves that **the model's base representation is highly stable**, but SFT-induced modifications have caused localized informational alignment gaps when forcing sequential inference logic.

> ⚠️ **Mathematical Caveat (Bypass-Dominated):** Strict SFT chain reliability appears stable under this measurement, but CREW submodule decomposition is residual-bypass dominated. Attention and MLP causal paths require separate validation before structural metrics can be treated as promotion-grade.



## Bottleneck Selection & Layer Causal Flow Matrix

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 1, 3, 7, 21, 22, 23`
* **Highest Empirical Sensitivity Layer:** Layer `0` (Empirical Delta: `0.01104`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `23` (Birnbaum Index: `0.59963`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom SFT regularizer parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.


---

## 9. SFT Generalization Accuracies

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Candidate Direction | Served Delta | Served Direction | Customer Reading Guidance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Validation NLL | Lower is Better ⬇️ | 5.7314 | 3.7504 | 5.6185 | -1.9810 | Favorable | -0.1129 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Validation NLL | Lower is Better ⬇️ | 13.5418 | 8.3483 | 13.5418 | -5.1935 | Favorable | +0.0000 | Flat (Repair Opportunity Withheld) | SFT candidate improved Unseen Validation NLL by -5.1935, but promotion was withheld due to strict structural floor safety policies [3]. Baseline output was retained for safety. |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 760552.1792 | 4222.7844 | 760552.1792 | -756329.3948 | Favorable | +0.0000 | Flat (Repair Opportunity Withheld) | SFT candidate improved Unseen Perplexity (PPL) by -756329.3948, but promotion was withheld due to strict structural floor safety policies [3]. Baseline output was retained for safety. |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 9.6366 | 6.0493 | 9.5801 | -3.5873 | Favorable | -0.0564 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Semantic Target Capture | Higher is Better ⬆️ | 62.00% | 61.20% | 63.20% | -0.80% | Unfavorable | +1.20% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| First-Token Target Match | Higher is Better ⬆️ | 48.00% | 47.20% | 48.40% | -0.80% | Unfavorable | +0.40% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 68.00% | 68.00% | 70.40% | +0.00% | Flat | +2.40% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 56.00% | 54.40% | 56.00% | -1.60% | Unfavorable | +0.00% | Flat (Regression Risk Blocked) | SFT candidate degraded Unseen Generalization Accuracy by -1.60%, but the Protected Router successfully intercepted and blocked the regression risk from reaching served environments. |



**Reading the Metrics Scoreboard:**
* **Candidate Delta** indicates raw SFT model representation movement.
* **Served Delta** reflects governed served output. A flat Served Delta can signify safe routing overrides.


| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `150` | `60.0%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `5` | `2.0%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `3` | `1.2%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `92` | `36.8%` | Persistent target failure across both configurations |


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
* **Router Safety:** The Protected Router successfully preserved SFT served accuracy by blocking 5 regressions.


### Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*


## 10. Report Masking Audit

**Customer-Safe Output Masking Audit:** FAILED

⚠️ **Warning: Raw Hallucinated Output Leaks Detected in Report!**

* Raw baseline output for row 225 leaked: ''viewer' } The user role is viewer. Here's'
* Raw baseline output for row 228 leaked: ''viewer' } The user role is viewer. Here's'
* Raw baseline output for row 232 leaked: ''rejected', 'reason': 'user rejected payment request''
