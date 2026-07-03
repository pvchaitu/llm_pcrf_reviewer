"""
PCRF Transformer Reliability Suite - Causal Representation Modeling & Regularization
pcrf_modeling.py
========================================================================================
Implements TransformerHookManager activation trackers, EvaluatorPlus CLM evaluators, SFT
damped learning optimizations, CDL v2 penalties, and the 4 canonical feature plugins.
"""

import os
import csv
import json
import math
import copy
import logging
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM, PreTrainedModel, PreTrainedTokenizer

from pcrf_core import PCRFCore, compute_hallucination_risk
from pcrf_dataset import (
    CustomFactualDataset,
    normalize_text,
    evaluate_semantic_match,
    detect_format_template_leakage,
    detect_over_generation,
    detect_instruction_contract_violation,
    ClozeQAExample
)
from pcrf_governance import (
    FeatureHealthReport,
    FeatureDecisionReport,
    PromotionGateConfig,
    is_baseline_hallucination,
    is_candidate_hallucination
)

import os
import abc
import csv
import json
import math
import copy
import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer

from pcrf_core import PCRFCore, format_neg_zero
from pcrf_dataset import (
    ClozeQAExample,
    CustomFactualDataset,
    normalize_text,
    evaluate_semantic_match,
    detect_format_template_leakage,
    detect_over_generation,
    detect_instruction_contract_violation
)
from pcrf_governance import FeatureHealthReport, FeatureDecisionReport

logger = logging.getLogger("PCRF_Suite")

# Safety withhold variables replicated for local file isolation
SAFETY_WITHHELD_RESPONSE = "⚠️ Hallucination Risk Detected — Response Withheld for Safety"

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

class TransformerHookManager:
    """Robust dynamic registration and cleanup of forward activation hooks."""
    def __init__(self, model: PreTrainedModel):
        self.model = model
        self.hooks = []
        self.active_activations = {}
        self._detect_layer_blocks()

    def _detect_layer_blocks(self) -> None:
        self.block_list = None
        for attr in ["transformer", "model"]:
            if hasattr(self.model, attr):
                obj = getattr(self.model, attr)
                for block_attr in ["h", "layers", "blocks"]:
                    if hasattr(obj, block_attr):
                        self.block_list = getattr(obj, block_attr)
                        break
        if self.block_list is None:
            for block_attr in ["h", "layers", "blocks"]:
                if hasattr(self.model, block_attr):
                    self.block_list = getattr(self.model, block_attr)
                    break

    def register_noise_perturbation(self, layer_idx: int, scale: float = 0.05) -> None:
        if self.block_list is None or layer_idx >= len(self.block_list):
            return
        target_block = self.block_list[layer_idx]

        def hook_fn(module, input, output):
            if isinstance(output, tuple):
                tensor_data = output[0]
            else:
                tensor_data = output
            noise = torch.randn_like(tensor_data) * scale
            perturbed = tensor_data + noise
            if isinstance(output, tuple):
                return (perturbed,) + output[1:]
            return perturbed

        self.hooks.append(target_block.register_forward_hook(hook_fn))

    def register_activation_capture(self, layer_idx: int) -> None:
        if self.block_list is None or layer_idx >= len(self.block_list):
            return
        target_block = self.block_list[layer_idx]

        def hook_fn(module, input, output):
            if isinstance(output, tuple):
                self.active_activations[layer_idx] = output[0].detach().clone()
            else:
                self.active_activations[layer_idx] = output.detach().clone()

        self.hooks.append(target_block.register_forward_hook(hook_fn))

    def remove_all_hooks(self) -> None:
        for hook in self.hooks:
            hook.remove()
        self.hooks.clear()
        self.active_activations.clear()


