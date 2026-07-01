# PCRF Transformer Reliability Executive Report
**Causal Reliability Flow & Derivative-Weighted Diagnostics Dashboard**

---

### [Customer Executive Summary Box]
* **What Happened?**
  The candidate model's Seen Validation exact-match accuracy was unchanged, while the Unseen Validation Generalization accuracy was improved by +5.00 percentage points. Generalization Negative Log-Likelihood (NLL) improved (decreased) by 0.1185, and Perplexity (PPL) improved (decreased) by 16.58.
* **Why was Direct Adoption Accepted/Rejected?**
  Adoption was APPROVED (SAFE_TO_APPLY) as all accuracy, continuous likelihood, and structural reliability constraints were fully satisfied.
* **What did PCRF Prove in This Run?**
  PCRF demonstrated repair promotion capabilities by successfully validating and promoting 1 correct candidate response(s).
* **Recommended Next Step:**
  Approved for weight promotion. Deploy optimized parameters directly into production under canary router surveillance.

---

## 1. Core Gating Status

* **Direct Candidate Weight Promotion Status:** `SAFE_TO_APPLY`
* **Safe Diagnostic Components:** derivative diagnostics, curriculum curation, structural monitoring, protected routing, direct weight promotion of optimized candidate weights
* **Unsafe Components:** None
* **Measurement-Only Components:** None
* **Router Governance Status:** Active Zero-Regression Gating Enabled


---

## 2. Metrics At-a-Glance

| Metric Dimension | Direction | Baseline | Candidate | Served Router | Candidate Delta | Served Delta | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Seen Exact-Match Accuracy | Higher is Better ⬆️ | 45.00% | 45.00% | 45.00% | +0.00% | +0.00% | Candidate Unchanged (+0.0000%), Served Unchanged (+0.0000%). |
| Unseen Generalization Accuracy | Higher is Better ⬆️ | 40.00% | 45.00% | 45.00% | +5.00% | +5.00% | Candidate Improved (+0.0500%), Served Improved (+0.0500%). |
| Seen Validation NLL | Lower is Better ⬇️ | 4.6311 | 4.3625 | 4.5640 | -0.2686 | -0.0671 | Candidate Improved (-0.2686), Served Improved (-0.0671). |
| Unseen Validation NLL | Lower is Better ⬇️ | 4.9995 | 4.8810 | 4.9888 | -0.1185 | -0.0107 | Candidate Improved (-0.1185), Served Improved (-0.0107). |
| Unseen Perplexity (PPL) | Lower is Better ⬇️ | 148.3320 | 131.7565 | 146.7547 | -16.5755 | -1.5772 | Candidate Improved (-16.5755), Served Improved (-1.5772). |
| Strict EM Accuracy | Higher is Better ⬆️ | 0.00% | 0.00% | 0.00% | +0.00% | +0.00% | Candidate Unchanged (+0.0000%), Served Unchanged (+0.0000%). |
| First-Token Target Match | Higher is Better ⬆️ | 37.50% | 37.50% | 37.50% | +0.00% | +0.00% | Candidate Unchanged (+0.0000%), Served Unchanged (+0.0000%). |
| Semantic Target Capture | Higher is Better ⬆️ | 42.50% | 45.00% | 45.00% | +2.50% | +2.50% | Candidate Improved (+0.0250%), Served Improved (+0.0250%). |
| Instruction Contract Violation Rate | Lower is Better ⬇️ | 100.00% | 100.00% | 100.00% | +0.00% | +0.00% | Candidate Unchanged (+0.0000%), Served Unchanged (+0.0000%). |
| Average Cross-Entropy Loss (NLL) | Lower is Better ⬇️ | 4.8153 | 4.6217 | 4.7764 | -0.1936 | -0.0389 | Candidate Improved (-0.1936), Served Improved (-0.0389). |


---

## 3. Integrated PCRF Scoreboard

| Feature Track / Module | Baseline Value | PCRF Result Value | Track Score | Gating Status |
|---|---|---|---|---|
| Derivatives | 0.00 (Unmeasured) | 0.00050 (Avg Sensitivity) | 0.5/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=3.48) | 69.7/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 100.00% | 100.0/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen Acc: 40.0% | Unseen Acc: 45.0% | 100.0/100 | `SAFE_TO_APPLY` |


---

## 4. Promotion Decision Evidence (**Breakup of Scoreboard)

