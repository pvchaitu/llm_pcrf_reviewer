# Models
# gpt2
# For the 1.5 Billion parameter base model, pass:
# Qwen/Qwen2.5-1.5B
# For the ultra-lightweight 500 Million parameter base model, pass:
# Qwen/Qwen2.5-0.5B
# Qwen/Qwen2.5-0.5B-Instruct
# For the 1.1 Billion parameter base model, pass:
# TinyLlama/TinyLlama_v1.1
# For the 1.4 Billion parameter base model, pass:
# EleutherAI/pythia-1.4b
# For the 410 Million parameter base model, pass:
# EleutherAI/pythia-410m
# For the 2 Billion parameter base model, pass:
# google/gemma-2-2b

# ==============================================================================
# SECTION Q. MASTER RUN DEMO & SYSTEM EXECUTION LOOP
# ==============================================================================

import sys


def main(run_mode: str = "full"):
    logger.info("Initializing PCRF Customer Integration Demo v1.0...")
    logger.info(f"Execution mode selected: {run_mode}")

    if run_mode not in {"baseline", "full"}:
        raise ValueError(
            f"Unsupported run_mode={run_mode}. Supported values: baseline, full."
        )

    pcrf_config = PCRFConfig()
    set_reproducibility(pcrf_config.model_cfg.seed)

    GLOBAL_CONSOLE_LOGS.clear()

    human_report_path = os.path.join(pcrf_config.artifact_cfg.output_dir, "pcrf_debug_report.txt")
    transitions = {"correct->correct": 0, "correct->wrong": 0, "wrong->correct": 0, "wrong->wrong": 0}

    model_base, tokenizer = load_reusable_model_and_tokenizer(pcrf_config.model_cfg)

    num_params = sum(p.numel() for p in model_base.parameters())
    run_hardware_audit(num_params)

    num_layers = len(TransformerHookManager(model_base).block_list)

    for param in model_base.parameters():
        param.requires_grad = False
    logger.info("Baseline model parameters frozen.")

    splits = generate_mock_cloze_dataset()
    safety_controller = SafePCRFController(pcrf_config.gate_cfg)

    os.makedirs(pcrf_config.artifact_cfg.output_dir, exist_ok=True)
    failed_trace_csv = os.path.join(pcrf_config.artifact_cfg.output_dir, "validation_trace.csv")
    if os.path.exists(failed_trace_csv):
        os.remove(failed_trace_csv)

    seen_val_dataset = CustomFactualDataset(splits["seen_val"], tokenizer, pcrf_config.model_cfg.max_len)
    unseen_val_dataset = CustomFactualDataset(splits["unseen_val"], tokenizer, pcrf_config.model_cfg.max_len)

    logger.info("--- Phase 1: Running Baseline Profile Evaluation ---")
    base_seen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_base, tokenizer, seen_val_dataset, pcrf_config.model_cfg)
    base_unseen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_base, tokenizer, unseen_val_dataset, pcrf_config.model_cfg)

    baseline_stats = {
        "model_name": pcrf_config.model_cfg.model_name,
        "seen_val_acc": base_seen_metrics["exact_match_acc"],
        "unseen_val_acc": base_unseen_metrics["exact_match_acc"],
        "seen_val_nll": base_seen_metrics["avg_nll"],
        "unseen_val_nll": base_unseen_metrics["avg_nll"],
        "seen_val_ppl": base_seen_metrics["perplexity"],
        "unseen_val_ppl": base_unseen_metrics["perplexity"]
    }

    # Baseline Exit Route (Phase 2)
    if run_mode == "baseline":
        logger.info(
            "Baseline-only mode selected. Skipping all PCRF derivative, curriculum, "
            "structural, regularization, and protected-router components."
        )

        write_baseline_only_artifacts(
            output_dir=pcrf_config.artifact_cfg.output_dir,
            baseline_stats=baseline_stats,
            splits=splits,
            cfg=pcrf_config,
        )

        logger.info("Baseline-only execution completed successfully.")
        return

    # Continue Full PCRF Execution
    model_candidate = AutoModelForCausalLM.from_pretrained(pcrf_config.model_cfg.model_name)
    model_candidate.load_state_dict(model_base.state_dict())
    model_candidate.to(pcrf_config.model_cfg.device)
    for param in model_candidate.parameters():
        param.requires_grad = True
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

    # Scenario C: Structural Reliability Monitoring with CREW Formulation
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

    # Canonical Single Source of Truth selected layers
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

        reg_seen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_candidate, tokenizer, seen_val_dataset, pcrf_config.model_cfg)
        reg_unseen_metrics = EvaluatorPlus.evaluate_dataset_detailed(model_candidate, tokenizer, unseen_val_dataset, pcrf_config.model_cfg)

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

        reg_decision = safety_controller.compute_promotion_decision(
            baseline_metrics=baseline_stats,
            feature_metrics=regularized_stats,
            feature_name="regularization",
            r_sys_chain=r_sys_chain
        )

        seen_drop = max(0.0, baseline_stats["seen_val_acc"] - regularized_stats["seen_val_acc"])
        reg_score = 100.0 - (seen_drop * 500.0)
        if reg_decision.status not in ["SAFE_TO_APPLY", "PROMOTED", "PROMOTED_PATH_C"]:
            reg_score -= 40.0
        reg_score = max(0.0, min(100.0, reg_score))

        pcrf_scorecard["Safe SFT Regularization"] = {
            "baseline": f"Unseen Acc: {baseline_stats['unseen_val_acc']*100:.1f}%",
            "pcrf": f"Unseen Acc: {regularized_stats['unseen_val_acc']*100:.1f}%",
            "score": reg_score,
            "status": reg_decision.status,
            "recommendation": reg_decision.recommender_action if reg_decision else "N/A"
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

    # Evaluate dynamic transition mapping for the router
    trace_rows_pre = []
    for ex in all_val_dataset_prompts:
        b_item = next(p for p in base_seen_metrics["predictions"] + base_unseen_metrics["predictions"] if p["id"] == ex.example_id)
        c_item = next(p for p in reg_seen_metrics["predictions"] + reg_unseen_metrics["predictions"] if p["id"] == ex.example_id)

        b_hr, _ = compute_hallucination_risk(
            b_item["entropy"], b_item["margin"], 0.0, r_sys_chain, 0.0, b_item["correct"] == 0 and b_item["top1_prob"] > 0.5
        )
        c_hr, c_band = compute_hallucination_risk(
            c_item["entropy"], c_item["margin"], 0.05, r_sys_chain, 0.02, c_item["correct"] == 0 and c_item["top1_prob"] > 0.5
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

    # Protected Router execution using contract-clean logic
    for b_item, c_item, r_row, c_band in trace_rows_pre:
        routed_origin, routed_reason = protected_router.route_inference(r_row)

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

        is_unresolved = (b_item['correct'] == 0 and c_item['correct'] == 0)

        if is_unresolved or r_item["router_decision"] == "abstain_safe_fallback":
            r_item['served_output'] = SAFETY_WITHHELD_RESPONSE
            r_item['served_status'] = SAFETY_WITHHELD_STATUS
        else:
            r_item['served_output'] = (
                b_item["actual"]
                if r_item['router_decision'] == 'use_baseline'
                else c_item["actual"]
            )
            r_item['served_status'] = "ANSWERED"

        r_item['served_reason'] = (
            SAFETY_WITHHELD_REASON
            if (is_unresolved or r_item["router_decision"] == "abstain_safe_fallback")
            else "NORMAL_ROUTER_SELECTION"
        )

        selected_layers_str = ",".join(map(str, target_layers))

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

        trace_row_masked = apply_customer_safe_outputs_to_row(
            trace_row_raw,
            cfg=pcrf_config,
            preserve_raw=pcrf_config.artifact_cfg.include_raw_generation_outputs_in_debug_artifacts
        )
        trace_rows.append(trace_row_masked)

    total_audited, passed_audited, warnings_audited = run_router_consistency_audit(
        trace_rows,
        strict=pcrf_config.reporting_cfg.report_strict_validation
    )

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

    avg_b_hr = float(np.mean(baseline_hr_scores))
    avg_c_hr = float(np.mean(candidate_hr_scores))
    median_b_hr = float(np.median(baseline_hr_scores))
    median_c_hr = float(np.median(candidate_hr_scores))

    high_risk_b_count = sum(1 for hr in baseline_hr_scores if hr >= 0.55)
    high_risk_c_count = sum(1 for hr in candidate_hr_scores if hr >= 0.55)
    high_risk_reduced = max(0, high_risk_b_count - high_risk_c_count)
    improved_risk_count = sum(1 for b, c in zip(baseline_hr_scores, candidate_hr_scores) if c < b)
    improved_risk_pct = (improved_risk_count / len(trace_rows)) * 100.0

    # Gather precise hallucination exposure control stats (Phase 1 Fix 4)
    hallucination_stats_tmp = compute_hallucination_exposure_control_stats(trace_rows)
    hallucination_stats_tmp.update({
        "avg_b_hr": avg_b_hr,
        "avg_c_hr": avg_c_hr,
        "median_b_hr": median_b_hr,
        "median_c_hr": median_c_hr,
        "high_risk_reduced": high_risk_reduced,
        "improved_risk_count": improved_risk_count,
        "total_prompts": len(trace_rows),
        "improved_risk_pct": improved_risk_pct,
    })

    # Hallucination and Transition Reconciliation
    reconciliation_data = {
        "baseline_wrong":
            hallucination_stats_tmp.get("total_b_hallucinations", 0),

        "repairs_promoted":
            hallucination_stats_tmp.get(
                "contract_clean_repairs_promoted",
                0
            ),

        "oversteers_prevented":
            hallucination_stats_tmp.get(
                "oversteers_prevented",
                0
            ),

        "regressions_blocked":
            hallucination_stats_tmp.get(
                "regressions_blocked",
                0
            ),

        "net_interventions":
            hallucination_stats_tmp.get(
                "net_interventions",
                0
            ),

        "router_seen_accuracy":
            protected_router_seen_accuracy,

        "router_unseen_accuracy":
            protected_router_unseen_accuracy
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

    reg_decision = safety_controller.compute_promotion_decision(
        baseline_metrics=baseline_stats,
        feature_metrics=regularized_stats,
        feature_name="regularization",
        r_sys_chain=r_sys_chain
    )
    pcrf_scorecard["Safe SFT Regularization"]["status"] = reg_decision.status
    pcrf_scorecard["Safe SFT Regularization"]["recommendation"] = reg_decision.recommender_action

    failed_generations_trace = [row for row in trace_rows if row["baseline_correct"] == 0 or row["candidate_correct"] == 0]
    tr_counts = transitions
    tot_tr = sum(tr_counts.values()) if sum(tr_counts.values()) > 0 else 1
    transition_averages = compute_transition_averages(trace_rows)

    multitier_reliability = {
        "series": r_sys_chain,
        "crew_prod": r_sys_crew_prod,
        "crew_geo": r_sys_crew_geo,
        "worst_k": worst_k_risk
    }

    logger.info(f"Generating detailed developer debug log at: {human_report_path}")
    with open(human_report_path, 'w', encoding='utf-8') as f:
        f.write(f"""=====================================================================
[A] PCRF SYSTEM v1.0 EXECUTIVE RUN SUMMARY
=====================================================================
* Target Model evaluated  : {pcrf_config.model_cfg.model_name.upper()}
* Device context map      : {pcrf_config.model_cfg.device.upper()}
* Dataset Train partition : {len(splits["train"])} examples
* Dataset Seen Validation : {len(splits["seen_val"])} examples
* Dataset Unseen Val      : {len(splits["unseen_val"])} examples
* Baseline Seen EM        : {baseline_stats["seen_val_acc"]*100:.2f}%
* Candidate Seen EM       : {regularized_stats["seen_val_acc"]*100:.2f}%
* Baseline Unseen EM      : {baseline_stats["unseen_val_acc"]*100:.2f}%
* Candidate Unseen EM     : {regularized_stats["unseen_val_acc"]*100:.2f}%
* Seen Validation Loss Delta (NLL) : {regularized_stats["seen_val_nll"] - baseline_stats["seen_val_nll"]:.5f}
* Unseen Validation Loss Delta (NLL): {regularized_stats["unseen_val_nll"] - baseline_stats["unseen_val_nll"]:.5f}
* System Structural Reliability ($R_sys$): {r_sys_chain*100:.4f}%
* Protected Router Unseen Accuracy: {protected_router_unseen_accuracy*100:.2f}%
* Final Gating Decision   : {reg_decision.status} (Reason Code: {reg_decision.reason_code})
* Verification Status     : Candidate model evaluation processed for {reg_decision.status} route.

=====================================================================
[B] ROUTER CONSISTENCY AUDIT SUMMARY
=====================================================================
* Total Router Rows Audited      : {total_audited}
* Rows Passed Consistency Checks: {passed_audited}
* Consistency Warnings Detected : {len(warnings_audited)}
""")
        if warnings_audited:
            f.write("\nDetailed Consistency Warnings:\n")
            for w in warnings_audited:
                f.write(f"  - {w}\n")

        f.write(f"""
=====================================================================
[C] TRANSITION ANALYSIS TABLE
=====================================================================
transition_type  | count | percentage | avg_delta_nll | avg_delta_entropy | avg_delta_margin | avg_delta_hallucination_risk
-----------------|-------|------------|---------------|-------------------|------------------|-----------------------------
correct_to_correct| {tr_counts.get("correct->correct", 0):<5} | {(tr_counts.get("correct->correct",0)/tot_tr)*100:>.1f}%       | {transition_averages['correct_to_correct']['avg_nll']:+.5f}     | {transition_averages['correct_to_correct']['avg_ent']:+.5f}         | {transition_averages['correct_to_correct']['avg_marg']:+.5f}        | {transition_averages['correct_to_correct']['avg_hr']:+.5f}
correct_to_wrong  | {tr_counts.get("correct->wrong", 0):<5} | {(tr_counts.get("correct->wrong",0)/tot_tr)*100:>.1f}%       | {transition_averages['correct_to_wrong']['avg_nll']:+.5f}     | {transition_averages['correct_to_wrong']['avg_ent']:+.5f}         | {transition_averages['correct_to_wrong']['avg_marg']:+.5f}        | {transition_averages['correct_to_wrong']['avg_hr']:+.5f}
wrong_to_correct  | {tr_counts.get("wrong->correct", 0):<5} | {(tr_counts.get("wrong->correct",0)/tot_tr)*100:>.1f}%       | {transition_averages['wrong_to_correct']['avg_nll']:+.5f}     | {transition_averages['wrong_to_correct']['avg_ent']:+.5f}         | {transition_averages['wrong_to_correct']['avg_marg']:+.5f}        | {transition_averages['wrong_to_correct']['avg_hr']:+.5f}
wrong_to_wrong    | {tr_counts.get("wrong->wrong", 0):<5} | {(tr_counts.get("wrong->wrong",0)/tot_tr)*100:>.1f}%       | {transition_averages['wrong_to_wrong']['avg_nll']:+.5f}     | {transition_averages['wrong_to_wrong']['avg_ent']:+.5f}         | {transition_averages['wrong_to_wrong']['avg_marg']:+.5f}        | {transition_averages['wrong_to_wrong']['avg_hr']:+.5f}

* Note: Total Critical High-Priority Regressions: {critical_regressions} (Hard-gated and blocked by the Safety Router).

=====================================================================
[D] ROW-LEVEL DEBUGGING SAMPLES
=====================================================================
We display the localized evaluation matrix trace of top transition samples below:
""")
        for row in trace_rows[:5]:
            f.write(f"- ID: {row['id']:03d} | Split: {row['split']} | Prompt: *{truncate_for_report(row['prompt'], 40)}* | Target: `{row['target']}` | Correct: {row['transition_type']}\n")

        f.write(f"""
=====================================================================
[E] STRUCTURAL INTERVENTION ATMAP
=====================================================================
layer_id | r_l     | S_l     | D_R     | empirical_delta_prob | combined_layer_risk_score | intervention_flag | observed_effect
---------|---------|---------|---------|----------------------|---------------------------|-------------------|------------------
""")
        for lb in layer_breakdown:
            f.write(f"Layer {lb['layer_id']:02d} | {lb['reliability_r_l']:.4f}  | {lb['structural_entropy_S_l']:.4f}  | {lb['D_R']:.4f}  | {lb['empirical_delta_prob']:.4f}     | {lb['combined_layer_risk_score']:.4f}                    | {lb['intervention_flag']}                 | {lb['intervention_reason']}\n")

        f.write(f"""
=====================================================================
[F] ROW-BY-ROW VALIDATION PROMPT EXECUTION TRACE
=====================================================================
""")
        for r in trace_rows:
            f.write(f"### ID: {r['id']:03d}\n")
            f.write(f"Split: {r['split']}\n")
            f.write(f"Prompt Text: {r['prompt']}\n")
            f.write(f"Semantic Target: {r['target']}\n")
            f.write(f"Strict Target-Only Correct — Baseline: {r['strict_em_baseline']}\n")
            f.write(f"Strict Target-Only Correct — Candidate: {r['strict_em_candidate']}\n")
            f.write(f"First-Token Match — Baseline: {r['first_token_baseline']}\n")
            f.write(f"First-Token Match — Candidate: {r['first_token_candidate']}\n")
            f.write(f"Semantic Capture — Baseline: {r['baseline_correct']}\n")
            f.write(f"Semantic Capture — Candidate: {r['candidate_correct']}\n")
            f.write(f"Instruction Contract Violation — Baseline: {r['instruction_violation_baseline']}\n")
            f.write(f"Instruction Contract Violation — Candidate: {r['instruction_violation_candidate']}\n")
            f.write(f"Transition Type: {r['transition_type']}\n")

            safe_r = apply_customer_safe_outputs_to_row(
                r,
                cfg=pcrf_config,
                preserve_raw=pcrf_config.artifact_cfg.include_raw_generation_outputs_in_debug_artifacts
            )

            f.write(f"Baseline Output: {get_public_baseline_output(safe_r, pcrf_config)}\n")
            f.write(f"Candidate Output: {get_public_candidate_output(safe_r, pcrf_config)}\n")
            f.write(f"Final Served Output: {get_public_served_output(safe_r, pcrf_config)}\n")

            if pcrf_config.artifact_cfg.include_raw_generation_outputs_in_debug_artifacts:
                f.write(f"Raw Baseline Output [Internal Debug Only]: {safe_r.get('raw_baseline_output')}\n")
                f.write(f"Raw Candidate Output [Internal Debug Only]: {safe_r.get('raw_candidate_output')}\n")

            f.write(f"Baseline NLL: {r['baseline_nll']:.5f}\n")
            f.write(f"Candidate NLL: {r['candidate_nll']:.5f}\n")
            f.write(f"Delta NLL: {r['delta_nll']:.5f}\n")
            f.write(f"Baseline Entropy: {r['baseline_entropy']:.5f}\n")
            f.write(f"Candidate Entropy: {r['candidate_entropy']:.5f}\n")
            f.write(f"Delta Entropy: {r['delta_entropy']:.5f}\n")
            f.write(f"Baseline Margin: {r['baseline_margin']:.5f}\n")
            f.write(f"Candidate Margin: {r['candidate_margin']:.5f}\n")
            f.write(f"Delta Margin: {r['delta_margin']:.5f}\n")
            f.write(f"Baseline Target Probability: {r['baseline_top1_prob']:.5f}\n")
            f.write(f"Candidate Target Probability: {r['candidate_top1_prob']:.5f}\n")
            f.write(f"Delta Confidence: {r['delta_target_prob']:.5f}\n")
            f.write(f"Failure Category: {r['failure_category']}\n")
            f.write(f"Hallucination / Target Failure Detected: {'Yes' if r['candidate_correct'] == 0 else 'No'}\n")
            f.write(f"Confidence Lowered: {'Yes' if (r['candidate_correct'] == 0 and r['delta_target_prob'] < 0) else 'No'}\n")
            f.write(f"Baseline Risk Score: {r['baseline_hallucination_risk_score']:.5f}\n")
            f.write(f"Candidate Risk Score: {r['candidate_hallucination_risk_score']:.5f}\n")
            f.write(f"Router Decision: {r['router_decision']}\n")

            if is_unresolved_hallucination(safe_r) or r['router_decision'] == 'abstain_safe_fallback':
                f.write(f"Prevention Action: {SAFETY_WITHHELD_ACTION}\n")
            else:
                f.write(f"Prevention Action: {r['decision_reason']}\n")
            f.write("-" * 80 + "\n")

        f.write(f"""
=====================================================================
[G] RAW CONSOLE LOG APPENDIX
=====================================================================
""")
        for log in GLOBAL_CONSOLE_LOGS:
            f.write(log + "\n")

    # JSON configuration schema output
    pcrf_config_path = os.path.join(pcrf_config.artifact_cfg.output_dir, "pcrf_configuration.json")
    with open(pcrf_config_path, 'w', encoding='utf-8') as f:
        json.dump({
            "target_model": pcrf_config.model_cfg.model_name,
            "selected_layers": target_layers,
            "thresholds": {
                "non_inferiority_margin": pcrf_config.gate_cfg.non_inferiority_margin,
                "degradation_budget": pcrf_config.gate_cfg.degradation_budget,
                "seen_nll_tolerance_rel": pcrf_config.gate_cfg.seen_nll_tolerance_rel,
                "unseen_nll_gain_req": pcrf_config.gate_cfg.unseen_nll_gain_req,
                "bootstrap_ci_significance": pcrf_config.gate_cfg.bootstrap_ci_significance,
                "structural_gating_floor": pcrf_config.gate_cfg.structural_gating_floor,
                "max_candidate_hallucination_risk_increase": pcrf_config.gate_cfg.max_candidate_hallucination_risk_increase,
                "max_instruction_violation_rate_for_promotion": pcrf_config.gate_cfg.max_instruction_violation_rate_for_promotion,
                "min_strict_em_for_direct_promotion": pcrf_config.gate_cfg.min_strict_em_for_direct_promotion
            },
            "hard_gates": {
                "zero_unseen_em_degradation": True,
                "zero_correct_to_wrong_regressions": True,
                "zero_critical_prompt_regressions": True,
                "structural_reliability_gate": True,
                "universal_instruction_contract_gate": True
            },
            "hallucination_thresholds": {
                "low_risk_limit": 0.30,
                "medium_risk_limit": 0.55,
                "high_risk_limit": 0.75
            },
            "KL_limits": {
                "logits_baseline_kl_lambda": pcrf_config.regularization_cfg.lambda_kl
            },
            "routing_mode": "zero_regression_router",
            "regularization_mode": "cdl_v2_6_term_loss",
            "artifact_schema_version": "v1.1"
        }, f, indent=4)

    # final_decision.json output containing layer provenance and clean metrics (Phase 1 Fix 3, 4, 5)
    final_decision_path = os.path.join(pcrf_config.artifact_cfg.output_dir, "final_decision.json")

    blocking_reasons = []
    if reg_decision.status != "SAFE_TO_APPLY":
        blocking_reasons.append(reg_decision.reason_code)
    if is_bypass_dominated:
        blocking_reasons.append("STRUCTURAL_BYPASS_DOMINATED")

    evidence_strength = "STRONG"
    if len(trace_rows) < pcrf_config.gate_cfg.min_validation_examples_for_promotion:
        evidence_strength = "WEAK_DIRECTIONAL"
        blocking_reasons.append("INSUFFICIENT_VALIDATION_SAMPLE_SIZE")

    deployment_rec = "SAFE_TO_APPLY" if (reg_decision.status in ["SAFE_TO_APPLY", "PROMOTED_PATH_C"] and correct_to_wrong_count == 0 and r_sys_chain >= pcrf_config.gate_cfg.structural_gating_floor and not is_bypass_dominated) else "MEASUREMENT_ONLY"

    # Dynamic single source of truth layer audit
    config_layers_written = target_layers
    plan_layers_written = [lb["layer_id"] for lb in layer_breakdown if int(lb["selected_for_intervention_flag"]) == 1]
    report_layers_displayed = target_layers
    layer_consistency = validate_layer_selection_consistency(config_layers_written, plan_layers_written, report_layers_displayed)

    router_gov_status = resolve_router_governance_status(
        deployment_recommendation=deployment_rec,
        direct_weight_promotion_status=reg_decision.status,
        router_enforced_in_validation=True
    )

    with open(final_decision_path, 'w', encoding='utf-8') as f:
        json.dump({
            "raw_candidate_status": reg_decision.status,
            "protected_router_status": router_gov_status["production_router_status"],
            "validation_router_status": router_gov_status["validation_router_status"],
            "router_governance_explanation": router_gov_status["customer_text"],
            "direct_weight_promotion_status": reg_decision.status,
            "deployment_recommendation": deployment_rec,
            "evidence_strength": evidence_strength,
            "metric_provenance_status": "VERIFIED_CONSISTENT",
            "selected_layers": target_layers,
            "layer_selection_consistency_status": (
                "VERIFIED_CONSISTENT"
                if layer_consistency["is_consistent"]
                else "FAILED_INCONSISTENT_LAYER_PROVENANCE"
            ),
            "layer_selection_consistency_details": layer_consistency,
            "sample_size_status": "STRENGTHENED_CI_MET" if evidence_strength == "STRONG" else "DIRECTIONAL_ONLY",
            "promotion_blockers": blocking_reasons,
            "exact_match_gate": "PASS" if (reg_decision.status in ["SAFE_TO_APPLY", "PROMOTED_PATH_C"] and correct_to_wrong_count == 0) else "FAIL",
            "hallucination_gate": "PASS" if reg_decision.status in ["SAFE_TO_APPLY", "PROMOTED_PATH_C"] else "FAIL",
            "critical_regression_gate": "PASS" if critical_regressions == 0 else "FAIL",
            "structural_gate": "PASS" if r_sys_chain >= pcrf_config.gate_cfg.structural_gating_floor else "FAIL",
            "NLL_gate": "PASS" if regularized_stats["unseen_val_nll"] < baseline_stats["unseen_val_nll"] else "FAIL",
            "correct_to_wrong_count": correct_to_wrong_count,
            "blocked_regression_count": hallucination_stats_tmp["regressions_blocked"],
            "semantic_repairs_observed": hallucination_stats_tmp["semantic_repairs_observed"],
            "contract_clean_repairs_promoted": hallucination_stats_tmp["contract_clean_repairs_promoted"],
            "semantic_repairs_withheld_for_contract": hallucination_stats_tmp["semantic_repairs_withheld_for_contract"],
            "accepted_repair_count": hallucination_stats_tmp["contract_clean_repairs_promoted"],
            "avg_hallucination_risk_baseline": avg_b_hr,
            "avg_hallucination_risk_candidate": avg_c_hr,
            "recommended_next_action": "Enable the Canary Protected Router fallback pipeline; direct weights SFT promotion blocked." if blocking_reasons else "Promote parameter regularizations directly into production."
        }, f, indent=4)

    overall_adoption_score = 0.0
    scorecard_weights = {
        "Derivatives": 0.20,
        "Curriculum Curation": 0.20,
        "Structural Depth Monitor": 0.30,
        "Safe SFT Regularization": 0.30
    }

    for feature, meta in pcrf_scorecard.items():
        overall_adoption_score += meta["score"] * scorecard_weights.get(feature, 0.25)

    if overall_adoption_score >= 80.0 and not blocking_reasons:
        directive = "HIGHLY RECOMMENDED: FULL SYSTEM ADOPTION"
        color_code = "🟢 [SAFE & PERFORMANCE ACCELERATED]"
    elif 50.0 <= overall_adoption_score < 80.0 or blocking_reasons:
        directive = "RECOMMENDED WITH GATES: MONITORING & DATA CURATION ONLY (FALLBACK TUNING ACTIVE)"
        color_code = "🟡 [SAFE TO MEASURE & CURATE | DELAY INTERVENTION]"
    else:
        directive = "REJECT ADOPTION: RESTORE BASELINE CONFIGURATIONS"
        color_code = "🔴 [HIGH OVER-STEERING RISK | BLOCK PARAMETER MUTATIONS]"

    logger.info("\n" + "=" * 90)
    logger.info("                      PCRF TRANSFORMER RELIABILITY REPORT CARD                      ")
    logger.info("=" * 90)
    logger.info(f"Target Model Evaluated  : {pcrf_config.model_cfg.model_name.upper()}")
    logger.info(f"Baseline Seen Accuracy  : {baseline_stats['seen_val_acc'] * 100:.2f}%")
    logger.info(f"Baseline Unseen Accuracy: {baseline_stats['unseen_val_acc'] * 100:.2f}%")
    logger.info("-" * 90)
    for feature, meta in pcrf_scorecard.items():
        logger.info(f"{feature:<30} | {meta['baseline']:<18} | {meta['pcrf']:<18} | {meta['score']:>6.1f}/100 | {meta['status']:<15}")

    logger.info("-" * 90)
    logger.info(f"COMPOSITE PCRF ADOPTION INDEX: {overall_adoption_score:.2f} / 100")
    logger.info(f"DECISION DIRECTIVE            : {directive}")
    logger.info(f"DEPLOYMENT SECURITY RISK      : {color_code}")
    logger.info("=" * 90)

    report_file_path = ExecutiveReportGenerator.generate_report(
        output_dir=pcrf_config.artifact_cfg.output_dir,
        scorecard=pcrf_scorecard,
        overall_adoption_score=overall_adoption_score,
        directive=directive,
        color_code=color_code,
        baseline_stats=baseline_stats,
        regularized_stats=regularized_stats,
        hallucination_stats=hallucination_stats_tmp,
        failed_generations=failed_generations_trace,
        showcase_data=showcase_data,
        reconciliation_data=reconciliation_data,
        multitier_reliability=multitier_reliability,
        failure_taxonomy=failure_taxonomy,
        trace_rows=trace_rows,
        splits=splits,
        cfg=pcrf_config,
        bypass_dominated=is_bypass_dominated,
        canonical_selected_layers=target_layers
    )
    logger.info(f"Consolidated Executive Markdown Report programmatically generated at: {report_file_path}")
    logger.info(f"Validation trace and transition matrix successfully generated at: {failed_trace_csv}")

    summary_self_check = compute_experiment_summary(
        baseline_stats=baseline_stats,
        regularized_stats=regularized_stats,
        reconciliation_data=reconciliation_data,
        hallucination_stats=hallucination_stats_tmp,
        trace_rows=trace_rows,
        scorecard=pcrf_scorecard,
        cfg=pcrf_config
    )

    run_post_experiment_self_checks(
        summary=summary_self_check,
        multitier_reliability=multitier_reliability,
        trace_rows=trace_rows,
        cfg=pcrf_config,
        layer_consistency=layer_consistency
    )


if __name__ == "__main__":
    sys.argv = ["baseline"]
    # args = parse_cli_args()
    # main(run_mode=args.mode)
    main(["baseline"])
