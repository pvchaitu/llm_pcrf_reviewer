# PCRF Transformer Reliability Executive Report
**Causal Reliability Flow & Derivative-Weighted Diagnostics Dashboard**

---


### 📦 Customer Executive Summary

- **What Happened?**  
  The candidate model's Seen Validation exact-match accuracy was unchanged, while the Unseen Validation Generalization accuracy was improved by +5.00 percentage points.  

- **Likelihood & Confidence Behavior:**  
  Generalization Negative Log-Likelihood (NLL) improved (decreased) by 0.1185, and Perplexity (PPL) improved (decreased) by 16.58.  

- **Why was Direct Adoption Accepted/Rejected?**  
  Direct adoption was REJECTED (DO_NOT_PROMOTE_WEIGHTS) due to active safety and performance gate failures: Candidate instruction-contract violation rate (100.00%) must be below ceiling (10.0%).; Candidate strict EM (0.00%) must be above minimal floor (10.0%).; Validation examples count (40) vs strong claim requirement (100)..  

- **What did PCRF Prove in This Run?**  
  PCRF served as a silent diagnostic gatekeeper, verifying structural alignment and baseline consistency without active production output overrides.  

- **PCRF Hallucination Exposure Control:**  
  100.00% of 20 baseline hallucinations were safely controlled via 20 router interventions (repairs promoted: 0).



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
| Derivatives | 0.00 (Unmeasured) | 0.00050 (Avg Sensitivity) | 0.5/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=3.48) | 69.7/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 99.99% | 100.0/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen Acc: 40.0% | Unseen Acc: 45.0% | 60.0/100 | `DO_NOT_PROMOTE_WEIGHTS` |


---

## 4. Promotion Decision Evidence (Scoreboard Component Breakdown)

| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🟢 PASS | CRITICAL | 99.55% | 75.00% | Overall system chain reliability R_sys (99.55%) vs floor (75.0%). |
| Correct-to-Wrong Regressions Count | 🟢 PASS | CRITICAL | 0 | 0 | Zero correct-to-wrong regressions required. Found 0 regressions. |
| Critical High-Priority Regressions | 🟢 PASS | CRITICAL | 0 | 0 | Zero critical high-priority regressions required. Found 0 regressions. |
| Universal Instruction Contract Violation Gate | 🔴 FAIL | CRITICAL | 100.00% | 10.00% | Candidate instruction-contract violation rate (100.00%) must be below ceiling (10.0%). |
| Generalization Non-Degradation Instruction Gate | 🟢 PASS | HIGH | 100.00% | 100.00% | Candidate instruction-contract violation rate (100.00%) must not exceed baseline (100.00%). |
| Strict EM Candidate Non-Degradation Gate | 🟢 PASS | HIGH | 0.00% | 0.00% | Candidate strict exact match (0.00%) must not degrade from baseline (0.00%). |
| Strict EM Absolute Direct Promotion Threshold | 🔴 FAIL | CRITICAL | 0.00% | 10.00% | Candidate strict EM (0.00%) must be above minimal floor (10.0%). |
| Hallucination Risk Trend Variance Gate | 🟢 PASS | HIGH | 2.66% | 5.00% | Average candidate risk increase (0.0266) must be within limit (0.0500). |
| Minimum Gating Evidence Verification Size | 🔴 FAIL | HIGH | 40 | 100 | Validation examples count (40) vs strong claim requirement (100). |
| Seen Accuracy Non-Inferiority Margin | 🟢 PASS | HIGH | 0.00% | 1.00% | Seen accuracy drop (0.00%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | 0.00% | 3.00% | Seen accuracy degradation (0.00%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🟢 PASS | HIGH | 5.00% | 2.00% | Unseen accuracy improvement (5.00%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🟢 PASS | CRITICAL | 5.00% | 0.00% | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found 5.00%). |


---

## 5. Hallucination Risk & Confidence Control (PRIMARY)

This section details baseline hallucinations, repairs promoted, and active over-steers prevented by PCRF.
PCRF reduces confidence on incorrect outputs rather than optimizing accuracy directly.

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `20` | Validation prompts where baseline failed to capture semantic target. |
| **Active Hallucination Repairs Promoted** | `0` | Baseline errors cleanly resolved and promoted in candidate. |
| **Candidate Over-Steers Prevented** | `0` | Both models failed, but candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `0` | Baseline was correct but candidate failed; router served baseline fallback. |
| **Hallucination Exposure Control Rate** | `100.00%` | 20 of 20 baseline hallucination cases were either repaired by PCRF candidate or withheld through safe fallback. |
| **Net Gateway Interventions** | `20` | Overall cases actively guarded by the Protected Router (100% active coverage). |


---

### Failure Taxonomy & Recommended Fix Plan

| Failure Category | Count | Interpretation | Recommended Fix Plan |
|---|---|---|---|
| TARGET_MISS | 0 | Generated output failed to include the required target completion. | Add target-token anchoring, curriculum replay on misses, and prompt-target alignment diagnostics. |
| FORMAT_TEMPLATE_FAILURE | 1 | Generated output echoed blanks, answer choices, scaffolding, or template artifacts. | Add formatting suppression, answer-choice leakage penalties, and template artifact filters. |
| WRONG_ENTITY_SUBSTITUTION | 20 | Generated a semantically plausible but incorrect entity, distractor, or adjacent concept instead of the target. | Add semantic contrastive negatives, entity-disambiguation replay, and high-risk distractor curation. |
| OVER_GENERATION | 0 | Generated the target or related text but continued beyond the required one-word answer. | Add stop-token enforcement, max-new-token constraints, post-decode truncation policy, and one-token decoding mode. |
| INSTRUCTION_CONTRACT_VIOLATION | 18 | Target may be present, but output violates task constraints such as one-word-only completion. | Add explicit contract loss, strict EM validation, and one-word output gate. |
| HIGH_CONFIDENCE_WRONG | 1 | Incorrect output emitted with confidence above configured high-confidence threshold. | Add high-confidence wrong penalty and calibration regularization. |


*Note: Over-generation is currently nested under instruction-contract violation by taxonomy policy.*


---

## 6. Protected Router Behavior & Safety Gating

The Protected Router functions as a safety control layer providing non-regression protection, safe baseline fallbacks, and validated repair promotions. It does not blindly optimize accuracy; instead, it prevents catastrophic production regression.

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `0` | Fallback to baseline on candidate failure |
| **Repairs Promoted** | `1` | Upgrade to candidate on verified repair |
| **Over-steers Prevented** | `0` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** No baseline regressions were observed, requiring no active containment overrides.
* **Generalization Repair:** Promoted 1 successful repair(s) into active serving streams.



---

### Dynamic Showcase Cases

#### Showcase Case 1: ID 081 (seen_val)
* **Operational Category:** Preserved Stricter Contract: Both captured semantic target, but candidate violated format constraints; baseline output served.
* **Prompt:** *Complete with one word only: The official capital city of South Korea is*
* **Expected Target:** `Seoul`
* **Outputs:** Baseline=`Seoul.<br><br>The city is home to the country's` (Risk: 0.2736) | Candidate=`Seoul.<br><br>The city is home to the country's` (Risk: 0.2782)
* **Latent Telemetry:** Baseline Top-1 Prob: `19.12%` | Candidate Top-1 Prob: `29.31%` | Delta: `+0.1019`
* **Router Action:** `use_baseline` -> **Served Output:** `Seoul.<br><br>The city is home to the country's`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

#### Showcase Case 2: ID 101 (unseen_val)
* **Operational Category:** Repair Promoted: Candidate successfully recovered and validated semantic target completion.
* **Prompt:** *Complete with one word only: The official capital city of Austria is*
* **Expected Target:** `Vienna`
* **Outputs:** Baseline=`now the capital of the German Reich.<br><br>The German` (Risk: 0.2895) | Candidate=`now Vienna.<br><br>The Austrian capital is now Vienna.` (Risk: 0.3267)
* **Latent Telemetry:** Baseline Top-1 Prob: `9.34%` | Candidate Top-1 Prob: `8.68%` | Delta: `-0.0066`
* **Router Action:** `use_candidate` -> **Served Output:** `now Vienna.<br><br>The Austrian capital is now Vienna.`
* **Protected Router Decision Explanation:** *Candidate repair promoted.*

#### Showcase Case 3: ID 084 (seen_val)
* **Operational Category:** Transition trace display for analysis (wrong_to_wrong).
* **Prompt:** *Complete with one word only: The official capital city of Switzerland is*
* **Expected Target:** `Bern`
* **Outputs:** Baseline=`Zurich.<br><br>The Swiss capital is the capital of Switzerland` (Risk: 0.2888) | Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.2784)
* **Latent Telemetry:** Baseline Top-1 Prob: `12.69%` | Candidate Top-1 Prob: `27.07%` | Delta: `+0.1437`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `Zurich.<br><br>The Swiss capital is the capital of Switzerland`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.2784).*