| Gate Check Name | Passed? | Severity | Metric Value | Threshold / Limit | Check Explanation |
|---|---|---|---|---|---|
| Structural Reliability Floor | 🟢 PASS | CRITICAL | 0.9955 | 0.7500 | Overall system chain reliability R_sys (99.55%) vs floor (75.0%). |
| Correct-to-Wrong Regressions Count | 🟢 PASS | CRITICAL | 0 | 0 | Zero correct-to-wrong regressions required. Found 0 regressions. |
| Critical High-Priority Regressions | 🟢 PASS | CRITICAL | 0 | 0 | Zero critical high-priority regressions required. Found 0 regressions. |
| Seen Accuracy Non-Inferiority Margin | 🟢 PASS | HIGH | 0.0000 | 0.0100 | Seen accuracy drop (0.00%) vs non-inferiority margin (1.0%). |
| Seen Accuracy Degradation Budget | 🟢 PASS | CRITICAL | 0.0000 | 0.0300 | Seen accuracy degradation (0.00%) vs budget (3.0%). |
| Unseen Accuracy Improvement | 🟢 PASS | HIGH | 0.0500 | 0.0200 | Unseen accuracy improvement (5.00%) vs requirement (2.0%). |
| Generalization Non-Degradation Guard | 🟢 PASS | CRITICAL | 0.0500 | 0.0000 | Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found 5.00%). |


---

### Structural Reliability Model Reconciliation

To ensure mathematical rigor, the framework evaluates multiple dimensions of representation integrity:

* **Strict Series $R_{sys}$:** `99.55%` (Gate Role: `conservative_promotion_veto`)
* **CREW Product $R_{sys}$:** `100.00%` (Gate Role: `residual_aware_diagnostic`)
* **CREW Geometric Reliability:** `100.00%` (Gate Role: primary continuous diagnostic invariant)
* **Worst-k CREW Bottleneck Risk:** `0.00%` (Gate Role: localized adapter targeting signal)

**Disagreement Reconciliation:** All structural metrics are in agreement; the representation spaces are stable.



---

## 4. Layer Sensitivity & Bottleneck Selection

* **Active Bottleneck Selection Policy:** `union_empirical_and_birnbaum`
* **Selected Intervention Layers:** `0, 1, 2, 3, 4, 7`
* **Highest Empirical Sensitivity Layer:** Layer `1` (Empirical Delta: `0.00162`)
* **Highest Birnbaum Sensitivity Layer (Structural Sensitivity metric D_R):** Layer `2` (Birnbaum Index: `0.99713`)

### Selection Policy Interpretation:
Under policy `union_empirical_and_birnbaum`, the intervention set is configured as the target for custom regularizer SFT parameters. 
Applying adapters specifically to these bottleneck blocks protects the mid-layer latent highway from drift and preserves structural alignment.


---

## 5. Hallucination, Target Failure & Contract Compliance Audit

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `23` | Validation prompts where baseline failed to capture semantic target. |
| **Active Hallucination Repairs Promoted** | `1` | Baseline errors cleanly resolved and promoted in candidate. |
| **Candidate Over-Steers Prevented** | `21` | Both models failed, but candidate risk was higher; baseline served. |
| **Catastrophic Regressions Blocked** | `0` | Baseline was correct but candidate failed; router served baseline fallback. |
| **Net Gateway Interventions** | `22` | Overall cases actively guarded by the Protected Router (100% active coverage). |


---

## 6. Protected Router Benefit Accounting

| Routing Action Type | Action Count | Operational Role |
|---|:---:|---|
| **Regressions Blocked** | `0` | Fallback to baseline on candidate failure |
| **Repairs Promoted** | `1` | Upgrade to candidate on verified repair |
| **Over-steers Prevented** | `21` | Fallback to baseline when candidate risk spikes |

### Served Output Impact:
**Regression Containment:** No baseline regressions were observed, requiring no active containment overrides.
* **Generalization Repair:** Promoted 1 successful repair(s) into active serving streams.



---

## 7. Transition Analysis

| Transition Type | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| **Correct ➔ Correct** | `17` | `42.5%` | Semantic target preserved across both models |
| **Correct ➔ Wrong (Regression)** | `0` | `0.0%` | Candidate degraded baseline correct output |
| **Wrong ➔ Correct (Repair)** | `1` | `2.5%` | Candidate successfully resolved baseline error |
| **Wrong ➔ Wrong (Persistent)** | `22` | `55.0%` | Persistent target failure across both configurations |


---

## 8. Dynamic Showcase Cases

### Showcase Case 1: ID 086 (seen_val)
* **Operational Category:** Over-steer Prevented: Both failed target capture, but candidate displayed higher latent risk; baseline fallback served.
* **Prompt:** *Complete with one word only: The noble element designated by atomic number 10 is*
* **Expected Target:** `Neon`
* **Outputs:** Baseline=`the most important element in the universe.<br><br>The most` (Risk: 0.2644) | Candidate=`the most important element in the universe.<br><br>The most` (Risk: 0.2996)
* **Latent Telemetry:** Baseline Top-1 Prob: `11.77%` | Candidate Top-1 Prob: `10.44%` | Delta: `-0.0133`
* **Router Action:** `use_baseline` -> **Served Output:** `the most important element in the universe.<br><br>The most`
* **Protected Router Decision Explanation:** *Candidate over-steer prevented; baseline retained because candidate risk was higher.*

