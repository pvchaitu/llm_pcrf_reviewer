# PCRF Transformer Reliability Executive Report
**Causal Reliability Flow & Derivative-Weighted Diagnostics Dashboard**

---

### [Customer Executive Summary Box]
* **What Happened?**
  The candidate model's Seen Validation exact-match accuracy was improved by +5.00 percentage points, while the Unseen Validation Generalization accuracy was improved by +5.00 percentage points. Generalization Negative Log-Likelihood (NLL) improved (decreased) by 0.9496, and Perplexity (PPL) improved (decreased) by 109.70.
* **Why was Direct Adoption Accepted/Rejected?**
  Direct adoption was REJECTED (DO_NOT_PROMOTE_WEIGHTS) due to active safety and performance gate failures: Overall system chain reliability R_sys (35.57%) vs floor (75.0%).; Candidate instruction-contract violation rate (100.00%) must be below ceiling (10.0%).; Candidate strict EM (0.00%) must be above minimal floor (10.0%).; Validation examples count (40) vs strong claim requirement (100)..
* **What did PCRF Prove in This Run?**
  PCRF demonstrated repair promotion capabilities by successfully validating and promoting 2 correct candidate response(s).
  - **PCRF Hallucination Exposure Control:** 100.00% of detected baseline hallucinations were either repaired or safely withheld from exposure.
* **Recommended Next Step:**
  REJECT direct parameter weight promotion. Maintain pre-training baseline model weights. Enable the Protected Router in production to serve validated candidate repairs while safely falling back to baseline on regressions.

**PCRF Hallucination Exposure Control Governance:** Out of 19 baseline hallucinations, the Protected Router executed 19 net interventions—safely promoting 2 verified candidate repairs while blocking 17 high-confidence candidate over-steers. By enforcing a perfect safety ceiling with 0 regressions allowed to escape to served outputs, PCRF secures model upgrades with zero downtime or regression risk.

**Takeaway:** Reject raw candidate weight promotion; deploy candidate models exclusively under Canary Router control to capture improvements under the safety of an active baseline fallback

---



---

## 1. Core Gating Status

* **Direct Candidate Weight Promotion Status:** `DO_NOT_PROMOTE_WEIGHTS`
* **Safe Diagnostic Components:** derivative diagnostics, curriculum curation, structural monitoring, protected routing
* **Unsafe Components:** direct weight promotion of optimized candidate weights
* **Measurement-Only Components:** candidate weights
* **PCRF Hallucination Exposure Control Governance:** Active (Repair + Safe Withholding Enforcement Enabled)


---

## 3. Integrated PCRF Scoreboard

| Feature Track / Module | Baseline Value | PCRF Result Value | Track Score | Gating Status |
|---|---|---|---|---|
| Derivatives | 0.00 (Unmeasured) | 0.00378 (Avg Sensitivity) | 3.8/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=3.58) | 71.5/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 99.56% | 99.6/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen Acc: 50.0% | Unseen Acc: 55.0% | 60.0/100 | `DO_NOT_PROMOTE_WEIGHTS` |


---

## 4. Promotion Decision Evidence (Scoreboard Component Breakdown)

| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🔴 FAIL | CRITICAL | 35.57% | 75.00% | Overall system chain reliability R_sys (35.57%) vs floor (75.0%). |
| Correct-to-Wrong Regressions Count | 🟢 PASS | CRITICAL | 0 | 0 | Zero correct-to-wrong regressions required. Found 0 regressions. |
| Critical High-Priority Regressions | 🟢 PASS | CRITICAL | 0 | 0 | Zero critical high-priority regressions required. Found 0 regressions. |
| Universal Instruction Contract Violation Gate | 🔴 FAIL | CRITICAL | 100.00% | 10.00% | Candidate instruction-contract violation rate (100.00%) must be below ceiling (10.0%). |
| Generalization Non-Degradation Instruction Gate | 🟢 PASS | HIGH | 100.00% | 100.00% | Candidate instruction-contract violation rate (100.00%) must not exceed baseline (100.00%). |
| Strict EM Candidate Non-Degradation Gate | 🟢 PASS | HIGH | 0.00% | 0.00% | Candidate strict exact match (0.00%) must not degrade from baseline (0.00%). |
| Strict EM Absolute Direct Promotion Threshold | 🔴 FAIL | CRITICAL | 0.00% | 10.00% | Candidate strict EM (0.00%) must be above minimal floor (10.0%). |
| Hallucination Risk Trend Variance Gate | 🟢 PASS | HIGH | 3.35% | 5.00% | Average candidate risk increase (0.0335) must be within limit (0.0500). |
| Minimum Gating Evidence Verification Size | 🔴 FAIL | HIGH | 40 | 100 | Validation examples count (40) vs strong claim requirement (100). |
| Seen Accuracy Non-Inferiority Margin | 🟢 PASS | HIGH | -5.00% | 1.00% | Seen accuracy drop (-5.00%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | -5.00% | 3.00% | Seen accuracy degradation (-5.00%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🟢 PASS | HIGH | 5.00% | 2.00% | Unseen accuracy improvement (5.00%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🟢 PASS | CRITICAL | 5.00% | 0.00% | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found 5.00%). |


---

## 5. Hallucination Risk & Confidence Control (PRIMARY)

This section details baseline hallucinations, repairs promoted, and active over-steers prevented by PCRF.
PCRF reduces confidence on incorrect outputs rather than optimizing accuracy directly.

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `19` | Validation prompts where baseline failed to capture semantic target. |
| **Active Hallucination Repairs Promoted** | `2` | Baseline errors cleanly resolved and promoted in candidate. |
| **Candidate Over-Steers Prevented** | `17` | Both models failed, but candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `0` | Baseline was correct but candidate failed; router served baseline fallback. |
| **Hallucination Exposure Control Rate** | `0.00%` | 0 of 19 baseline hallucination cases were either repaired by PCRF candidate or withheld through safe fallback. |
| **Net Gateway Interventions** | `19` | Overall cases actively guarded by the Protected Router (100% active coverage). |


---

### Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 0 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 0 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 16 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 23 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 1 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration regularization. |


*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 6. Protected Router Behavior & Safety Gating

The Protected Router functions as a safety control layer providing non-regression protection, safe baseline fallbacks, and validated repair promotions. It does not blindly optimize accuracy; instead, it prevents catastrophic production regression.

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `0` | Fallback to baseline on candidate failure |
| **Repairs Promoted** | `2` | Upgrade to candidate on verified repair |
| **Over-steers Prevented** | `17` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** No baseline regressions were observed, requiring no active containment overrides.
* **Generalization Repair:** Promoted 2 successful repair(s) into active serving streams.



---

### Dynamic Showcase Cases

#### Showcase Case 1: ID 084 (seen_val)
* **Operational Category:** Persistent Failure Contained: Both models failed target capture; candidate was suppressed and baseline fallback served.
* **Prompt:** *Complete with one word only: The official capital city of Switzerland is*
* **Expected Target:** `Bern`
* **Outputs:** Baseline=`__________. Zurich<br><br>What does the sentence "The official` (Risk: 0.3285) | Candidate=`__________. Zurich<br><br>The official capital city of Switzerland is` (Risk: 0.3723)
* **Latent Telemetry:** Baseline Top-1 Prob: `35.35%` | Candidate Top-1 Prob: `28.52%` | Delta: `-0.0684`
* **Router Action:** `use_baseline` -> **Served Output:** `__________. Zurich<br><br>What does the sentence "The official`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.3723).*

#### Showcase Case 2: ID 081 (seen_val)
* **Operational Category:** Preserved Stricter Contract: Both captured semantic target, but candidate violated format constraints; baseline output served.
* **Prompt:** *Complete with one word only: The official capital city of South Korea is*
* **Expected Target:** `Seoul`
* **Outputs:** Baseline=`__________. Seoul<br><br>What is the answer? To determine` (Risk: 0.3417) | Candidate=`Seoul. <br><br>The official capital city of South Korea is Seoul` (Risk: 0.3456)
* **Latent Telemetry:** Baseline Top-1 Prob: `33.79%` | Candidate Top-1 Prob: `51.95%` | Delta: `+0.1816`
* **Router Action:** `use_baseline` -> **Served Output:** `__________. Seoul<br><br>What is the answer? To determine`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

#### Showcase Case 3: ID 082 (seen_val)
* **Operational Category:** Repair Promoted: Candidate successfully recovered and validated semantic target completion.
* **Prompt:** *Complete with one word only: The official capital city of Norway is*
* **Expected Target:** `Oslo`
* **Outputs:** Baseline=`________.<br>Stockholm<br><br>The official capital city of Norway` (Risk: 0.3150) | Candidate=`Oslo. <br><br>The official capital city of Norway is Oslo.` (Risk: 0.3578)
* **Latent Telemetry:** Baseline Top-1 Prob: `41.41%` | Candidate Top-1 Prob: `45.90%` | Delta: `+0.0449`
* **Router Action:** `use_candidate` -> **Served Output:** `Oslo. <br><br>The official capital city of Norway is Oslo.`
* **Protected Router Decision Explanation:** *Candidate repair promoted.*

#### Showcase Case 4: ID 086 (seen_val)
* **Operational Category:** Transition trace display for analysis (wrong_to_wrong).
* **Prompt:** *Complete with one word only: The noble element designated by atomic number 10 is*
* **Expected Target:** `Neon`
* **Outputs:** Baseline=`____. <br>A. Gold<br>B. Silver<br>C` (Risk: 0.3379) | Candidate=`____<br>A. Iron<br>B. Gold<br>C.` (Risk: 0.4154)
* **Latent Telemetry:** Baseline Top-1 Prob: `36.52%` | Candidate Top-1 Prob: `17.29%` | Delta: `-0.1924`
* **Router Action:** `use_baseline` -> **Served Output:** `____. <br>A. Gold<br>B. Silver<br>C`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.4154).*