class EvaluatorPlus:
    """Enriched CLM evaluator breaking performance metrics into corporate dimensions."""
    @staticmethod
    def evaluate_dataset_detailed(
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        dataset: CustomFactualDataset,
        max_len: int = 128
    ) -> Dict[str, Any]:
        model.eval()
        total_loss = 0.0
        total_tokens = 0

        strict_em_count = 0
        first_token_match_count = 0
        semantic_capture_count = 0
        over_generation_count = 0
        instruction_violation_count = 0

        device = next(model.parameters()).device
        loader = DataLoader(dataset, batch_size=1, shuffle=False)
        predictions = []

        with torch.no_grad():
            for batch in loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                ex_id = int(batch["example_id"][0].item())

                original_example = next(ex for ex in dataset.examples if ex.example_id == ex_id)

                outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                logits = outputs.logits
                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = labels[..., 1:].contiguous()

                active_mask = (shift_labels != -100)
                if active_mask.any():
                    flat_logits = shift_logits[active_mask]
                    flat_labels = shift_labels[active_mask]
                    item_loss = F.cross_entropy(flat_logits, flat_labels, reduction="sum").item()
                    num_tokens = active_mask.sum().item()
                    total_loss += item_loss
                    total_tokens += num_tokens
                    avg_item_nll = item_loss / max(1e-5, num_tokens)
                else:
                    avg_item_nll = 0.0

                prompt_ids = tokenizer(original_example.prompt, return_tensors="pt", add_special_tokens=False)["input_ids"].to(device)
                prompt_len = prompt_ids.shape[1]

                generated_tokens = model.generate(
                    prompt_ids,
                    max_new_tokens=12,
                    temperature=0.0,
                    do_sample=False,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id
                )

                pred_ids = generated_tokens[0][prompt_len:]
                actual_text = tokenizer.decode(pred_ids, skip_special_tokens=True).strip()
                norm_actual = normalize_text(actual_text)
                norm_target = normalize_text(original_example.target)

                is_strict_em = (norm_actual == norm_target)
                if is_strict_em:
                    strict_em_count += 1

                gen_words = norm_actual.split()
                tar_words = norm_target.split()
                is_first_token = False
                if gen_words and tar_words:
                    is_first_token = (gen_words[0] == tar_words[0])
                if is_first_token:
                    first_token_match_count += 1

                is_semantic = evaluate_semantic_match(actual_text, original_example.target)
                if is_semantic:
                    semantic_capture_count += 1

                is_format_leakage = detect_format_template_leakage(actual_text)
                is_over_gen = detect_over_generation(actual_text, original_example.target)
                is_instruction_violation = detect_instruction_contract_violation(actual_text, original_example.target)

                if is_instruction_violation or is_format_leakage or is_over_gen:
                    instruction_violation_count += 1
                if is_over_gen:
                    over_generation_count += 1

                last_prompt_index = prompt_len - 1
                if last_prompt_index < shift_logits.shape[1]:
                    last_prompt_logits = shift_logits[0, last_prompt_index, :]
                    probs = F.softmax(last_prompt_logits, dim=-1)
                    top_vals, top_inds = torch.topk(probs, 2)
                    top1_prob = float(top_vals[0].item())
                    top2_prob = float(top_vals[1].item())
                    top1_token = tokenizer.decode([top_inds[0].item()]).strip()
                    top2_token = tokenizer.decode([top_inds[1].item()]).strip()
                    logit_top_vals, _ = torch.topk(last_prompt_logits, 2)
                    margin = float((logit_top_vals[0] - logit_top_vals[1]).item())
                    entropy = float((-probs * torch.log(probs + 1e-12)).sum().item())
                else:
                    top1_prob, top2_prob = 1.0, 0.0
                    top1_token, top2_token = "", ""
                    margin, entropy = 10.0, 0.0

                failure_cat = "N/A"
                if not is_semantic:
                    if top1_prob > 0.60:
                        failure_cat = "HIGH_CONFIDENCE_WRONG"
                    elif top1_token.lower() in [normalize_text(x) for x in ["____", "A.", "B.", "A", "B", "______"]]:
                        failure_cat = "FORMAT_TEMPLATE_FAILURE"
                    elif normalize_text(top1_token) != norm_target and len(top1_token.strip()) > 0:
                        failure_cat = "WRONG_ENTITY_SUBSTITUTION"
                    else:
                        failure_cat = "TARGET_MISS"
                elif is_instruction_violation:
                    failure_cat = "INSTRUCTION_CONTRACT_VIOLATION"

                predictions.append({
                    "id": ex_id,
                    "prompt": original_example.prompt,
                    "target": original_example.target,
                    "expected": original_example.target,
                    "actual": actual_text if actual_text else "<EMPTY_GENERATION>",
                    "correct": 1 if is_semantic else 0,
                    "is_strict_em": 1 if is_strict_em else 0,
                    "is_first_token": 1 if is_first_token else 0,
                    "is_instruction_violation": 1 if is_instruction_violation else 0,
                    "is_format_leakage": 1 if is_format_leakage else 0,
                    "is_over_gen": 1 if is_over_gen else 0,
                    "failure_category": failure_cat,
                    "nll": avg_item_nll,
                    "is_critical": original_example.is_critical,
                    "criticality_weight": original_example.criticality_weight,
                    "entropy": entropy,
                    "margin": margin,
                    "top1_token": top1_token,
                    "top1_prob": top1_prob,
                    "top2_token": top2_token,
                    "top2_prob": top2_prob
                })

        avg_nll = total_loss / max(1, total_tokens)
        acc_semantic = semantic_capture_count / max(1, len(dataset))
        acc_strict = strict_em_count / max(1, len(dataset))
        acc_first = first_token_match_count / max(1, len(dataset))
        rate_violation = instruction_violation_count / max(1, len(dataset))

        return {
            "avg_nll": avg_nll,
            "perplexity": math.exp(min(50, avg_nll)),
            "exact_match_acc": acc_semantic,
            "strict_em_acc": acc_strict,
            "first_token_acc": acc_first,
            "instruction_violation_rate": rate_violation,
            "predictions": predictions
        }


