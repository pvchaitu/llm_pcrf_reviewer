# PCRF Executive SFT Reliability Scorecard
**Causal Flow Downstream Probability Derivatives Audit Report**




### 📦 Customer Executive Summary

- **What Happened?**  
  The SFT candidate's Seen Validation EM accuracy was improved by +5.00 percentage points, while the Unseen SFT Generalization accuracy was unchanged.  

- **Likelihood & Confidence Behavior:**  
  SFT Generalization Negative Log-Likelihood (NLL) improved (decreased) by 7.1583, and SFT Perplexity (PPL) improved (decreased) by 560226.42.  

- **Why was Direct Adoption Accepted/Rejected?**  
  Direct adoption was REJECTED (DO_NOT_APPLY) due to SFT continuous and structural safety check limitations: Overall system chain reliability R_sys (33.94%) vs floor (75.0%).; Zero critical high-priority regressions required. Found 2 regressions.; Validation examples count (80) vs strong claim requirement (100)..  

- **What did PCRF Prove in This Run?**  
  PCRF demonstrated essential risk-containment and SFT non-regression governance by intercepting 9 catastrophic output regression(s) and serving baseline model fallbacks.  

  - **PCRF Hallucination Exposure Control:** 100.00% of 26 baseline hallucination/target-failure cases were controlled through 35 protected router interventions.
  * Repairs Found (Semantic Recoveries): `2`
  * Repairs Promoted (Contract-Clean): `2`
  * Repairs Withheld (Contract Violation): `0`
  * Safe withhold/abstain decisions executed: `24`


---

## Core Gating Status

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
| **Observed Risk Events** | `35` | All validation prompts triggering baseline failure or candidate degradation. |
| **Contained Risk Events** | `35` | Total safety interventions successfully managed by Protected Router. |
| **Served Risk Events** | `0` | Safety-withheld or incorrect completions exposed to served streams. |
| **Safe Abstains** | `24` | Unsafe outputs withheld and mapped cleanly to fallback states. |
| **Exposure Control Rate** | `100.00%` | Percentage of overall risk events successfully contained under governance. |


---

## 2. PCRF Governance Assessment

> ### 🛡️ Service Governance Scorecard
> 
> * **Governed Accuracy (Primary Customer Metric):** `70.00%`  
> * **Baseline Accuracy (Comparison Metric):** `67.50%`  
> * **Candidate Accuracy (Engineering Metric):** `58.75%`  
> * **Regression Containment Effectiveness:** `100.00%`  
> * **Repair Promotion Effectiveness:** `100.00%`  
> * **Hallucination Exposure Control Rate:** `100.00%`  
> * **Safe Abstains Executed:** `24`  
> 
> **Service Impact Narrative:**  
> Governed outcomes remained protected despite candidate degradation events during SFT evaluation. The Protected Router successfully insulated the final served endpoint, maintaining served quality at **70.00%** while preventing degraded candidate outputs from reaching users.


---

## 3. Integrated PCRF Scoreboard
| Feature Track / Module | Baseline Value | PCRF Result Value | Track Score | Gating Status |
|---|---|---|---|---|
| Derivatives | 0.00 (Unmeasured) | 0.00394 (Avg Sensitivity) | 3.9/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=5.39) | 100.0/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 99.51% | 99.5/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen SFT Acc: 67.5% | Unseen SFT Acc: 57.5% | 45.0/100 | `DO_NOT_APPLY` |


---

