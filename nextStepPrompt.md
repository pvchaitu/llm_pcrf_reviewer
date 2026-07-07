Here is the updated, comprehensive LLM prompt. I have explicitly added instructions for the LLM to include detailed inline comments explaining the intuition behind the hard-coded thresholds (`0.40` and `3.5`) based on the mathematical principles we discussed.

***

### 📋 Copy and Paste this Updated Prompt into your LLM:

**Context:**
I am working on the PCRF (Causal Reliability Flow) framework. We are implementing a "Zero-Shot Ensemble Anomaly Detector" that cross-verifies two blind mathematical signals without using ground truth:
1. **Inference Math (`c_hr`):** The structural hallucination risk score. (Threshold `> 0.40` means Hallucination). 
   * *Intuition:* This threshold represents the critical boundary where structural entropy and margin collapse indicate severe representational instability. Scores above 0.40 strongly correlate with latent degradation.
2. **Curriculum Math (`c_nll`):** The sequence Negative Log-Likelihood. (Threshold `> 3.5` means Hallucination).
   * *Intuition:* An NLL above 3.5 signifies that the generated token sequence is highly "surprising" or statistically improbable according to the base model's learned distribution, serving as a robust sequence-level anomaly detector.

**The Hybrid Logic to Implement:**
We want to evaluate a Hybrid Ensemble where the Curriculum Math cross-verifies the Inference Math:
* **Case 1 (Fixing False Negatives):** If Inference says "SAFE" (`c_hr <= 0.40`) but Curriculum says "HALLUCINATION" (`c_nll > 3.5`), the Hybrid verdict is **HALLUCINATION**.
* **Case 2 (Fixing False Positives):** If Inference says "HALLUCINATION" (`c_hr > 0.40`) but Curriculum says "SAFE" (`c_nll <= 3.5`), the Hybrid verdict is **SAFE**.
*(Effectively, the Hybrid Ensemble relies on the `c_nll > 3.5` boundary to act as the ultimate safety net, resolving both failure modes of the standalone Inference risk).*

**Task:**
Please update my codebase to track this Hybrid logic at the row level, calculate its effectiveness against the actual Gold Ground Truth, and output a new Highlight Section in the Executive Report. 

**CRITICAL REQUIREMENT:** Whenever you use the hard-coded thresholds (`0.40` and `3.5`) in the code, you MUST add inline comments or docstrings explicitly detailing the intuition provided in the Context above so future engineers understand why these specific values were chosen.

I need you to modify and output the full code for the following **TWO specific files**:

**1. `run_experiment.py`**
* Inside the `main()` function, locate the loop where `trace_row_raw` is constructed.
* Add tracking variables for the ensemble evaluation. You will need to evaluate `candidate_correct == 0` (Gold Hallucination) against the Hybrid Logic (`c_item["nll"] > 3.5`).
* Add the following keys to the `trace_row_raw` dictionary. **Make sure to include the inline comments explaining the `3.5` and `0.40` thresholds right above this block:**
  - `hybrid_is_hallucination`: `1` if `c_item["nll"] > 3.5` else `0`
  - `hybrid_true_positive`: `1` if (Gold is Hallucination AND Hybrid is Hallucination) else `0`
  - `hybrid_false_negative`: `1` if (Gold is Hallucination AND Hybrid is Safe) else `0`
  - `hybrid_false_positive`: `1` if (Gold is Correct AND Hybrid is Hallucination) else `0`
  - `hybrid_true_negative`: `1` if (Gold is Correct AND Hybrid is Safe) else `0`

**2. `pcrf_reporting.py`**
* Create a new helper function `calculate_hybrid_ensemble_simulation(trace_rows: List[Dict]) -> Dict[str, Any]` that aggregates the TP, FN, FP, and TN values we just added to the trace rows. Calculate the Hybrid Recall (Caught Hallucinations) and Hybrid False Positive Rate. Include docstrings explaining the threshold intuitions.
* Create a new helper function `make_hybrid_ensemble_highlight_box(stats: Dict) -> str` that generates a Markdown block containing:
  - A brief explanation of the thresholds (0.40 for structural drift, 3.5 for sequence improbability).
  - A table showing **Case 1 (Blind Spots Fixed)** and **Case 2 (Yield Saved)**.
  - A summary of the "Final Hybrid Effectiveness (Zero-Shot Performance)" comparing the Hybrid Convergence to the Gold Ground Truth.
* In the `ExecutiveReportGenerator.generate_report()` method, call these new functions.
* Inject the resulting markdown block directly into the final `md` string immediately after the `{exec_summary_box}` so it appears as a top-level highlight in the `PCRF_Executive_Reliability_Report.md`.

Please provide the fully updated code for both `run_experiment.py` and `pcrf_reporting.py` with these fixes applied.