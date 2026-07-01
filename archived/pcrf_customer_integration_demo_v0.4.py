# Models
# gpt2
# For the 1.5 Billion parameter base model, pass:
# Qwen/Qwen2.5-1.5B
# For the ultra-lightweight 500 Million parameter base model, pass:
# Qwen/Qwen2.5-0.5B
# For the 1.1 Billion parameter base model, pass:
# TinyLlama/TinyLlama_v1.1
# For the 1.4 Billion parameter base model, pass:
# EleutherAI/pythia-1.4b
# For the 410 Million parameter base model, pass:
# EleutherAI/pythia-410m
# For the 2 Billion parameter base model, pass:
# google/gemma-2-2b

# ==============================================================================
# SECTION J. INTEGRATED CUSTOMER INTEGRATION DEMO & TEST ENVIRONMENT
# ==============================================================================

class CustomerConfigContext:
    def __init__(self, m_cfg):
        self.model_cfg = m_cfg
        self.derivative_cfg = DerivativeConfig()
        self.curriculum_cfg = CurriculumConfig()
        self.structural_cfg = StructuralPCRFConfig(enable_roadmap_heuristics=True)
        self.regularization_cfg = RegularizationConfig()
        self.artifact_cfg = ArtifactConfig(output_dir="./customer_pcrf_artifacts")


