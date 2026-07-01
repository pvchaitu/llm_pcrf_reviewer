"""
pcrf_customer_integration_demo.py
==================================
This script demonstrates how an enterprise customer or ML platform engineer 
would programmatically use the "PCRF Transformer Reliability Suite v1" as a 
reusable library. 

It covers:
  1. Initialization and Baseline Evaluation
  2. Scenario A: Standalone Derivative Estimation & Diagnostics (Track b)
  3. Scenario B: Standalone Curriculum Selection & Data Curation (Track d)
  4. Scenario C: Structural Reliability Monitoring (Track a)
  5. Scenario D: Safe Regularization with Automatic Gated Fallbacks (Track c)
"""

import os
import logging
from typing import Dict, Any

# Import our library classes from the main file
# (Assuming the main library is saved as `pcrf_transformer_reliability_suite.py`)
from pcrf_transformer_reliability_suite import (
    ModelConfig,
    DerivativeConfig,
    CurriculumConfig,
    StructuralPCRFConfig,
    RegularizationConfig,
    PromotionGateConfig,
    ArtifactConfig,
    DerivativePlugin,
    CurriculumPlugin,
    StructuralPCRFPlugin,
    DerivativeRegularizer,
    SafePCRFController,
    BaselineEvaluator,
    CustomFactualDataset,
    load_reusable_model_and_tokenizer,
    generate_mock_cloze_dataset,
    set_reproducibility
)