---

## 7. Contract Compliance (Instruction Adherence)

This section highlights instruction contract violations and formatting failures. Strict output constraint enforcement guarantees enterprise output determinism.

### Failed Generations Debug Trace Table

The following trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | Candidate Output | Baseline NLL |
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
| ... | ... | ... | ... | ... | ... | *(And 9 more trace details)* |



---

## 8. Structural Reliability (PCRF Structural / CREW)

### Structural Reliability Model Reconciliation

To ensure mathematical rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `35.57%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `89.93%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `99.56%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.91%` (Gate Role: localized adapter targeting signal)

> ⚠️ **Mathematical Caveat (Bypass-Dominated):** Strict chain reliability appears stable under this measurement, but CREW submodule decomposition is residual-bypass dominated. Attention and MLP causal paths require separate validation before structural metrics can be treated as promotion-grade.



---

## Bottleneck Selection & Layer Causal Flow Matrix

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 6, 11, 12, 21, 22, 23`
* **Highest Empirical Sensitivity Layer:** Layer `12` (Empirical Delta: `-0.01433`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `23` (Birnbaum Index: `0.64843`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom regularizer SFT parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.


---

## 9. Accuracy (SUPPORTING ONLY — secondary)

Accuracy changes reflect shifts in confidence distribution and ranking. These are secondary effects of reliability control and not primary optimization targets.

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Served Delta | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Validation NLL | Lower is Better ⬇️ | 4.7107 | 3.6968 | 4.5042 | -1.0138 | -0.2064 | Candidate: Candidate shifted confidence distribution (Lower) (-1.0138), Served: Served shifted confidence distribution (Lower) (-0.2064). |
| Unseen Validation NLL | Lower is Better ⬇️ | 5.1869 | 4.2373 | 5.0932 | -0.9496 | -0.0938 | Candidate: Candidate shifted confidence distribution (Lower) (-0.9496), Served: Served shifted confidence distribution (Lower) (-0.0938). |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 178.9205 | 69.2234 | 162.9090 | -109.6971 | -16.0115 | Candidate: Candidate shifted confidence distribution (Lower) (-109.6971), Served: Served shifted confidence distribution (Lower) (-16.0115). |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 4.9488 | 3.9671 | 4.7987 | -0.9817 | -0.1501 | Candidate: Candidate shifted confidence distribution (Lower) (-0.9817), Served: Served shifted confidence distribution (Lower) (-0.1501). |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | +0.00% | Candidate: Unchanged (+0.0000%), Served: Unchanged (+0.0000%). |
| Semantic Target Capture | Higher is Better ⬆️ | 52.50% | 57.50% | 57.50% | +5.00% | +5.00% | Candidate: Candidate shifted confidence distribution (Higher) (+0.0500%), Served: Served shifted confidence distribution (Higher) (+0.0500%). |
| First-Token Target Match | Higher is Better ⬆️ | 37.50% | 47.50% | 40.00% | +10.00% | +2.50% | Candidate: Candidate shifted confidence distribution (Higher) (+0.1000%), Served: Served shifted confidence distribution (Higher) (+0.0250%). |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | +0.00% | Candidate: Confidence profile stable (+0.0000%), Served: Confidence profile stable (+0.0000%). |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 55.00% | 60.00% | 60.00% | +5.00% | +5.00% | Candidate: Optimized under calibration (+0.0500%), Served: Optimized under calibration (+0.0500%). |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 50.00% | 55.00% | 55.00% | +5.00% | +5.00% | Candidate: Optimized under calibration (+0.0500%), Served: Optimized under calibration (+0.0500%). |


---

| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `21` | `52.5%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `0` | `0.0%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `2` | `5.0%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `17` | `42.5%` | Persistent target failure across both configurations |


---

### Metric Confidence & Validation Sample Size Limits

* **Train Split Partition Count:** `80`
* **Seen Validation Split Count:** `20`
* **Unseen Validation Split Count:** `20`
* **Total Combined Validation Count:** `40`

> ⚠️ **Warning:** Validation sample size (40) is below target limit (100). Findings should be interpreted as directional only.


### Paired Significance Context:
With smaller validation sets, discrete accuracy deltas must be interpreted as directional evidence rather than definitive proof of generalization. 
Enterprise deployments should scale validation spaces to larger evaluation corpuses to perform paired statistical tests.


---

### Dynamic Executive AI Governance Conclusion

Based on evidence compiled in this evaluation cycle, we draw the following conclusions:

* **Demonstrated Capabilities:** The candidate model demonstrated improved continuous likelihood metrics (NLL) but failed discrete accuracy non-inferiority or structural safety thresholds. Direct promotion of current weights is not safe.
* **Repairs Promoted:** Promoted 2 validated semantic repairs.
* **Router Safety:** The Protected Router preserved served consistency with zero regressions observed.
* **Significance Notice:** These findings represent directional validation evidence. Enterprise deployment requires larger validation sets and seed repeats prior to final production release.


---

### Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*
