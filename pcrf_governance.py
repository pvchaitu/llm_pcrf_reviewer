"""
PCRF Transformer Reliability Suite - Routing & Gating Governance Engine
pcrf_governance.py
========================================================================================
Implements real-time ProtectedRouter logic, SafePCRFController gates, and exposure control metrics.
"""

from typing import Any, Dict, List, Tuple
import logging
from pcrf_dataset import is_contract_clean_candidate_repair
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional

logger = logging.getLogger("PCRF_Suite")

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


def resolve_router_governance_status(
    deployment_recommendation: str,
    direct_weight_promotion_status: str,
    router_enforced_in_validation: bool,
) -> Dict[str, str]:
    """Separates validation-time router behavior from production deployment status."""
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
    """Validate consistency across transition types, correctness flags, risk comparisons, and explanations."""
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
    """Runs high-integrity diagnostic sweeps over entire row-level inference traces."""
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
    """Single source of truth for hallucination exposure control."""
    total_baseline_hallucinations = 0
    semantic_repairs_observed = 0
    contract_clean_repairs_promoted = 0
    semantic_repairs_withheld_for_contract = 0
    safe_abstains = 0
    regressions_blocked = 0
    oversteers_prevented = 0
    uncontrolled = 0

    wrong_to_wrong_count = 0
    wrong_to_correct_count = 0

    for row in trace_rows:
        b_corr = _as_bool_int(row.get("baseline_correct", 0))
        c_corr = _as_bool_int(row.get("candidate_correct", 0))
        decision = str(row.get("router_decision", "")).strip()

        baseline_failed = not b_corr
        candidate_failed = not c_corr

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
                    safe_abstains += 1
                else:
                    uncontrolled += 1
            else:
                wrong_to_wrong_count += 1
                if decision == "abstain_safe_fallback":
                    safe_abstains += 1
                    oversteers_prevented += 1
                else:
                    uncontrolled += 1

        if b_corr and candidate_failed:
            if decision in {"use_baseline", "abstain_safe_fallback"}:
                regressions_blocked += 1
            else:
                uncontrolled += 1

    exposure_control_count = contract_clean_repairs_promoted + safe_abstains
    exposure_control_rate = (
        exposure_control_count / total_baseline_hallucinations
        if total_baseline_hallucinations else 1.0
    )

    return {
        "total_b_hallucinations": total_baseline_hallucinations,
        "semantic_repairs_observed": semantic_repairs_observed,
        "contract_clean_repairs_promoted": contract_clean_repairs_promoted,
        "semantic_repairs_withheld_for_contract": semantic_repairs_withheld_for_contract,
        "repairs_promoted": contract_clean_repairs_promoted,
        "accepted_repair_count": contract_clean_repairs_promoted,
        "safe_abstains": safe_abstains,
        "oversteers_prevented": oversteers_prevented,
        "regressions_blocked": regressions_blocked,
        "uncontrolled_hallucination_exposures": uncontrolled,
        "wrong_to_wrong_count": wrong_to_wrong_count,
        "wrong_to_correct_count": wrong_to_correct_count,
        "hallucination_exposure_control_count": exposure_control_count,
        "hallucination_exposure_control_rate": exposure_control_rate,
        "net_interventions": contract_clean_repairs_promoted + safe_abstains + regressions_blocked,
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

    def route_inference(self, row: Dict[str, Any]) -> Tuple[str, str]:
        base_correct = int(row.get("baseline_correct", 0))
        cand_correct = int(row.get("candidate_correct", 0))
        base_hr = float(row.get("baseline_hr", 0.0))
        cand_hr = float(row.get("candidate_hr", 0.0))
        base_ent = float(row.get("baseline_entropy", 0.0))
        cand_ent = float(row.get("candidate_entropy", 0.0))

        if base_correct == 1 and cand_correct == 0:
            self.blocked_regressions += 1
            decision = "baseline"
            reason = "Candidate blocked because baseline captured the target and candidate failed."
        elif base_correct == 0 and cand_correct == 1:
            self.semantic_repairs_observed += 1
            if is_contract_clean_candidate_repair(row):
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
            if cand_contract_violation:
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
        correct_to_wrong_count = transition_stats.get("correct->wrong", 0)
        checks.append(GateCheck(
            name="Correct-to-Wrong Regressions Count",
            passed=correct_to_wrong_count == 0,
            severity="CRITICAL",
            metric_value=correct_to_wrong_count,
            threshold=0,
            explanation=f"Zero correct-to-wrong regressions required. Found {correct_to_wrong_count} regressions."
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
            name="Generalization Non-Degradation Instruction Gate",
            passed=True if not self.gate_cfg.enforce_instruction_contract_gate else (cand_inst_violation <= base_inst_violation),
            severity="DIAGNOSTIC_ONLY" if not self.gate_cfg.enforce_instruction_contract_gate else "HIGH",
            metric_value=cand_inst_violation,
            threshold=base_inst_violation,
            explanation="Instruction contract tracking operated diagnostically for this validation pass." if not self.gate_cfg.enforce_instruction_contract_gate else f"Candidate instruction-contract violation rate ({cand_inst_violation*100:.2f}%) must not exceed baseline ({base_inst_violation*100:.2f}%)."
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
        checks.append(GateCheck(
            name="Hallucination Risk Trend Variance Gate",
            passed=risk_increase <= self.gate_cfg.max_candidate_hallucination_risk_increase,
            severity="HIGH",
            metric_value=risk_increase,
            threshold=self.gate_cfg.max_candidate_hallucination_risk_increase,
            explanation=f"Average candidate risk increase ({risk_increase:.4f}) must be within limit ({self.gate_cfg.max_candidate_hallucination_risk_increase:.4f})."
        ))

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
            seen_drop = seen_baseline_acc - seen_cand_acc
            checks.append(GateCheck(
                name="Seen Accuracy Non-Inferiority Margin",
                passed=seen_drop <= self.gate_cfg.non_inferiority_margin,
                severity="HIGH",
                metric_value=seen_drop,
                threshold=self.gate_cfg.non_inferiority_margin,
                explanation=f"Seen accuracy drop ({seen_drop*100:.2f}%) vs non-inferiority margin ({self.gate_cfg.non_inferiority_margin*100:.1f}%)."
            ))

            checks.append(GateCheck(
                name="Seen Accuracy Degradation Budget",
                passed=seen_drop <= self.gate_cfg.degradation_budget,
                severity="CRITICAL",
                metric_value=seen_drop,
                threshold=self.gate_cfg.degradation_budget,
                explanation=f"Seen accuracy degradation ({seen_drop*100:.2f}%) vs budget ({self.gate_cfg.degradation_budget*100:.1f}%)."
            ))

            unseen_gain = unseen_cand_acc - unseen_baseline_acc
            checks.append(GateCheck(
                name="Unseen Accuracy Improvement",
                passed=unseen_gain >= self.gate_cfg.min_unseen_improvement,
                severity="HIGH",
                metric_value=unseen_gain,
                threshold=self.gate_cfg.min_unseen_improvement,
                explanation=f"Unseen accuracy improvement ({unseen_gain*100:.2f}%) vs requirement ({self.gate_cfg.min_unseen_improvement*100:.1f}%)."
            ))

            checks.append(GateCheck(
                name="Generalization Non-Degradation Guard",
                passed=unseen_gain >= 0.0,
                severity="CRITICAL",
                metric_value=unseen_gain,
                threshold=0.0,
                explanation=f"Generalization failure guard: Unseen validation exact match gain must be >= 0.0% (Found {unseen_gain*100:.2f}%)."
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
    """Decouples localized validation outcomes into failures and calibration categories."""
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
    """Explicitly audits and resolves discrepancies between aggregate loop metrics and trace means."""
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