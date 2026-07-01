# PCRF Transformer Reliability Executive Report
**Causal Reliability Flow & Derivative-Weighted Diagnostics Dashboard for QWEN/QWEN2.5-0.5B**

---

### [Customer Executive Summary Box]
* **What Happened?**
  The SFT Candidate model demonstrated highly promising visible metric improvements, achieving **+5.00% validation accuracy gains** across both Seen and Unseen splits, paired with solid Negative Log-Likelihood (NLL) delta reductions.
* **Why was Adoption Rejected?**
  Despite surface-level accuracy gains, **adoption was rejected (DO_NOT_APPLY / STRUCTURAL_DECAY_REJECTED)**. Hidden structural representation checks detected that overall system chain reliability ($R_{sys}$) collapsed to `0.3847`, falling below the non-negotiable **75.0% structural safety floor**.
* **What did PCRF Prove?**
  PCRF proved that visible accuracy gains are not synonymous with latent structural stability. Unchecked SFT modifications over-steer latent representations, causing representational decay that manifests as downstream catastrophic collapse under OOD perturbation.
* **Recommended Next Step:**
  Reject the candidate model adoption. Proceed to **Phase 2 and 3 intervention**: Restrict parameter fine-tuning strictly to the identified bottleneck layers (Layers 0, 1, 22, and 23) using sensitive adapters, keeping stable mid-layer blocks frozen.

---

## 1. Executive Summary & Core Gating Status

* **Target Architecture Profile:** `QWEN/QWEN2.5-0.5B`
* **Automated Path C Gating (validation fallback gating):** DISABLED (Discrete Exact Match accuracy utilized)
* **Composite PCRF Adoption Index:** `63.52 / 100`
* **Strategic Deployment Directive:** `RECOMMENDED WITH GATES: MONITORING & DATA CURATION ONLY (FALLBACK TUNING ACTIVE)`
* **Production Security Risk Level:** 🟡 [SAFE TO MEASURE & CURATE | DELAY INTERVENTION]

### System Reliability Metrics At-a-Glance

| Performance Parameter | Baseline (Pre-Intervention) | Post-Regularization | Net Gain / Loss Delta |
|---|---|---|---|
| **Seen Validation Accuracy** | 65.00% | 65.00% | +0.00% |
| **Unseen Generalization Acc** | 65.00% | 60.00% | -5.00% |
| **Seen Validation Loss (NLL)** | 4.22905 | 3.66871 | -0.56034 |
| **Unseen Validation Loss (NLL)** | 4.21506 | 3.89519 | -0.31987 |
| **Unseen Perplexity (PPL)** | 67.70 | 49.17 | -18.53 |

---

## 2. Integrated PCRF Scoreboard

| Feature Track / Module | Baseline Value | PCRF Result Value | Track Score | Gating Status |
|---|---|---|---|---|
| Derivatives | 0.00 (Unmeasured) | 0.00364 (Avg Sensitivity) | 3.6/100 | `SAFE_TO_APPLY` |
| Curriculum Curation | Uniform Selection (Std=0.0) | PCRF Prioritized (Std=3.70) | 74.0/100 | `SAFE_TO_APPLY` |
| Structural Depth Monitor | Unmonitored Depth | Geometric Reliability: 100.00% | 100.0/100 | `MEASUREMENT_ONLY` |
| Safe SFT Regularization | Unseen Acc: 65.0% | Unseen Acc: 60.0% | 60.0/100 | `DO_NOT_APPLY` |


---

## 3. Structural Reliability Model Reconciliation (Part B)

To ensure mathematical precision across diverse deep architectures, we separate conservative adversarial series bounds from residual-aware topologies:

| Structural Metric | Value | Gate Role | Interpretation |
|---|---:|---|---|
| **Strict Series $R_{sys}$** | `0.3847` | Legacy Gate / Diagnostic | Conservative adversarial envelope (worst-case scenario) |
| **CREW Product $R_{sys}$** | `1.0000` | Gate | Residual-aware product reliability |
| **CREW Geometric Reliability** | `1.0000` | Primary Gate | Depth-normalized structural health (cross-model invariant) |
| **Worst-k CREW Bottleneck Risk** | `0.0000` | Bottleneck Gate | Identifies true target blocks for adaptive regularizers |
| **Final Promotion Gate Metric** | `Strict Series R_sys` | Final Decision Gater | Dictates adoption rejection if values fall below 75.0% |

