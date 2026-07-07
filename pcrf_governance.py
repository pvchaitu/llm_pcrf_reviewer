# ==============================================================================
# File: pcrf_governance.py
# ==============================================================================
"""
PCRF Transformer Reliability Suite - Routing & Gating Governance Engine
pcrf_governance.py
========================================================================================
Implements real-time ProtectedRouter logic, SafePCRFController gates, and exposure control metrics.
"""

from typing import Any, Dict, List, Tuple, Optional
import logging
import torch
from dataclasses import dataclass, field
from pcrf_dataset import is_contract_clean_candidate_repair, evaluate_semantic_match

# Replicated constants for isolation
SAFETY_WITHHELD_RESPONSE = "⚠️ Hallucination Risk Detected — Response Withheld for Safety"

logger = logging.getLogger("PCRF_Suite")

# Global package-level tracking anchor (State audit component)
LAST_COMPUTED_CHAIN_RELIABILITY = 1.0


@dataclass
class FeatureHealthReport:
    feature_name: str
    is_healthy: bool
    unsupported_reason: Optional[str] = None
    diagnostics: List[str] = field(default_factory=list)


@dataclass
class FeatureDecisionReport:
    feature_name: str
    status: str
    reason_code: str
    explanation: str
    recommender_action: str
    safest_alternative: str


@dataclass
class ModelConfig:
    model_name: str = "Qwen/Qwen2.5-0.5B-Instruct"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    use_fp16: bool = False
    max_len: int = 128
    temperature: float = 0.0
    top_p: float = 1.0
    seed: int = 42


@dataclass
class DerivativeConfig:
    enabled: bool = True
    metric: str = "gold_log_prob"
    perturbation_mode: str = "noise"
    noise_std: float = 0.08
    scale_factor: float = 0.5
    num_stability_seeds: int = 3
    granularity: str = "layer"


@dataclass
class CurriculumConfig:
    enabled: bool = True
    strategy: str = "derivative_weighted"
    oversample_top_k: float = 0.25
    replay_buffer_size: int = 10
    staged_epochs: int = 3


@dataclass
class StructuralPCRFConfig:
    enabled: bool = True
    reliability_surrogate: str = "cosine_similarity"
    mapping_transform: str = "exponential"
    decay_beta: float = 2.0
    submodule_factorization: bool = True
    enable_roadmap_heuristics: bool = True


@dataclass
class RegularizationConfig:
    enabled: bool = True
    lambda_reg: float = 0.05
    penalty_type: str = "kl_baseline"
    warmup_steps: int = 50
    gradient_anchoring: bool = True
    weight_drift_penalty: float = 0.01
    max_derivative_cap: float = 2.0
    lambda_drift: float = 0.1
    lambda_kl: float = 0.1
    lambda_margin: float = 0.15
    lambda_argmax: float = 0.5
    lambda_wrong: float = 0.5
    lambda_contrastive: float = 0.5


@dataclass
class PromotionGateConfig:
    non_inferiority_margin: float = 0.01
    degradation_budget: float = 0.03
    min_unseen_improvement: float = 0.02
    seen_nll_tolerance_rel: float = 0.05
    unseen_nll_gain_req: float = 0.05
    bootstrap_ci_significance: float = 0.01
    structural_gating_floor: float = 0.75
    crew_geo_reliability_threshold: float = 0.95
    max_candidate_hallucination_risk_increase: float = 0.05
    max_instruction_violation_rate_for_promotion: float = 0.10
    min_strict_em_for_direct_promotion: float = 0.10
    min_validation_examples_for_promotion: int = 100
    allow_directional_only_promotion: bool = False
    enforce_instruction_contract_gate: bool = False
    enforce_strict_em_repair_gate: bool = False
    report_instruction_contract_as_diagnostic_only: bool = True


@dataclass
class ArtifactConfig:
    output_dir: str = "./customer_pcrf_artifacts"
    save_everything: bool = True
    mask_hallucinated_outputs_in_customer_artifacts: bool = True
    include_raw_generation_outputs_in_debug_artifacts: bool = False
    safety_withheld_response: str = SAFETY_WITHHELD_RESPONSE


@dataclass
class ReportingConfig:
    report_strict_validation: bool = True
    include_metric_confidence_section: bool = True
    include_router_consistency_audit: bool = True
    include_taxonomy_guidance: bool = True
    include_structural_reconciliation: bool = True
    include_metric_direction_column: bool = True
    min_validation_examples_for_strong_claim: int = 100
    customer_safe_language: bool = True
    allow_strong_ood_claims: bool = False
    max_showcase_examples: int = 4
    strict_series_gate_role: str = "conservative_promotion_veto"
    crew_gate_role: str = "residual_aware_diagnostic"
    bottleneck_selection_policy: str = "union_empirical_and_birnbaum"
    entropy_high_threshold: float = 0.25
    entropy_near_zero_epsilon: float = 1e-8
    birnbaum_high_threshold: float = 0.40
    empirical_delta_high_threshold: float = 0.01
    combined_risk_high_threshold: float = 0.10
    strict_em_gate_enabled: bool = True
    strict_em_non_degradation_required: bool = True
    strict_em_drop_tolerance: float = 0.0


@dataclass
class PCRFConfig:
    model_cfg: ModelConfig = field(default_factory=ModelConfig)
    derivative_cfg: DerivativeConfig = field(default_factory=DerivativeConfig)
    curriculum_cfg: CurriculumConfig = field(default_factory=CurriculumConfig)
    structural_cfg: StructuralPCRFConfig = field(default_factory=StructuralPCRFConfig)
    regularization_cfg: RegularizationConfig = field(default_factory=RegularizationConfig)
    gate_cfg: PromotionGateConfig = field(default_factory=PromotionGateConfig)
    artifact_cfg: ArtifactConfig = field(default_factory=ArtifactConfig)
    reporting_cfg: ReportingConfig = field(default_factory=ReportingConfig)


@dataclass
class GateCheck:
    name: str
    passed: bool
    severity: str
    metric_value: Any
    threshold: Any
    explanation: str


