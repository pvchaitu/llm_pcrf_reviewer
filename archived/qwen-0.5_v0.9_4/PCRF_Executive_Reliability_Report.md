# PCRF Transformer Reliability Executive Report
**Causal Reliability Flow & Derivative-Weighted Diagnostics Dashboard**

---

### [Customer Executive Summary Box]
* **What Happened?**
  The candidate model's Seen Validation exact-match accuracy was unchanged, while the Unseen Validation Generalization accuracy was regressed by -5.00 percentage points. Generalization Negative Log-Likelihood (NLL) improved (decreased) by 0.3042, and Perplexity (PPL) improved (decreased) by 17.12.
* **Why was Direct Adoption Accepted/Rejected?**
  Direct adoption was REJECTED (DO_NOT_APPLY) due to active safety and performance gate failures: Overall system chain reliability R_sys (38.47%) vs floor (75.0%).; Zero correct-to-wrong regressions required. Found 1 regressions.; Unseen accuracy improvement (-5.00%) vs requirement (2.0%).; Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -5.00%)..
* **What did PCRF Prove in This Run?**
  PCRF demonstrated essential risk-containment and non-regression governance by intercepting 1 catastrophic output regression(s) and serving safe baseline fallbacks.
* **Recommended Next Step:**
  REJECT direct parameter weight promotion. Maintain pre-training baseline model weights. Enable the Protected Router in production to serve validated candidate repairs while safely falling back to baseline on regressions.

---

## 1. Core Gating Status

* **Direct Candidate Weight Promotion Status:** `DO_NOT_APPLY`
* **Safe Diagnostic Components:** derivative diagnostics, curriculum curation, structural monitoring, protected routing
* **Unsafe Components:** direct weight promotion of the current regularized candidate weights
* **Measurement-Only Components:** candidate weights
* **Router Governance Status:** Active Zero-Regression Gating Enabled


---

## 2. Metrics At-a-Glance

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Served Delta | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 65.00% | 65.00% | 65.00% | +0.00% | +0.00% | Candidate Unchanged (+0.0000%), Served Unchanged (+0.0000%). |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 65.00% | 60.00% | 65.00% | -5.00% | +0.00% | Candidate Worsened (-0.0500%), Served Unchanged (+0.0000%). |
| Seen Validation NLL | Lower is Better ⬇️ | 4.3207 | 3.7314 | 4.1910 | -0.5893 | -0.1297 | Candidate Improved (-0.5893), Served Improved (-0.1297). |
| Unseen Validation NLL | Lower is Better ⬇️ | 4.1787 | 3.8745 | 4.1772 | -0.3042 | -0.0016 | Candidate Improved (-0.3042), Served Improved (-0.0016). |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 65.2841 | 48.1609 | 65.1822 | -17.1232 | -0.1019 | Candidate Improved (-17.1232), Served Improved (-0.1019). |
| Strict EM Accuracy | Higher is Better ⬆️ | 7.50% | 0.00% | 7.50% | -7.50% | +0.00% | Candidate Worsened (-0.0750%), Served Unchanged (+0.0000%). |
| First-Token Target Match | Higher is Better ⬆️ | 35.00% | 42.50% | 40.00% | +7.50% | +5.00% | Candidate Improved (+0.0750%), Served Improved (+0.0500%). |
| Semantic Target Capture | Higher is Better ⬆️ | 65.00% | 62.50% | 65.00% | -2.50% | +0.00% | Candidate Worsened (-0.0250%), Served Unchanged (+0.0000%). |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 57.50% | 62.50% | 57.50% | +5.00% | +0.00% | Candidate Worsened (+0.0500%), Served Unchanged (+0.0000%). |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 4.2497 | 3.8030 | 4.1841 | -0.4467 | -0.0656 | Candidate Improved (-0.4467), Served Improved (-0.0656). |


---

## 3. Promotion Decision Evidence

| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🔴 FAIL | CRITICAL | 0.3847 | 0.7500 | Overall system chain reliability R_sys (38.47%) vs floor (75.0%). |
| Correct-to-Wrong Regressions Count | 🔴 FAIL | CRITICAL | 1 | 0 | Zero correct-to-wrong regressions required. Found 1 regressions. |
| Critical High-Priority Regressions | 🟢 PASS | CRITICAL | 0 | 0 | Zero critical high-priority regressions required. Found 0 regressions. |
| Seen Accuracy Non-Inferiority Margin | 🟢 PASS | HIGH | 0.0000 | 0.0100 | Seen accuracy drop (0.00%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | 0.0000 | 0.0300 | Seen accuracy degradation (0.00%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🔴 FAIL | HIGH | -0.0500 | 0.0200 | Unseen accuracy improvement (-5.00%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🔴 FAIL | CRITICAL | -0.0500 | 0.0000 | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found -5.00%). |


---

### Structural Reliability Model Reconciliation

To ensure mathematical rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `38.47%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `100.00%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `100.00%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.00%` (Gate Role: localized adapter targeting signal)

**Disagreement Reconciliation:** The conservative strict-series veto triggered (`38.47%` < `75.0%`) while the residual-aware CREW metric remained healthy (`100.00%` >= `95.0%`). This represents a conservative promotion rejection under the configured gate policy, prioritizing raw multi-sequence robustness over localized bypass paths.

> ⚠️ **Report Consistency Warning:** Displayed individual layer survival probabilities appear near-perfect while the combined system chain reliability is significantly lower (`38.47%`). This represents a granularity and recursion mismatch: the individual layers reflect localized resilience (carrying bypass signals), whereas the strict system reliability evaluates the un-bypassed sequential dependency of the entire chain.



---

## 4. Layer Sensitivity & Bottleneck Selection

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 1, 6, 12, 21, 22, 23`
* **Highest Empirical Sensitivity Layer:** Layer `1` (Empirical Delta: `0.01200`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `23` (Birnbaum Index: `0.65482`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom regularizer SFT parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.


---

## 5. Hallucination, Target Failure & Contract Compliance Audit

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `14` | Validation prompts where baseline failed to capture semantic target. |
| **Active Hallucination Repairs Promoted** | `0` | Baseline errors cleanly resolved and promoted in candidate. |
| **Candidate Over-Steers Prevented** | `13` | Both models failed, but candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `1` | Baseline was correct but candidate failed; router served baseline fallback. |
| **Net Gateway Interventions** | `14` | Overall cases actively guarded by the Protected Router (100% active coverage). |


---

## 6. Protected Router Benefit Accounting

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `1` | Fallback to baseline on candidate failure |
| **Repairs Promoted** | `0` | Upgrade to candidate on verified repair |
| **Over-steers Prevented** | `13` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** The router successfully blocked 1 regression(s) where candidate degraded baseline correct outputs. This demonstrates absolute regression safety.
* **Generalization Repair:** No clean semantic repairs were promoted in this run.



---

## 7. Transition Analysis

| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `25` | `62.5%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `1` | `2.5%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `0` | `0.0%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `14` | `35.0%` | Persistent target failure across both configurations |


---

## 8. Dynamic Showcase Cases

### Showcase Case 1: ID 120 (unseen_val)
* **Operational Category:** Regression Blocked: Baseline was correct but candidate regressed; protected router successfully intervened.
* **Prompt:** *Complete with one word only: The physical block boundary used to serialize hard drive data tracks is a*
* **Expected Target:** `Sector`
* **Outputs:** Baseline=`(n) ________.<br>A. Track<br>B. Sector` (Risk: 0.4062) | Candidate=`(n) ________.<br>A. cylinder<br>B. head` (Risk: 0.4443)
* **Latent Telemetry:** Baseline Top-1 Prob: `9.72%` | Candidate Top-1 Prob: `4.47%` | Delta: `-0.0525`
* **Router Action:** `use_baseline` -> **Served Output:** `(n) ________.<br>A. Track<br>B. Sector`
* **Protected Router Decision Explanation:** *Candidate blocked because baseline captured the target and candidate failed.*

### Showcase Case 2: ID 086 (seen_val)
* **Operational Category:** Over-steer Prevented: Both failed target capture, but candidate displayed higher latent risk; baseline fallback served.
* **Prompt:** *Complete with one word only: The noble element designated by atomic number 10 is*
* **Expected Target:** `Neon`
* **Outputs:** Baseline=`____<br>A. Sodium<br>B. Magnesium<br>C` (Risk: 0.3781) | Candidate=`____<br>A. Sodium<br>B. Magnesium<br>C` (Risk: 0.4256)
* **Latent Telemetry:** Baseline Top-1 Prob: `19.14%` | Candidate Top-1 Prob: `13.18%` | Delta: `-0.0596`
* **Router Action:** `use_baseline` -> **Served Output:** `____<br>A. Sodium<br>B. Magnesium<br>C`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; baseline retained because candidate risk was higher.*

### Showcase Case 3: ID 084 (seen_val)
* **Operational Category:** Preserved Stricter Contract: Both captured semantic target, but candidate violated format constraints; baseline output served.
* **Prompt:** *Complete with one word only: The official capital city of Switzerland is*
* **Expected Target:** `Bern`
* **Outputs:** Baseline=`___________.<br>A. Bern<br>B. Zurich` (Risk: 0.3495) | Candidate=`___________.<br>A. Bern<br>B. Zurich` (Risk: 0.3881)
* **Latent Telemetry:** Baseline Top-1 Prob: `28.91%` | Candidate Top-1 Prob: `24.80%` | Delta: `-0.0410`
* **Router Action:** `use_baseline` -> **Served Output:** `___________.<br>A. Bern<br>B. Zurich`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

### Showcase Case 4: ID 087 (seen_val)
* **Operational Category:** Transition trace display for analysis (wrong_to_wrong).
* **Prompt:** *Complete with one word only: The volatile element designated by atomic number 16 is*
* **Expected Target:** `Sulfur`
* **Outputs:** Baseline=`____<br>A. Sodium<br>B. Magnesium<br>C` (Risk: 0.3837) | Candidate=`____<br>A. Sodium<br>B. Magnesium<br>C` (Risk: 0.4331)
* **Latent Telemetry:** Baseline Top-1 Prob: `16.31%` | Candidate Top-1 Prob: `11.08%` | Delta: `-0.0522`
* **Router Action:** `use_baseline` -> **Served Output:** `____<br>A. Sodium<br>B. Magnesium<br>C`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; baseline retained because candidate risk was higher.*



---

## 9. Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 0 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 0 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 15 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 25 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 0 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration regularization. |


*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 10. Metric Confidence & Validation Sample Size Limits

* **Train Split Partition Count:** `80`
* **Seen Validation Split Count:** `20`
* **Unseen Validation Split Count:** `20`
* **Total Combined Validation Count:** `40`

> ⚠️ **Warning:** Validation sample size (40) is below target limit (100). Findings should be interpreted as directional only.


### Paired Significance Context:
With smaller validation sets, discrete accuracy deltas must be interpreted as directional evidence rather than definitive proof of generalization. 
Enterprise deployments should scale validation spaces to larger evaluation corpuses to perform paired statistical tests.


---

## 11. Failed Generations Debug Trace Table

The following trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | Candidate Output | Baseline NLL |
|---|---|---|---|---|---|---|
| seen_val | 86 | *Complete with one word only: The noble element ...* | `Neon` | `____<br>A. Sodium<br>B. Mag...` | `____<br>A. Sodium<br>B. Mag...` | 9.9375 |
| seen_val | 87 | *Complete with one word only: The volatile eleme...* | `Sulfur` | `____<br>A. Sodium<br>B. Mag...` | `____<br>A. Sodium<br>B. Mag...` | 3.3125 |
| seen_val | 89 | *Complete with one word only: The yellow dwarf s...* | `Sun` | `closest star to Earth, and ...` | `closest star to Earth, and ...` | 3.2031 |
| seen_val | 90 | *Complete with one word only: Mechanical acousti...* | `Vacuum` | `medium. They are only able ...` | `medium. They are only able ...` | 12.5000 |
| seen_val | 96 | *Complete with one word only: To enforce unique ...* | `Set` | `technique called "hashing."...` | `technique called hashing. H...` | 6.5625 |
| seen_val | 98 | *Complete with one word only: An execution failu...* | `Bug` | `(n) ________.<br>A. Logical...` | `(n) ____.<br>A. Error<br>B....` | 10.6875 |
| seen_val | 99 | *Complete with one word only: A standardized tex...* | `JSON` | `called a ____.<br>A. Struct...` | `called a ____.<br>A. Struct...` | 10.4375 |
| unseen_val | 106 | *Complete with one word only: Mammalian red bloo...* | `Oxygen` | `substances in the body. The...` | `substances in the body. The...` | 9.1875 |
| unseen_val | 109 | *Complete with one word only: The dual-helix mac...* | `DNA` | `called a(n) ________.<br>A....` | `the ______ of the cell.<br>...` | 6.0625 |
| unseen_val | 111 | *Complete with one word only: An unexpected, com...* | `blue` | `ordinary. The word is "unus...` | `ordinary. An unexpected, co...` | 3.0312 |
| ... | ... | ... | ... | ... | ... | *(And 5 more trace details)* |



---

## 12. Dynamic Executive AI Governance Conclusion

Based on evidence compiled in this evaluation cycle, we draw the following conclusions:

* **Demonstrated Capabilities:** The candidate model demonstrated improved continuous likelihood metrics (NLL) but failed discrete accuracy non-inferiority or structural safety thresholds. Direct promotion of current weights is not safe.
* **Repairs Promoted:** No clean hallucination repairs were promoted in this run.
* **Router Safety:** The Protected Router successfully preserved baseline served accuracy by blocking 1 regressions.
* **Significance Notice:** These findings represent directional validation evidence. Enterprise deployment requires larger validation sets and seed repeats prior to final production release.


---

## 13. Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*