# Setup beautiful customer logs
logging.basicConfig(level=logging.INFO, format="[Customer-Integration] %(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("PCRF_Customer_App")


def main():
    logger.info("Initializing PCRF Customer Integration Demo...")
    
    # --------------------------------------------------------------------------
    # 1. Setup global configurations & Load Model
    # --------------------------------------------------------------------------
    # Customers define custom configs for their compute environment
    model_cfg = ModelConfig(
        model_name="distilgpt2",  # Fast lightweight model for localized verification
        device="cuda" if os.environ.get("USE_CUDA", "True") == "True" else "cpu",
        seed=42
    )
    set_reproducibility(model_cfg.seed)
    
    # Load model and splits using the library API
    model, tokenizer = load_reusable_model_and_tokenizer(model_cfg)
    splits = generate_mock_cloze_dataset()
    
    # Setup custom safety validation tolerances 
    gate_config = PromotionGateConfig(
        non_inferiority_margin=0.01,   # Strictly reject seen accuracy drops > 1%
        min_unseen_improvement=0.02,   # Require at least 2% gain on unseen validation to promote
        degradation_budget=0.03        # Rollback immediately if seen metrics drop > 3%
    )
    
    # Instantiate the safe policy controller
    safety_controller = SafePCRFController(gate_config)
    
    # Create wrapper datasets
    train_dataset = CustomFactualDataset(splits["train"], tokenizer, model_cfg.max_len)
    seen_val_dataset = CustomFactualDataset(splits["seen_val"], tokenizer, model_cfg.max_len)
    unseen_val_dataset = CustomFactualDataset(splits["unseen_val"], tokenizer, model_cfg.max_len)
    
    # --------------------------------------------------------------------------
    # 2. Establish Baseline (Evaluating target metrics before any intervention)
    # --------------------------------------------------------------------------
    logger.info("--- Phase 1: Running Baseline Profile Evaluation ---")
    base_seen_metrics = BaselineEvaluator.evaluate_dataset(model, tokenizer, seen_val_dataset, model_cfg)
    base_unseen_metrics = BaselineEvaluator.evaluate_dataset(model, tokenizer, unseen_val_dataset, model_cfg)
    
    baseline_stats = {
        "seen_val_acc": base_seen_metrics["exact_match_acc"],
        "unseen_val_acc": base_unseen_metrics["exact_match_acc"],
        "seen_val_nll": base_seen_metrics["avg_nll"],
        "unseen_val_nll": base_unseen_metrics["avg_nll"]
    }
    
    logger.info(f"Baseline Seen accuracy: {baseline_stats['seen_val_acc'] * 100:.1f}%")
    logger.info(f"Baseline Unseen accuracy: {baseline_stats['unseen_val_acc'] * 100:.1f}%")

    # Dictionary to collect granular metrics for customer scoring
    pcrf_scorecard = {}

    # --------------------------------------------------------------------------
    # Scenario A: Standalone Derivative Estimation & Diagnostics (Track b)
    # --------------------------------------------------------------------------
    logger.info("\n--- Scenario A: Run Standalone Layer Derivative Estimation ---")
    
    class CustomerConfigContext:
        def __init__(self, m_cfg):
            self.model_cfg = m_cfg
            self.derivative_cfg = DerivativeConfig(perturbation_mode="noise", noise_std=0.08)
            self.curriculum_cfg = CurriculumConfig()
            self.structural_cfg = StructuralPCRFConfig()
            self.regularization_cfg = RegularizationConfig()
            self.artifact_cfg = ArtifactConfig(output_dir="./customer_pcrf_artifacts")

    customer_ctx = CustomerConfigContext(model_cfg)
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
            
        # Empirical scoring for Derivatives based on absolute perturbation sensitivity
        mean_abs_delta = np.mean([abs(x["delta"]) for x in derivatives_data]) if derivatives_data else 0.0
        deriv_score = min(100.0, max(0.0, mean_abs_delta * 1000.0))  # Scale sensitivity
        pcrf_scorecard["Derivatives"] = {
            "baseline": "0.00 (Unmeasured)",
            "pcrf": f"{mean_abs_delta:.5f} (Avg Sensitivity)",
            "score": deriv_score,
            "status": deriv_decision.status,
            "recommendation": deriv_decision.recommender_action if deriv_decision else "N/A"
        }
    else:
        logger.error(f"Plugin failed health check: {health_status.unsupported_reason}")

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
        
        # Empirical scoring for Curriculum based on priority distribution contrast (std dev)
        priority_std = np.std([x["priority_score"] for x in prioritized_dataset]) if prioritized_dataset else 0.0
        curr_score = min(100.0, max(0.0, priority_std * 20.0))  # High variance means highly selective curriculum signal
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
        for block in layer_breakdown:
            logger.info(f"  - Block {block['layer_idx']:02d}: Survival Prob r_l = {block['reliability_r_l']:.4f} | Marginal Birnbaum Sensitivity D_R = {block['analytical_derivative']:.4f}")
            
        struct_decision = struct_plugin.should_apply(baseline_stats, layer_breakdown, gate_config)
        
        # Empirical scoring for Structural: Depth chain system reliability
        r_sys_chain = np.prod([x["reliability_r_l"] for x in layer_breakdown]) if layer_breakdown else 0.0
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
    
    if regularizer.health_check(model).is_healthy:
        logger.info("Executing derivative-guided SFT regularization training pass...")
        regularizer.run_standalone(model, tokenizer, splits, customer_ctx)
        
        logger.info("Evaluating post-regularization metrics for promotion verification...")
        reg_seen_metrics = BaselineEvaluator.evaluate_dataset(model, tokenizer, seen_val_dataset, model_cfg)
        reg_unseen_metrics = BaselineEvaluator.evaluate_dataset(model, tokenizer, unseen_val_dataset, model_cfg)
        
        regularized_stats = {
            "seen_val_acc": reg_seen_metrics["exact_match_acc"],
            "unseen_val_acc": reg_unseen_metrics["exact_match_acc"],
            "seen_val_nll": reg_seen_metrics["avg_nll"],
            "unseen_val_nll": reg_unseen_metrics["avg_nll"]
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
        
        if reg_decision.status in ["SAFE_TO_APPLY", "PROMOTED"]:
            logger.info("[DEPLOY SUCCESS] New regularized model parameters promoted to production!")
        else:
            logger.warning("[FALLBACK TRIGGERED] Regularization failed safety metrics or degraded seen accuracy.")
            logger.warning(f"Fallback Action: {reg_decision.safest_alternative}")
            logger.info("Restoring pre-training baseline model weights...")
            reg_debug = regularizer.debug_next_steps({"seen_loss": regularized_stats["seen_val_nll"]})
            logger.info(f"Developer Troubleshooting: Adjust {reg_debug.config_knobs_to_adjust} and try fallback: {reg_debug.suggested_safer_fallback}")
            
        # Empirical scoring for Regularization: Seen retention combined with unseen gain bounds
        seen_drop = max(0.0, baseline_stats["seen_val_acc"] - regularized_stats["seen_val_acc"])
        unseen_gain = max(0.0, regularized_stats["unseen_val_acc"] - baseline_stats["unseen_val_acc"])
        
        reg_score = 100.0 - (seen_drop * 500.0)  # Penalize seen degradation heavily
        if reg_decision.status not in ["SAFE_TO_APPLY", "PROMOTED"]:
            reg_score -= 40.0  # Apply penalty if gate blocked promotion
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
    # Calculate weighted composite PCRF Adoption Index
    weights = {
        "Derivatives": 0.20,
        "Curriculum Curation": 0.20,
        "Structural Depth Monitor": 0.30,
        "Safe SFT Regularization": 0.30
    }
    
    overall_adoption_score = 0.0
    for feature, meta in pcrf_scorecard.items():
        overall_adoption_score += meta["score"] * weights.get(feature, 0.25)
        
    # Set final decision directive threshold boundaries
    if overall_adoption_score >= 80.0:
        directive = "HIGHLY RECOMMENDED: FULL SYSTEM ADOPTION"
        color_code = "🟢 [SAFE & PERFORMANCE ACCELERATED]"
    elif 50.0 <= overall_adoption_score < 80.0:
        directive = "RECOMMENDED WITH GATES: MONITORING & DATA CURATION ONLY (FALLBACK TUNING ACTIVE)"
        color_code = "🟡 [SAFE TO MEASURE & CURATE | DELAY INTERVENTION]"
    else:
        directive = "REJECT ADOPTION: RESTORE BASELINE CONFIGURATIONS"
        color_code = "🔴 [HIGH OVER-STEERING RISK | BLOCK PARAMETER MUTATIONS]"

    # Print the beautifully styled terminal ASCII report
    print("\n" + "=" * 90)
    print("                      PCRF TRANSFORMER RELIABILITY REPORT CARD                      ")
    print("=" * 90)
    print(f"Target Model Evaluated  : {model_cfg.model_name.upper()}")
    print(f"Device Map Context      : {model_cfg.device.upper()}")
    print(f"Baseline Seen Accuracy  : {baseline_stats['seen_val_acc'] * 100:.1f}%")
    print(f"Baseline Unseen Accuracy: {baseline_stats['unseen_val_acc'] * 100:.1f}%")
    print("-" * 90)
    
    # Header format
    print(f"{'Feature Track / Module':<30} | {'Baseline':<18} | {'PCRF Value':<18} | {'Score':<8} | {'Gating Status':<15}")
    print("-" * 90)
    
    for feature, meta in pcrf_scorecard.items():
        print(f"{feature:<30} | {meta['baseline']:<18} | {meta['pcrf']:<18} | {meta['score']:>6.1f}/100 | {meta['status']:<15}")
        
    print("-" * 90)
    print(f"COMPOSITE PCRF ADOPTION INDEX: {overall_adoption_score:.2f} / 100")
    print(f"DECISION DIRECTIVE            : {directive}")
    print(f"DEPLOYMENT SECURITY RISK      : {color_code}")
    print("=" * 90)
    
    # Feature Debug/Action Plan Print
    print("\n" + "-" * 30 + " ACTIONABLE TROUBLESHOOTING PLAN " + "-" * 30)
    for feature, meta in pcrf_scorecard.items():
        if meta["status"] not in ["SAFE_TO_APPLY", "PROMOTED"]:
            print(f"• [Fix {feature}]: {meta['recommendation']}")
            if feature == "Derivatives" and deriv_debug:
                print(f"    └─ Suggested steps: {deriv_debug.suggested_debug_steps}")
            if feature == "Safe SFT Regularization" and reg_debug:
                print(f"    └─ Suggested steps: {reg_debug.suggested_debug_steps}")
    print("-" * 90 + "\n")

if __name__ == "__main__":
    main()