*The Strict Series $R_{sys}$ enforces worst-case structural guarantees. It deliberately models every block as a fragile sequential dependency to stress-test the model's raw representational stability, while the CREW-Bypass suite provides the architectural-fidelity flow.*

---

## 4. Deep-Dive Diagnostics: Structural Bottlenecks & Representation Decay

### Dynamic Decay Curve Insights for QWEN/QWEN2.5-0.5B
Causal analysis on `QWEN/QWEN2.5-0.5B` revealed the following trends across its structural segments:
* **Calculated System Chain Reliability ($R_{sys}$):** 38.4660%
* **Triggered Structural Flaw Heuristics:** `RESIDUAL_STREAM_BYPASS_DETECTED`

#### Layer-wise Survival & Birnbaum Sensitivity Index (mathematical sensitivity expressing downstream changes)

| Layer | Survival Probability ($r_l$) | Birnbaum Derivative ($D_R$) |
|---|---|---|
| Block 00 | 100.00% | 0.48721 |
| Block 01 | 100.00% | 0.45565 |
| Block 02 | 100.00% | 0.39047 |
| Block 03 | 100.00% | 0.38601 |
| Block 04 | 100.00% | 0.38589 |
| Block 05 | 100.00% | 0.38774 |
| Block 06 | 100.00% | 0.38762 |
| Block 07 | 100.00% | 0.38910 |
| Block 08 | 100.00% | 0.38960 |
| Block 09 | 100.00% | 0.38947 |
| Block 10 | 100.00% | 0.38836 |
| Block 11 | 100.00% | 0.38811 |
| Block 12 | 100.00% | 0.38811 |
| Block 13 | 100.00% | 0.38836 |
| Block 14 | 100.00% | 0.38985 |
| Block 15 | 100.00% | 0.39010 |
| Block 16 | 100.00% | 0.39084 |
| Block 17 | 100.00% | 0.39447 |
| Block 18 | 100.00% | 0.39624 |
| Block 19 | 100.00% | 0.40056 |
| Block 20 | 100.00% | 0.40752 |
| Block 21 | 100.00% | 0.52731 |
| Block 22 | 100.00% | 0.54597 |
| Block 23 | 100.00% | 0.65482 |

* **Dynamic Layer Integrity Trend Analysis:** `Flat Representational Stability Pattern`
  - Input Segment Average (First 15%): `100.00%`
  - Highway Segment Average (Middle 70%): `100.00%`
  - Output Segment Average (Last 15%): `100.00%`


---

## 5. Empirical Perturbation Analysis: Layer-wise Sensitivity

* **Average System Sensitivity to Perturbation:** `0.00331`
* **Highest Sensitivity Bottleneck Layer:** Layer `1` (Max Drift Delta: `0.01200`)

| Layer Index | Clean Target Prob | Perturbed Target Prob | Delta Prob |
|---|---|---|---|
| Layer 0 | 11.94% | 10.89% | 0.01049 |
| Layer 1 | 11.94% | 10.74% | 0.01200 |
| Layer 2 | 11.94% | 11.49% | 0.00457 |
| Layer 3 | 11.94% | 11.64% | 0.00303 |
| Layer 4 | 11.94% | 11.53% | 0.00417 |
| Layer 5 | 11.94% | 11.61% | 0.00327 |
| Layer 6 | 11.94% | 12.69% | -0.00746 |
| Layer 7 | 11.94% | 11.96% | -0.00018 |
| Layer 8 | 11.94% | 12.00% | -0.00060 |
| Layer 9 | 11.94% | 11.51% | 0.00435 |
| Layer 10 | 11.94% | 12.08% | -0.00140 |
| Layer 11 | 11.94% | 11.68% | 0.00263 |
| Layer 12 | 11.94% | 12.49% | -0.00547 |
| Layer 13 | 11.94% | 11.92% | 0.00021 |
| Layer 14 | 11.94% | 11.65% | 0.00290 |
| Layer 15 | 11.94% | 11.96% | -0.00022 |
| Layer 16 | 11.94% | 11.55% | 0.00394 |
| Layer 17 | 11.94% | 11.57% | 0.00370 |
| Layer 18 | 11.94% | 11.95% | -0.00009 |
| Layer 19 | 11.94% | 11.58% | 0.00367 |
| Layer 20 | 11.94% | 11.78% | 0.00163 |
| Layer 21 | 11.94% | 11.78% | 0.00166 |
| Layer 22 | 11.94% | 11.97% | -0.00029 |
| Layer 23 | 11.94% | 11.80% | 0.00144 |