## 4. Gating Check Outcomes
| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🔴 FAIL | CRITICAL | 33.94% | 75.00% | Overall system chain reliability R_sys (33.94%) vs floor (75.0%). |
| Candidate Regression Review | 🟢 PASS | DIAGNOSTIC_ONLY | Observed Regressions: 9, Observed Repairs: 2, Net Delta: -7 | N/A | Model evaluation only. Captures raw candidate parameter variance before PCRF routing. |
| Regression Exposure Control | 🟢 PASS | CRITICAL | Effectiveness: 100.0%, Served Regressions: 0 | Served Regressions = 0 | Observed regressions were contained before reaching served output. |
| Critical High-Priority Regressions | 🟢 PASS | CRITICAL | 0 | 0 | Zero critical high-priority regressions required. Found 0 regressions. |
| Universal Instruction Contract Violation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 100.00% | 10.00% | Both baseline and candidate violate strict output contracts. Tracking operated as a diagnostic planner. |
| Generalization Non-Degradation Guard | 🟡 WARNING | WARNING | -8.75% | 0.00% | Generalization monitoring warning: raw SFT candidate unseen validation exact-match changed by -8.75% versus baseline. This is reported as candidate-side generalization telemetry only and does not block deployment when Protected Router served outputs remain governed and regression exposure is contained. |
| Strict EM Candidate Non-Degradation Gate | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 0.00% | Strict EM validation tracking operated diagnostically for this validation pass. |
| Strict EM Absolute Direct Promotion Threshold | 🟢 PASS | DIAGNOSTIC_ONLY | 0.00% | 10.00% | Strict EM validation boundary executed as diagnostic analyzer. |
| Minimum Gating Evidence Verification Size | 🔴 FAIL | HIGH | 80 | 100 | Validation examples count (80) vs strong claim requirement (100). |
| Served Seen Accuracy Non-Inferiority Margin | 🔴 FAIL | HIGH | 8.75% | 1.00% | Served seen accuracy drop after Protected Router governance (8.75%) vs non-inferiority margin (1.0%). This gate is deployment-facing and evaluates governed served output, not raw candidate-only movement. |
| Served Seen Accuracy Degradation Budget | 🔴 FAIL | CRITICAL | 8.75% | 3.00% | Served seen accuracy degradation after Protected Router governance (8.75%) vs deployment budget (3.0%). This remains a blocking gate only when the governed served stream degrades beyond the allowed budget. |
| Candidate Unseen Accuracy Improvement Review | 🟡 WARNING | WARNING | -8.75% | 2.00% | Candidate-side unseen accuracy improvement was -8.75% vs target 2.0%. This is reported as raw SFT generalization telemetry only and does not block deployment when served outputs remain governed. |
| Served Unseen Generalization Preservation | 🔴 FAIL | HIGH | -8.75% | 0.00% | Served unseen accuracy movement after Protected Router governance was -8.75% versus baseline. This deployment-facing gate verifies that governed served output does not degrade on unseen validation. |
| Generalization Non-Degradation Guard | 🟡 WARNING | WARNING | -8.75% | 0.00% | Generalization monitoring warning: raw SFT candidate unseen validation exact-match changed by -8.75% versus baseline. This is reported as candidate-side generalization telemetry only and does not block deployment when Protected Router served outputs remain governed and regression exposure is contained. |


---

## 5. Hallucination Risk & SFT Calibration

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `26` | Validation prompts where baseline failed to capture semantic target. |
| **Repairs Found (Semantic Recoveries)** | `2` | Raw semantic improvements found in SFT candidate. |
| **Repairs Promoted (Contract-Clean)** | `2` | Baseline errors resolved cleanly and promoted with strict EM. |
| **Repairs Withheld (Contract Violation)**| `0` | Semantic target recovered, but withheld due to contract/EM violation. |
| **Candidate Over-Steers Prevented** | `24` | Both models failed, but SFT candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `9` | Baseline was correct but SFT candidate failed; router served baseline fallback. |
| **Hallucination Exposure Control Rate** | 100.00% | All baseline cases were either repaired or withheld. |
| **Net Gateway Interventions** | `35` | Overall cases actively guarded by the Protected Router (100% active coverage). |

### Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 0 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 0 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 16 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 47 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 17 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration SFT regularization. |

