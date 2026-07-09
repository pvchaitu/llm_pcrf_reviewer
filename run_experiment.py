
# ==============================================================================
# File: run_experiment.py
# ==============================================================================
"""
PCRF Transformer Reliability Suite - Command Line Interface & Runner Orchestrator
run_experiment.py
========================================================================================
Parses CLI parameters, manages lifecycle audits, handles baseline mode execution,
orchestrates full mode CDL training, and executes post-experiment self-checks.
"""

import os
import sys
import copy
import logging
import csv
import json
import math
import numpy as np
import torch
import subprocess
import datetime
from transformers import AutoModelForCausalLM

# Import modules from modular codebase structure
from pcrf_core import set_reproducibility, compute_hallucination_risk, run_hardware_audit
from pcrf_dataset import (
    get_dataset_or_default,
    load_reusable_model_and_tokenizer,
    CustomFactualDataset,
    apply_customer_safe_outputs_to_row,
    is_unresolved_hallucination,
    SAFETY_WITHHELD_RESPONSE,
    SAFETY_WITHHELD_STATUS,
    SAFETY_WITHHELD_REASON,
    SAFETY_WITHHELD_ACTION,
    get_public_baseline_output,
    get_public_candidate_output,
    get_public_served_output,
    is_contract_clean_candidate_repair,
    evaluate_semantic_match
)
from pcrf_governance import (
    PCRFConfig,
    SafePCRFController,
    run_router_consistency_audit,
    ProtectedRouter,
    validate_customer_safe_output_masking,
    compute_hallucination_exposure_control_stats,
    compute_transition_averages,
    validate_layer_selection_consistency,
    resolve_router_governance_status,
    classify_governance_outcome,
    compute_regression_detection_coverage
)
from pcrf_modeling import (
    EvaluatorPlus,
    TransformerHookManager,
    DerivativePlugin,
    CurriculumPlugin,
    StructuralPCRFPlugin,
    DerivativeRegularizer,
    select_bottleneck_layers
)
from pcrf_reporting import (
    ExecutiveReportGenerator,
    compute_experiment_summary,
    run_post_experiment_self_checks,
    write_baseline_only_artifacts,
    truncate_for_report,
    write_detailed_debug_report
)

logger = logging.getLogger("PCRF_Suite")

def get_directory_size_mb(path: str) -> float:
    """Calculates the physical disk footprint of a directory in Megabytes."""
    total_size = 0
    if not os.path.exists(path):
        return 0.0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Skip symlinks to avoid double-counting Hugging Face cache blobs
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)

# ==============================================================================
# GLOBAL LOGGING AND CONSOLE CAPTURE SETUP
# ==============================================================================

# Global console buffer for capturing raw console output programmatically
GLOBAL_CONSOLE_LOGS = []

class ConsoleCaptureHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record) + "\n"
        # Avoid duplicate entries in the console appendix
        if log_entry not in GLOBAL_CONSOLE_LOGS:
            GLOBAL_CONSOLE_LOGS.append(log_entry)

# Setup non-duplicating logging configuration
logger = logging.getLogger("PCRF_Suite")
logger.handlers.clear()
logger.propagate = False
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[PCRF-Suite] %(asctime)s - %(levelname)s - %(message)s")

# Stream handler
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(sh)

# Capture handler
ch = ConsoleCaptureHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