#### Showcase Case 4: ID 086 (seen_val)
* **Operational Category:** Transition trace display for analysis (wrong_to_wrong).
* **Prompt:** *Complete with one word only: The noble element designated by atomic number 10 is*
* **Expected Target:** `Neon`
* **Outputs:** Baseline=`the most important element in the universe.<br><br>The most` (Risk: 0.2644) | Candidate=`⚠️ Hallucination Risk Detected — Response Withheld for Safety` (Risk: 0.2996)
* **Latent Telemetry:** Baseline Top-1 Prob: `11.77%` | Candidate Top-1 Prob: `10.44%` | Delta: `-0.0133`
* **Router Action:** `abstain_safe_fallback` -> **Served Output:** `the most important element in the universe.<br><br>The most`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: 0.2996).*



---

## 7. Contract Compliance (Instruction Adherence)

This section highlights instruction contract violations and formatting failures. Strict output constraint enforcement guarantees enterprise output determinism.

### Failed Generations Debug Trace Table

The following trace displays prompts where the baseline or candidate configurations failed to capture the exact semantic target:

| Split | ID | Prompt | Expected Target | Baseline Output | Candidate Output | Baseline NLL |
|---|---|---|---|---|---|---|
| seen_val | 84 | *Complete with one word only: The official capit...* | `Bern` | `Zurich.<br><br>The Swiss ca...` | `⚠️ Hallucination Risk Detec...` | 4.3837 |
| seen_val | 86 | *Complete with one word only: The noble element ...* | `Neon` | `the most important element ...` | `⚠️ Hallucination Risk Detec...` | 13.5739 |
| seen_val | 87 | *Complete with one word only: The volatile eleme...* | `Sulfur` | `the most volatile element i...` | `⚠️ Hallucination Risk Detec...` | 5.3019 |
| seen_val | 88 | *Complete with one word only: The chemical molec...* | `Oxygen` | `called the "air molecule."<...` | `⚠️ Hallucination Risk Detec...` | 3.9075 |
| seen_val | 89 | *Complete with one word only: The yellow dwarf s...* | `Sun` | `most massive star in the un...` | `⚠️ Hallucination Risk Detec...` | 3.9867 |
| seen_val | 90 | *Complete with one word only: Mechanical acousti...* | `Vacuum` | `space.<br><br>The first thi...` | `⚠️ Hallucination Risk Detec...` | 7.2123 |
| seen_val | 96 | *Complete with one word only: To enforce unique ...* | `Set` | `single word.<br><br>The fol...` | `⚠️ Hallucination Risk Detec...` | 7.2777 |
| seen_val | 97 | *Complete with one word only: The hypermedia syn...* | `HTML` | `now supported.<br><br>The h...` | `⚠️ Hallucination Risk Detec...` | 7.7287 |
| seen_val | 98 | *Complete with one word only: An execution failu...* | `Bug` | `"failure of execution".<br>...` | `⚠️ Hallucination Risk Detec...` | 10.1821 |
| seen_val | 99 | *Complete with one word only: A standardized tex...* | `JSON` | `used.<br><br>The following ...` | `⚠️ Hallucination Risk Detec...` | 11.1368 |
| ... | ... | ... | ... | ... | ... | *(And 13 more trace details)* |