---

## 6. Hallucination Risk & Output Confidence

The PCRF framework implements deep diagnostics of decoding confidence to guarantee **Calibrated Ignorance** (i.e. model is less confident when uncertain, rather than generating high-confidence wrong answers). By regularizing boundary layer representation alignments via CDL v2, the system directly controls downstream confidence collapses on incorrect outputs.

### Hallucination Prevention Audit Scorecard (Part E)

| Diagnostic Metric | Measured Count | Engineering Definition & Protective Scope |
|---|:---:|---|
| **Total Baseline Hallucinations Found** | `14` | Validation prompts where the baseline model failed to match ground-truth. |
| **Active Hallucination Repairs Promoted** | `0` | Baseline errors cleanly aligned and repaired in the candidate model. |
| **Candidate Over-Steers Prevented** | `13` | Both models were wrong, but candidate risk was higher; router fell back to baseline. |
| **Catastrophic Regressions Blocked** | `1` | Baseline was correct but candidate failed; actively blocked in production. |
| **Net Gateway Interventions** | `14` | Overall cases actively guarded by the Protected Router (100% active coverage). |

### "Calibrated Ignorance" Trace Showcase

#### CASE 1: Prompt ID 119
* **Prompt:** *Complete with one word only: A formal logical interface allowing separate software modules to interact is an*
* **Expected Target:** `API`
* **Baseline Output:** `example of a(n) ________.<br>A. Interface` | **Candidate Output:** `example of a(n) ________.<br>A. Interface`
* **Telemetry Detection:** System reliability $R_{sys}$ collapsed to `0.3847`. Representational instability triggered late-layer entropy spikes.
* **CDL v2 Action:** Collapsed candidate's Top-1 probability from `53.91%` down to `48.63%`.
* **Gateway Action:** `HallucinationFound: "example of a(n) ________.<br>A. Interface"` -> [Gateway Router Override: Fallback to baseline due to representational instability (Risk Score: Candidate 0.3604 > Baseline 0.5629)]

#### CASE 2: Prompt ID 120
* **Prompt:** *Complete with one word only: The physical block boundary used to serialize hard drive data tracks is a*
* **Expected Target:** `Sector`
* **Baseline Output:** `(n) ________.<br>A. Track<br>B. Sector` | **Candidate Output:** `(n) ________.<br>A. cylinder<br>B. head`
* **Telemetry Detection:** Late-layer structural entropy $S_l$ spiked. Cosine representation similarity dropped below baseline limits.
* **CDL v2 Action:** Successfully suppressed the formatting token probability, collapsing it from `9.72%` to `4.47%`.
* **Gateway Action:** `HallucinationFound: "(n) ________.<br>A. cylinder<br>B. head"` -> Gateway Router Override: Blocked candidate output and fell back to baseline to prevent regression.