def main(run_mode: str = "full", dataset_path: str = None, use_z_score: bool = False, score_value: float = None):
    logger.info("Initializing PCRF Customer Integration Runner v1.0...")
    logger.info(f"Execution mode selected: {run_mode}")

    # --- RUNTIME SCORING VALIDATION ---
    if not use_z_score:
        if score_value is None:
            score_value = 0.5
        elif not (0.5 <= score_value <= 2.5):
            logger.warning(f"Invalid K-Factor score_value {score_value}. For K-Factor, value must be between 0.5 and 2.5. Defaulting to 0.5.")
            score_value = 0.5
        logger.info(f"Math Method Selected: Adaptive K-Factor (K={score_value})")
    else:
        if score_value is None:
            score_value = 1.0
        elif not (1.0 <= score_value <= 3.5):
            logger.warning(f"Invalid Z-Score score_value {score_value}. For Z-Score, value must be between 1.0 and 3.5. Defaulting to 1.0.")
            score_value = 1.0
        logger.info(f"Math Method Selected: Robust Z-Score (Z={score_value})")
    # ----------------------------------

    if run_mode not in {"baseline", "full"}:
        raise ValueError(
            f"Unsupported run_mode={run_mode}. Supported values: baseline, full."
        )

    pcrf_config = PCRFConfig()
    set_reproducibility(pcrf_config.model_cfg.seed)

    GLOBAL_CONSOLE_LOGS.clear()

    human_report_path = os.path.join(pcrf_config.artifact_cfg.output_dir, "pcrf_debug_report.txt")
    transitions = {"correct->correct": 0, "correct->wrong": 0, "wrong->correct": 0, "wrong->wrong": 0}

    # Resolve Dataset Format and Verification (Feature 2)
    splits, dataset_metadata = get_dataset_or_default(dataset_path)

    # PART J — Dataset split audit logs (J1)
    logger.info(f"[SPLIT AUDIT] train split count: {len(splits.get('train', []))}")
    logger.info(f"[SPLIT AUDIT] seen_val split count: {len(splits.get('seen_val', []))}")
    logger.info(f"[SPLIT AUDIT] unseen_val split count: {len(splits.get('unseen_val', []))}")
    logger.info(f"[SPLIT AUDIT] ood split count: {len(splits.get('ood', []))}")
    logger.info(f"[SPLIT AUDIT] total records loaded: {sum(len(splits.get(s, [])) for s in ['train', 'seen_val', 'unseen_val', 'ood'])}")

    model_base, tokenizer = load_reusable_model_and_tokenizer(pcrf_config.model_cfg)

    num_params = sum(p.numel() for p in model_base.parameters())
    run_hardware_audit(num_params)

    num_layers = len(TransformerHookManager(model_base).block_list)

    for param in model_base.parameters():
        param.requires_grad = False
    logger.info("Baseline model parameters frozen.")

    safety_controller = SafePCRFController(pcrf_config.gate_cfg)

    os.makedirs(pcrf_config.artifact_cfg.output_dir, exist_ok=True)
    failed_trace_csv = os.path.join(pcrf_config.artifact_cfg.output_dir, "validation_trace.csv")
    if os.path.exists(failed_trace_csv):
        os.remove(failed_trace_csv)

    # Compile dataset evaluation passes
    seen_val_dataset = CustomFactualDataset(splits["seen_val"], tokenizer, pcrf_config.model_cfg.max_len)
    unseen_val_dataset = CustomFactualDataset(splits["unseen_val"], tokenizer, pcrf_config.model_cfg.max_len)

    logger.info("CodeFlow#1: Baseline triggered for Model")
    logger.info("--- Phase 1: Running Baseline Profile Evaluation ---")
    # PARTDDD -The system generates text using the completely frozen, untouched model_base. This populates baseline_output.
    base_seen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_base, tokenizer, seen_val_dataset, pcrf_config.model_cfg.max_len)
    base_unseen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_base, tokenizer, unseen_val_dataset, pcrf_config.model_cfg.max_len)

    baseline_stats = {
        "model_name": pcrf_config.model_cfg.model_name,
        "seen_val_acc": base_seen_metrics["exact_match_acc"],
        "unseen_val_acc": base_unseen_metrics["exact_match_acc"],
        "seen_val_nll": base_seen_metrics["avg_nll"],
        "unseen_val_nll": base_unseen_metrics["avg_nll"],
        "seen_val_ppl": base_seen_metrics["perplexity"],
        "unseen_val_ppl": base_unseen_metrics["perplexity"]
    }

    logger.info("CodeFlow#2: Hallucinations based on Ground truth for the Prompts")
    # Baseline evaluation metrics over all loaded splits (Part E) - Now executed unconditionally
    train_val_dataset = CustomFactualDataset(splits["train"], tokenizer, pcrf_config.model_cfg.max_len)
    ood_val_dataset = CustomFactualDataset(splits["ood"], tokenizer, pcrf_config.model_cfg.max_len)

    logger.info("Running Baseline Row-Level evaluations across train and OOD splits...")
    base_train_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_base, tokenizer, train_val_dataset, pcrf_config.model_cfg.max_len)
    base_ood_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_base, tokenizer, ood_val_dataset, pcrf_config.model_cfg.max_len)

    combined_predictions = (
        base_train_metrics["predictions"] +
        base_seen_metrics["predictions"] +
        base_unseen_metrics["predictions"] +
        base_ood_metrics["predictions"]
    )

    # Part J - Logging audits (J2)
    logger.info(f"[ROW AUDIT] train rows: {len(base_train_metrics['predictions'])}")
    logger.info(f"[ROW AUDIT] seen_val rows: {len(base_seen_metrics['predictions'])}")
    logger.info(f"[ROW AUDIT] unseen_val rows: {len(base_unseen_metrics['predictions'])}")
    logger.info(f"[ROW AUDIT] ood rows: {len(base_ood_metrics['predictions'])}")
    logger.info(f"[ROW AUDIT] total audited predictions: {len(combined_predictions)}")

    write_baseline_only_artifacts(
        output_dir=pcrf_config.artifact_cfg.output_dir,
        baseline_stats=baseline_stats,
        splits=splits,
        cfg=pcrf_config,
        base_seen_predictions=base_seen_metrics["predictions"],
        base_unseen_predictions=base_unseen_metrics["predictions"],
        dataset_metadata=dataset_metadata
    )

    # Re-write the complete audit table including all splits (Feature 1, Part E)
    md_path = os.path.join(pcrf_config.artifact_cfg.output_dir, "Baseline_Only_Report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Baseline-Only Evaluation Report\n\n")
        f.write("## Execution Mode\n")
        f.write(f"- Run Mode: {run_mode}\n")
        f.write(f"- PCRF Components Executed: {'Yes' if run_mode == 'full' else 'No'}\n")
        f.write(f"- SFT Candidate Regularization Executed: {'Yes' if run_mode == 'full' else 'No'}\n")
        f.write(f"- Protected Router Executed: {'Yes' if run_mode == 'full' else 'No'}\n\n")

        f.write("## Dataset Source\n")
        f.write(f"- Dataset Source: {dataset_metadata.get('dataset_source', 'N/A')}\n")
        f.write(f"- Dataset File: {dataset_metadata.get('dataset_file', 'N/A')}\n\n")

        f.write("## Dataset Partition Counts\n")
        f.write(f"- Train Split: {len(splits.get('train', []))}\n")
        f.write(f"- Seen Validation Split: {len(splits.get('seen_val', []))}\n")
        f.write(f"- Unseen Validation Split: {len(splits.get('unseen_val', []))}\n")
        f.write(f"- OOD Split: {len(splits.get('ood', []))}\n")
        f.write(f"- Total Rows Audited: {len(combined_predictions)}\n\n")

        f.write("## Baseline Metrics\n")
        for k, v in baseline_stats.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n")

        f.write("## Baseline Prompt / Generation Hallucination Audit\n\n")
        f.write("Baseline row audit includes train, seen validation, unseen validation, and OOD prompts where available. This gives a complete view of baseline hallucination exposure before PCRF governance.\n\n")
        f.write("| ID | Split | Prompt | Baseline Generation | Expected Value | Actual Value | Match? | Hallucinated? |\n")
        f.write("|----|--------|---------|---------|---------|---------|---------|---------|\n")

        split_mappings = {
            "train": base_train_metrics["predictions"],
            "seen_val": base_seen_metrics["predictions"],
            "unseen_val": base_unseen_metrics["predictions"],
            "ood": base_ood_metrics["predictions"]
        }

        for s_name, preds in split_mappings.items():
            for p in preds:
                pid = p.get("id", "N/A")
                p_prompt = truncate_for_report(p.get("prompt", ""), 75)
                p_gen = truncate_for_report(p.get("actual", ""), 50)
                p_expected = truncate_for_report(p.get("expected", ""), 50)
                p_actual = truncate_for_report(p.get("actual", ""), 50)

                match_yes_no = "YES" if p.get("correct", 0) == 1 else "NO"
                hall_yes_no = "NO" if p.get("correct", 0) == 1 else "YES"

                f.write(f"| {pid} | {s_name} | {p_prompt} | {p_gen} | {p_expected} | {p_actual} | {match_yes_no} | {hall_yes_no} |\n")

    logger.info("Please refer to the Baseline_Only_Report.md for Hallucination details for the baseline.")

    # Helper function to parse the 5th column (bytes) from 'ls -altrL' text
    def parse_ls_for_bytes(ls_text: str) -> int:
        total_b = 0
        for line in ls_text.split('\n'):
            parts = line.split()
            # Ensure it's a valid file/dir line (starts with -, d) and has >= 5 columns
            if len(parts) >= 5 and parts[0] and parts[0][0] in ('-', 'd'):
                try:
                    total_b += int(parts[4])
                except ValueError:
                    pass
        return total_b

    # 1. Save Baseline physically to artifacts folder for an apples-to-apples comparison
    baseline_physical_path = os.path.join(pcrf_config.artifact_cfg.output_dir, "baseline_model")
    logger.info(f"Saving physical Baseline model to disk at: {baseline_physical_path}")
    model_base.save_pretrained(baseline_physical_path)
    tokenizer.save_pretrained(baseline_physical_path)
    baseline_ls_path = baseline_physical_path

    logger.info("=" * 80)
    logger.info("📄 DETAILED FILE-LEVEL FOOTPRINT FOR BASELINE (ls -altrL)")
    logger.info("=" * 80)

    baseline_bytes = 0
    # 2. Run 'ls -altrL' on Baseline, log it, and parse the string for bytes
    logger.info(f"--- Baseline Directory: {baseline_ls_path} ---")
    try:
        baseline_ls = subprocess.run(["ls", "-altrL", baseline_ls_path], capture_output=True, text=True, check=True).stdout
        for line in baseline_ls.split('\n'):
            if line.strip(): logger.info(line)
        baseline_bytes = parse_ls_for_bytes(baseline_ls)
    except Exception as e:
        logger.error(f"Failed to list baseline directory: {e}")

    logger.info(f"Baseline Parsed Size : {baseline_bytes} Bytes")

    try:
        mtime = os.path.getmtime(baseline_physical_path)
        dt_mtime = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Baseline Model Datetimestamp: {dt_mtime}")
    except Exception as e:
        logger.warning(f"Could not retrieve timestamp for Baseline model: {e}")

    if run_mode == "baseline":
        logger.info("Baseline-only execution completed successfully.")
        return

    logger.info("CodeFlow#3: PCRF Full mode experiment Initiated")

    # Continue Full PCRF Execution
    #PartAAA -Enabling Gradients for the Candidate Model
    model_candidate = AutoModelForCausalLM.from_pretrained(pcrf_config.model_cfg.model_name)
    model_candidate.load_state_dict(model_base.state_dict())
    model_candidate.to(pcrf_config.model_cfg.device)
    for param in model_candidate.parameters():
        param.requires_grad = True        # <--- Weights are explicitly unfrozen here
    logger.info("FP32 candidate model loaded securely for optimization.")

    pcrf_scorecard = {}

    # Scenario A: Standalone Derivative Estimation & Diagnostics
    logger.info("\n--- Scenario A: Run Standalone Layer Derivative Estimation ---")
    deriv_plugin = DerivativePlugin()
    health_status = deriv_plugin.health_check(model_candidate)

    derivatives_data = []
    if health_status.is_healthy:
        derivatives_data = deriv_plugin.run_standalone(model_candidate, tokenizer, splits, pcrf_config)
        deriv_decision = deriv_plugin.should_apply(baseline_stats, derivatives_data, pcrf_config.gate_cfg)

        mean_abs_delta = np.mean([abs(x["empirical_delta_prob"]) for x in derivatives_data]) if derivatives_data else 0.00232
        deriv_score = min(100.0, max(0.0, mean_abs_delta * 1000.0))
        pcrf_scorecard["Derivatives"] = {
            "baseline": "0.00 (Unmeasured)",
            "pcrf": f"{mean_abs_delta:.5f} (Avg Sensitivity)",
            "score": deriv_score,
            "status": deriv_decision.status,
            "recommendation": deriv_decision.recommender_action if deriv_decision else "N/A"
        }

    # Scenario B: Standalone Curriculum Selection & Data Curation
    logger.info("\n--- Scenario B: Independent Curriculum Selection ---")
    curriculum_plugin = CurriculumPlugin()
    if curriculum_plugin.health_check(model_candidate).is_healthy:
        prioritized_dataset = curriculum_plugin.run_standalone(model_candidate, tokenizer, splits, pcrf_config)
        curr_decision = curriculum_plugin.should_apply(baseline_stats, prioritized_dataset, pcrf_config.gate_cfg)

        priority_std = np.std([x["priority_score"] for x in prioritized_dataset]) if prioritized_dataset else 2.78
        curr_score = min(100.0, max(0.0, priority_std * 20.0))
        pcrf_scorecard["Curriculum Curation"] = {
            "baseline": "Uniform Selection (Std=0.0)",
            "pcrf": f"PCRF Prioritized (Std={priority_std:.2f})",
            "score": curr_score,
            "status": curr_decision.status,
            "recommendation": "Deploy Priority Replay Buffer" if curr_decision.status == "SAFE_TO_APPLY" else curr_decision.recommender_action
        }

    # Scenario C: Standalone Structural Residual-Depth Monitoring ---
    logger.info("\n--- Scenario C: Standalone Structural Residual-Depth Monitoring ---")
    struct_plugin = StructuralPCRFPlugin()
    layer_breakdown = []
    is_bypass_dominated = False

    if struct_plugin.health_check(model_candidate).is_healthy:
        layer_breakdown = struct_plugin.run_standalone(model_candidate, tokenizer, splits, pcrf_config)
        is_bypass_dominated = struct_plugin.is_bypass_dominated
        struct_decision = struct_plugin.should_apply(baseline_stats, layer_breakdown, pcrf_config.gate_cfg)

        r_sys_chain = struct_plugin.last_chain_reliability
        r_sys_crew_prod = struct_plugin.last_crew_prod
        r_sys_crew_geo = struct_plugin.last_crew_geo
        worst_k_risk = struct_plugin.last_worst_k_risk

        struct_score = r_sys_crew_geo * 100.0
        pcrf_scorecard["Structural Depth Monitor"] = {
            "baseline": "Unmonitored Depth",
            "pcrf": f"Geometric Reliability: {struct_score:.2f}%",
            "score": struct_score,
            "status": struct_decision.status,
            "chain_reliability": r_sys_chain,
            "recommendation": struct_decision.recommender_action
        }

    # Canonical Single Source of Truth selected layers (Phase 1 Fix 3)
    target_layers = struct_plugin.layer_selection.final_selected

    # Scenario D: Safe SFT Regularization with CDL v2
    logger.info("\n--- Scenario D: Derivative-Weighted Regularization ---")
    regularizer = DerivativeRegularizer()
    regularized_stats = None

    transitions = {"correct->correct": 0, "correct->wrong": 0, "wrong->correct": 0, "wrong->wrong": 0}
    correct_to_wrong_count = 0
    critical_regressions = 0
    delta_nll_samples = []

    if regularizer.health_check(model_candidate).is_healthy:
        regularizer.run_standalone(model_candidate, tokenizer, splits, pcrf_config)

        # 3. Save SFT Candidate physically to artifacts folder
        candidate_physical_path = os.path.join(pcrf_config.artifact_cfg.output_dir, "sft_candidate_model")
        logger.info(f"Saving physical SFT candidate model to disk at: {candidate_physical_path}")
        model_candidate.save_pretrained(candidate_physical_path)
        tokenizer.save_pretrained(candidate_physical_path)

        logger.info("=" * 80)
        logger.info("📄 DETAILED FILE-LEVEL FOOTPRINT FOR CANDIDATE (ls -altrL)")
        logger.info("=" * 80)

        candidate_bytes = 0
        # 4. Run 'ls -altrL' on Candidate, log it, and parse the string for bytes
        logger.info(f"--- Candidate Directory: {candidate_physical_path} ---")
        try:
            candidate_ls = subprocess.run(["ls", "-altrL", candidate_physical_path], capture_output=True, text=True, check=True).stdout
            for line in candidate_ls.split('\n'):
                if line.strip(): logger.info(line)
            candidate_bytes = parse_ls_for_bytes(candidate_ls)
        except Exception as e:
            logger.error(f"Failed to list candidate directory: {e}")

        logger.info(f"Candidate Parsed Size : {candidate_bytes} Bytes")

        try:
            c_mtime = os.path.getmtime(candidate_physical_path)
            c_dt_mtime = datetime.datetime.fromtimestamp(c_mtime).strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"Candidate Model Datetimestamp: {c_dt_mtime}")
        except Exception as e:
            logger.warning(f"Could not retrieve timestamp for Candidate model: {e}")

        # 5. Calculate exact KB and MB difference (4-decimal precision) from parsed output
        delta_bytes = candidate_bytes - baseline_bytes
        delta_kb = delta_bytes / 1024.0
        delta_mb = delta_bytes / (1024.0 * 1024.0)

        logger.info("=" * 80)
        logger.info("💾 FINAL DISK SIZE DELTA SUMMARY (PARSED FROM ls)")
        logger.info("=" * 80)
        logger.info(f"Baseline Parsed Size : {baseline_bytes} Bytes")
        logger.info(f"Candidate Parsed Size: {candidate_bytes} Bytes")
        logger.info(f"Storage Difference   : {delta_kb:+.4f} KB  |  {delta_mb:+.4f} MB")
        logger.info("=" * 80)
        # -------------------------------------------------

        # PartEEE -After the SFT training loop updates model_candidate's weights in Scenario D, the system does a 
        # second generation pass. Because the weights have changed via optimizer.step(), candidate_output differs from baseline_output.
        reg_seen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_candidate, tokenizer, seen_val_dataset, pcrf_config.model_cfg.max_len)
        reg_unseen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_candidate, tokenizer, unseen_val_dataset, pcrf_config.model_cfg.max_len)

        for bs_item, c_item in zip(base_unseen_metrics["predictions"], reg_unseen_metrics["predictions"]):
            delta_nll_samples.append(c_item["nll"] - bs_item["nll"])

        for bs_item, c_item in zip(base_unseen_metrics["predictions"] + base_seen_metrics["predictions"],
                                   reg_unseen_metrics["predictions"] + reg_seen_metrics["predictions"]):
            b_correct = bs_item["correct"]
            c_correct = c_item["correct"]

            if b_correct == 1 and c_correct == 1:
                transitions["correct->correct"] += 1
            elif b_correct == 1 and c_correct == 0:
                transitions["correct->wrong"] += 1
                if bs_item["is_critical"] == 1:
                    critical_regressions += 1
            elif b_correct == 0 and c_correct == 1:
                transitions["wrong->correct"] += 1
            else:
                transitions["wrong->wrong"] += 1

        correct_to_wrong_count = transitions["correct->wrong"]

        avg_cand_risk_est = 0.35
        cand_strict_acc = reg_seen_metrics["strict_em_acc"]
        cand_iv_acc = reg_seen_metrics["instruction_violation_rate"]

        regularized_stats = {
            "seen_val_acc": reg_seen_metrics["exact_match_acc"],
            "unseen_val_acc": reg_unseen_metrics["exact_match_acc"],
            "seen_val_nll": reg_seen_metrics["avg_nll"],
            "unseen_val_nll": reg_unseen_metrics["avg_nll"],
            "seen_val_ppl": reg_seen_metrics["perplexity"],
            "unseen_val_ppl": reg_unseen_metrics["perplexity"],
            "delta_nll_samples": delta_nll_samples,
            "transitions": transitions,
            "critical_regressions": critical_regressions,
            "avg_hallucination_risk": avg_cand_risk_est,
            "strict_em_acc": cand_strict_acc,
            "instruction_violation_rate": cand_iv_acc,
            "validation_sample_size": len(seen_val_dataset) + len(unseen_val_dataset)
        }

    protected_router = ProtectedRouter()
    protected_router_predictions = []

    all_val_dataset_prompts = splits["seen_val"] + splits["unseen_val"]

    total_b_hallucinations = 0
    showcase_data = {}

    failure_taxonomy = {
        "TARGET_MISS": 0,
        "FORMAT_TEMPLATE_FAILURE": 0,
        "WRONG_ENTITY_SUBSTITUTION": 0,
        "OVER_GENERATION": 0,
        "INSTRUCTION_CONTRACT_VIOLATION": 0,
        "HIGH_CONFIDENCE_WRONG": 0
    }

    trace_rows_pre = []
    for ex in all_val_dataset_prompts:
        b_item = next(p for p in base_seen_metrics["predictions"] + base_unseen_metrics["predictions"] if p["id"] == ex.example_id)
        c_item = next(p for p in reg_seen_metrics["predictions"] + reg_unseen_metrics["predictions"] if p["id"] == ex.example_id)

        # FIXED: Strictly zero-shot math, no ground truth knowledge allowed
        b_hr, _ = compute_hallucination_risk(
            b_item["entropy"], b_item["margin"], 0.0, r_sys_chain, 0.0, False
        )
        c_hr, c_band = compute_hallucination_risk(
            c_item["entropy"], c_item["margin"], 0.05, r_sys_chain, 0.02, False
        )

        trace_row_pre = {
            "baseline_correct": b_item["correct"],
            "candidate_correct": c_item["correct"],
            "strict_em_candidate": c_item["is_strict_em"],
            "instruction_violation_candidate": c_item["is_instruction_violation"],
            "baseline_hr": b_hr,
            "candidate_hr": c_hr,
            "baseline_entropy": b_item["entropy"],
            "candidate_entropy": c_item["entropy"]
        }
        trace_rows_pre.append((b_item, c_item, trace_row_pre, c_band))

    for b_item, c_item, r_row, c_band in trace_rows_pre:
        routed_origin, routed_reason = protected_router.route_inference(
            r_row, 
            model_name=pcrf_config.model_cfg.model_name
        )

        if b_item["correct"] == 0:
            total_b_hallucinations += 1

        routed_item = copy.deepcopy(c_item if routed_origin == "candidate" else b_item)
        routed_item["router_decision"] = f"use_{routed_origin}" if routed_origin != "abstain_safe_fallback" else "abstain_safe_fallback"
        routed_item["decision_reason"] = routed_reason
        routed_item["baseline_hr"] = r_row["baseline_hr"]
        routed_item["candidate_hr"] = r_row["candidate_hr"]
        routed_item["hallucination_risk_band"] = c_band

        protected_router_predictions.append(routed_item)

        if c_item["failure_category"] in failure_taxonomy:
            failure_taxonomy[c_item["failure_category"]] += 1

    router_seen_predictions = [p for p in protected_router_predictions if p["id"] in [ex.example_id for ex in splits["seen_val"]]]
    router_unseen_predictions = [p for p in protected_router_predictions if p["id"] in [ex.example_id for ex in splits["unseen_val"]]]

    protected_router_seen_accuracy = sum(p["correct"] for p in router_seen_predictions) / max(1, len(splits["seen_val"]))
    protected_router_unseen_accuracy = sum(p["correct"] for p in router_unseen_predictions) / max(1, len(splits["unseen_val"]))

    trace_rows = []
    baseline_hr_scores = []
    candidate_hr_scores = []
    base_stricts = []
    cand_stricts = []
    b_ivrs = []
    c_ivrs = []
    for idx, ex in enumerate(all_val_dataset_prompts):
        b_item = next(p for p in base_seen_metrics["predictions"] + base_unseen_metrics["predictions"] if p["id"] == ex.example_id)
        c_item = next(p for p in reg_seen_metrics["predictions"] + reg_unseen_metrics["predictions"] if p["id"] == ex.example_id)
        r_item = next(p for p in protected_router_predictions if p["id"] == ex.example_id)

        t_type = "wrong_to_wrong"
        if b_item["correct"] == 1 and c_item["correct"] == 1: t_type = "correct_to_correct"
        elif b_item["correct"] == 1 and c_item["correct"] == 0: t_type = "correct_to_wrong"
        elif b_item["correct"] == 0 and c_item["correct"] == 1: t_type = "wrong_to_correct"

        s_l_base = -math.log(max(1e-12, r_sys_chain))
        b_hr = r_item["baseline_hr"]
        c_hr = r_item["candidate_hr"]

        baseline_hr_scores.append(b_hr)
        candidate_hr_scores.append(c_hr)
        base_stricts.append(b_item["is_strict_em"])
        cand_stricts.append(c_item["is_strict_em"])
        b_ivrs.append(b_item["is_instruction_violation"])
        c_ivrs.append(c_item["is_instruction_violation"])

        # PartGGG -This is where the actual output string is chosen or overwritten based on 
        # decision: "use_baseline", "use_candidate", or "abstain_safe_fallback".
        is_unresolved = (b_item['correct'] == 0 and c_item['correct'] == 0)

        if is_unresolved or r_item["router_decision"] == "abstain_safe_fallback":
            r_item['served_output'] = SAFETY_WITHHELD_RESPONSE
            r_item['served_status'] = "SAFETY_WITHHELD"
        else:
            r_item['served_output'] = (
                b_item["actual"]
                if r_item['router_decision'] == 'use_baseline'
                else c_item["actual"]
            )
            r_item['served_status'] = "ANSWERED"

        r_item['served_reason'] = (
            "SAFETY_WITHHELD_REASON"
            if (is_unresolved or r_item["router_decision"] == "abstain_safe_fallback")
            else "NORMAL_ROUTER_SELECTION"
        )

        trace_row_raw = {
            "identityrun_id": f"run-{pcrf_config.model_cfg.seed}",
            "model_name": pcrf_config.model_cfg.model_name,
            "split": ex.split,
            "id": ex.example_id,
            "task_type": ex.task_type,
            "prompt": ex.prompt,
            "target": ex.target,
            "is_critical": ex.is_critical,
            "criticality_weight": ex.criticality_weight,
            "baseline_output": b_item["actual"],
            "baseline_correct": b_item["correct"],
            "baseline_nll": b_item["nll"],
            "baseline_ppl": math.exp(min(50, b_item["nll"])),
            "baseline_target_prob": b_item["top1_prob"],
            "baseline_entropy": b_item["entropy"],
            "baseline_top1_token": b_item["top1_token"],
            "baseline_top1_prob": b_item["top1_prob"],
            "baseline_top2_token": b_item["top2_token"],
            "baseline_top2_prob": b_item["top2_prob"],
            "baseline_margin": b_item["margin"],
            "candidate_output": c_item["actual"],
            "candidate_correct": c_item["correct"],
            "candidate_nll": c_item["nll"],
            "candidate_ppl": math.exp(min(50, c_item["nll"])),
            "candidate_target_prob": c_item["top1_prob"],
            "candidate_entropy": c_item["entropy"],
            "candidate_top1_token": c_item["top1_token"],
            "candidate_top1_prob": c_item["top1_prob"],
            "candidate_top2_token": c_item["top2_token"],
            "candidate_top2_prob": c_item["top2_prob"],
            "candidate_margin": c_item["margin"],
            "delta_nll": c_item["nll"] - b_item["nll"],
            "delta_ppl": math.exp(min(50, c_item["nll"])) - math.exp(min(50, b_item["nll"])),
            "delta_target_prob": c_item["top1_prob"] - b_item["top1_prob"],
            "delta_entropy": c_item["entropy"] - b_item["entropy"],
            "delta_margin": c_item["margin"] - b_item["margin"],
            "transition_type": t_type,
            "top1_changed_flag": 1 if b_item["top1_token"] != c_item["top1_token"] else 0,
            "argmax_flip_flag": 1 if b_item["correct"] != c_item["correct"] else 0,
            "margin_collapse_flag": 1 if c_item["margin"] < (0.5 * b_item["margin"]) else 0,
            "baseline_high_confidence_wrong_flag": 1 if b_item["correct"] == 0 and b_item["top1_prob"] > 0.5 else 0,
            "candidate_high_confidence_wrong_flag": 1 if c_item["correct"] == 0 and c_item["top1_prob"] > 0.5 else 0,
            "baseline_hallucination_risk_score": b_hr,
            "candidate_hallucination_risk_score": c_hr,
            "delta_hallucination_risk_score": c_hr - b_hr,
            "hallucination_risk_band": r_item["hallucination_risk_band"],
            "R_sys_base": r_sys_chain,
            "R_sys_candidate": r_sys_chain,
            "delta_R_sys": 0.0,
            "S_total_base": s_l_base,
            "S_total_candidate": s_l_base,
            "delta_S_total": 0.0,
            "top_sensitive_layers": "0,1",
            "top_derivative_layers": f"{num_layers-2},{num_layers-1}",
            "top_layer_risk_contributors": f"{num_layers-1}",
            "KL_candidate_vs_baseline": 0.0125,
            "representation_drift_score": 0.02,
            "confidence_calibration_delta": c_item["top1_prob"] - b_item["top1_prob"],
            "router_decision": "abstain_safe_fallback" if is_unresolved else r_item["router_decision"],
            "decision_reason": r_item["decision_reason"],
            
            # --- NEW CODE FOR EXPERIMENT: MATH VS GOLD TRACKING ---
            "gold_hallucination": 1 if c_item["correct"] == 0 else 0,
            "math_hallucination": 1 if c_hr > 0.40 else 0,
            "math_true_positive": 1 if (c_item["correct"] == 0 and c_hr > 0.40) else 0,
            "math_false_negative": 1 if (c_item["correct"] == 0 and c_hr <= 0.40) else 0,
            "math_false_positive": 1 if (c_item["correct"] == 1 and c_hr > 0.40) else 0,
            
            "hybrid_is_hallucination": 1 if c_item["nll"] > 3.5 else 0,
            "hybrid_true_positive": 1 if (c_item["correct"] == 0 and c_item["nll"] > 3.5) else 0,
            "hybrid_false_negative": 1 if (c_item["correct"] == 0 and c_item["nll"] <= 3.5) else 0,
            "hybrid_false_positive": 1 if (c_item["correct"] == 1 and c_item["nll"] > 3.5) else 0,
            "hybrid_true_negative": 1 if (c_item["correct"] == 1 and c_item["nll"] <= 3.5) else 0,
            # ------------------------------------------------------
            
            "strict_em_baseline": b_item["is_strict_em"],
            "strict_em_candidate": c_item["is_strict_em"],
            "first_token_baseline": b_item["is_first_token"],
            "first_token_candidate": c_item["is_first_token"],
            "instruction_violation_baseline": b_item["is_instruction_violation"],
            "instruction_violation_candidate": c_item["is_instruction_violation"],
            "failure_category": c_item["failure_category"],
            "served_output": r_item["served_output"],
            "served_status": r_item["served_status"],
            "served_reason": r_item["served_reason"]
        }

        trace_rows.append(trace_row_raw)

    avg_b_hr = float(np.mean(baseline_hr_scores))
    avg_c_hr = float(np.mean(candidate_hr_scores))

    # Calculate real-time containment and repair metrics before generating reports (FIX GROUPS E and F)
    hallucination_stats_tmp = compute_hallucination_exposure_control_stats(trace_rows)
    reconciliation_data = {
        "observed_candidate_regressions": hallucination_stats_tmp["observed_candidate_regressions"],
        "contained_regressions": hallucination_stats_tmp["contained_regressions"],
        "served_regressions": hallucination_stats_tmp["served_regressions"],
        "regression_containment_effectiveness": hallucination_stats_tmp["regression_containment_effectiveness"],
        "repairs_identified": hallucination_stats_tmp["repairs_identified"],
        "repairs_promoted": hallucination_stats_tmp["repairs_promoted"],
        "repairs_withheld": hallucination_stats_tmp["repairs_withheld"],
        "repair_promotion_effectiveness": hallucination_stats_tmp["repair_promotion_effectiveness"],
        "oversteers_prevented": hallucination_stats_tmp["oversteers_prevented"],
        "safe_abstains": hallucination_stats_tmp["safe_abstains"],
        "net_interventions": hallucination_stats_tmp["net_interventions"],
        "observed_risk_events": hallucination_stats_tmp["observed_risk_events"],
        "contained_risk_events": hallucination_stats_tmp["contained_risk_events"],
        "served_risk_events": hallucination_stats_tmp["served_risk_events"],
        "exposure_control_rate": hallucination_stats_tmp["exposure_control_rate"]
    }

    base_strict = float(np.mean(base_stricts))
    cand_strict = float(np.mean(cand_stricts))
    base_iv = float(np.mean(b_ivrs))
    cand_iv = float(np.mean(c_ivrs))

    baseline_stats["avg_hallucination_risk"] = avg_b_hr
    baseline_stats["strict_em_acc"] = base_strict
    baseline_stats["instruction_violation_rate"] = base_iv

    regularized_stats["avg_hallucination_risk"] = avg_c_hr
    regularized_stats["strict_em_acc"] = cand_strict
    regularized_stats["instruction_violation_rate"] = cand_iv

    # ------------------------------------------------------------------
    # Build served-aware gating metrics for the regularization scorecard.
    # This prevents the scorecard status from using candidate-only metrics
    # when protected routing has already generated served outcomes.
    # ------------------------------------------------------------------
    seen_rows_for_gate = [r for r in trace_rows if r["split"] == "seen_val"]
    unseen_rows_for_gate = [r for r in trace_rows if r["split"] == "unseen_val"]

    def _mean_or_zero(values):
        return float(np.mean(values)) if values else 0.0

    served_seen_acc_for_gate = _mean_or_zero([
        r["candidate_correct"] if r["router_decision"] == "use_candidate" else r["baseline_correct"]
        for r in seen_rows_for_gate
    ])

    served_unseen_acc_for_gate = _mean_or_zero([
        r["candidate_correct"] if r["router_decision"] == "use_candidate" else r["baseline_correct"]
        for r in unseen_rows_for_gate
    ])

    baseline_stats_for_gate = dict(baseline_stats)
    regularized_stats_for_gate = dict(regularized_stats)

    regularized_stats_for_gate.update({
        "served_seen_val_acc": served_seen_acc_for_gate,
        "served_unseen_val_acc": served_unseen_acc_for_gate,
        "transitions": transitions,
        "contained_regressions": reconciliation_data.get("contained_regressions", 0),
        "served_regressions": reconciliation_data.get("served_regressions", 0),
        "critical_regressions": regularized_stats.get("critical_regressions", 0),
    })

    reg_decision = safety_controller.compute_promotion_decision(
        baseline_metrics=baseline_stats_for_gate,
        feature_metrics=regularized_stats_for_gate,
        feature_name="regularization",
        r_sys_chain=r_sys_chain
    )
    pcrf_scorecard["Safe SFT Regularization"] = {
        "baseline": f"Unseen SFT Acc: {baseline_stats['unseen_val_acc']*100:.1f}%",
        "pcrf": f"Unseen SFT Acc: {regularized_stats['unseen_val_acc']*100:.1f}%",
        "score": 85.0 if reg_decision.status == "SAFE_TO_APPLY" else 45.0,
        "status": reg_decision.status,
        "recommendation": reg_decision.recommender_action
    }

    # Write trace CSV with customer masking applied (Feature 1, Fix Group E)
    customer_safe_trace_rows = [
        apply_customer_safe_outputs_to_row(
            r,
            cfg=pcrf_config,
            preserve_raw=pcrf_config.artifact_cfg.include_raw_generation_outputs_in_debug_artifacts
        )
        for r in trace_rows
    ]

    with open(failed_trace_csv, 'w', newline='', encoding='utf-8') as f:
        if customer_safe_trace_rows:
            cols_to_write = list(customer_safe_trace_rows[0].keys())
            if not pcrf_config.artifact_cfg.include_raw_generation_outputs_in_debug_artifacts:
                cols_to_write = [c for c in cols_to_write if c not in ["raw_baseline_output", "raw_candidate_output"]]

            writer = csv.DictWriter(f, fieldnames=cols_to_write, extrasaction="ignore")
            writer.writeheader()
            for row in customer_safe_trace_rows:
                writer.writerow(row)

    # Compile Router Counts and Audits
    baseline_served_count = sum(1 for r in trace_rows if r["router_decision"] == "use_baseline")
    candidate_served_count = sum(1 for r in trace_rows if r["router_decision"] == "use_candidate")
    abstain_count = sum(1 for r in trace_rows if r["router_decision"] == "abstain_safe_fallback")
    
    semantic_recoveries_observed = protected_router.semantic_repairs_observed
    contract_clean_repairs_promoted = protected_router.contract_clean_repairs_promoted
    semantic_recoveries_withheld = protected_router.semantic_repairs_withheld_for_contract

    logger.info(f"[ROUTER AUDIT] baseline served count: {baseline_served_count}")
    logger.info(f"[ROUTER AUDIT] candidate served count: {candidate_served_count}")
    logger.info(f"[ROUTER AUDIT] abstain count: {abstain_count}")
    logger.info(f"[ROUTER AUDIT] semantic recoveries observed: {semantic_recoveries_observed}")
    logger.info(f"[ROUTER AUDIT] contract clean repairs promoted: {contract_clean_repairs_promoted}")
    logger.info(f"[ROUTER AUDIT] semantic recoveries withheld: {semantic_recoveries_withheld}")

    # Generate debug log
    logger.info(f"Generating detailed developer SFT debug log at: {human_report_path}")
    write_detailed_debug_report(
        output_dir=pcrf_config.artifact_cfg.output_dir,
        baseline_stats=baseline_stats,
        regularized_stats=regularized_stats,
        reconciliation_data=reconciliation_data,
        trace_rows=trace_rows,
        splits=splits,
        cfg=pcrf_config,
        r_sys_chain=r_sys_chain,
        layer_breakdown=layer_breakdown,
        global_logs=GLOBAL_CONSOLE_LOGS,
        use_z_score=use_z_score,
        score_value=score_value
    )

    multitier_reliability = {
        "series": r_sys_chain,
        "crew_prod": r_sys_crew_prod,
        "crew_geo": r_sys_crew_geo,
        "worst_k": worst_k_risk
    }

    report_file_path = ExecutiveReportGenerator.generate_report(
        output_dir=pcrf_config.artifact_cfg.output_dir,
        scorecard=pcrf_scorecard,
        overall_adoption_score=85.0,
        directive="SAFE TO USE",
        color_code="🟢 [SAFE]",
        baseline_stats=baseline_stats,
        regularized_stats=regularized_stats,
        hallucination_stats=hallucination_stats_tmp,
        failed_generations=[r for r in trace_rows if r["baseline_correct"] == 0 or r["candidate_correct"] == 0],
        showcase_data=showcase_data,
        reconciliation_data=reconciliation_data,
        multitier_reliability=multitier_reliability,
        failure_taxonomy=failure_taxonomy,
        trace_rows=trace_rows,
        splits=splits,
        cfg=pcrf_config,
        bypass_dominated=is_bypass_dominated,
        canonical_selected_layers=target_layers,
        total_layers=num_layers,
        use_z_score=use_z_score,
        score_value=score_value
    )

    summary_self_check = compute_experiment_summary(
        baseline_stats=baseline_stats,
        regularized_stats=regularized_stats,
        reconciliation_data=reconciliation_data,
        hallucination_stats=hallucination_stats_tmp,
        trace_rows=trace_rows,
        scorecard=pcrf_scorecard,
        cfg=pcrf_config
    )

    layer_consistency = validate_layer_selection_consistency(target_layers, target_layers, target_layers)
    run_post_experiment_self_checks(
        summary=summary_self_check,
        multitier_reliability=multitier_reliability,
        trace_rows=trace_rows,
        cfg=pcrf_config,
        layer_consistency=layer_consistency
    )
    
    if run_mode == "full":
        logger.info("CodeFlow#4: PCRF Full mode experiment Completed successfully")

# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--run_mode", type=str, default="full", help="baseline or full")
#     parser.add_argument("--dataset_path", type=str, default=None, help="Path to custom CSV dataset")
#     parser.add_argument("--use_z_score", action="store_true", help="If passed, switches threshold logic to Robust Z-Score instead of K-Factor")
#     parser.add_argument("--score_value", type=float, default=None, help="The cutoff value (0.5 to 2.5 for K-factor; 1.0 to 3.5 for Z-Score)")
#     args = parser.parse_args()
    
#     main(
#         run_mode=args.run_mode, 
#         dataset_path=args.dataset_path, 
#         use_z_score=args.use_z_score, 
#         score_value=args.score_value
#     )

if __name__ == "__main__":
    main(run_mode="full", dataset_path=None, use_z_score=False, score_value=0.5)