### Showcase Case 2: ID 081 (seen_val)
* **Operational Category:** Preserved Stricter Contract: Both captured semantic target, but candidate violated format constraints; baseline output served.
* **Prompt:** *Complete with one word only: The official capital city of South Korea is*
* **Expected Target:** `Seoul`
* **Outputs:** Baseline=`Seoul.<br><br>The city is home to the country's` (Risk: 0.2736) | Candidate=`Seoul.<br><br>The city is home to the country's` (Risk: 0.2782)
* **Latent Telemetry:** Baseline Top-1 Prob: `19.12%` | Candidate Top-1 Prob: `29.31%` | Delta: `+0.1019`
* **Router Action:** `use_baseline` -> **Served Output:** `Seoul.<br><br>The city is home to the country's`
* **Protected Router Decision Explanation:** *Baseline served to preserve stricter output contract or lower risk.*

### Showcase Case 3: ID 101 (unseen_val)
* **Operational Category:** Repair Promoted: Candidate successfully recovered and validated semantic target completion.
* **Prompt:** *Complete with one word only: The official capital city of Austria is*
* **Expected Target:** `Vienna`
* **Outputs:** Baseline=`now the capital of the German Reich.<br><br>The German` (Risk: 0.2895) | Candidate=`now Vienna.<br><br>The Austrian capital is now Vienna.` (Risk: 0.3267)
* **Latent Telemetry:** Baseline Top-1 Prob: `9.34%` | Candidate Top-1 Prob: `8.68%` | Delta: `-0.0066`
* **Router Action:** `use_candidate` -> **Served Output:** `now Vienna.<br><br>The Austrian capital is now Vienna.`
* **Protected Router Decision Explanation:** *Candidate repair promoted.*

### Showcase Case 4: ID 084 (seen_val)
* **Operational Category:** Transition trace display for analysis (wrong_to_wrong).
* **Prompt:** *Complete with one word only: The official capital city of Switzerland is*
* **Expected Target:** `Bern`
* **Outputs:** Baseline=`Zurich.<br><br>The Swiss capital is the capital of Switzerland` (Risk: 0.2888) | Candidate=`Zurich.<br><br>The Swiss capital is the capital of Switzerland` (Risk: 0.2784)
* **Latent Telemetry:** Baseline Top-1 Prob: `12.69%` | Candidate Top-1 Prob: `27.07%` | Delta: `+0.1437`
* **Router Action:** `use_candidate` -> **Served Output:** `Zurich.<br><br>The Swiss capital is the capital of Switzerland`
* **Protected Router Decision Explanation:** *Both outputs failed target capture; candidate had lower computed risk and was selected by risk-minimization policy. This is not a repair.*



---

## 9. Failure Taxonomy & Recommended Fix Plan

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
| seen_val | 84 | *Complete with one word only: The official capit...* | `Bern` | `Zurich.<br><br>The Swiss ca...` | `Zurich.<br><br>The Swiss ca...` | 4.3837 |
| seen_val | 86 | *Complete with one word only: The noble element ...* | `Neon` | `the most important element ...` | `the most important element ...` | 13.5739 |
| seen_val | 87 | *Complete with one word only: The volatile eleme...* | `Sulfur` | `the most volatile element i...` | `the volatile element of the...` | 5.3019 |
| seen_val | 88 | *Complete with one word only: The chemical molec...* | `Oxygen` | `called the "air molecule."<...` | `called a "chemical compound...` | 3.9075 |
| seen_val | 89 | *Complete with one word only: The yellow dwarf s...* | `Sun` | `most massive star in the un...` | `closest thing to a star we'...` | 3.9867 |
| seen_val | 90 | *Complete with one word only: Mechanical acousti...* | `Vacuum` | `space.<br><br>The first thi...` | `space.<br><br>The first ste...` | 7.2123 |
| seen_val | 96 | *Complete with one word only: To enforce unique ...* | `Set` | `single word.<br><br>The fol...` | `single word.<br><br>The fol...` | 7.2777 |
| seen_val | 97 | *Complete with one word only: The hypermedia syn...* | `HTML` | `now supported.<br><br>The h...` | `now supported.<br><br>The h...` | 7.7287 |
| seen_val | 98 | *Complete with one word only: An execution failu...* | `Bug` | `"failure of execution".<br>...` | `"failure".<br><br>The follo...` | 10.1821 |
| seen_val | 99 | *Complete with one word only: A standardized tex...* | `JSON` | `used.<br><br>The following ...` | `used.<br><br>The following ...` | 11.1368 |
| ... | ... | ... | ... | ... | ... | *(And 13 more trace details)* |



---

## 12. Dynamic Executive AI Governance Conclusion

Based on evidence compiled in this evaluation cycle, we draw the following conclusions:

* **Demonstrated Capabilities:** The candidate model weights demonstrated stable latent representations and met accuracy expectations. Weight promotion is safe.
* **Repairs Promoted:** Promoted 1 validated semantic repairs.
* **Router Safety:** The Protected Router preserved served consistency with zero regressions observed.
* **Significance Notice:** These findings represent directional validation evidence. Enterprise deployment requires larger validation sets and seed repeats prior to final production release.


---

## 13. Compute Environment Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Active CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*