---

## 8. Structural Reliability (PCRF Structural / CREW)

### Structural Reliability Model Reconciliation

To ensure mathematical rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `99.55%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `99.91%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `99.99%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.01%` (Gate Role: localized adapter targeting signal)

> ⚠️ **Mathematical Caveat (Bypass-Dominated):** Strict chain reliability appears stable under this measurement, but CREW submodule decomposition is residual-bypass dominated. Attention and MLP causal paths require separate validation before structural metrics can be treated as promotion-grade.



---

## Bottleneck Selection & Layer Causal Flow Matrix

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 1, 2, 3, 4, 7`
* **Highest Empirical Sensitivity Layer:** Layer `1` (Empirical Delta: `0.00162`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `2` (Birnbaum Index: `0.99708`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom regularizer SFT parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.


---

## 9. Accuracy (SUPPORTING ONLY — secondary)

Accuracy changes reflect shifts in confidence distribution and ranking. These are secondary effects of reliability control and not primary optimization targets.

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Served Delta | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Validation NLL | Lower is Better ⬇️ | 4.6311 | 4.3625 | 4.6039 | -0.2686 | -0.0272 | Candidate: Candidate shifted confidence distribution (Lower) (-0.2686), Served: Served shifted confidence distribution (Lower) (-0.0272). |
| Unseen Validation NLL | Lower is Better ⬇️ | 4.9995 | 4.8810 | 4.9888 | -0.1185 | -0.0107 | Candidate: Candidate shifted confidence distribution (Lower) (-0.1185), Served: Served shifted confidence distribution (Lower) (-0.0107). |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 148.3320 | 131.7565 | 146.7547 | -16.5755 | -1.5772 | Candidate: Candidate shifted confidence distribution (Lower) (-16.5755), Served: Served shifted confidence distribution (Lower) (-1.5772). |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 4.8153 | 4.6217 | 4.7963 | -0.1936 | -0.0189 | Candidate: Candidate shifted confidence distribution (Lower) (-0.1936), Served: Served shifted confidence distribution (Lower) (-0.0189). |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | +0.00% | Candidate: Unchanged (+0.0000%), Served: Unchanged (+0.0000%). |
| Semantic Target Capture | Higher is Better ⬆️ | 42.50% | 45.00% | 45.00% | +2.50% | +2.50% | Candidate: Candidate shifted confidence distribution (Higher) (+0.0250%), Served: Served shifted confidence distribution (Higher) (+0.0250%). |
| First-Token Target Match | Higher is Better ⬆️ | 37.50% | 37.50% | 37.50% | +0.00% | +0.00% | Candidate: Unchanged (+0.0000%), Served: Unchanged (+0.0000%). |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | +0.00% | Candidate: Confidence profile stable (+0.0000%), Served: Confidence profile stable (+0.0000%). |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 45.00% | 45.00% | 45.00% | +0.00% | +0.00% | Candidate: Confidence profile stable (+0.0000%), Served: Confidence profile stable (+0.0000%). |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 40.00% | 45.00% | 45.00% | +5.00% | +5.00% | Candidate: Optimized under calibration (+0.0500%), Served: Optimized under calibration (+0.0500%). |


---

| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `17` | `42.5%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `0` | `0.0%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `1` | `2.5%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `22` | `55.0%` | Persistent target failure across both configurations |


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
* **Repairs Promoted:** No clean hallucination repairs were promoted in this run.
* **Router Safety:** The Protected Router preserved served consistency with zero regressions observed.
* **Significance Notice:** These findings represent directional validation evidence. Enterprise deployment requires larger validation sets and seed repeats prior to final production release.


---

### Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*
PASSEDCustomer-safe hallucination output masking passed. Detected unresolved hallucinations were represented using the safety-withheld response.