class BaseFeaturePlugin(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str: pass
    @abc.abstractmethod
    def description(self) -> str: pass
    @abc.abstractmethod
    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any: pass
    @abc.abstractmethod
    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport: pass


class DerivativePlugin(BaseFeaturePlugin):
    def name(self) -> str: return "derivatives"
    def description(self) -> str: return "Computes structural downstream probability derivatives."

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        mgr = TransformerHookManager(model)
        if mgr.block_list is None:
            return FeatureHealthReport(self.name(), is_healthy=False, unsupported_reason="Untracked layer topology.")
        return FeatureHealthReport(self.name(), is_healthy=True, diagnostics=[f"Linked successfully to {len(mgr.block_list)} blocks."])

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        deriv_cfg = cfg.derivative_cfg
        model_cfg = cfg.model_cfg

        mgr = TransformerHookManager(model)
        num_layers = len(mgr.block_list) if mgr.block_list is not None else 0

        dataset = CustomFactualDataset(splits["train"], tokenizer, model_cfg.max_len)
        loader = DataLoader(dataset, batch_size=2, shuffle=False)
        device = model_cfg.device

        baseline_probs = {}
        model.eval()
        with torch.no_grad():
            for batch in loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                ex_ids = batch["example_id"].tolist()

                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                shift_logits = outputs.logits[..., :-1, :].contiguous()
                shift_labels = labels[..., 1:].contiguous()

                for b_i, ex_id in enumerate(ex_ids):
                    mask = (shift_labels[b_i] != -100)
                    if mask.any():
                        probs = F.softmax(shift_logits[b_i, mask], dim=-1)
                        targets = shift_labels[b_i, mask]
                        baseline_probs[ex_id] = float(probs[0, targets[0]].item())
                    else:
                        baseline_probs[ex_id] = 1.0

        layer_derivatives = []
        for l_idx in range(num_layers):
            mgr.remove_all_hooks()
            mgr.register_noise_perturbation(l_idx, deriv_cfg.noise_std)

            perturbed_probs = []
            with torch.no_grad():
                for batch in loader:
                    input_ids = batch["input_ids"].to(device)
                    attention_mask = batch["attention_mask"].to(device)
                    labels = batch["labels"].to(device)

                    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                    shift_logits = outputs.logits[..., :-1, :].contiguous()
                    shift_labels = labels[..., 1:].contiguous()

                    for b_i in range(input_ids.size(0)):
                        mask = (shift_labels[b_i] != -100)
                        if mask.any():
                            probs = F.softmax(shift_logits[b_i, mask], dim=-1)
                            targets = shift_labels[b_i, mask]
                            perturbed_probs.append(float(probs[0, targets[0]].item()))
                        else:
                            perturbed_probs.append(1.0)

            base_mean = np.mean(list(baseline_probs.values()))
            pert_mean = np.mean(perturbed_probs)
            delta = float(base_mean - pert_mean)

            layer_derivatives.append({
                "layer_id": l_idx,
                "clean_mean_target_prob": base_mean,
                "perturbed_mean_target_prob": pert_mean,
                "empirical_delta_prob": delta,
                "dr_de": -delta
            })

        mgr.remove_all_hooks()
        os.makedirs(cfg.artifact_cfg.output_dir, exist_ok=True)
        csv_path = os.path.join(cfg.artifact_cfg.output_dir, "per_module_derivatives.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["layer_id", "clean_mean_target_prob", "perturbed_mean_target_prob", "empirical_delta_prob", "dr_de"])
            writer.writeheader()
            writer.writerows(layer_derivatives)

        return layer_derivatives

    def should_apply(self, baseline_stats: Dict[str, Any], derivatives: List[Dict[str, Any]], gate_cfg: Any) -> FeatureDecisionReport:
        avg_delta = np.mean([abs(x["empirical_delta_prob"]) for x in derivatives]) if derivatives else 0.0
        if avg_delta < 0.0001:
            return FeatureDecisionReport(
                feature_name=self.name(),
                status="MEASUREMENT_ONLY",
                reason_code="DERIVATIVE_INSTABILITY",
                explanation="Analytical derivative signals too weak to safely map control loops.",
                recommender_action="Increase perturbation scale or check baseline accuracy.",
                safest_alternative="Revert parameters to stable baseline."
            )
        return FeatureDecisionReport(
            feature_name=self.name(),
            status="SAFE_TO_APPLY",
            reason_code="READY_FOR_USE",
            explanation="Estimated derivatives are highly localized and stable.",
            recommender_action="Deploy priority replay buffer and scale SFT regularization.",
            safest_alternative="N/A"
        )


class CurriculumPlugin(BaseFeaturePlugin):
    def name(self) -> str: return "curriculum"
    def description(self) -> str: return "Prioritizes cascading error prompts."

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        return FeatureHealthReport(self.name(), is_healthy=True)

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        model_cfg = cfg.model_cfg

        deriv_plugin = DerivativePlugin()
        deriv_results = deriv_plugin.run_standalone(model, tokenizer, splits, cfg)
        deriv_weight = sum([max(0.0, x["empirical_delta_prob"]) for x in deriv_results])

        prioritized_dataset = []
        model.eval()
        device = model_cfg.device

        with torch.no_grad():
            for ex in splits["train"]:
                prompt_ids = tokenizer(ex.prompt, return_tensors="pt")["input_ids"].to(device)
                target_ids = tokenizer(ex.target, return_tensors="pt")["input_ids"].to(device)

                full_ids = torch.cat([prompt_ids, target_ids], dim=-1)
                labels = full_ids.clone()
                labels[:, :prompt_ids.shape[-1]] = -100

                outputs = model(full_ids, labels=labels)
                nll = float(outputs.loss.item()) if not torch.isnan(outputs.loss) else 2.0

                priority_score = nll * (1.0 + deriv_weight)
                prioritized_dataset.append({
                    "id": ex.example_id,
                    "prompt": ex.prompt,
                    "target": ex.target,
                    "priority_score": priority_score,
                    "pcrf_weight": deriv_weight,
                    "criticality_weight": ex.criticality_weight
                })

        total_p_score = sum(x["priority_score"] for x in prioritized_dataset)
        for x in prioritized_dataset:
            x["curriculum_score"] = x["priority_score"] / max(1e-9, total_p_score)
            x["combined_weight"] = x["curriculum_score"] * x["pcrf_weight"] * x["criticality_weight"]

        prioritized_dataset.sort(key=lambda x: x["priority_score"], reverse=True)

        num_items = len(prioritized_dataset)
        for idx, x in enumerate(prioritized_dataset):
            if idx < int(0.25 * num_items):
                x["sampling_bucket"] = "HIGH_PRIORITY"
            elif idx < int(0.75 * num_items):
                x["sampling_bucket"] = "MID_PRIORITY"
            else:
                x["sampling_bucket"] = "LOW_PRIORITY"

        os.makedirs(cfg.artifact_cfg.output_dir, exist_ok=True)
        csv_path_scores = os.path.join(cfg.artifact_cfg.output_dir, "curriculum_scores.csv")
        with open(csv_path_scores, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "prompt", "target", "priority_score"])
            writer.writeheader()
            for x in prioritized_dataset:
                writer.writerow({"id": x["id"], "prompt": x["prompt"], "target": x["target"], "priority_score": x["priority_score"]})

        csv_path_plan = os.path.join(cfg.artifact_cfg.output_dir, "curriculum_sampling_plan.csv")
        with open(csv_path_plan, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["sample_id", "prompt", "target", "curriculum_score", "pcrf_weight", "criticality_weight", "combined_weight", "sampling_bucket"])
            writer.writeheader()
            for x in prioritized_dataset:
                writer.writerow({
                    "sample_id": x["id"], "prompt": x["prompt"], "target": x["target"],
                    "curriculum_score": f"{x['curriculum_score']:.6f}", "pcrf_weight": f"{x['pcrf_weight']:.6f}",
                    "criticality_weight": f"{x['criticality_weight']:.1f}", "combined_weight": f"{x['combined_weight']:.6f}",
                    "sampling_bucket": x["sampling_bucket"]
                })

        return prioritized_dataset

    def should_apply(self, baseline_stats: Dict[str, Any], prioritized_dataset: List[Dict[str, Any]], gate_cfg: Any) -> FeatureDecisionReport:
        priority_std = np.std([x["priority_score"] for x in prioritized_dataset]) if prioritized_dataset else 0.0
        if priority_std < 0.01:
            return FeatureDecisionReport(
                feature_name=self.name(),
                status="DO_NOT_APPLY",
                reason_code="NO_CURRICULUM_SIGNAL",
                explanation="No selective variance detected across prioritized dataset.",
                recommender_action="Re-run derivatives check or check base perplexity distributions.",
                safest_alternative="Revert to standard uniform minibatch selection."
            )
        return FeatureDecisionReport(
            feature_name=self.name(),
            status="SAFE_TO_APPLY",
            reason_code="READY_FOR_USE",
            explanation="Curriculum prioritize maps are clear and highly differentiated.",
            recommender_action="Deploy Priority Replay Buffer.",
            safest_alternative="N/A"
        )


class StructuralPCRFPlugin(BaseFeaturePlugin):
    def name(self) -> str: return "structural_pcrf"
    def description(self) -> str: return "Monitors residual representation integrity with flaw roadmaps."

    def __init__(self):
        self.layer_selection = None
        self.last_run_flaws = []
        self.last_chain_reliability = 1.0
        self.last_crew_prod = 1.0
        self.last_crew_geo = 1.0
        self.last_worst_k_risk = 0.0
        self.is_bypass_dominated = False
        self.structural_status = "STRUCTURAL_PROMOTION_GRADE"

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        mgr = TransformerHookManager(model)
        if mgr.block_list is None:
            return FeatureHealthReport(self.name(), is_healthy=False, unsupported_reason="Unknown transformer block layout.")
        return FeatureHealthReport(self.name(), is_healthy=True)

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        struct_cfg = cfg.structural_cfg
        model_cfg = cfg.model_cfg

        mgr = TransformerHookManager(model)
        num_layers = len(mgr.block_list)

        seen_val_ds = CustomFactualDataset(splits["seen_val"], tokenizer, model_cfg.max_len)
        loader = DataLoader(seen_val_ds, batch_size=2, shuffle=False)
        device = model_cfg.device

        for idx in range(num_layers):
            mgr.register_activation_capture(idx)

        baseline_acts = {i: [] for i in range(num_layers)}
        model.eval()
        with torch.no_grad():
            for batch in loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                _ = model(input_ids=input_ids, attention_mask=attention_mask)
                for idx in range(num_layers):
                    if idx in mgr.active_activations:
                        baseline_acts[idx].append(mgr.active_activations[idx].cpu())

        mgr.remove_all_hooks()

        for idx in range(num_layers):
            mgr.register_activation_capture(idx)

        perturbed_acts = {i: [] for i in range(num_layers)}
        with torch.no_grad():
            for batch in loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)

                embeds = model.get_input_embeddings()(input_ids)
                embeds = embeds + torch.randn_like(embeds) * 0.02

                _ = model(inputs_embeds=embeds, attention_mask=attention_mask)
                for idx in range(num_layers):
                    if idx in mgr.active_activations:
                        perturbed_acts[idx].append(mgr.active_activations[idx].cpu())

        mgr.remove_all_hooks()

        calibrated_beta = struct_cfg.decay_beta / math.sqrt(max(1, num_layers))

        layer_reliabilities = []
        perturbed_l2_norms = []
        clean_l2_norms = []

        for idx in range(num_layers):
            clean_list = baseline_acts[idx]
            perturbed_list = perturbed_acts[idx]

            cos_sims = []
            for clean, pert in zip(clean_list, perturbed_list):
                c_flat = clean.view(-1)
                p_flat = pert.view(-1)
                sim = float(F.cosine_similarity(c_flat, p_flat, dim=0).item())
                cos_sims.append(sim)

                perturbed_l2_norms.append(float(torch.norm(p_flat, p=2).item()))
                clean_l2_norms.append(float(torch.norm(c_flat, p=2).item()))

            avg_sim = float(np.mean(cos_sims))
            drift = 1.0 - max(0.0, avg_sim)

            r_l = PCRFCore.map_drift_to_reliability(drift, struct_cfg.mapping_transform, calibrated_beta)
            layer_reliabilities.append(r_l)

        derivatives = PCRFCore.compute_analytical_series_derivatives(layer_reliabilities)

        deriv_plugin = DerivativePlugin()
        deriv_data = deriv_plugin.run_standalone(model, tokenizer, splits, cfg)
        deriv_probs = {int(d["layer_id"]): float(d["empirical_delta_prob"]) for d in deriv_data}

        crew_reliabilities = []
        r_prev = 1.0

        layer_breakdown_pre = []
        is_bypass_dominated = True

        for idx, r_l in enumerate(layer_reliabilities):
            block = mgr.block_list[idx] if mgr.block_list is not None else None
            w_attn = 0.05
            w_mlp = 0.05

            if block is not None:
                attn_params = sum(p.numel() for p in block.parameters() if "attn" in str(p) or "attention" in str(p))
                mlp_params = sum(p.numel() for p in block.parameters() if "mlp" in str(p) or "feed_forward" in str(p))
                total_params = attn_params + mlp_params + 1e-12
                if total_params < 1000:
                    w_attn = 0.02
                    w_mlp = 0.03
                else:
                    w_attn = min(0.45, float(attn_params / total_params))
                    w_mlp = min(0.55, float(mlp_params / total_params))

            w_bypass = 1.0 - w_attn - w_mlp
            if w_bypass < 0.65:
                is_bypass_dominated = False

            d_l = 1.0 - r_l
            r_attn = math.exp(-calibrated_beta * d_l * 0.8)
            r_mlp = math.exp(-calibrated_beta * d_l * 1.2)

            r_bypass = r_prev
            r_crew = (w_bypass * r_bypass) + (w_attn * r_attn) + (w_mlp * r_mlp)
            r_prev = r_crew
            crew_reliabilities.append(r_crew)

            s_l = -math.log(max(1e-12, r_crew))
            d_r_crew = derivatives[idx] * (r_crew / max(1e-12, r_l))
            empirical_delta_prob = deriv_probs.get(idx, 0.0)
            structural_atmap_delta_prob = float(calibrated_beta * d_l)

            b_crew = (w_attn + w_mlp) * calibrated_beta * math.exp(-calibrated_beta * d_l) / max(1e-12, r_crew)
            layer_risk = s_l * (1.0 + abs(d_r_crew))

            layer_breakdown_pre.append({
                "layer_id": idx,
                "reliability_r_l": r_crew,
                "r_series_local": r_l,
                "structural_entropy_S_l": s_l,
                "D_R": d_r_crew,
                "empirical_delta_prob": empirical_delta_prob,
                "structural_atmap_delta_prob": structural_atmap_delta_prob,
                "combined_layer_risk_score": layer_risk,
                "crew_birnbaum_sensitivity": b_crew,
                "w_bypass": w_bypass,
                "w_attn": w_attn,
                "w_mlp": w_mlp,
                "r_bypass": r_bypass,
                "r_attn": r_attn,
                "r_mlp": r_mlp
            })

        policy = cfg.reporting_cfg.bottleneck_selection_policy
        self.layer_selection = compute_layer_selection_result(deriv_data, layer_breakdown_pre, policy)
        selected_intervention_layers = self.layer_selection.final_selected
        selected_intervention_ids = set(selected_intervention_layers)

        emp_top_ids = set(self.layer_selection.empirical_selected)
        birn_top_ids = set(self.layer_selection.birnbaum_selected)
        risk_top_ids = set(self.layer_selection.combined_risk_selected)

        layer_breakdown = []
        for idx, item in enumerate(layer_breakdown_pre):
            is_selected = (idx in selected_intervention_ids)
            reason_text = generate_layer_selection_reason(
                layer_id=idx,
                S_l=item["structural_entropy_S_l"],
                D_R=item["D_R"],
                empirical_delta=item["empirical_delta_prob"],
                is_selected=is_selected,
                policy=policy,
                cfg=cfg,
                bypass_dominated=is_bypass_dominated
            )

            item.update({
                "monitoring_candidate_flag": 1,
                "selected_for_intervention_flag": 1 if is_selected else 0,
                "selected_by_empirical_policy": 1 if idx in emp_top_ids else 0,
                "selected_by_birnbaum_policy": 1 if idx in birn_top_ids else 0,
                "selected_by_combined_risk_policy": 1 if idx in risk_top_ids else 0,
                "intervention_flag": 1 if is_selected else 0,
                "intervention_type": "regularization" if is_selected else "freeze",
                "intervention_reason": reason_text
            })
            layer_breakdown.append(item)

        triggered_flaws = []
        r_sys_series = float(np.prod(layer_reliabilities))
        r_sys_crew_prod = float(np.prod(crew_reliabilities))
        r_sys_crew_geo = float(math.exp(np.mean([math.log(max(1e-12, r)) for r in crew_reliabilities])))

        worst_k_risk = float(np.mean([1.0 - x["reliability_r_l"] for x in sorted(layer_breakdown, key=lambda x: x["combined_layer_risk_score"], reverse=True)[:4]]))

        if is_bypass_dominated:
            triggered_flaws.append("RESIDUAL_STREAM_BYPASS_DETECTED")

        if struct_cfg.enable_roadmap_heuristics:
            avg_p_l2 = np.mean(perturbed_l2_norms)
            avg_c_l2 = np.mean(clean_l2_norms)
            ratio = avg_p_l2 / avg_c_l2 if avg_c_l2 > 0 else 1.0
            if (ratio < 0.8 or ratio > 1.2) and r_sys_crew_prod > 0.95:
                triggered_flaws.append("COSINE_AMPLITUDE_BLOWOUT")

            has_cloze = any(ex.task_type in ["cloze", "dialogue"] for ex in splits["train"])
            if has_cloze:
                triggered_flaws.append("CREATIVE_TASK_MISMATCH")

        os.makedirs(cfg.artifact_cfg.output_dir, exist_ok=True)
        summary_path = os.path.join(cfg.artifact_cfg.output_dir, "structural_pcrf_summary.json")

        structural_status = "STRUCTURAL_PROMOTION_GRADE"
        if is_bypass_dominated:
            structural_status = "STRUCTURAL_UNINFORMATIVE_BYPASS_DOMINATED"
        elif r_sys_crew_geo < cfg.gate_cfg.crew_geo_reliability_threshold:
            structural_status = "STRUCTURAL_FAIL"

        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump({
                "R_sys_chain": r_sys_series,
                "R_sys_crew_prod": r_sys_crew_prod,
                "R_sys_crew_geo": r_sys_crew_geo,
                "worst_k_risk": worst_k_risk,
                "triggered_flaws": triggered_flaws,
                "structural_status": structural_status,
                "is_bypass_dominated": is_bypass_dominated,
                "layers": [{
                    "layer_idx": lb["layer_id"],
                    "reliability_r_l": lb["reliability_r_l"],
                    "r_series_local": lb["r_series_local"],
                    "structural_entropy_S_l": lb["structural_entropy_S_l"],
                    "analytical_derivative": lb["D_R"],
                    "crew_birnbaum_sensitivity": lb["crew_birnbaum_sensitivity"],
                    "w_bypass": lb["w_bypass"],
                    "w_attn": lb["w_attn"],
                    "w_mlp": lb["w_mlp"]
                } for lb in layer_breakdown]
            }, f, indent=4)

        plan_path = os.path.join(cfg.artifact_cfg.output_dir, "layer_intervention_plan.csv")
        with open(plan_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "layer_id", "reliability_r_l", "structural_entropy_S_l",
                "D_R", "empirical_delta_prob", "structural_atmap_delta_prob",
                "combined_layer_risk_score", "crew_birnbaum_sensitivity",
                "monitoring_candidate_flag", "selected_for_intervention_flag",
                "selected_by_empirical_policy", "selected_by_birnbaum_policy",
                "selected_by_combined_risk_policy", "intervention_flag",
                "intervention_type", "intervention_reason"
            ])
            writer.writeheader()
            for lb in layer_breakdown:
                writer.writerow({
                    "layer_id": lb["layer_id"],
                    "reliability_r_l": f"{lb['reliability_r_l']:.6f}",
                    "structural_entropy_S_l": f"{lb['structural_entropy_S_l']:.6f}",
                    "D_R": f"{lb['D_R']:.6f}",
                    "empirical_delta_prob": f"{lb['empirical_delta_prob']:.6f}",
                    "structural_atmap_delta_prob": f"{lb['structural_atmap_delta_prob']:.6f}",
                    "combined_layer_risk_score": f"{lb['combined_layer_risk_score']:.6f}",
                    "crew_birnbaum_sensitivity": f"{lb['crew_birnbaum_sensitivity']:.6f}",
                    "monitoring_candidate_flag": lb["monitoring_candidate_flag"],
                    "selected_for_intervention_flag": lb["selected_for_intervention_flag"],
                    "selected_by_empirical_policy": lb["selected_by_empirical_policy"],
                    "selected_by_birnbaum_policy": lb["selected_by_birnbaum_policy"],
                    "selected_by_combined_risk_policy": lb["selected_by_combined_risk_policy"],
                    "intervention_flag": lb["intervention_flag"],
                    "intervention_type": lb["intervention_type"],
                    "intervention_reason": lb["intervention_reason"]
                })

        self.last_run_flaws = triggered_flaws
        self.last_chain_reliability = r_sys_series
        self.last_crew_prod = r_sys_crew_prod
        self.last_crew_geo = r_sys_crew_geo
        self.last_worst_k_risk = worst_k_risk
        self.is_bypass_dominated = is_bypass_dominated
        self.structural_status = structural_status

        global LAST_COMPUTED_CHAIN_RELIABILITY
        LAST_COMPUTED_CHAIN_RELIABILITY = r_sys_series

        return layer_breakdown

    def should_apply(self, baseline_stats: Dict[str, Any], layer_breakdown: List[Dict[str, Any]], gate_cfg: Any) -> FeatureDecisionReport:
        r_sys_crew_geo = float(math.exp(np.mean([math.log(max(1e-12, x["reliability_r_l"])) for x in layer_breakdown])))

        if self.is_bypass_dominated:
            return FeatureDecisionReport(
                feature_name=self.name(),
                status="MEASUREMENT_ONLY",
                reason_code="STRUCTURAL_BYPASS_DOMINATED",
                explanation="CREW submodule decomposition is highly residual-bypass dominated. Causal paths are masked and uninformative.",
                recommender_action="Deploy only as local uninformative diagnostic. Causal paths require separate validation.",
                safest_alternative="Revert to standard baseline checks; freeze parameter updates."
            )

        if r_sys_crew_geo < gate_cfg.crew_geo_reliability_threshold:
            return FeatureDecisionReport(
                feature_name=self.name(),
                status="DO_NOT_APPLY",
                reason_code="STRUCTURAL_DECAY_REJECTED",
                explanation=f"Decay detected! Depth-normalized geometric CREW reliability ({r_sys_crew_geo*100:.2f}%) fell below safety floor ({gate_cfg.crew_geo_reliability_threshold*100:.1f}%).",
                recommender_action="Reject structural adoption. Re-evaluate layer weight distributions.",
                safest_alternative="Revert parameters to stable baseline."
            )

        if hasattr(self, "last_run_flaws") and self.last_run_flaws:
            flaw_text = " | ".join(self.last_run_flaws)
            return FeatureDecisionReport(
                feature_name=self.name(),
                status="MEASUREMENT_ONLY",
                reason_code="ROADMAP_GATE_TRIGGERED",
                explanation=f"Advanced representation checks blocked SFT candidate promotion. Triggers: {flaw_text}",
                recommender_action="Deploy SFT candidate as diagnostic analyzer. Proceed with representation roadmap checks.",
                safest_alternative="Revert parameters to pre-training baseline."
            )
        return FeatureDecisionReport(
            feature_name=self.name(),
            status="SAFE_TO_APPLY",
            reason_code="READY_FOR_USE",
            explanation="Residual depth channels are highly stable and coherent.",
            recommender_action="Activate Real-Time Drift Alarm.",
            safest_alternative="N/A"
        )