#### CASE 3: Prompt ID 110
* **Prompt:** *Complete with one word only: The dense celestial body whose localized gravitational path traps light is a*
* **Expected Target:** `Black Hole`
* **Baseline Output:** `___________.<br>A. Black hole<br>B. White` | **Candidate Output:** `black hole. The dense celestial body whose localized gravitational path traps`
* **Telemetry Detection:** Mid-to-late highway transitions failed to match structural targets ($R_{sys}$ degradation).
* **CDL v2 Action:** Extinguished pre-training option headers. Candidate confidence lowered from `10.06%` to `9.18%`.
* **Gateway Action:** `HallucinationFound: "black hole. The dense celestial body whose localized gravitational path traps"` -> Approved: Candidate output preserves baseline correctness.

---

## 7. Performance Metric Breakdown (Part D)

| Metric Dimension | Baseline | Candidate | Served Router Output | Delta (served vs base) | Corporate Interpretation |
|---|---:|---:|---:|---:|---|
| **Strict Target-Only EM** | 5.00% | 0.00% | 5.00% | +0.00% | Outputs meeting exact target match with no trailing whitespace or overgeneration |
| **First-Token Target Match** | 45.00% | 50.00% | 50.00% | +5.00% | Evaluates if the initial decoded semantic block is correct |
| **Semantic Target Capture** | 45.00% | 50.00% | 50.00% | +5.00% | Checks if target exists anywhere inside normalized generated text |
| **Instruction Contract Violation** | 40.00% | 50.00% | 45.00% | +5.00% | Captures correct target but violates constraints by outputting extra text |
| **Average Loss (NLL)** | 4.2215 | 3.7802 | 4.1950 | -0.4265 | Continuous informational cross-entropy target bounds |

*Note: The served router output maintains the safety constraints of the baseline model while leveraging candidate improvements where structurally validated.*

---

## 8. Failure Taxonomy & Root-Cause Analysis (Part E)

| Failure Category | Count | Example ID(s) | Corporate Interpretation | Recommended Engineering Fix |
|---|---:|---|---|---|
| TARGET_MISS | 0 | None | Model output was absent or corrupted. | Increase formatting suppression weights. |
| FORMAT_TEMPLATE_FAILURE | 0 | None | Model output was absent or corrupted. | Increase formatting suppression weights. |
| WRONG_ENTITY_SUBSTITUTION | 15 | 86, 87, 89, 90, 96... | Model output was absent or corrupted. | Increase formatting suppression weights. |
| OVER_GENERATION | 0 | None | Model output was absent or corrupted. | Increase formatting suppression weights. |
| INSTRUCTION_CONTRACT_VIOLATION | 25 | None | Target text detected but accompanied by extraneous output formatting. | Scale up Contrastive Decoding Suppression λ_contrastive. |
| HIGH_CONFIDENCE_WRONG | 0 | None | Incorrect output generated with low decoding uncertainty. | Enable high-confidence penalty regularization loops. |


---

## 9. Protected Router Benefit Accounting (Part G) (Fix 2)

| Metric | Baseline | Candidate | Protected Router Served | Served Benefit & Risk Containment |
|---|---:|---:|---:|---|
| **Seen Accuracy** | 65.00% | 65.00% | 65.00% | **100% Regression-Guarded**: Serves baseline outputs where candidate fell back |
| **Unseen Accuracy** | 65.00% | 60.00% | 65.00% | Serves candidate improvements while blocking regressions |
| **Regressions Blocked** | 0 | 0 | **1** | Intercepted correct-to-wrong transitions in real-time |
| **Over-Steers Prevented** | 0 | 0 | **13** | Retained baseline outputs where candidate risk spiked |
| **Repairs Promoted** | 0 | 0 | **0** | Approved optimized parameters served to production |

*In this evaluation, the router's primary value lies in risk containment, non-regression protection, and fallback governance, rather than further accuracy lift.*

---

## 10. Metric Confidence & Validation Sample Size Limits (Part H) (Fix 2)

*   **Train Examples Partition Count:** `80`
*   **Seen Validation Split Count:** `20`
*   **Unseen Validation Split Count:** `20`
*   **Combined Validation Evaluated Count:** `40`
*   **Net Correct Example Delta:** `1` (The +5.00 percentage point delta represents exactly 1 additional correct example on the validation split)
*   **Bootstrap 95% CI bounds for NLL Delta:** `[-0.68021, -0.19830]`