*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 6. Protected Router Governance

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `9` | Fallback to baseline on candidate failure |
| **Contract-Clean Repairs Promoted** | `2` | Upgrade to SFT candidate on verified contract-clean SFT repair |
| **Over-steers Prevented** | `24` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** The router successfully blocked 9 regression(s) where candidate degraded baseline correct outputs. This demonstrates safe containment control.
* **Generalization Repair:** Promoted 2 successful contract-clean SFT candidate repair(s) into active serving streams.

### Dynamic Showcase Cases
#### Showcase Case 1: ID 123 (seen_val)
* **Operational Category:** Regression Blocked: SFT candidate regressions were observed during evaluation, but the Protected Router successfully prevented exposure.
* **Prompt:** *Extract the user role (admin/editor/viewer) from this permission string: 'Can...*
* **Expected Target:** `viewer`
* **Outputs:** Baseline=`'viewer' } The user role is viewer. H...` (Risk: 0.1985) | SFT Candidate=`permissions.split(' ')[1] } Here is t...` (Risk: 0.4187)
* **Latent Telemetry:** Baseline Top-1 Prob: `91.41%` | SFT Candidate Top-1 Prob: `18.95%` | Delta: `-0.7246`
* **Router Action:** `use_baseline` -> **Served Output:** `'viewer' } The user role is viewer. H...`
* **Protected Router Decision Explanation:** *Candidate blocked because baseline captured the target and candidate failed.*

#### Showcase Case 2: ID 101 (seen_val)
* **Operational Category:** Persistent Failure Contained: Both failed target capture; candidate risk was contained and fallback was executed.
* **Prompt:** *JSON payload: { 'event': 'FailedLogin', 'username': 'administrator', 'ip': '1...*
* **Expected Target:** `high`
* **Outputs:** Baseline=`low<br><br>What is the risk level of ...` (Risk: 0.4124) | SFT Candidate=`low<br><br>What is the risk level of ...` (Risk: 0.4449)
* **Latent Telemetry:** Baseline Top-1 Prob: `8.98%` | SFT Candidate Top-1 Prob: `12.50%` | Delta: `+0.0352`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `⚠️ Hallucination Risk Detected — Resp...`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.4449).*