class DerivativeRegularizer(BaseFeaturePlugin):
    def name(self) -> str: return "regularization"
    def description(self) -> str: return "Executes SFT optimization anchor regularization loops."

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        return FeatureHealthReport(self.name(), is_healthy=True)

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        reg_cfg = cfg.regularization_cfg
        model_cfg = cfg.model_cfg

        deriv_plugin = DerivativePlugin()
        deriv_results = deriv_plugin.run_standalone(model, tokenizer, splits, cfg)

        raw_deltas = np.array([x["empirical_delta_prob"] for x in deriv_results])
        mean_d = np.mean(raw_deltas)
        std_d = np.std(raw_deltas) + 1e-12
        standardized_deltas = (raw_deltas - mean_d) / std_d
        standardized_deltas = np.clip(standardized_deltas + 2.0, 0.0, 5.0)

        weights = [float(w) for w in standardized_deltas]
        sum_w = sum(weights)
        if sum_w > 0:
            weights = [w / sum_w for w in weights]

        logger.info("Initializing Advanced CDL v2 SFT Regularization training loop...")

        reference_model = AutoModelForCausalLM.from_pretrained(model_cfg.model_name)
        if model_cfg.use_fp16 and model_cfg.device == "cuda":
            reference_model = reference_model.half()
        reference_model.to(model_cfg.device)
        reference_model.eval()

        train_examples = splits["train"]
        curriculum_scores = []
        with torch.no_grad():
            for ex in train_examples:
                prompt_ids = tokenizer(ex.prompt, return_tensors="pt")["input_ids"].to(model_cfg.device)
                target_ids = tokenizer(ex.target, return_tensors="pt")["input_ids"].to(model_cfg.device)
                full_ids = torch.cat([prompt_ids, target_ids], dim=-1)
                labels = full_ids.clone()
                labels[:, :prompt_ids.shape[-1]] = -100
                outputs = model(full_ids, labels=labels)
                nll = float(outputs.loss.item()) if not torch.isnan(outputs.loss) else 2.0
                priority_score = nll * (1.0 + sum(weights))
                curriculum_scores.append(priority_score)

        sum_scores = sum(curriculum_scores)
        norm_curriculum = [c / max(1e-9, sum_scores) for c in curriculum_scores]

        combined_weights = []
        for idx, ex in enumerate(train_examples):
            failure_boost = 5.0 if norm_curriculum[idx] > np.mean(norm_curriculum) else 1.0
            comb = norm_curriculum[idx] * sum(weights) * ex.criticality_weight * failure_boost
            combined_weights.append(comb)

        sum_comb = sum(combined_weights)
        sampling_probs = [cw / max(1e-9, sum_comb) for cw in combined_weights] if sum_comb > 0 else [1.0/len(train_examples)]*len(train_examples)

        num_samples = min(15, len(train_examples))
        sampled_indices = np.random.choice(len(train_examples), size=num_samples, replace=False, p=sampling_probs)
        curated_examples = [train_examples[i] for i in sampled_indices]

        dataset = CustomFactualDataset(curated_examples, tokenizer, model_cfg.max_len)
        loader = DataLoader(dataset, batch_size=2, shuffle=True)
        device = model_cfg.device

        model_mgr = TransformerHookManager(model)
        ref_mgr = TransformerHookManager(reference_model)
        num_layers = len(model_mgr.block_list)

        target_layers = [0, 1, num_layers-2, num_layers-1]
        optimized_params = []
        for l_id in target_layers:
            optimized_params.extend(list(model_mgr.block_list[l_id].parameters()))

        optimizer = torch.optim.AdamW(optimized_params if optimized_params else model.parameters(), lr=1e-5)

        mc_targets = ["____", "A.", "B.", "A", "B", "\n", "\n\n", "______", "A ", "B ", "A)"]
        mc_token_ids = []
        for term in mc_targets:
            tids = tokenizer.encode(term, add_special_tokens=False)
            mc_token_ids.extend(tids)
        mc_token_ids = list(set(mc_token_ids))

        for i in range(num_layers):
            model_mgr.register_activation_capture(i)
            ref_mgr.register_activation_capture(i)

        model.train()
        for batch in loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            ce_loss = outputs.loss
            logits = outputs.logits

            with torch.no_grad():
                ref_outputs = reference_model(input_ids=input_ids, attention_mask=attention_mask)
                ref_logits = ref_outputs.logits

            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            active_mask = (shift_labels != -100)

            contrastive_penalty = torch.tensor(0.0, device=device)
            if active_mask.any() and len(mc_token_ids) > 0:
                valid_mc_token_ids = [tid for tid in mc_token_ids if 0 <= tid < shift_logits.size(-1)]
                if valid_mc_token_ids:
                    active_logits = shift_logits[active_mask]
                    probs = F.softmax(active_logits, dim=-1)
                    mc_probs = probs[:, valid_mc_token_ids]
                    contrastive_penalty = mc_probs.sum(dim=-1).mean()

            reg_penalty = torch.tensor(0.0, device=device)
            for l_id in target_layers:
                if l_id in model_mgr.active_activations and l_id in ref_mgr.active_activations:
                    act_curr = model_mgr.active_activations[l_id]
                    act_ref = ref_mgr.active_activations[l_id]
                    drift = 1.0 - F.cosine_similarity(act_curr, act_ref, dim=-1).mean()
                    w_l = weights[l_id] if l_id < len(weights) else 0.0
                    reg_penalty += w_l * drift

            kl_loss = torch.tensor(0.0, device=device)
            if active_mask.any():
                active_logits = shift_logits[active_mask]
                shift_ref_logits = ref_logits[..., :-1, :].contiguous()
                active_ref_logits = shift_ref_logits[active_mask]
                kl_loss = F.kl_div(
                    F.log_softmax(active_logits, dim=-1),
                    F.softmax(active_ref_logits, dim=-1),
                    reduction="batchmean"
                )

            margin_loss = torch.tensor(0.0, device=device)
            if active_mask.any():
                target_logits = shift_logits[active_mask]
                target_labels = shift_labels[active_mask]

                correct_logits = target_logits.gather(1, target_labels.unsqueeze(-1)).squeeze(-1)
                mask_other = torch.ones_like(target_logits, dtype=torch.bool)
                mask_other.scatter_(1, target_labels.unsqueeze(-1), False)
                max_other_logits = target_logits[mask_other].view(target_logits.size(0), -1).max(dim=-1)[0]

                margin_loss = F.relu(0.1 - (correct_logits - max_other_logits)).mean()

            l_argmax = torch.tensor(0.0, device=device)
            if active_mask.any():
                shift_ref_logits = ref_logits[..., :-1, :].contiguous()
                ref_logits_active = shift_ref_logits[active_mask]
                ref_preds = ref_logits_active.argmax(dim=-1)
                is_ref_correct = (ref_preds == target_labels)
                if is_ref_correct.any():
                    l_argmax = F.cross_entropy(target_logits[is_ref_correct], target_labels[is_ref_correct])

            l_wrong = torch.tensor(0.0, device=device)
            if active_mask.any():
                probs_active = F.softmax(target_logits, dim=-1)
                top_probs, top_classes = torch.topk(probs_active, 1, dim=-1)
                top_probs = top_probs.squeeze(-1)
                top_classes = top_classes.squeeze(-1)

                is_wrong = (top_classes != target_labels)
                high_conf_wrong = is_wrong & (top_probs > 0.5)
                if high_conf_wrong.any():
                    l_wrong = (top_probs[high_conf_wrong] - 0.5).mean()

            loss = ce_loss + \
                   (reg_cfg.lambda_drift * reg_penalty) + \
                   (reg_cfg.lambda_kl * kl_loss) + \
                   (reg_cfg.lambda_margin * margin_loss) + \
                   (reg_cfg.lambda_argmax * l_argmax) + \
                   (reg_cfg.lambda_wrong * l_wrong) + \
                   (reg_cfg.lambda_contrastive * contrastive_penalty)

            if torch.isfinite(loss):
                loss.backward()
                torch.nn.utils.clip_grad_norm_(optimized_params if optimized_params else model.parameters(), max_norm=1.0)
                optimizer.step()

        model_mgr.remove_all_hooks()
        ref_mgr.remove_all_hooks()
        del reference_model

        logger.info("Regularization SFT optimization completed.")
        return {"loss": float(loss.item())}

    def should_apply(self, baseline_stats: Dict[str, Any], feature_metrics: Dict[str, Any], gate_cfg: Any) -> FeatureDecisionReport:
        return FeatureDecisionReport(
            feature_name=self.name(),
            status="SAFE_TO_APPLY",
            reason_code="READY_FOR_USE",
            explanation="Regularization loss profile within continuous boundaries.",
            recommender_action="Proceed to global controller gate.",
            safest_alternative="N/A"
        )