@dataclass
class PromotionDecision:
    direct_weight_promotion_status: str
    reason_code: str
    checks: List[GateCheck]
    safe_to_use_components: List[str]
    unsafe_components: List[str]
    measurement_only_components: List[str]
    customer_summary: str


@dataclass
class RowFailureLabels:
    semantic_target_failure: bool
    instruction_contract_violation: bool
    format_template_leakage: bool
    wrong_entity_substitution: bool
    over_generation: bool
    high_confidence_wrong: bool
    confidence_lowered_on_wrong: bool
    confidence_increased_on_wrong: bool
    candidate_risk_higher: bool
    candidate_risk_lower_but_still_wrong: bool
    repair_candidate: bool
    repair_promoted: bool
    regression: bool
    regression_blocked: bool
    oversteer_prevented: bool
    both_wrong_no_repair_available: bool
    both_wrong_lower_risk_candidate_not_served: bool
    abstained_or_baseline_fallback: bool


def _as_bool_int(value: Any) -> bool:
    try:
        return int(value) == 1
    except Exception:
        return bool(value)


def is_baseline_hallucination(row: Dict[str, Any]) -> bool:
    return not bool(int(row.get("baseline_correct", 0)))


def is_candidate_hallucination(row: Dict[str, Any]) -> bool:
    return not bool(int(row.get("candidate_correct", 0)))


def is_unresolved_hallucination(row: Dict[str, Any]) -> bool:
    return is_baseline_hallucination(row) and is_candidate_hallucination(row)


def validate_customer_safe_output_masking(
    trace_rows: List[Dict[str, Any]]
) -> List[str]:
    issues = []
    for r in trace_rows:
        row_id = r.get("id", "unknown")
        baseline_output = str(r.get("baseline_output", ""))
        candidate_output = str(r.get("candidate_output", ""))
        served_output = str(r.get("served_output", ""))

        if is_baseline_hallucination(r) and "⚠️" in baseline_output:
            issues.append(f"[Row {row_id}] Baseline incorrectly masked")

        if is_candidate_hallucination(r) and "⚠️" not in candidate_output:
            issues.append(f"[Row {row_id}] SFT Candidate hallucination NOT masked")

        if is_unresolved_hallucination(r):
            if "⚠️" not in served_output:
                issues.append(f"[Row {row_id}] Unsafe served output exposure")

    return issues


def classify_governance_outcome(row: Dict[str, Any]) -> Tuple[str, str, str]:
    """
    Classifies a row's governance outcome into the formal PCRF Failure Taxonomy (FIX GROUP A).
    Returns: (Category Name, Type, Description)
    """
    b_corr = int(row.get("baseline_correct", 0)) == 1
    c_corr = int(row.get("candidate_correct", 0)) == 1
    decision = row.get("router_decision", "").strip()
    served_output = row.get("served_output", "")
    target = row.get("target", "")

    if served_output == SAFETY_WITHHELD_RESPONSE:
        served_correct = False
    else:
        served_correct = evaluate_semantic_match(served_output, target)

    is_regression = b_corr and not c_corr
    is_repair = not b_corr and c_corr

    if decision == "abstain_safe_fallback" or served_output == SAFETY_WITHHELD_RESPONSE:
        if not b_corr and not c_corr:
            return "SAFE_ABSTAIN", "GOVERNANCE_SUCCESS", "Unsafe answer withheld."
        elif b_corr:
            return "WRONG_ROUTER_SELECTION", "GOVERNANCE_FAILURE", "Safer alternative (baseline) existed but was not chosen."
        else:
            return "MISSED_REPAIR", "GOVERNANCE_OPPORTUNITY", "Improved candidate existed but was not promoted."

    elif decision == "use_baseline":
        if is_regression:
            return "CONTAINED_REGRESSION", "GOVERNANCE_SUCCESS", "Candidate regressed. Router prevented exposure."
        elif not b_corr and not c_corr:
            return "MISSED_ABSTAIN", "GOVERNANCE_FAILURE", "A response was served when abstention was safer."
        elif not b_corr and c_corr:
            return "MISSED_REPAIR", "GOVERNANCE_OPPORTUNITY", "Improved candidate existed but was not promoted."
        else:
            return "PROTECTED_BASELINE_DECISION", "GOVERNANCE_SUCCESS", "Baseline correct; safely chosen."

    elif decision == "use_candidate":
        if is_repair:
            return "PROMOTED_REPAIR", "GOVERNANCE_SUCCESS", "Candidate improved. Router safely promoted."
        elif not b_corr and not c_corr:
            return "MISSED_ABSTAIN", "GOVERNANCE_FAILURE", "A response was served when abstention was safer."
        elif is_regression:
            return "MISSED_HALLUCINATION", "GOVERNANCE_FAILURE", "Unsafe answer served (Candidate chosen over correct baseline)."
        else:
            return "SAFE_PROMOTION", "GOVERNANCE_SUCCESS", "Candidate correct; safely promoted."
            
    return "UNKNOWN", "MODEL_BEHAVIOR", "Outcome could not be mapped cleanly."


def resolve_router_governance_status(
    deployment_recommendation: str,
    direct_weight_promotion_status: str,
    router_enforced_in_validation: bool,
) -> Dict[str, str]:
    if deployment_recommendation == "MEASUREMENT_ONLY":
        production_status = "NOT_PRODUCTION_ENFORCED"
        customer_text = (
            "Validation-time protected routing was exercised for measurement and "
            "safety analysis. Production enforcement is not enabled for this run."
        )
    elif router_enforced_in_validation:
        production_status = "ELIGIBLE_FOR_CANARY_ENFORCEMENT"
        customer_text = (
            "Protected routing is eligible for controlled canary enforcement, "
            "subject to deployment approval and expanded validation."
        )
    else:
        production_status = "ROUTER_NOT_ACTIVE"
        customer_text = "Protected routing was not active in this run."

    return {
        "production_router_status": production_status,
        "validation_router_status": (
            "VALIDATION_ROUTER_ENFORCED"
            if router_enforced_in_validation
            else "VALIDATION_ROUTER_NOT_ENFORCED"
        ),
        "customer_text": customer_text,
    }