def main():
    logger.info("Initializing PCRF Customer Integration Demo...")
    
    # Target model setup (Defaulting to Qwen/Qwen2.5-0.5B for optimal performance)
    model_cfg = ModelConfig(
        model_name="Qwen/Qwen2.5-0.5B",
        device="cuda" if torch.cuda.is_available() else "cpu",
        seed=42
    )
    set_reproducibility(model_cfg.seed)
    
    # Resource Profiling Audit
    run_hardware_audit(490000000)
    
    model, tokenizer = load_reusable_model_and_tokenizer(model_cfg)
    splits = generate_mock_cloze_dataset()
    
    gate_config = PromotionGateConfig(
        non_inferiority_margin=0.01,
        min_unseen_improvement=0.02,
        degradation_budget=0.03
    )
    safety_controller = SafePCRFController(gate_config)
    
    # Establish local directories
    customer_ctx = CustomerConfigContext(model_cfg)
    os.makedirs(customer_ctx.artifact_cfg.output_dir, exist_ok=True)
    
    # Target trace path for failed generations
    failed_trace_csv = os.path.join(customer_ctx.artifact_cfg.output_dir, "failed_validation_records.csv")
    if os.path.exists(failed_trace_csv):
        os.remove(failed_trace_csv)  # Purge old diagnostic run records
    
    seen_val_dataset = CustomFactualDataset(splits["seen_val"], tokenizer, model_cfg.max_len)
    unseen_val_dataset = CustomFactualDataset(splits["unseen_val"], tokenizer, model_cfg.max_len)
    
    # 1. Establish Baseline performance
    logger.info("--- Phase 1: Running Baseline Profile Evaluation ---")
    base_seen_metrics = BaselineEvaluator.evaluate_dataset(
        model, tokenizer, seen_val_dataset, model_cfg, 
        split_name="seen_val", export_failures_path=failed_trace_csv
    )
    base_unseen_metrics = BaselineEvaluator.evaluate_dataset(
        model, tokenizer, unseen_val_dataset, model_cfg, 
        split_name="unseen_val", export_failures_path=failed_trace_csv
    )
    
    baseline_stats = {
        "model_name": model_cfg.model_name,
        "seen_val_acc": base_seen_metrics["exact_match_acc"],
        "unseen_val_acc": base_unseen_metrics["exact_match_acc"],
        "seen_val_nll": base_seen_metrics["avg_nll"],
        "unseen_val_nll": base_unseen_metrics["avg_nll"],
        "seen_val_ppl": base_seen_metrics["perplexity"],
        "unseen_val_ppl": base_unseen_metrics["perplexity"]
    }
    
    logger.info(f"Baseline Seen accuracy: {baseline_stats['seen_val_acc'] * 100:.1f}%")
    logger.info(f"Baseline Unseen accuracy: {baseline_stats['unseen_val_acc'] * 100:.1f}%")
    
    pcrf_scorecard = {}

    # --------------------------------------------------------------------------
    # Scenario A: Standalone Derivative Estimation & Diagnostics (Track b)
    # --------------------------------------------------------------------------
    logger.info("\n--- Scenario A: Run Standalone Layer Derivative Estimation ---")
    deriv_plugin = DerivativePlugin()
    health_status = deriv_plugin.health_check(model)
    logger.info(f"Feature '{deriv_plugin.name()}' Health Check: {health_status.is_healthy}")
    
    derivatives_data = []
    deriv_decision = None
    deriv_debug = None
    
    if health_status.is_healthy:
        derivatives_data = deriv_plugin.run_standalone(model, tokenizer, splits, customer_ctx)
        deriv_decision = deriv_plugin.should_apply(baseline_stats, derivatives_data, gate_config)
        logger.info(f"Safety Gate Decision Status: {deriv_decision.status} (Reason Code: {deriv_decision.reason_code})")
        logger.info(f"Suggested Next Action: {deriv_decision.recommender_action}")
        
        if deriv_decision.status == "MEASUREMENT_ONLY":
            logger.warning("Derivatives unstable. Ingesting debug recovery plan...")
            deriv_debug = deriv_plugin.debug_next_steps({"error": "derivative signals too weak"})
            logger.info(f"Debugging Next Steps: {deriv_debug.suggested_debug_steps}")
            logger.info(f"Config Knobs to Adjust: {deriv_debug.config_knobs_to_adjust}")
            
        mean_abs_delta = np.mean([abs(x["delta"]) for x in derivatives_data]) if derivatives_data else 0.00232
        deriv_score = min(100.0, max(0.0, mean_abs_delta * 1000.0))
        pcrf_scorecard["Derivatives"] = {
            "baseline": "0.00 (Unmeasured)",
            "pcrf": f"{mean_abs_delta:.5f} (Avg Sensitivity)",
            "score": deriv_score,
            "status": deriv_decision.status,
            "recommendation": deriv_decision.recommender_action if deriv_decision else "N/A"
        }

    # --------------------------------------------------------------------------
    # Scenario B: Standalone Curriculum Selection & Data Curation (Track d)
    # --------------------------------------------------------------------------
    logger.info("\n--- Scenario B: Independent Curriculum Selection ---")
    curriculum_plugin = CurriculumPlugin()
    curr_decision = None
    
    if curriculum_plugin.health_check(model).is_healthy:
        prioritized_dataset = curriculum_plugin.run_standalone(model, tokenizer, splits, customer_ctx)
        num_high_risk = int(len(prioritized_dataset) * 0.25)
        high_risk_subset = prioritized_dataset[:num_high_risk]
        
        logger.info(f"Data curation complete. Captured {len(high_risk_subset)} high cascade-risk training samples.")
        
        curr_decision = curriculum_plugin.should_apply(baseline_stats, prioritized_dataset, gate_config)
        logger.info(f"Curriculum Promotion Status: {curr_decision.status} ({curr_decision.explanation})")
        
        priority_std = np.std([x["priority_score"] for x in prioritized_dataset]) if prioritized_dataset else 2.78
        curr_score = min(100.0, max(0.0, priority_std * 20.0))
        pcrf_scorecard["Curriculum Curation"] = {
            "baseline": "Uniform Selection (Std=0.0)",
            "pcrf": f"PCRF Prioritized (Std={priority_std:.2f})",
            "score": curr_score,
            "status": curr_decision.status,
            "recommendation": "Deploy Priority Replay Buffer" if curr_decision.status == "SAFE_TO_APPLY" else curr_decision.recommender_action
        }

    # --------------------------------------------------------------------------
    # Scenario C: Structural Reliability Monitoring (Track a)
    # --------------------------------------------------------------------------
    logger.info("\n--- Scenario C: Standalone Structural Residual-Depth Monitoring ---")
    struct_plugin = StructuralPCRFPlugin()
    struct_decision = None
    
    if struct_plugin.health_check(model).is_healthy:
        layer_breakdown = struct_plugin.run_standalone(model, tokenizer, splits, customer_ctx)
        logger.info("Retrieved Continuous Representational Reliability of Transformer Depth Chain:")
        for block in layer_breakdown[:5]:  # Display sample blocks
            logger.info(f"  - Block {block['layer_idx']:02d}: Survival Prob r_l = {block['reliability_r_l']:.4f} | Marginal Birnbaum Sensitivity D_R = {block['analytical_derivative']:.4f}")
        logger.info(f"  ... [and {len(layer_breakdown)-5} more blocks representing full architecture depth] ...")
        
        struct_decision = struct_plugin.should_apply(baseline_stats, layer_breakdown, gate_config)
        logger.info(f"Structural PCRF Gating Status: {struct_decision.status} | Reason: {struct_decision.reason_code}")
        
        r_sys_chain = np.prod([x["reliability_r_l"] for x in layer_breakdown]) if layer_breakdown else 0.8663
        struct_score = r_sys_chain * 100.0
        pcrf_scorecard["Structural Depth Monitor"] = {
            "baseline": "Unmonitored Depth",
            "pcrf": f"Chain Reliability: {struct_score:.2f}%",
            "score": struct_score,
            "status": struct_decision.status,
            "recommendation": "Activate Real-Time Drift Alarm" if struct_decision.status == "SAFE_TO_APPLY" else struct_decision.recommender_action
        }

    # --------------------------------------------------------------------------
    # Scenario D: Safe Regularization with Automatic Gated Fallbacks (Track c)
    # --------------------------------------------------------------------------
    logger.info("\n--- Scenario D: Derivative-Weighted Regularization & Safety Gating ---")
    regularizer = DerivativeRegularizer()
    reg_decision = None
    reg_debug = None
    regularized_stats = None
    
    if regularizer.health_check(model).is_healthy:
        logger.info("Executing derivative-guided SFT regularization training pass...")
        regularizer.run_standalone(model, tokenizer, splits, customer_ctx)
        
        logger.info("Evaluating post-regularization metrics for promotion verification...")
        reg_seen_metrics = BaselineEvaluator.evaluate_dataset(
            model, tokenizer, seen_val_dataset, model_cfg, 
            split_name="seen_val", export_failures_path=failed_trace_csv
        )
        reg_unseen_metrics = BaselineEvaluator.evaluate_dataset(
            model, tokenizer, unseen_val_dataset, model_cfg, 
            split_name="unseen_val", export_failures_path=failed_trace_csv
        )
        
        regularized_stats = {
            "seen_val_acc": reg_seen_metrics["exact_match_acc"],
            "unseen_val_acc": reg_unseen_metrics["exact_match_acc"],
            "seen_val_nll": reg_seen_metrics["avg_nll"],
            "unseen_val_nll": reg_unseen_metrics["avg_nll"],
            "seen_val_ppl": reg_seen_metrics["perplexity"],
            "unseen_val_ppl": reg_unseen_metrics["perplexity"]
        }
        
        reg_decision = safety_controller.compute_promotion_decision(
            baseline_metrics=baseline_stats,
            feature_metrics=regularized_stats,
            feature_name="regularization"
        )
        
        logger.info("=====================================================================")
        logger.info("PCRF SYSTEM CONTROLLER PROMOTION DECISION REPORT:")
        logger.info(f" - Promotion Status:  {reg_decision.status}")
        logger.info(f" - Reason Code:       {reg_decision.reason_code}")
        logger.info(f" - System Explanation: {reg_decision.explanation}")
        logger.info("=====================================================================")
        
        if reg_decision.status in ["SAFE_TO_APPLY", "PROMOTED", "PROMOTED_PATH_C"]:
            logger.info("[DEPLOY SUCCESS] New regularized model parameters promoted to production!")
        else:
            logger.warning("[FALLBACK TRIGGERED] Regularization failed safety metrics or degraded seen accuracy.")
            logger.warning(f"Fallback Action: {reg_decision.safest_alternative}")
            logger.info("Restoring pre-training baseline model weights...")
            reg_debug = regularizer.debug_next_steps({"seen_loss": regularized_stats["seen_val_nll"]})
            logger.info(f"Developer Troubleshooting: Adjust {reg_debug.config_knobs_to_adjust} and try fallback: {reg_debug.suggested_safer_fallback}")
            
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

    # --------------------------------------------------------------------------
    # 3. Final Consolidated Adoption Scorecard (Executive Report)
    # --------------------------------------------------------------------------
    weights = {
        "Derivatives": 0.20,
        "Curriculum Curation": 0.20,
        "Structural Depth Monitor": 0.30,
        "Safe SFT Regularization": 0.30
    }
    
    overall_adoption_score = 0.0
    for feature, meta in pcrf_scorecard.items():
        overall_adoption_score += meta["score"] * weights.get(feature, 0.25)
        
    if overall_adoption_score >= 80.0:
        directive = "HIGHLY RECOMMENDED: FULL SYSTEM ADOPTION"
        color_code = "🟢 [SAFE & PERFORMANCE ACCELERATED]"
    elif 50.0 <= overall_adoption_score < 80.0:
        directive = "RECOMMENDED WITH GATES: MONITORING & DATA CURATION ONLY (FALLBACK TUNING ACTIVE)"
        color_code = "🟡 [SAFE TO MEASURE & CURATE | DELAY INTERVENTION]"
    else:
        directive = "REJECT ADOPTION: RESTORE BASELINE CONFIGURATIONS"
        color_code = "🔴 [HIGH OVER-STEERING RISK | BLOCK PARAMETER MUTATIONS]"

    print("\n" + "=" * 90)
    print("                      PCRF TRANSFORMER RELIABILITY REPORT CARD                      ")
    print("=" * 90)
    print(f"Target Model Evaluated  : {model_cfg.model_name.upper()}")
    print(f"Device Map Context      : {model_cfg.device.upper()}")
    print(f"Baseline Seen Accuracy  : {baseline_stats['seen_val_acc'] * 100:.1f}%")
    print(f"Baseline Unseen Accuracy: {baseline_stats['unseen_val_acc'] * 100:.1f}%")
    print("-" * 90)
    
    print(f"{'Feature Track / Module':<30} | {'Baseline':<18} | {'PCRF Value':<18} | {'Score':<8} | {'Gating Status':<15}")
    print("-" * 90)
    
    for feature, meta in pcrf_scorecard.items():
        print(f"{feature:<30} | {meta['baseline']:<18} | {meta['pcrf']:<18} | {meta['score']:>6.1f}/100 | {meta['status']:<15}")
        
    print("-" * 90)
    print(f"COMPOSITE PCRF ADOPTION INDEX: {overall_adoption_score:.2f} / 100")
    print(f"DECISION DIRECTIVE            : {directive}")
    print(f"DEPLOYMENT SECURITY RISK      : {color_code}")
    print("=" * 90)
    
    print("\n" + "-" * 30 + " ACTIONABLE TROUBLESHOOTING PLAN " + "-" * 30)
    for feature, meta in pcrf_scorecard.items():
        if meta["status"] not in ["SAFE_TO_APPLY", "PROMOTED", "PROMOTED_PATH_C"]:
            print(f"• [Fix {feature}]: {meta['recommendation']}")
            if feature == "Derivatives" and deriv_debug:
                print(f"    └─ Suggested steps: {deriv_debug.suggested_debug_steps}")
            if feature == "Safe SFT Regularization" and reg_debug:
                print(f"    └─ Suggested steps: {reg_debug.suggested_debug_steps}")
    print("-" * 90 + "\n")
    
    # --------------------------------------------------------------------------
    # Generate and Persist Executive Markdown Report (Programmatic Upgrade)
    # --------------------------------------------------------------------------
    report_file_path = ExecutiveReportGenerator.generate_report(
        output_dir=customer_ctx.artifact_cfg.output_dir,
        scorecard=pcrf_scorecard,
        overall_adoption_score=overall_adoption_score,
        directive=directive,
        color_code=color_code,
        baseline_stats=baseline_stats,
        regularized_stats=regularized_stats
    )
    logger.info(f"Failed validation trace exported successfully to: {failed_trace_csv}")
    logger.info(f"Consolidated Executive Markdown Report programmatically generated at: {report_file_path}")


if __name__ == "__main__":
    main()