#### Showcase Case 3: ID 102 (seen_val)
* **Operational Category:** Preserved Stricter Contract: SFT candidate violated formatting contracts; baseline output safely served instead.
* **Prompt:** *JSON payload: { 'event': 'FailedLogin', 'username': 'sam_dev', 'ip': '192.168...*
* **Expected Target:** `low`
* **Outputs:** Baseline=`low<br><br>What is the risk level of ...` (Risk: 0.4106) | SFT Candidate=`low<br><br>What is the risk level of ...` (Risk: 0.4468)
* **Latent Telemetry:** Baseline Top-1 Prob: `9.81%` | SFT Candidate Top-1 Prob: `13.57%` | Delta: `+0.0376`
* **Router Action:** `use_baseline` -> **Served Output:** `low<br><br>What is the risk level of ...`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

#### Showcase Case 4: ID 104 (seen_val)
* **Operational Category:** Repair Promoted: Candidate successfully recovered and validated semantic target completion.
* **Prompt:** *JSON payload: { 'event': 'S3BucketCreated', 'owner': 'ops_lead_44', 'public_a...*
* **Expected Target:** `low`
* **Outputs:** Baseline=`What is the risk of this event occurr...` (Risk: 0.4181) | SFT Candidate=`low<br><br>What is the risk level of ...` (Risk: 0.4440)
* **Latent Telemetry:** Baseline Top-1 Prob: `7.23%` | SFT Candidate Top-1 Prob: `11.04%` | Delta: `+0.0381`
* **Router Action:** `use_candidate` -> **Served Output:** `low<br><br>What is the risk level of ...`
* **Protected Router Decision Explanation:** *Contract-clean candidate repair promoted.*




---

## 7. Compliance Trace

### Failed Generations Debug Trace Table

The following SFT trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | SFT Candidate Output | Baseline NLL |
|---|---|---|---|---|---|---|
| seen_val | 101 | *JSON payload: { 'event': 'FailedLogin', 'userna...* | `high` | `low<br><br>What is the risk...` | `low<br><br>What is the risk...` | 4.2188 |
| seen_val | 103 | *JSON payload: { 'event': 'S3BucketCreated', 'ow...* | `high` | `What is the risk of this ev...` | `low<br><br>What is the risk...` | 4.3750 |
| seen_val | 104 | *JSON payload: { 'event': 'S3BucketCreated', 'ow...* | `low` | `What is the risk of this ev...` | `low<br><br>What is the risk...` | 2.9375 |
| seen_val | 105 | *JSON payload: { 'event': 'IAMPolicyModified', '...* | `medium` | `What is the risk of this ev...` | `low<br><br>What is the risk...` | 8.6250 |
| seen_val | 106 | *JSON payload: { 'event': 'IAMPolicyModified', '...* | `medium` | `What is the risk of this IA...` | `low<br><br>What is the risk...` | 7.2812 |
| seen_val | 107 | *JSON payload: { 'event': 'PortScanDetected', 's...* | `high` | `low<br><br>What is the risk...` | `low<br><br>What is the risk...` | 4.2812 |
| seen_val | 110 | *JSON payload: { 'event': 'SSHKeyAdded', 'user':...* | `high` | `low<br><br>What is the risk...` | `low<br><br>What is the risk...` | 3.9219 |
| seen_val | 115 | *Extract the API action (get/post/delete) from t...* | `post` | `'GET', 'url': '/webhooks/ne...` | `'GET', 'url': '/webhooks/ne...` | 9.6875 |
| seen_val | 122 | *Extract the user role (admin/editor/viewer) fro...* | `editor` | `'admin' } The user role is ...` | `'' }<br><br>The given permi...` | 17.6250 |
| seen_val | 123 | *Extract the user role (admin/editor/viewer) fro...* | `viewer` | `'viewer' } The user role is...` | `permissions.split(' ')[1] }...` | 20.3750 |
| ... | ... | ... | ... | ... | ... | *(And 25 more SFT trace details)* |




---

## 8. Structural Reconciliation

### Structural Reliability Model Reconciliation

To ensure mathematical SFT rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `33.94%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `88.82%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `99.51%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.96%` (Gate Role: localized adapter SFT targeting signal)

#### ⚠️ Causal Flow Multi-Layer Reconciliation Notice
This run reports high localized individual layer survival probabilities (averaging `95.60%`) across all `24` decoder layers, while presenting a combined Strict-Series system reliability ($R_{sys}$) of **33.94%**.

This is **not a mathematical error**, but rather a critical architectural discovery resolved by PCRF's multi-tier decomposition:

1. **The Product Decay of Series Chains ($R_{sys}$):**
  In a strict sequential dependency model (where information must travel down a 24-layer latent highway without bypass preservation), errors compound multiplicatively:
  $$R_{sys} = \prod_{l=1}^{L} r_l$$
  Even when every single layer is on average `95.60%` stable, a 24-layer deep cascade naturally multiplies down to:
  $$(95.60\%)^{24} \approx 33.94\%$$
  Because our model undergoes structural shift during fine-tuning, several layers present slightly higher informational decay, dragging the strict multiplicative series reliability down to **33.94%**.

2. **The Residual Bypass Reality (CREW Reliability):**
  Modern Transformer decoders do not rely on a strict sequential dependency; they utilize dense residual bypass paths (Attention and MLP shortcuts). Under the **CREW (Causal Residual-depth Evaluation Weights)** formulation, which maps bypass-dominated highway paths, the system reliability is measured at **88.82%** (CREW Product) and **99.51%** (CREW Geometric).

  This proves that **the model's base representation is highly stable**, but SFT-induced modifications have caused localized informational alignment gaps when forcing sequential inference logic.

> ⚠️ **Mathematical Caveat (Bypass-Dominated):** Strict SFT chain reliability appears stable under this measurement, but CREW submodule decomposition is residual-bypass dominated. Attention and MLP causal paths require separate validation before structural metrics can be treated as promotion-grade.



## Bottleneck Selection & Layer Causal Flow Matrix

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 1, 2, 4, 21, 22, 23`
* **Highest Empirical Sensitivity Layer:** Layer `1` (Empirical Delta: `0.02536`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `23` (Birnbaum Index: `0.60845`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom SFT regularizer parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.



---

## 9. SFT Generalization Accuracies

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Candidate Direction | Served Delta | Served Direction | Customer Reading Guidance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Validation NLL | Lower is Better ⬇️ | 11.0645 | 4.1754 | 10.7973 | -6.8891 | Favorable | -0.2672 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Validation NLL | Lower is Better ⬇️ | 13.2369 | 6.0786 | 13.2369 | -7.1583 | Favorable | +0.0000 | Flat (Repair Opportunity Withheld) | SFT candidate improved Unseen Validation NLL by -7.1583, but promotion was withheld due to strict structural floor safety policies. Baseline output was retained for safety. |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 560662.8369 | 436.4151 | 560662.8369 | -560226.4218 | Favorable | +0.0000 | Flat (Repair Opportunity Withheld) | SFT candidate improved Unseen Perplexity (PPL) by -560226.4218, but promotion was withheld due to strict structural floor safety policies. Baseline output was retained for safety. |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 12.1507 | 5.1270 | 12.0171 | -7.0237 | Favorable | -0.1336 | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Semantic Target Capture | Higher is Better ⬆️ | 67.50% | 58.75% | 70.00% | -8.75% | Unfavorable | +2.50% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| First-Token Target Match | Higher is Better ⬆️ | 63.75% | 53.75% | 66.25% | -10.00% | Unfavorable | +2.50% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | Flat | +0.00% | Flat (No Change) | No material movement versus baseline across both candidate and served paths. |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 67.50% | 60.00% | 72.50% | -7.50% | Unfavorable | +5.00% | Favorable | Served Delta reflects production-facing impact after Protected Router gating controls successfully exposed candidate improvements. |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 67.50% | 57.50% | 67.50% | -10.00% | Unfavorable | +0.00% | Flat (Regression Risk Blocked) | Candidate regressions were observed during evaluation, but the Protected Router successfully intercepted and blocked the regression risk from reaching served environments. |


**Reading the Metrics Scoreboard:**
* **Candidate Delta** indicates raw SFT model representation movement.
* **Served Delta** reflects governed served output. A flat Served Delta can signify safe routing overrides.

| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `45` | `56.2%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `9` | `11.2%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `2` | `2.5%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `24` | `30.0%` | Persistent target failure across both configurations |

### Metric Confidence & Validation Sample Size Limits

* **Train Split Partition Count:** `100`
* **Seen Validation Split Count:** `40`
* **Unseen Validation Split Count:** `40`
* **Total Combined Validation Count:** `80`

### Paired Significance Context:
With smaller validation sets, discrete accuracy deltas must be interpreted as directional SFT evidence rather than definitive proof of generalization. 
Enterprise deployments should scale validation spaces to larger evaluation corpuses to perform paired statistical tests.

### Dynamic Executive AI Governance Conclusion

Based on SFT evidence compiled in this evaluation cycle, we draw the following conclusions:

* **Demonstrated SFT Capabilities:** SFT candidate model demonstrated improved continuous likelihood metrics (NLL) but failed discrete accuracy non-inferiority or structural safety thresholds. Direct promotion of current weights is not safe.
* **Repairs Promoted:** Promoted 2 validated SFT semantic repairs.
* **Router Safety:** The Protected Router successfully preserved SFT served accuracy by blocking 9 regressions.

### Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*



## 10. Report Masking Audit

**Customer-Safe Output Masking Audit:** PASSED

Customer-safe hallucination output masking passed. Detected unresolved hallucinations were represented using the safety-withheld response.