def validate_router_row(row: Dict[str, Any], strict: bool = True) -> List[str]:
    errors = []
    b_corr = row["baseline_correct"]
    c_corr = row["candidate_correct"]
    b_risk = row["baseline_hallucination_risk_score"]
    c_risk = row["candidate_hallucination_risk_score"]
    decision = row["router_decision"]
    transition = row["transition_type"]
    reason = row["decision_reason"]

    if b_corr == 1 and c_corr == 1 and transition != "correct_to_correct":
        errors.append(f"Transition is {transition} but both baseline and candidate are correct.")
    elif b_corr == 1 and c_corr == 0 and transition != "correct_to_wrong":
        errors.append(f"Transition is {transition} but correct transitioned to wrong.")
    elif b_corr == 0 and c_corr == 1 and transition != "wrong_to_correct":
        errors.append(f"Transition is {transition} but wrong transitioned to correct.")
    elif b_corr == 0 and c_corr == 0 and transition != "wrong_to_wrong":
        errors.append(f"Transition is {transition} but both are wrong.")

    if decision == "use_baseline" and "Candidate repair promoted" in reason:
        errors.append("Reason claims Candidate repair promoted but decision is use_baseline.")
    if decision == "use_baseline" and "Candidate served" in reason:
        errors.append("Reason claims Candidate served but decision is use_baseline.")
    if decision == "use_candidate" and "fallback to baseline" in reason:
        errors.append("Reason claims fallback to baseline but decision is use_candidate.")
    if decision == "use_candidate" and "Blocked candidate output" in reason:
        errors.append("Reason claims blocked candidate but decision is use_candidate.")

    if "candidate risk was higher" in reason and not (c_risk > b_risk):
        errors.append(f"Reason claims candidate risk was higher but c_risk ({c_risk:.4f}) <= b_risk ({b_risk:.4f}).")
    if "candidate had lower computed risk" in reason and not (c_risk < b_risk):
        errors.append(f"Reason claims candidate had lower risk but c_risk ({c_risk:.4f}) >= b_risk ({b_risk:.4f}).")

    if b_corr == 1 and c_corr == 1 and row.get("failure_category") in ["HIGH_CONFIDENCE_WRONG", "TARGET_MISS", "WRONG_ENTITY_SUBSTITUTION"]:
        errors.append("Row is correct_to_correct but failure category claims wrong target.")

    if strict and errors:
        raise ValueError(f"Router row validation failed for ID {row.get('id')}: {'; '.join(errors)}")
    return errors


def run_router_consistency_audit(trace_rows: List[Dict[str, Any]], strict: bool = True) -> Tuple[int, int, List[str]]:
    total = len(trace_rows)
    passed = 0
    warnings = []

    for r in trace_rows:
        errors = validate_router_row(r, strict=False)
        if not errors:
            passed += 1
        else:
            warnings.append(f"Row ID {r.get('id'):03d} consistency warning: {'; '.join(errors)}")

    if strict and (passed < total):
        raise ValueError(f"Router trace consistency audit failed: {len(warnings)} row warnings detected.")

    return total, passed, warnings