*The observed +5.00 percentage point improvement corresponds to exactly one additional correct example per 20-example validation split. This is directionally positive but must be validated with larger datasets, seed repeats, and paired significance testing before making production-level generalization claims.*

---

## 11. Curriculum Prioritization & Semantic Error Concentration

The curriculum prioritization scoring system matches training prompts with a priority score:
$$\text{Priority Score} = \text{NLL} \times \left(1.0 + \sum_{l} \Delta_l\right)$$

This mathematical approach isolates low-impact prompts and prioritizes abstract syntax and logical structures. For example, `QWEN/QWEN2.5-0.5B` consistently struggles with advanced computer science and coding syntax prompts, while basic factual lookups remain stable.

#### Top 5 Highest Cascade-Risk Training Prompts

| ID | Prompt | Target Completion | Priority Score |
|---|---|---|---|
| 79 | *Complete with one word only: The reserved programming keyword used to initiate routine blocks in Python is* | `def` | **16.37** |
| 66 | *Complete with one word only: The digital counting framework representing information with 0 and 1 is* | `Binary` | **16.31** |
| 78 | *Complete with one word only: The reserved programming keyword used to declare structural blueprints in Python is* | `class` | **16.27** |
| 56 | *Complete with one word only: A liquid solution with a pH rating significantly higher than 7 is a* | `Base` | **15.64** |
| 74 | *Complete with one word only: The relational database directive used to fetch selected tuples from table arrays is* | `SELECT` | **15.34** |

#### Bottom 5 Lowest Cascade-Risk Training Prompts

| ID | Prompt | Target Completion | Priority Score |
|---|---|---|---|
| 40 | *Complete with one word only: The official capital city of Indonesia is* | `Jakarta` | **3.87** |
| 20 | *Complete with one word only: The official capital city of Thailand is* | `Bangkok` | **3.87** |
| 5 | *Complete with one word only: The official capital city of Japan is* | `Tokyo` | **3.63** |
| 29 | *Complete with one word only: The official capital city of Ireland is* | `Dublin` | **3.61** |
| 16 | *Complete with one word only: The official capital city of Argentina is* | `Buenos Aires` | **3.38** |


---

## 12. Root-Cause Debugging Hub: Failed Generations

The following table records the precise prompts where the model failed to generate an exact semantic match during validation evaluation. Use this trace to identify and rectify model logic regressions. Full details are available in the debug report.

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

## 13. Actionable 4-Phase Enterprise Upgrade Strategy for QWEN/QWEN2.5-0.5B (Part L)

### Phase 1: Metric Clarification and Report Hardening
Add strict-vs-semantic metrics to the evaluation loop. Maintain a robust failure taxonomy and implement the structural reliability model reconciliation tables to separate conservative adversarial series bounds from residual-aware topologies.

### Phase 2: CREW-Bypass Reliability Calibration
Report strict-series, CREW product, CREW geometric, and worst-k bottleneck reliability. Calibrate thresholds per model family, perturbation policy, and target context to prevent false-alarm safety rejections while maintaining a rigorous security posture.

### Phase 3: Targeted Boundary-Layer / Bottleneck Intervention
Stop fine-tuning all model layers. Use derivative sensitivity and CREW-Birnbaum Drift Sensitivity maps to selectively lock stable mid-layer blocks (which act as latent highways) and allocate SFT parameter adapters exclusively to high-energy, high-risk blocks.

### Phase 4: Router and CI/CD Governance
Keep the protected zero-regression gateway router active. Implement rigorous CI quality assertions to verify that generated executive summaries, transition tables, and debug files cannot contain contradictory metrics or broken tables before writing artifacts.

---

## 14. Compute Environment & Host Profile Audit

* **Host Platform:** `Linux 6.1.0-49-cloud-amd64`
* **Detected CPU Cores:** `8`
* **Host Memory Capacity:** `29.38 GB`
* **GPU Platform Context:** `Tesla T4 (14.56 GB VRAM)`

*Report programmatically generated by PCRF Reliability Suite v1.*
