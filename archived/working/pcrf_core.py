# ==============================================================================
# File: pcrf_core.py
# ==============================================================================
"""
PCRF Transformer Reliability Suite - Core Reliability Mathematics
pcrf_core.py
========================================================================================
Implements the continuous mathematical foundations, Birnbaum structural importance, 
entropy diagnostics, and analytical risk equations for Causal Reliability Flow.
"""

import math
from typing import List, Dict, Any, Tuple
import torch
import numpy as np
import os
import random
import logging

logger = logging.getLogger("PCRF_Suite")

class PCRFDAGNode:
    """Represents a structural component inside a general multi-module Causal Flow DAG."""
    def __init__(self, node_id: str, operator: str = "AND", r: float = 1.0):
        self.node_id = node_id
        self.operator = operator
        self.r = r
        self.parents: List['PCRFDAGNode'] = []

    def add_parent(self, parent_node: 'PCRFDAGNode') -> None:
        self.parents.append(parent_node)


class PCRFDAGCalculator:
    """Analytical derivatives solver for complex Causal Reliability Flow networks using PyTorch Autograd."""
    @staticmethod
    def calculate_reliability(nodes: List[PCRFDAGNode], target_node_id: str) -> Dict[str, float]:
        sorted_nodes = PCRFDAGCalculator._topological_sort(nodes, target_node_id)
        
        r_tensors = {n.node_id: torch.tensor(n.r, dtype=torch.float64, requires_grad=True) for n in sorted_nodes}
        prob_correct = {}
        
        for node in sorted_nodes:
            r_curr = r_tensors[node.node_id]
            if not node.parents:
                prob_correct[node.node_id] = r_curr
            else:
                parent_probs = [prob_correct[p.node_id] for p in node.parents]
                if node.operator == "AND":
                    prod_val = parent_probs[0]
                    for p in parent_probs[1:]:
                        prod_val = prod_val * p
                    prob_correct[node.node_id] = r_curr * prod_val
                elif node.operator == "OR":
                    one_minus_prod = torch.tensor(1.0, dtype=torch.float64)
                    for p in parent_probs:
                        one_minus_prod = one_minus_prod * (1.0 - p)
                    prob_correct[node.node_id] = r_curr * (1.0 - one_minus_prod)
                    
        sys_rel = prob_correct[target_node_id]
        sys_rel.backward()
        
        results = {"R_sys": float(sys_rel.item())}
        for node in sorted_nodes:
            results[f"dRsys_dr_{node.node_id}"] = float(r_tensors[node.node_id].grad.item())
            results[f"dRsys_dep_{node.node_id}"] = -float(r_tensors[node.node_id].grad.item())
        return results

    @staticmethod
    def _topological_sort(nodes: List[PCRFDAGNode], target_node_id: str) -> List[PCRFDAGNode]:
        node_map = {n.node_id: n for n in nodes}
        visited = set()
        stack = []

        def visit(n: PCRFDAGNode):
            if n.node_id in visited:
                return
            visited.add(n.node_id)
            for p in n.parents:
                visit(p)
            stack.append(n)

        visit(node_map[target_node_id])
        return stack


class PCRFCore:
    """Continuous relaxation mapper translating vector representation drifts to modular survival probability."""
    @staticmethod
    def map_drift_to_reliability(drift_val: float, transform_mode: str = "exponential", beta: float = 2.0) -> float:
        drift_val = max(0.0, drift_val)
        if transform_mode == "exponential":
            return float(math.exp(-beta * drift_val))
        elif transform_mode == "sigmoid":
            return float(2.0 / (1.0 + math.exp(beta * drift_val)))
        return float(max(0.0, min(1.0, 1.0 - beta * drift_val)))

    @staticmethod
    def compute_analytical_series_derivatives(r_list: List[float]) -> List[float]:
        """
        Computes Birnbaum Analytical Derivative component reliability importance:
        D_R(e_i) = -R_sys / r_i.
        """
        n = len(r_list)
        if n == 0:
            return []
        zeros = r_list.count(0.0)
        prod_val = 1.0
        for r in r_list:
            if r != 0.0:
                prod_val *= r
                
        derivatives = []
        for r in r_list:
            if zeros > 1:
                derivatives.append(0.0)
            elif zeros == 1:
                derivatives.append(prod_val if r == 0.0 else 0.0)
            else:
                derivatives.append(prod_val / r)
        return derivatives