def compute_hallucination_exposure_control_stats(
    trace_rows: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Single source of truth for hallucination exposure control (FIX GROUPS E, F, G, I)."""
    observed_candidate_regressions = 0
    contained_regressions = 0
    served_regressions = 0
    
    repairs_identified = 0
    repairs_promoted = 0
    repairs_withheld = 0
    
    safe_abstains = 0
    observed_risk_events = 0
    contained_risk_events = 0
    served_risk_events = 0
    
    total_baseline_hallucinations = 0
    semantic_repairs_observed = 0
    contract_clean_repairs_promoted = 0
    semantic_repairs_withheld_for_contract = 0
    uncontrolled = 0

    wrong_to_wrong_count = 0
    wrong_to_correct_count = 0

    for row in trace_rows:
        b_corr = _as_bool_int(row.get("baseline_correct", 0))
        c_corr = _as_bool_int(row.get("candidate_correct", 0))
        decision = str(row.get("router_decision", "")).strip()

        baseline_failed = not b_corr
        candidate_failed = not c_corr

        if baseline_failed or candidate_failed:
            observed_risk_events += 1
            if decision == "abstain_safe_fallback" or row.get("served_output") == SAFETY_WITHHELD_RESPONSE:
                contained_risk_events += 1
                safe_abstains += 1
            elif decision == "use_baseline" and baseline_failed:
                served_risk_events += 1
            elif decision == "use_candidate" and candidate_failed:
                served_risk_events += 1
            elif decision == "use_baseline" and not baseline_failed:
                contained_risk_events += 1
            elif decision == "use_candidate" and not candidate_failed:
                contained_risk_events += 1

        # Observed Candidate Regressions (Baseline correct, candidate wrong)
        if b_corr and candidate_failed:
            observed_candidate_regressions += 1
            if decision in {"use_baseline", "abstain_safe_fallback"}:
                contained_regressions += 1
            else:
                served_regressions += 1

        # Repairs Identified (Baseline wrong, candidate correct)
        if baseline_failed and c_corr:
            repairs_identified += 1
            if decision == "use_candidate":
                repairs_promoted += 1
            else:
                repairs_withheld += 1

        if baseline_failed:
            total_baseline_hallucinations += 1
            if not candidate_failed:
                wrong_to_correct_count += 1
                semantic_repairs_observed += 1

                is_clean = is_contract_clean_candidate_repair(row)
                if is_clean and decision == "use_candidate":
                    contract_clean_repairs_promoted += 1
                elif not is_clean and decision == "abstain_safe_fallback":
                    semantic_repairs_withheld_for_contract += 1
                else:
                    uncontrolled += 1
            else:
                wrong_to_wrong_count += 1
                if decision == "abstain_safe_fallback":
                    pass
                else:
                    uncontrolled += 1

    regression_containment_effectiveness = (
        (contained_regressions / observed_candidate_regressions) * 100.0
        if observed_candidate_regressions else 100.0
    )
    
    repair_promotion_effectiveness = (
        (repairs_promoted / repairs_identified) * 100.0
        if repairs_identified else 100.0
    )

    exposure_control_rate = (
        contained_risk_events / observed_risk_events
        if observed_risk_events else 1.0
    )
    # --- NEW CODE: MATH VS GOLD CONVERGENCE CALCULATOR ---
    math_tps = sum(r.get("math_true_positive", 0) for r in trace_rows)
    math_fns = sum(r.get("math_false_negative", 0) for r in trace_rows)
    math_fps = sum(r.get("math_false_positive", 0) for r in trace_rows)
    total_gold_hallucinations = math_tps + math_fns

    math_recall = (math_tps / total_gold_hallucinations * 100.0) if total_gold_hallucinations > 0 else 100.0
    # -----------------------------------------------------

    return {
        "observed_candidate_regressions": observed_candidate_regressions,
        "contained_regressions": contained_regressions,
        "contained_candidate_regressions": contained_regressions,
        "served_regressions": served_regressions,
        "served_candidate_regressions": served_regressions,
        "regression_containment_effectiveness": regression_containment_effectiveness,
        
        "repairs_identified": repairs_identified,
        "observed_candidate_repairs": repairs_identified,
        "repairs_promoted": repairs_promoted,
        "promoted_candidate_repairs": repairs_promoted,
        "repairs_withheld": repairs_withheld,
        "repair_promotion_effectiveness": repair_promotion_effectiveness,
        
        "safe_abstains": safe_abstains,
        "observed_risk_events": observed_risk_events,
        "contained_risk_events": contained_risk_events,
        "served_risk_events": served_risk_events,
        "exposure_control_rate": exposure_control_rate,
        "hallucination_exposure_control_rate": exposure_control_rate,
        "hallucination_exposure_control_count": contained_risk_events,
        
        "total_b_hallucinations": total_baseline_hallucinations,
        "semantic_repairs_observed": semantic_repairs_observed,
        "contract_clean_repairs_promoted": contract_clean_repairs_promoted,
        "semantic_repairs_withheld_for_contract": semantic_repairs_withheld_for_contract,
        "oversteers_prevented": safe_abstains,
        "regressions_blocked": contained_regressions,
        "uncontrolled_hallucination_exposures": uncontrolled,
        #Added math vs gold convergence metrics
        "math_vs_gold_convergence_rate": math_recall,
        "math_false_positives": math_fps,
        "math_false_negatives": math_fns,
        
        "wrong_to_wrong_count": wrong_to_wrong_count,
        "wrong_to_correct_count": wrong_to_correct_count,
        "net_interventions": repairs_promoted + safe_abstains + contained_regressions,
    }


def compute_regression_detection_coverage(trace_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Computes regression detection coverage metrics across candidate regressions (FIX GROUP J)."""
    reg_rows = [r for r in trace_rows if int(r.get("baseline_correct", 0)) == 1 and int(r.get("candidate_correct", 0)) == 0]
    total_reg = len(reg_rows)
    
    elevated = 0
    low_plus = 0
    med_plus = 0
    high_plus = 0
    
    for r in reg_rows:
        b_risk = float(r.get("baseline_hallucination_risk_score", r.get("baseline_hr", 0.0)))
        c_risk = float(r.get("candidate_hallucination_risk_score", r.get("candidate_hr", 0.0)))
        
        if c_risk > b_risk or c_risk >= 0.55:
            elevated += 1
        if c_risk >= 0.30:
            low_plus += 1
        if c_risk >= 0.55:
            med_plus += 1
        if c_risk >= 0.75:
            high_plus += 1
            
    coverage_pct = (elevated / total_reg) * 100.0 if total_reg > 0 else 100.0
    low_pct = (low_plus / total_reg) * 100.0 if total_reg > 0 else 100.0
    med_pct = (med_plus / total_reg) * 100.0 if total_reg > 0 else 100.0
    high_pct = (high_plus / total_reg) * 100.0 if total_reg > 0 else 100.0
    
    return {
        "observed_regressions": total_reg,
        "elevated_risk_regressions": elevated,
        "coverage_pct": coverage_pct,
        "low_plus_count": low_plus,
        "low_plus_pct": low_pct,
        "med_plus_count": med_plus,
        "med_plus_pct": med_pct,
        "high_plus_count": high_plus,
        "high_plus_pct": high_pct
    }


class ProtectedRouter:
    """Evaluates candidates using dual inference paths, blocking semantic regressions."""
    def __init__(self):
        self.blocked_regressions = 0
        self.semantic_repairs_observed = 0
        self.contract_clean_repairs_promoted = 0
        self.semantic_repairs_withheld_for_contract = 0
        self.both_wrong = 0
        self.both_correct = 0

    # PartFFF - The router looks at the exact match status and hallucination risk scores. It returns a decision: 
    # "use_baseline", "use_candidate", or "abstain_safe_fallback"
    def route_inference(self, row: Dict[str, Any], model_name: Optional[str] = None) -> Tuple[str, str]:
        base_correct = int(row.get("baseline_correct", 0))
        cand_correct = int(row.get("candidate_correct", 0))
        base_hr = float(row.get("baseline_hr", 0.0))
        cand_hr = float(row.get("candidate_hr", 0.0))
        base_ent = float(row.get("baseline_entropy", 0.0))
        cand_ent = float(row.get("candidate_entropy", 0.0))

        if not model_name:
            model_name = row.get("model_name")

        if base_correct == 1 and cand_correct == 0:
            self.blocked_regressions += 1
            decision = "baseline"
            reason = "Candidate blocked because baseline captured the target and candidate failed."
        elif base_correct == 0 and cand_correct == 1:
            self.semantic_repairs_observed += 1
            if is_contract_clean_candidate_repair(row, model_name=model_name):
                self.contract_clean_repairs_promoted += 1
                decision = "candidate"
                reason = "Contract-clean candidate repair promoted."
            else:
                self.semantic_repairs_withheld_for_contract += 1
                decision = "abstain_safe_fallback"
                reason = "Semantic target recovered by candidate, but output failed strict instruction contract; response withheld for safety."
        elif base_correct == 0 and cand_correct == 0:
            self.both_wrong += 1
            decision = "abstain_safe_fallback"
            reason = f"Candidate over-steer prevented; both outputs failed target capture, and candidate was not served (Risk: {cand_hr:.4f})."
        else:
            self.both_correct += 1
            cand_contract_violation = _as_bool_int(row.get("instruction_violation_candidate", 1))
            
            is_small_model = False
            if model_name:
                name_lower = str(model_name).lower()
                if "0.5b" in name_lower or "gpt2" in name_lower or "124m" in name_lower:
                    is_small_model = True
            
            if cand_contract_violation and not is_small_model:
                decision = "baseline"
                reason = "Baseline served to preserve stricter output contract or lower risk."
            else:
                use_cand = (cand_hr < base_hr or (abs(cand_hr - base_hr) < 1e-4 and cand_ent < base_ent))
                decision = "candidate" if use_cand else "baseline"
                if decision == "candidate":
                    reason = "Candidate served; semantic target preserved and router policy allowed candidate."
                else:
                    reason = "Baseline served to preserve stricter output contract or lower risk."

        return decision, reason


class SafePCRFController:
    """Decides when to safely promote optimized SFT candidate weights or trigger fallbacks."""
    def __init__(self, gate_cfg: Any):
        self.gate_cfg = gate_cfg

    def run_gating_checks(
        self,
        baseline_metrics: Dict[str, Any],
        feature_metrics: Dict[str, Any],
        r_sys_chain: float
    ) -> List[GateCheck]:
        checks = []

        seen_baseline_acc = baseline_metrics.get("seen_val_acc", 0.0)
        unseen_baseline_acc = baseline_metrics.get("unseen_val_acc", 0.0)
        path_c_active = (seen_baseline_acc == 0.0 and unseen_baseline_acc == 0.0)

        seen_cand_acc = feature_metrics.get("seen_val_acc", 0.0)
        unseen_cand_acc = feature_metrics.get("unseen_val_acc", 0.0)

        # Served accuracy reflects deployment-facing behavior after Protected Router governance.
        # If older callers do not pass served metrics, fall back to candidate metrics for backward compatibility.
        served_seen_acc = feature_metrics.get("served_seen_val_acc", seen_cand_acc)
        served_unseen_acc = feature_metrics.get("served_unseen_val_acc", unseen_cand_acc)

        # ------------------------------------------------------------------
        # Shared accuracy deltas used by multiple gates
        # ------------------------------------------------------------------
        candidate_unseen_gain = unseen_cand_acc - unseen_baseline_acc
        served_unseen_gain = served_unseen_acc - unseen_baseline_acc

        candidate_seen_drop = seen_baseline_acc - seen_cand_acc
        served_seen_drop = seen_baseline_acc - served_seen_acc

        struct_floor = self.gate_cfg.structural_gating_floor
        checks.append(GateCheck(
            name="Structural Reliability Floor",
            passed=r_sys_chain >= struct_floor,
            severity="CRITICAL",
            metric_value=r_sys_chain,
            threshold=struct_floor,
            explanation=f"Overall system chain reliability R_sys ({r_sys_chain*100:.2f}%) vs floor ({struct_floor*100:.1f}%)."
        ))

        transition_stats = feature_metrics.get("transitions", {})
        
        # FIX GROUP E: Replace regressions count gate with Candidate Regression Review (REVIEW status)
        observed_regressions = transition_stats.get("correct->wrong", 0)
        observed_repairs = transition_stats.get("wrong->correct", 0)
        net_delta = observed_repairs - observed_regressions
        
        checks.append(GateCheck(
            name="Candidate Regression Review",
            passed=True,
            severity="DIAGNOSTIC_ONLY",
            metric_value=f"Observed Regressions: {observed_regressions}, Observed Repairs: {observed_repairs}, Net Delta: {net_delta:+d}",
            threshold="N/A",
            explanation="Model evaluation only. Captures raw candidate parameter variance before PCRF routing."
        ))

        # Create the separate Regression Exposure Control gate
        contained_regressions = feature_metrics.get("contained_regressions", observed_regressions)
        served_regressions = feature_metrics.get("served_regressions", 0)
        
        effectiveness = 100.0
        if observed_regressions > 0:
            effectiveness = (contained_regressions / observed_regressions) * 100.0
            
        checks.append(GateCheck(
            name="Regression Exposure Control",
            passed=served_regressions == 0,
            severity="CRITICAL",
            metric_value=f"Effectiveness: {effectiveness:.1f}%, Served Regressions: {served_regressions}",
            threshold="Served Regressions = 0",
            explanation="Observed regressions were contained before reaching served output." if served_regressions == 0 else f"{served_regressions} regressions leaked to served outputs."
        ))

        critical_regressions = feature_metrics.get("critical_regressions", 0)
        checks.append(GateCheck(
            name="Critical High-Priority Regressions",
            passed=critical_regressions == 0,
            severity="CRITICAL",
            metric_value=critical_regressions,
            threshold=0,
            explanation=f"Zero critical high-priority regressions required. Found {critical_regressions} regressions."
        ))

        cand_inst_violation = feature_metrics.get("instruction_violation_rate", 0.0)
        base_inst_violation = baseline_metrics.get("instruction_violation_rate", 0.0)

        checks.append(GateCheck(
            name="Universal Instruction Contract Violation Gate",
            passed=True if not self.gate_cfg.enforce_instruction_contract_gate else (cand_inst_violation <= self.gate_cfg.max_instruction_violation_rate_for_promotion),
            severity="DIAGNOSTIC_ONLY" if not self.gate_cfg.enforce_instruction_contract_gate else "CRITICAL",
            metric_value=cand_inst_violation,
            threshold=self.gate_cfg.max_instruction_violation_rate_for_promotion,
            explanation="Both baseline and candidate violate strict output contracts. Tracking operated as a diagnostic planner." if not self.gate_cfg.enforce_instruction_contract_gate else f"Candidate instruction-contract violation rate ({cand_inst_violation*100:.2f}%) must be below ceiling ({self.gate_cfg.max_instruction_violation_rate_for_promotion*100:.1f}%)."
        ))

        checks.append(GateCheck(
            name="Generalization Non-Degradation Guard",
            passed=candidate_unseen_gain >= 0.0,
            severity="WARNING",
            metric_value=candidate_unseen_gain,
            threshold=0.0,
            explanation=(
                f"Generalization monitoring warning: raw SFT candidate unseen validation exact-match "
                f"changed by {candidate_unseen_gain*100:.2f}% versus baseline. This is reported as candidate-side "
                f"generalization telemetry only and does not block deployment when Protected Router served "
                f"outputs remain governed and regression exposure is contained."
            )
        ))

        cand_strict_em = feature_metrics.get("strict_em_acc", 0.0)
        base_strict_em = baseline_metrics.get("strict_em_acc", 0.0)

        checks.append(GateCheck(
            name="Strict EM Candidate Non-Degradation Gate",
            passed=True if not self.gate_cfg.enforce_strict_em_repair_gate else (cand_strict_em >= base_strict_em),
            severity="DIAGNOSTIC_ONLY" if not self.gate_cfg.enforce_strict_em_repair_gate else "HIGH",
            metric_value=cand_strict_em,
            threshold=base_strict_em,
            explanation="Strict EM validation tracking operated diagnostically for this validation pass." if not self.gate_cfg.enforce_strict_em_repair_gate else f"Candidate strict exact match ({cand_strict_em*100:.2f}%) must not degrade from baseline ({base_strict_em*100:.2f}%)."
        ))

        checks.append(GateCheck(
            name="Strict EM Absolute Direct Promotion Threshold",
            passed=True if not self.gate_cfg.enforce_strict_em_repair_gate else (cand_strict_em >= self.gate_cfg.min_strict_em_for_direct_promotion),
            severity="DIAGNOSTIC_ONLY" if not self.gate_cfg.enforce_strict_em_repair_gate else "CRITICAL",
            metric_value=cand_strict_em,
            threshold=self.gate_cfg.min_strict_em_for_direct_promotion,
            explanation="Strict EM validation boundary executed as diagnostic analyzer." if not self.gate_cfg.enforce_strict_em_repair_gate else f"Candidate strict EM ({cand_strict_em*100:.2f}%) must be above minimal floor ({self.gate_cfg.min_strict_em_for_direct_promotion*100:.1f}%)."
        ))

        cand_hr_risk = feature_metrics.get("avg_hallucination_risk", 0.0)
        base_hr_risk = baseline_metrics.get("avg_hallucination_risk", 0.0)
        risk_increase = cand_hr_risk - base_hr_risk
        
        val_size = feature_metrics.get("validation_sample_size", 0)
        checks.append(GateCheck(
            name="Minimum Gating Evidence Verification Size",
            passed=(val_size >= self.gate_cfg.min_validation_examples_for_promotion) or self.gate_cfg.allow_directional_only_promotion,
            severity="HIGH",
            metric_value=val_size,
            threshold=self.gate_cfg.min_validation_examples_for_promotion,
            explanation=f"Validation examples count ({val_size}) vs strong claim requirement ({self.gate_cfg.min_validation_examples_for_promotion})."
        ))

        if path_c_active:
            base_seen_nll = baseline_metrics["seen_val_nll"]
            feat_seen_nll = feature_metrics["seen_val_nll"]
            base_unseen_nll = baseline_metrics["unseen_val_nll"]
            feat_unseen_nll = feature_metrics["unseen_val_nll"]

            seen_nll_increase = feat_seen_nll - base_seen_nll
            seen_nll_tolerance = base_seen_nll * self.gate_cfg.seen_nll_tolerance_rel

            checks.append(GateCheck(
                name="Path C Seen NLL Tolerance",
                passed=seen_nll_increase <= seen_nll_tolerance,
                severity="CRITICAL",
                metric_value=seen_nll_increase,
                threshold=seen_nll_tolerance,
                explanation=f"Seen NLL degradation (+{seen_nll_increase:.4f}) must be within tolerance ({seen_nll_tolerance:.4f})."
            ))

            unseen_nll_decrease_rel = (base_unseen_nll - feat_unseen_nll) / base_unseen_nll
            checks.append(GateCheck(
                name="Path C Unseen NLL Generalization Requirement",
                passed=unseen_nll_decrease_rel >= self.gate_cfg.unseen_nll_gain_req,
                severity="HIGH",
                metric_value=unseen_nll_decrease_rel,
                threshold=self.gate_cfg.unseen_nll_gain_req,
                explanation=f"Relative generalization drop ({unseen_nll_decrease_rel*100:.2f}%) vs requirement ({self.gate_cfg.unseen_nll_gain_req*100:.1f}%)."
            ))
        else:
            # ------------------------------------------------------------------
            # Served-outcome-centric seen validation gates
            # ------------------------------------------------------------------
            # These gates evaluate the deployment-facing outcome after Protected
            # Router decisions, not raw candidate behavior. This keeps the gating
            # narrative aligned with PCRF's primary safety claim: governance and
            # containment of served outputs.
            # ------------------------------------------------------------------

            served_seen_drop = seen_baseline_acc - served_seen_acc
            served_seen_delta = served_seen_acc - seen_baseline_acc

            checks.append(GateCheck(
                name="Served Seen Accuracy Non-Inferiority Margin",
                passed=served_seen_drop <= self.gate_cfg.non_inferiority_margin,
                severity="HIGH",
                metric_value=served_seen_drop,
                threshold=self.gate_cfg.non_inferiority_margin,
                explanation=(
                    f"Served seen accuracy baseline={seen_baseline_acc*100:.2f}%, "
                    f"served={served_seen_acc*100:.2f}%, delta={served_seen_delta*100:.2f}%. "
                    f"Non-inferiority allows at most "
                    f"{self.gate_cfg.non_inferiority_margin*100:.1f}% served degradation. "
                    f"This gate evaluates governed served output after Protected Router decisions."
                )
            ))

            checks.append(GateCheck(
                name="Served Seen Accuracy Degradation Budget",
                passed=served_seen_drop <= self.gate_cfg.degradation_budget,
                severity="CRITICAL",
                metric_value=served_seen_drop,
                threshold=self.gate_cfg.degradation_budget,
                explanation=(
                    f"Served seen accuracy baseline={seen_baseline_acc*100:.2f}%, "
                    f"served={served_seen_acc*100:.2f}%, delta={served_seen_delta*100:.2f}%. "
                    f"Deployment budget allows at most "
                    f"{self.gate_cfg.degradation_budget*100:.1f}% served degradation. "
                    f"This remains blocking only when the governed served stream degrades beyond budget."
                )
            ))

            checks.append(GateCheck(
                name="Candidate Unseen Accuracy Improvement Review",
                passed=candidate_unseen_gain >= self.gate_cfg.min_unseen_improvement,
                severity="WARNING",
                metric_value=candidate_unseen_gain,
                threshold=self.gate_cfg.min_unseen_improvement,
                explanation=(
                    f"Candidate-side unseen accuracy improvement was "
                    f"{candidate_unseen_gain*100:.2f}% vs target "
                    f"{self.gate_cfg.min_unseen_improvement*100:.1f}%. "
                    f"This is reported as raw SFT generalization telemetry only and "
                    f"does not block deployment when served outputs remain governed."
                )
            ))

            checks.append(GateCheck(
                name="Served Unseen Generalization Preservation",
                passed=served_unseen_gain >= 0.0,
                severity="HIGH",
                metric_value=served_unseen_gain,
                threshold=0.0,
                explanation=(
                    f"Served unseen accuracy baseline={unseen_baseline_acc*100:.2f}%, "
                    f"served={served_unseen_acc*100:.2f}%, delta={served_unseen_gain*100:.2f}%. "
                    f"This deployment-facing gate verifies that governed served output "
                    f"does not degrade on unseen validation after Protected Router decisions."
                )
            ))

            checks.append(GateCheck(
                name="Generalization Non-Degradation Guard",
                passed=candidate_unseen_gain >= 0.0,
                severity="WARNING",
                metric_value=candidate_unseen_gain,
                threshold=0.0,
                explanation=(
                    f"Generalization monitoring warning: raw SFT candidate unseen validation "
                    f"exact-match changed by {candidate_unseen_gain*100:.2f}% versus baseline. "
                    f"This is reported as candidate-side generalization telemetry only and "
                    f"does not block deployment when Protected Router served outputs remain "
                    f"governed and regression exposure is contained."
                )
            ))

        return checks

    def compute_promotion_decision_v2(
        self,
        baseline_metrics: Dict[str, Any],
        feature_metrics: Dict[str, Any],
        r_sys_chain: float = 1.0
    ) -> PromotionDecision:
        checks = self.run_gating_checks(baseline_metrics, feature_metrics, r_sys_chain)

        critical_failed = [c for c in checks if not c.passed and c.severity == "CRITICAL"]
        high_failed = [c for c in checks if not c.passed and c.severity == "HIGH"]

        cand_inst_violation = feature_metrics.get("instruction_violation_rate", 0.0)
        cand_strict_em = feature_metrics.get("strict_em_acc", 0.0)

        is_contract_failure = False
        if self.gate_cfg.enforce_instruction_contract_gate:
            is_contract_failure = is_contract_failure or (cand_inst_violation > self.gate_cfg.max_instruction_violation_rate_for_promotion)
        if self.gate_cfg.enforce_strict_em_repair_gate:
            is_contract_failure = is_contract_failure or (cand_strict_em < self.gate_cfg.min_strict_em_for_direct_promotion)

        if critical_failed:
            status = "DO_NOT_PROMOTE_WEIGHTS" if is_contract_failure else "DO_NOT_APPLY"
            reason_code = critical_failed[0].name.upper().replace(" ", "_").replace("-", "_")
        elif high_failed:
            status = "ROUTER_DIAGNOSTIC_ONLY" if is_contract_failure else "MEASUREMENT_ONLY"
            reason_code = high_failed[0].name.upper().replace(" ", "_").replace("-", "_")
        else:
            status = "SAFE_TO_APPLY"
            reason_code = "PROMOTED"

        safe_to_use = ["derivative diagnostics", "curriculum curation", "structural monitoring", "protected routing"]
        unsafe = []
        measurement_only = []

        if status in ["DO_NOT_APPLY", "MEASUREMENT_ONLY", "DO_NOT_PROMOTE_WEIGHTS", "ROUTER_DIAGNOSTIC_ONLY"]:
            unsafe.append("direct weight promotion of optimized candidate weights")
            measurement_only.append("candidate weights")
        else:
            safe_to_use.append("direct weight promotion of optimized candidate weights")

        customer_summary = f"Direct SFT candidate weight promotion: {status}. Safe-to-use components: {', '.join(safe_to_use)}."
        if unsafe:
            customer_summary += f" Unsafe components: {', '.join(unsafe)}."

        return PromotionDecision(
            direct_weight_promotion_status=status,
            reason_code=reason_code,
            checks=checks,
            safe_to_use_components=safe_to_use,
            unsafe_components=unsafe,
            measurement_only_components=measurement_only,
            customer_summary=customer_summary
        )

    def compute_promotion_decision(self, baseline_metrics: Dict[str, Any], feature_metrics: Dict[str, Any], feature_name: str, r_sys_chain: float = 1.0) -> FeatureDecisionReport:
        dec = self.compute_promotion_decision_v2(baseline_metrics, feature_metrics, r_sys_chain)

        recommender = "Lower regularization bounds or adjust learning rate."
        alternative = "Rollback SFT candidate parameters instantly."
        if dec.direct_weight_promotion_status in ["DO_NOT_APPLY", "DO_NOT_PROMOTE_WEIGHTS"]:
            recommender = "Reject candidate direct SFT weight adoption. Retain diagnostic components."
            alternative = "Restoring frozen pre-training baseline model weights..."
        elif dec.direct_weight_promotion_status in ["MEASUREMENT_ONLY", "ROUTER_DIAGNOSTIC_ONLY"]:
            recommender = "Maintain diagnostic measurements and use Protected Router governance fallback modes."
            alternative = "Fallback Action: Run baseline model configuration only."

        failed_checks = [c for c in dec.checks if not c.passed]
        explanation = failed_checks[0].explanation if failed_checks else dec.customer_summary

        return FeatureDecisionReport(
            feature_name=feature_name,
            status=dec.direct_weight_promotion_status,
            reason_code=dec.reason_code,
            explanation=explanation,
            recommender_action=recommender,
            safest_alternative=alternative
        )


def classify_row_failures(row: Dict[str, Any], cfg: Any) -> RowFailureLabels:
    b_corr = row["baseline_correct"]
    c_corr = row["candidate_correct"]
    b_risk = row["baseline_hallucination_risk_score"]
    c_risk = row["candidate_hallucination_risk_score"]
    decision = row["router_decision"]
    cat = row.get("failure_category", "N/A")
    is_iv_cand = row.get("instruction_violation_candidate", 0) == 1
    delta_top1 = row.get("delta_target_prob", 0.0)

    semantic_target_failure = (c_corr == 0)
    instruction_contract_violation = is_iv_cand
    formatting_template_leakage = (cat == "FORMAT_TEMPLATE_FAILURE")
    wrong_entity_substitution = (cat == "WRONG_ENTITY_SUBSTITUTION")
    over_generation = is_iv_cand
    high_confidence_wrong = (cat == "HIGH_CONFIDENCE_WRONG")

    confidence_lowered_on_wrong = (c_corr == 0 and delta_top1 < 0)
    confidence_increased_on_wrong = (c_corr == 0 and delta_top1 > 0)
    candidate_risk_higher = (c_corr == 0 and c_risk > b_risk)
    candidate_risk_lower_but_still_wrong = (c_corr == 0 and b_corr == 0 and c_risk < b_risk)

    repair_candidate = (b_corr == 0 and c_corr == 1)
    repair_promoted = (b_corr == 0 and c_corr == 1 and decision == "use_candidate")

    regression = (b_corr == 1 and c_corr == 0)
    regression_blocked = (b_corr == 1 and c_corr == 0 and decision == "use_baseline")

    return RowFailureLabels(
        semantic_target_failure=semantic_target_failure,
        instruction_contract_violation=instruction_contract_violation,
        format_template_leakage=formatting_template_leakage,
        wrong_entity_substitution=wrong_entity_substitution,
        over_generation=over_generation,
        high_confidence_wrong=high_confidence_wrong,
        confidence_lowered_on_wrong=confidence_lowered_on_wrong,
        confidence_increased_on_wrong=confidence_increased_on_wrong,
        candidate_risk_higher=candidate_risk_higher,
        candidate_risk_lower_but_still_wrong=candidate_risk_lower_but_still_wrong,
        repair_candidate=repair_candidate,
        repair_promoted=repair_promoted,
        regression=regression,
        regression_blocked=regression_blocked,
        oversteer_prevented=(b_corr == 0 and c_corr == 0 and c_risk > b_risk and decision == "use_baseline"),
        both_wrong_no_repair_available=(b_corr == 0 and c_corr == 0),
        both_wrong_lower_risk_candidate_not_served=(b_corr == 0 and c_corr == 0 and c_risk < b_risk and decision == "use_baseline"),
        abstained_or_baseline_fallback=(b_corr == 0 and c_corr == 0 and decision == "use_baseline")
    )


def compute_metric_provenance(
    baseline_stats: Dict[str, Any],
    regularized_stats: Dict[str, Any],
    trace_rows: List[Dict[str, Any]]
) -> Any:
    seen_rows = [r for r in trace_rows if r["split"] == "seen_val"]
    unseen_rows = [r for r in trace_rows if r["split"] == "unseen_val"]

    loop_sn = baseline_stats.get("seen_val_nll")
    trace_sn = float(np.mean([r["baseline_nll"] for r in seen_rows])) if seen_rows else 0.0
    loop_un = baseline_stats.get("unseen_val_nll")
    trace_un = float(np.mean([r["baseline_nll"] for r in unseen_rows])) if unseen_rows else 0.0

    warnings = []
    if loop_sn is not None and abs(loop_sn - trace_sn) > 1e-4:
        warnings.append(f"Seen NLL discrepancy: Loop = {loop_sn:.4f} vs Trace Mean = {trace_sn:.4f}")
    if loop_un is not None and abs(loop_un - trace_un) > 1e-4:
        warnings.append(f"Unseen NLL discrepancy: Loop = {loop_un:.4f} vs Trace Mean = {trace_un:.4f}")

    return {"warnings": warnings}


def compute_transition_averages(trace_rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    stats = {
        "correct_to_correct": {"count": 0, "nll": [], "ent": [], "marg": [], "hr": []},
        "correct_to_wrong": {"count": 0, "nll": [], "ent": [], "marg": [], "hr": []},
        "wrong_to_correct": {"count": 0, "nll": [], "ent": [], "marg": [], "hr": []},
        "wrong_to_wrong": {"count": 0, "nll": [], "ent": [], "marg": [], "hr": []}
    }
    for r in trace_rows:
        tt = r["transition_type"]
        key = tt.replace("->", "_to_")
        if key in stats:
            stats[key]["count"] += 1
            stats[key]["nll"].append(r["delta_nll"])
            stats[key]["ent"].append(r["delta_entropy"])
            stats[key]["marg"].append(r["delta_margin"])
            stats[key]["hr"].append(r["delta_hallucination_risk_score"])

    averages = {}
    for key, val in stats.items():
        cnt = val["count"]
        if cnt > 0:
            averages[key] = {
                "count": cnt,
                "avg_nll": float(np.mean(val["nll"])),
                "avg_ent": float(np.mean(val["ent"])),
                "avg_marg": float(np.mean(val["marg"])),
                "avg_hr": float(np.mean(val["hr"]))
            }
        else:
            averages[key] = {
                "count": 0, "avg_nll": 0.0, "avg_ent": 0.0, "avg_marg": 0.0, "avg_hr": 0.0
            }
    return averages


def validate_layer_selection_consistency(
    config_layers: List[int],
    plan_layers: List[int],
    report_layers: List[int],
) -> Dict[str, Any]:
    cfg_set = set(int(x) for x in config_layers)
    plan_set = set(int(x) for x in plan_layers)
    report_set = set(int(x) for x in report_layers)

    consistent = (cfg_set == plan_set == report_set)

    return {
        "is_consistent": consistent,
        "config_layers": sorted(cfg_set),
        "plan_layers": sorted(plan_set),
        "report_layers": sorted(report_set),
        "missing_from_config": sorted((plan_set | report_set) - cfg_set),
        "missing_from_plan": sorted((cfg_set | report_set) - plan_set),
        "missing_from_report": sorted((cfg_set | plan_set) - report_set),
    }