def compute_hallucination_risk(
    entropy: float,
    margin: float,
    kl_divergence: float,
    r_sys: float,
    instability: float,
    is_wrong_high_conf: bool,
    w1: float = 0.15,
    w2: float = 0.15,
    w3: float = 0.10,
    w4: float = 0.20,
    w5: float = 0.15,
    w6: float = 0.25
) -> Tuple[float, str]:
    """Calculates continuous Hallucination Risk Score mapped to corresponding risk bands."""
    ent_risk = min(1.0, entropy / 5.0)
    marg_risk = 1.0 - min(1.0, margin / 5.0)
    kl_risk = min(1.0, kl_divergence / 2.0)
    struct_risk = 1.0 - r_sys
    instab_risk = min(1.0, abs(instability) / 0.1)
    hcw_risk = 1.0 if is_wrong_high_conf else 0.0
    
    hr_score = (w1 * ent_risk) + (w2 * marg_risk) + (w3 * kl_risk) + (w4 * struct_risk) + (w5 * instab_risk) + (w6 * hcw_risk)
    hr_score = float(max(0.0, min(1.0, hr_score)))
    
    if hr_score < 0.30:
        band = "LOW"
    elif hr_score < 0.55:
        band = "MEDIUM"
    elif hr_score < 0.75:
        band = "HIGH"
    else:
        band = "CRITICAL"
        
    return hr_score, band

def format_neg_zero(val: float) -> str:
    """Formats float values to prevent negative zero display in reports."""
    s = f"{val:.4f}"
    if s == "-0.0000" or s == "-0.00":
        return "0.0000"
    return s


def set_reproducibility(seed: int) -> None:
    """Enforces absolute reproducibility guidelines across Python, NumPy, and PyTorch backends."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ["PYTHONHASHSEED"] = str(seed)
    logger.info(f"System-wide reproducibility seeds fixed at baseline value: {seed}")

def get_hardware_profile_details() -> Dict[str, Any]:
    """Queries compute architecture limits dynamically using platform and system resources."""
    import platform
    cpu_count = os.cpu_count() or 1
    total_ram_gb = 8.0
    try:
        import psutil
        if psutil is not None:
            vmem = psutil.virtual_memory()
            total_ram_gb = vmem.total / (1024 ** 3)
    except ImportError:
        pass

    cuda_available = torch.cuda.is_available()
    gpu_name = "None"
    total_vram_gb = 0.0
    if cuda_available:
        gpu_name = torch.cuda.get_device_name(0)
        total_vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)

    return {
        "os": f"{platform.system()} {platform.release()}",
        "cpu_cores": cpu_count,
        "ram_gb": round(total_ram_gb, 2),
        "gpu_available": cuda_available,
        "gpu_name": gpu_name,
        "vram_gb": round(total_vram_gb, 2)
    }


def run_hardware_audit(model_size_params: int) -> None:
    """Executes a hardware resource profile and emits setup recommendations."""
    hw = get_hardware_profile_details()
    logger.info("=" * 90)
    logger.info("                  PCRF RESOURCE AUDIT & COMPUTE PROFILING SYSTEM                  ")
    logger.info("=" * 90)
    logger.info(f"Host OS Platform          : {hw['os']}")
    logger.info(f"Active CPU Cores Detected : {hw['cpu_cores']}")
    logger.info(f"Host System RAM           : {hw['ram_gb']:.2f} GB")
    logger.info(f"GPU Hardware Accelerator  : {hw['gpu_name']}")
    if hw['gpu_available']:
        logger.info(f"Dedicated VRAM Capacity   : {hw['vram_gb']:.2f} GB")
    else:
        logger.info("GPU Hardware Accelerator  : None (CPU Fallback Mode)")

    logger.info(f"Target Model Size (Params): {model_size_params / 1e6:.1f} Million Parameters")
    logger.info("-" * 90)

    logger.info("RECOMMENDED GCP COMPUTE INFRASTRUCTURE SETUP:")
    if model_size_params < 500e6:
        recommendation = (
            "  - Recommended GCP Tier  : n1-standard-8 (8 vCPUs, 30 GB RAM)\n"
            "  - Accelerator Context   : 1x NVIDIA T4 (16 GB VRAM)\n"
            "  - Technical Reason      : Light parameter profiles run perfectly inside standard T4 envelopes.\n"
            "                            At least 30 GB Host RAM prevents OS swap stalls during model download."
        )
    elif 500e6 <= model_size_params <= 3e9:
        recommendation = (
            "  - Recommended GCP Tier  : g2-standard-8 (8 vCPUs, 32 GB RAM)\n"
            "  - Accelerator Context   : 1x NVIDIA L4 (24 GB VRAM)\n"
            "  - Technical Reason      : Mid-tier generative nodes require dense floating-point structures.\n"
            "                            L4 yields modern Ada Lovelace optimizations with plenty of VRAM headroom."
        )
    else:
        recommendation = (
            "  - Recommended GCP Tier  : a2-highgpu-1g (12 vCPUs, 85 GB RAM)\n"
            "  - Accelerator Context   : 1x NVIDIA A100 (40 GB VRAM)\n"
            "  - Technical Reason      : Massive sequence spaces require high tensor throughput."
        )
    logger.info(recommendation)
    logger.info("-" * 90)
    logger.info("GCP COMPUTE ENGINE SAFETY GUIDELINES (OOME PREVENTION):")
    logger.info(" 1. Always purge dangling activations using 'torch.cuda.empty_cache()' during hooks teardown.")
    logger.info(" 2. Enable half-precision (FP16/BF16) modes across all forward passes.")
    logger.info(" 3. Anchor maximum sequence length limits (`max_len`) tightly to block quadratic expansion.")
    logger.info("=" * 90 + "\n")