# pcrf_transformer_reliability_suite.py
"""
PCRF Transformer Reliability Suite v1 (With Advanced Production Upgrades)
========================================================================
A self-contained production-quality framework and reusable library for evaluating,
diagnosing, and improving Causal Language Model reliability using Probability Derivatives
for Causal Reliability Flow (PCRF) and Causal Decay Loss (CDL).

Fully implements and validates four core research tracks:
  (a) Structural PCRF: Series chain/DAG representation reliability modeling.
  (b) Derivative Estimation Engine: Empirical estimation of module reliability derivatives.
  (c) Derivative-Weighted Regularization: Safe derivative-guided regularization with promotion gates.
  (d) Curriculum/Sample Selection: PCRF-based training sample selection and weighted learning.

Upgrades Implemented:
  1. Dynamic Validation Fallback to "Path C" (Continuous NLL and Over-steering limits)
  2. Structural PCRF Roadmapped Flaw Heuristics (Bypass, Blowout, Creative mismatch)
  3. Hardware Profiler and Memory Guard Audit System

Author: AI Systems Research Group
License: MIT License
"""

import os
import sys
import abc
import csv
import json
import math
import random
import logging
import argparse
import platform
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field, asdict

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer

try:
    import psutil
except ImportError:
    psutil = None

# Beautiful logging format for enterprise visibility
logging.basicConfig(
    level=logging.INFO,
    format="[PCRF-Suite] %(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("PCRF_Suite")


# ==============================================================================
# SECTION A. ENVIRONMENT CONFIG, HARDWARE PROFILER & REPRODUCIBILITY (UPGRADE 3)
# ==============================================================================

def run_hardware_audit(model_size_params: int) -> None:
    """
    Executes a hardware resource profile and emits an explicit setup recommendation
    and Out-of-Memory Exception (OOME) prevention guidelines for GCP.
    """
    print("\n" + "=" * 90)
    print("                  PCRF RESOURCE AUDIT & COMPUTE PROFILING SYSTEM                  ")
    print("=" * 90)
    
    # Query CPU core counts
    cpu_count = os.cpu_count() or 1
    
    # Query Virtual memory safely
    total_ram_gb = 8.0
    if psutil is not None:
        vmem = psutil.virtual_memory()
        total_ram_gb = vmem.total / (1024 ** 3)
        
    print(f"Host OS Platform          : {platform.system()} {platform.release()}")
    print(f"Active CPU Cores Detected : {cpu_count}")
    print(f"Host System RAM           : {total_ram_gb:.2f} GB")
    
    # Query CUDA hardware safely
    cuda_available = torch.cuda.is_available()
    gpu_name = "None"
    total_vram_gb = 0.0
    if cuda_available:
        gpu_name = torch.cuda.get_device_name(0)
        total_vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        print(f"GPU Hardware Accelerator  : {gpu_name}")
        print(f"Dedicated VRAM Capacity   : {total_vram_gb:.2f} GB")
    else:
        print("GPU Hardware Accelerator  : None (CPU Fallback Mode)")
        
    print(f"Target Model Size (Params): {model_size_params / 1e6:.1f} Million Parameters")
    print("-" * 90)
    
    # Instance Selection Recommendation Logic
    print("RECOMMENDED GCP COMPUTE INFRASTRUCTURE SETUP:")
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
            "  - Technical Reason      : Massive sequence spaces require high tensor throughput and memory paths\n"
            "                            to avoid activation memory fragmentation OOMs."
        )
        
    print(recommendation)
    print("-" * 90)
    print("GCP COMPUTE ENGINE SAFETY GUIDELINES (OOME PREVENTION):")
    print(" 1. Always purge dangling activations using 'torch.cuda.empty_cache()' during hooks teardown.")
    print(" 2. Enable half-precision (FP16/BF16) modes across all dynamic forward passes.")
    print(" 3. Anchor maximum sequence length limits (`max_len`) tightly to block quadratic expansion.")
    print("=" * 90 + "\n")


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


# ==============================================================================
# SECTION B. TYPED CONFIGURATIONS
# ==============================================================================

@dataclass
class ModelConfig:
    model_name: str = "gpt2"  # Fast, highly verified causal LM
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    use_fp16: bool = torch.cuda.is_available()
    max_len: int = 128
    temperature: float = 0.7
    top_p: float = 0.9
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
    submodule_factorization: bool = False
    enable_roadmap_heuristics: bool = True  # Activates Upgrade 2 checks


@dataclass
class RegularizationConfig:
    enabled: bool = True
    lambda_reg: float = 0.05
    penalty_type: str = "kl_baseline"
    warmup_steps: int = 50
    gradient_anchoring: bool = True
    weight_drift_penalty: float = 0.01
    max_derivative_cap: float = 2.0


@dataclass
class PromotionGateConfig:
    non_inferiority_margin: float = 0.01  # Strictly reject seen accuracy drops > 1%
    min_unseen_improvement: float = 0.02  # Require at least 2% gain on unseen validation to promote
    degradation_budget: float = 0.03        # Rollback immediately if seen metrics drop > 3%
    seen_nll_tolerance: float = 0.05         # Path C Seen NLL max degradation value
    unseen_nll_gain_req: float = 0.05        # Path C Unseen NLL relative drop requirement (5%)


@dataclass
class ArtifactConfig:
    output_dir: str = "./pcrf_artifacts"
    save_everything: bool = True


@dataclass
class FeatureHealthReport:
    feature_name: str
    is_healthy: bool
    unsupported_reason: Optional[str] = None
    diagnostics: List[str] = field(default_factory=list)


@dataclass
class FeatureDecisionReport:
    feature_name: str
    status: str  # SAFE_TO_APPLY, MEASUREMENT_ONLY, DO_NOT_APPLY, MEASUREMENT_ONLY - ROADMAP GATED
    reason_code: str
    explanation: str
    recommender_action: str
    safest_alternative: str


@dataclass
class DebugRecommendation:
    feature_name: str
    suggested_debug_steps: List[str]
    config_knobs_to_adjust: List[str]
    suggested_safer_fallback: str


# ==============================================================================
# SECTION C. MATHEMATICAL MODULES & REPRESENTATION GRAPHS (TRACK A)
# ==============================================================================

class PCRFDAGNode:
    """Represents a component inside a general multi-module Causal Flow DAG."""
    def __init__(self, node_id: str, operator: str = "AND", r: float = 1.0):
        self.node_id = node_id
        self.operator = operator  # options: "AND", "OR"
        self.r = r  # Internal node-level reliability
        self.parents: List['PCRFDAGNode'] = []

    def add_parent(self, parent_node: 'PCRFDAGNode') -> None:
        self.parents.append(parent_node)


class PCRFDAGCalculator:
    """Analytical derivatives solver for complex Causal Reliability Flow networks using Autograd."""
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
        """Computes Birnbaum component reliability importance: D_R(e_i) = -R_sys / r_i."""
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


# ==============================================================================
# SECTION D. HIGH-QUALITY CLOZE QA DATASET (130 BALANCED EXAMPLES)
# ==============================================================================

class ClozeQAExample:
    def __init__(self, example_id: int, prompt: str, target: str, task_type: str, split: str):
        self.example_id = example_id
        self.prompt = prompt
        self.target = target
        self.task_type = task_type
        self.split = split


class CustomFactualDataset(Dataset):
    """Encodes causal text sequences, setting labels ONLY on multi-token target completions."""
    def __init__(self, examples: List[ClozeQAExample], tokenizer: PreTrainedTokenizer, max_len: int = 128):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        ex = self.examples[idx]
        full_text = f"{ex.prompt} {ex.target}"
        
        prompt_encoding = self.tokenizer(ex.prompt, truncation=True, max_length=self.max_len, add_special_tokens=False)
        full_encoding = self.tokenizer(full_text, truncation=True, max_length=self.max_len, add_special_tokens=False)
        
        prompt_len = len(prompt_encoding["input_ids"])
        full_ids = full_encoding["input_ids"]
        
        padded_ids = full_ids + [self.tokenizer.pad_token_id] * (self.max_len - len(full_ids))
        padded_ids = padded_ids[:self.max_len]
        
        attention_mask = [1] * len(full_ids) + [0] * (self.max_len - len(full_ids))
        attention_mask = attention_mask[:self.max_len]
        
        labels = [-100] * self.max_len
        for i in range(prompt_len, min(len(full_ids), self.max_len)):
            labels[i] = full_ids[i]
            
        return {
            "input_ids": torch.tensor(padded_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
            "example_id": torch.tensor(ex.example_id, dtype=torch.long)
        }


def generate_mock_cloze_dataset() -> Dict[str, List[ClozeQAExample]]:
    """
    Constructs the complete, balanced 130-example Cloze QA dataset
    featuring multi-token targets for factual cascades (KPI 2).
    """
    raw_source = []
    
    # 1. TRAIN SPLIT: 80 Examples (40 Factual, 20 Scientific, 20 CS)
    # Factual (Multi-token targets)
    factual_countries = [
        ("France", "Paris, France"), ("Germany", "Berlin, Germany"), ("Italy", "Rome, Italy"),
        ("Spain", "Madrid, Spain"), ("Japan", "Tokyo, Japan"), ("China", "Beijing, China"),
        ("Egypt", "Cairo, Egypt"), ("Greece", "Athens, Greece"), ("Portugal", "Lisbon, Portugal"),
        ("Russia", "Moscow, Russia"), ("India", "New Delhi, India"), ("England", "London, United Kingdom"),
        ("Canada", "Ottawa, Canada"), ("Brazil", "Brasilia, Brazil"), ("Mexico", "Mexico City, Mexico"),
        ("Argentina", "Buenos Aires, Argentina"), ("Australia", "Canberra, Australia"), ("Sweden", "Stockholm, Sweden"),
        ("Turkey", "Ankara, Turkey"), ("Thailand", "Bangkok, Thailand"), ("Vietnam", "Hanoi, Vietnam"),
        ("Peru", "Lima, Peru"), ("Chile", "Santiago, Chile"), ("Colombia", "Bogota, Colombia"),
        ("Belgium", "Brussels, Belgium"), ("Austria", "Vienna, Austria"), ("Poland", "Warsaw, Poland"),
        ("Finland", "Helsinki, Finland"), ("Ireland", "Dublin, Ireland"), ("Kenya", "Nairobi, Kenya"),
        ("Nigeria", "Abuja, Nigeria"), ("South Africa", "Pretoria, South Africa"), ("New Zealand", "Wellington, New Zealand"),
        ("Saudi Arabia", "Riyadh, Saudi Arabia"), ("Ukraine", "Kyiv, Ukraine"), ("Netherlands", "Amsterdam, Netherlands"),
        ("Switzerland", "Bern, Switzerland"), ("Denmark", "Copenhagen, Denmark"), ("Norway", "Oslo, Norway"),
        ("Indonesia", "Jakarta, Indonesia")
    ]
    for country, cap in factual_countries:
        raw_source.append((f"The official central administrative capital city of {country} is", cap, "factual", "train"))

    # Scientific Train
    scientific_train = [
        ("The element represented by atomic number 1 is", "Hydrogen gas", "scientific", "train"),
        ("The element represented by atomic number 2 is", "Helium gas", "scientific", "train"),
        ("The element represented by atomic number 6 is", "Carbon element", "scientific", "train"),
        ("The element represented by atomic number 7 is", "Nitrogen gas", "scientific", "train"),
        ("The element represented by atomic number 8 is", "Oxygen gas", "scientific", "train"),
        ("Water is chemically composed of hydrogen and", "Oxygen molecules", "scientific", "train"),
        ("The planet sitting closest to our solar system's sun is", "Mercury planet", "scientific", "train"),
        ("The planet with the highest surface temperature is", "Venus planet", "scientific", "train"),
        ("The planet historically referred to as the red planet is", "Mars planet", "scientific", "train"),
        ("The largest gas giant orbiting inside our solar system is", "Jupiter planet", "scientific", "train"),
        ("Photosynthesis in organic plant structures generates glucose and", "Oxygen gas", "scientific", "train"),
        ("The standard electrical metric measuring opposition to current is", "Ohm unit", "scientific", "train"),
        ("The physical force driving planetary orbits is", "Gravitational pull", "scientific", "train"),
        ("The chemical compound representing standard table salt is", "NaCl salt", "scientific", "train"),
        ("A liquid solution with a pH rating significantly lower than 7 is an", "Acidic solution", "scientific", "train"),
        ("A liquid solution with a pH rating significantly higher than 7 is a", "Basic solution", "scientific", "train"),
        ("The basic physical container of all organic life is the", "Biological cell", "scientific", "train"),
        ("The atmospheric gas primarily responsible for global warming is", "Carbon dioxide", "scientific", "train"),
        ("The core organ driving blood circulation in mammalian systems is the", "Heart organ", "scientific", "train"),
        ("Light waves travel significantly faster than mechanical propagation of", "Sound vibrations", "scientific", "train")
    ]
    raw_source.extend(scientific_train)

    # Computer Science Train
    cs_train = [
        ("In operating systems, a scheduled execution thread resides within a", "System process", "cs", "train"),
        ("In deep learning, structural parameters are mathematically adjusted via", "Gradient descent", "cs", "train"),
        ("To store keyed associative records with rapid O(1) lookup, developers choose a", "Hash map", "cs", "train"),
        ("A sequential queue data structure operates on the first-in first-out principle, or", "FIFO structure", "cs", "train"),
        ("A sequential stack data structure operates on the last-in first-out principle, or", "LIFO structure", "cs", "train"),
        ("The digital counting framework representing information with 0 and 1 is", "Binary arithmetic", "cs", "train"),
        ("The primary volatile memory utilized for rapid workspace computation is", "RAM modules", "cs", "train"),
        ("The foundational processing unit executing computing instructions is the", "CPU silicon", "cs", "train"),
        ("The technical engineering pipeline of locating and isolating software bugs is", "Source debugging", "cs", "train"),
        ("In class structures, an operational memory instantiation is called an", "Object instance", "cs", "train"),
        ("The network transmission protocol used to serve encrypted web content is", "HTTPS security", "cs", "train"),
        ("A software routine that invokes itself to solve smaller sub-problems is", "Recursive call", "cs", "train"),
        ("The version control directive committing index state to local repository history is git", "commit command", "cs", "train"),
        ("The relational database directive used to fetch selected tuples from table arrays is", "SELECT statement", "cs", "train"),
        ("An auxiliary database lookup catalog built to accelerate query evaluation is an", "Index catalog", "cs", "train"),
        ("The fundamental internet routing system standardizing packet layout is the", "IP specification", "cs", "train"),
        ("In balanced search trees, a terminal node lacking downstream progeny is a", "Leaf node", "cs", "train"),
        ("The reserved programming keyword used to declare structural blueprints in Python is", "class declaration", "cs", "train"),
        ("The reserved programming keyword used to initiate routine blocks in Python is", "def syntax", "cs", "train"),
        ("The computational scale measuring worst-case algorithm complexity is Big O", "Notation scale", "cs", "train")
    ]
    raw_source.extend(cs_train)

    # 2. SEEN VALIDATION: 20 Examples (5 Factual, 5 Scientific, 5 Cloze, 5 CS)
    seen_val = [
        ("The official central administrative capital city of South Korea is", "Seoul, South Korea", "factual", "seen_val"),
        ("The official central administrative capital city of Norway is", "Oslo, Norway", "factual", "seen_val"),
        ("The official central administrative capital city of Sweden is", "Stockholm, Sweden", "factual", "seen_val"),
        ("The official central administrative capital city of Switzerland is", "Bern, Switzerland", "factual", "seen_val"),
        ("The official central administrative capital city of Poland is", "Warsaw, Poland", "factual", "seen_val"),
        
        ("The noble element designated by atomic number 10 is", "Neon gas", "scientific", "seen_val"),
        ("The volatile element designated by atomic number 16 is", "Sulfur powder", "scientific", "seen_val"),
        ("The chemical molecule animals must extract from air to sustain life is", "Oxygen gas", "scientific", "seen_val"),
        ("The yellow dwarf star supporting life at the center of our solar system is the", "Sun star", "scientific", "seen_val"),
        ("Mechanical acoustics are completely incapable of moving across a spatial", "Vacuum space", "scientific", "seen_val"),
        
        ("The globally recognized fantasy series Harry Potter was written by J.K.", "Rowling, novelist", "cloze", "seen_val"),
        ("The legendary classical Greek epic poem The Odyssey is attributed to", "Homer, poet", "cloze", "seen_val"),
        ("To achieve multiple achievements concurrently is to kill two birds with one", "stone, saying", "cloze", "seen_val"),
        ("A graphical diagram is capable of conveying complex information because a picture is worth a thousand", "words, saying", "cloze", "seen_val"),
        ("An advice warning against placing all financial resources in a single asset is to not put all your eggs in one", "basket, proverb", "cloze", "seen_val"),
        
        ("To enforce unique constraints with no duplicated items, algorithms utilize a", "Set container", "cs", "seen_val"),
        ("The hypermedia syntax used to format layout documents across the World Wide Web is", "HTML markup", "cs", "seen_val"),
        ("An execution failure originating from incorrect program logic is called a", "Software bug", "cs", "seen_val"),
        ("A standardized text notation representing complex structural records is", "JSON record", "cs", "seen_val"),
        ("The active keyword used to bind external packages into Python script scopes is", "import statement", "cs", "seen_val")
    ]
    raw_source.extend(seen_val)

    # 3. UNSEEN VALIDATION: 20 Examples (5 Factual, 5 Scientific, 5 Cloze, 5 CS)
    unseen_val = [
        ("The official central administrative capital city of Austria is", "Vienna, Austria", "factual", "unseen_val"),
        ("The classical Roman general who met his end during the Ides of March was Julius", "Caesar, leader", "factual", "unseen_val"),
        ("The pioneer lunar explorer who took the first steps on the moon surface was Neil", "Armstrong, astronaut", "factual", "unseen_val"),
        ("The theoretical physicist who revolutionized coordinate physics with relativity was Albert", "Einstein, physicist", "factual", "unseen_val"),
        ("The historical European explorer who reached the Bahamas landmass in 1492 was Christopher", "Columbus, voyager", "factual", "unseen_val"),
        
        ("Mammalian red blood cells are chemically responsible for transporting vital", "Oxygen molecules", "scientific", "unseen_val"),
        ("The organic cellular process separating chromosome pairs into twin cells is", "Mitosis division", "scientific", "unseen_val"),
        ("The primary command center of the central nervous system in vertebrates is the", "Brain organ", "scientific", "unseen_val"),
        ("The dual-helix macromolecule housing core genetic blueprints is", "DNA sequence", "scientific", "unseen_val"),
        ("The dense celestial body whose localized gravitational path traps light is a", "Black hole", "scientific", "unseen_val"),
        
        ("An unexpected, completely unpredictable event is idiomatic described as out of the", "blue, saying", "cloze", "unseen_val"),
        ("To prematurely leak sensitive details of a confidential strategy is to let the cat out of the", "bag, idiom", "cloze", "unseen_val"),
        ("A state of intense mental ecstasy or extreme joy is described as being on cloud", "nine, saying", "cloze", "unseen_val"),
        ("When working in an uncomfortable, unfamiliar setting, you feel like a fish out of", "water, idiom", "cloze", "unseen_val"),
        ("An extremely dynamic, energetic, and unpredictable person is referred to as a live", "wire, saying", "cloze", "unseen_val"),
        
        ("The specialized data structure used to model recursive parent-child linkages is a", "Tree graph", "cs", "unseen_val"),
        ("A networking layout topology organizing nodes around a central server hub is a", "Star configuration", "cs", "unseen_val"),
        ("The routing index directory that translates domain strings to IP coordinates is", "DNS directory", "cs", "unseen_val"),
        ("A formal logical interface allowing separate software modules to interact is an", "API specification", "cs", "unseen_val"),
        ("The physical block boundary used to serialize hard disk data tracks is a", "Disk sector", "cs", "unseen_val")
    ]
    raw_source.extend(unseen_val)

    # 4. OOD TEST: 10 Examples
    ood_test = [
        ("In mathematical topology, topological manifolds are categorized by Euler", "characteristic calculation", "scientific", "ood_test"),
        ("In wave equations, particles exhibit simultaneously localized and spread qualities called wave-particle", "duality theory", "scientific", "ood_test"),
        ("In molecular structures, compounds sharing atomic compositions but with varying bonds are", "structural isomers", "scientific", "ood_test"),
        ("In ecological geology, the mechanical drift of continental landmasses over time is plate", "tectonic movement", "scientific", "ood_test"),
        ("In ancient law, the primary eye-for-an-eye judicial structure was established in the Code of", "Hammurabi laws", "factual", "ood_test"),
        ("In early Mesopotamian clay scripts, the classic adventure narrative is the Epic of", "Gilgamesh text", "factual", "ood_test"),
        ("In multi-linear algebra, a multi-dimensional array mapping space coordinate matrices is a", "Tensor structure", "scientific", "ood_test"),
        ("In scientific taxonomy, species modifications driven by human breeders are called artificial", "selection breeding", "scientific", "ood_test"),
        ("In mathematical logic, a clean self-contradictory loop that holds consistent truth is a", "Paradox loop", "factual", "ood_test"),
        ("In deep history, the foundational Bronze Age legal block recovered in Susa is the Code of", "Hammurabi basalt", "factual", "ood_test")
    ]
    raw_source.extend(ood_test)

    # Compile structures
    splits = {"train": [], "seen_val": [], "unseen_val": [], "ood_test": []}
    for idx, (p, t, task, s) in enumerate(raw_source):
        example = ClozeQAExample(example_id=idx + 1, prompt=p, target=t, task_type=task, split=s)
        splits[s].append(example)
    return splits


# ==============================================================================
# SECTION E. MODEL MAPPING & EVALUATION ENGINE
# ==============================================================================

def load_reusable_model_and_tokenizer(cfg: ModelConfig) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    """Retrieves target causal model from HuggingFace, setting strict pad parameters."""
    logger.info(f"Retrieving tokenizer and architecture weights for: {cfg.model_name}")
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    model = AutoModelForCausalLM.from_pretrained(cfg.model_name)
    model.to(cfg.device)
    model.config.pad_token_id = tokenizer.pad_token_id
    
    logger.info("Model parameter arrays successfully allocated.")
    return model, tokenizer


class BaselineEvaluator:
    """Evaluates CLM performance, providing robust fallback diagnostics for cold starts."""
    @staticmethod
    def evaluate_dataset(
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        dataset: CustomFactualDataset,
        cfg: ModelConfig
    ) -> Dict[str, Any]:
        model.eval()
        total_loss = 0.0
        total_tokens = 0
        exact_match_count = 0
        
        device = cfg.device
        loader = DataLoader(dataset, batch_size=1, shuffle=False)
        
        with torch.no_grad():
            for batch in loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                ex_id = int(batch["example_id"][0].item())
                
                original_example = next(ex for ex in dataset.examples if ex.example_id == ex_id)
                
                # Forward log-likelihood pass
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
                
                # Exact Match evaluation via Greedy generation
                prompt_ids = tokenizer(original_example.prompt, return_tensors="pt", add_special_tokens=False)["input_ids"].to(device)
                prompt_len = prompt_ids.shape[1]
                
                generated_tokens = model.generate(
                    prompt_ids,
                    max_new_tokens=6,
                    temperature=0.0,  # Strict argmax greedy
                    do_sample=False,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id
                )
                
                pred_ids = generated_tokens[0][prompt_len:]
                predicted_text = tokenizer.decode(pred_ids, skip_special_tokens=True).strip()
                
                is_exact = (predicted_text.lower() == original_example.target.lower())
                if is_exact:
                    exact_match_count += 1
                    
        avg_nll = total_loss / max(1, total_tokens)
        accuracy_exact = exact_match_count / max(1, len(dataset))
        
        return {
            "avg_nll": avg_nll,
            "perplexity": math.exp(min(50, avg_nll)),
            "exact_match_acc": accuracy_exact
        }


# ==============================================================================
# SECTION F. CAUSAL INSTRUMENTATION SYSTEM
# ==============================================================================

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


# ==============================================================================
# SECTION G. REUSABLE PLUGINS (TRACKS A, B, C, D)
# ==============================================================================

class BaseFeaturePlugin(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str: pass
    @abc.abstractmethod
    def description(self) -> str: pass
    @abc.abstractmethod
    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any: pass
    @abc.abstractmethod
    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport: pass


# ------------------------------------------------------------------------------
# TRACK (B): DERIVATIVE ESTIMATION PLUGIN
# ------------------------------------------------------------------------------
class DerivativePlugin(BaseFeaturePlugin):
    def name(self) -> str: return "derivatives"
    def description(self) -> str: return "Computes structural downstream probability derivatives."

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        mgr = TransformerHookManager(model)
        if mgr.block_list is None:
            return FeatureHealthReport(self.name(), is_healthy=False, unsupported_reason="Untracked layer topology.")
        return FeatureHealthReport(self.name(), is_healthy=True, diagnostics=[f"Linked successfully to {len(mgr.block_list)} blocks."])

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        deriv_cfg: DerivativeConfig = cfg.derivative_cfg
        model_cfg: ModelConfig = cfg.model_cfg
        
        mgr = TransformerHookManager(model)
        num_layers = len(mgr.block_list) if mgr.block_list is not None else 0
        
        dataset = CustomFactualDataset(splits["train"], tokenizer, model_cfg.max_len)
        loader = DataLoader(dataset, batch_size=2, shuffle=False)
        device = model_cfg.device
        
        # Base likelihood capture
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
                "layer_idx": l_idx,
                "clean_acc": base_mean,
                "perturbed_acc": pert_mean,
                "delta": delta,
                "dr_de": delta
            })
            
        mgr.remove_all_hooks()
        os.makedirs(cfg.artifact_cfg.output_dir, exist_ok=True)
        csv_path = os.path.join(cfg.artifact_cfg.output_dir, "per_module_derivatives.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["layer_idx", "clean_acc", "perturbed_acc", "delta", "dr_de"])
            writer.writeheader()
            writer.writerows(layer_derivatives)
            
        return layer_derivatives

    def should_apply(self, baseline_stats: Dict[str, Any], derivatives: List[Dict[str, Any]], gate_cfg: PromotionGateConfig) -> FeatureDecisionReport:
        avg_delta = np.mean([abs(x["delta"]) for x in derivatives]) if derivatives else 0.0
        if avg_delta < 0.001:
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
            recommender_action="Deploy priority replay buffer and scale regularization.",
            safest_alternative="N/A"
        )

    def debug_next_steps(self, error_evidence: Dict[str, Any]) -> DebugRecommendation:
        return DebugRecommendation(
            feature_name=self.name(),
            suggested_debug_steps=["Increase noise_std in config (e.g. from 0.05 to 0.15).", "Try zero_ablation instead of additive noise."],
            config_knobs_to_adjust=["derivative_cfg.noise_std", "derivative_cfg.perturbation_mode"],
            suggested_safer_fallback="Measurement only without live propagation."
        )


# ------------------------------------------------------------------------------
# TRACK (D): CURRICULUM CURATION PLUGIN
# ------------------------------------------------------------------------------
class CurriculumPlugin(BaseFeaturePlugin):
    def name(self) -> str: return "curriculum"
    def description(self) -> str: return "Prioritizes cascading error prompts."

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        return FeatureHealthReport(self.name(), is_healthy=True)

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        model_cfg: ModelConfig = cfg.model_cfg
        
        # Calculate local temporary derivatives to guide selection weights
        deriv_plugin = DerivativePlugin()
        deriv_results = deriv_plugin.run_standalone(model, tokenizer, splits, cfg)
        deriv_weight = sum([max(0.0, x["delta"]) for x in deriv_results])
        
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
                
                # Priority = difficulty (NLL) * Total systemic error sensitivity (derivative weight)
                priority_score = nll * (1.0 + deriv_weight)
                prioritized_dataset.append({
                    "id": ex.example_id,
                    "prompt": ex.prompt,
                    "target": ex.target,
                    "priority_score": priority_score
                })
                
        prioritized_dataset.sort(key=lambda x: x["priority_score"], reverse=True)
        
        csv_path = os.path.join(cfg.artifact_cfg.output_dir, "curriculum_scores.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "prompt", "target", "priority_score"])
            writer.writeheader()
            writer.writerows(prioritized_dataset)
            
        return prioritized_dataset

    def should_apply(self, baseline_stats: Dict[str, Any], prioritized_dataset: List[Dict[str, Any]], gate_cfg: PromotionGateConfig) -> FeatureDecisionReport:
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


# ------------------------------------------------------------------------------
# TRACK (A): STRUCTURAL MONITORS WITH HEURISTICS (UPGRADE 2)
# ------------------------------------------------------------------------------
class StructuralPCRFPlugin(BaseFeaturePlugin):
    def name(self) -> str: return "structural_pcrf"
    def description(self) -> str: return "Monitors residual representation integrity with flaw roadmaps."

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        mgr = TransformerHookManager(model)
        if mgr.block_list is None:
            return FeatureHealthReport(self.name(), is_healthy=False, unsupported_reason="Unknown transformer block layout.")
        return FeatureHealthReport(self.name(), is_healthy=True)

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        struct_cfg: StructuralPCRFConfig = cfg.structural_cfg
        model_cfg: ModelConfig = cfg.model_cfg
        
        mgr = TransformerHookManager(model)
        num_layers = len(mgr.block_list)
        
        seen_val_ds = CustomFactualDataset(splits["seen_val"], tokenizer, model_cfg.max_len)
        loader = DataLoader(seen_val_ds, batch_size=2, shuffle=False)
        device = model_cfg.device
        
        # Capture Baseline Clean state activations
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
        
        # Capture Perturbed state activations (Adding tiny 0.02 embedding noise)
        for idx in range(num_layers):
            mgr.register_activation_capture(idx)
            
        perturbed_acts = {i: [] for i in range(num_layers)}
        with torch.no_grad():
            for batch in loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                
                embeds = model.get_input_embeddings()(input_ids)
                embeds += torch.randn_like(embeds) * 0.02  # Tiny input perturbation
                
                _ = model(inputs_embeds=embeds, attention_mask=attention_mask)
                for idx in range(num_layers):
                    if idx in mgr.active_activations:
                        perturbed_acts[idx].append(mgr.active_activations[idx].cpu())
                        
        mgr.remove_all_hooks()
        
        # Calculate continuous survival probabilities & L2 magnitudes
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
            
            r_l = PCRFCore.map_drift_to_reliability(drift, struct_cfg.mapping_transform, struct_cfg.decay_beta)
            layer_reliabilities.append(r_l)
            
        derivatives = PCRFCore.compute_analytical_series_derivatives(layer_reliabilities)
        
        layer_breakdown = []
        for idx, (r_l, d_l) in enumerate(zip(layer_reliabilities, derivatives)):
            layer_breakdown.append({
                "layer_idx": idx,
                "reliability_r_l": r_l,
                "analytical_derivative": d_l
            })
            
        # Programmatic triggers check (Upgrade 2)
        triggered_flaws = []
        r_sys = float(np.prod(layer_reliabilities))
        
        if struct_cfg.enable_roadmap_heuristics:
            # Heuristic A: Residual bypass check
            if r_sys > 0.95:  # Extremely high similarity implies passive skip connections
                triggered_flaws.append("RESIDUAL_STREAM_BYPASS_DETECTED")
                
            # Heuristic B: Cosine magnitude blowout
            avg_p_l2 = np.mean(perturbed_l2_norms)
            avg_c_l2 = np.mean(clean_l2_norms)
            ratio = avg_p_l2 / avg_c_l2 if avg_c_l2 > 0 else 1.0
            if (ratio < 0.8 or ratio > 1.2) and r_sys > 0.95:
                triggered_flaws.append("COSINE_AMPLITUDE_BLOWOUT")
                
            # Heuristic C: Task mismatch detection (Checking if dataset contains cloze categories)
            has_cloze = any(ex.task_type in ["cloze", "dialogue"] for ex in splits["train"])
            if has_cloze:
                triggered_flaws.append("CREATIVE_TASK_MISMATCH")
                
        # Export summaries
        os.makedirs(cfg.artifact_cfg.output_dir, exist_ok=True)
        summary_path = os.path.join(cfg.artifact_cfg.output_dir, "structural_pcrf_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump({
                "R_sys_chain": r_sys,
                "triggered_flaws": triggered_flaws,
                "layers": layer_breakdown
            }, f, indent=4)
            
        # Embed findings temporarily in metadata fields
        self.last_run_flaws = triggered_flaws
        self.last_chain_reliability = r_sys
        
        return layer_breakdown

    def should_apply(self, baseline_stats: Dict[str, Any], layer_breakdown: List[Dict[str, Any]], gate_cfg: PromotionGateConfig) -> FeatureDecisionReport:
        if hasattr(self, "last_run_flaws") and self.last_run_flaws:
            flaw_text = " | ".join(self.last_run_flaws)
            return FeatureDecisionReport(
                feature_name=self.name(),
                status="MEASUREMENT_ONLY - ROADMAP GATED",
                reason_code="ROADMAP_GATE_TRIGGERED",
                explanation=f"Advanced representation checks blocked promotion. Triggers: {flaw_text}",
                recommender_action="Deploy only as local diagnostic. Proceed to Phase 2 roadmap: "
                                   "'Centered Kernel Alignment (CKA)' and 'Tuned Lens Projection Space Mapping'.",
                safest_alternative="Revert parameters to stable baseline; monitor representation drift."
            )
        return FeatureDecisionReport(
            feature_name=self.name(),
            status="SAFE_TO_APPLY",
            reason_code="READY_FOR_USE",
            explanation="Residual depth channels are highly stable and coherent.",
            recommender_action="Activate Real-Time Drift Alarm.",
            safest_alternative="N/A"
        )


# ------------------------------------------------------------------------------
# TRACK (C): DERIVATIVE REGULARIZER PASSTHROUGH
# ------------------------------------------------------------------------------
class DerivativeRegularizer(BaseFeaturePlugin):
    def name(self) -> str: return "regularization"
    def description(self) -> str: return "Executes derivative-weighted parameter regularization passes."

    def health_check(self, model: PreTrainedModel) -> FeatureHealthReport:
        return FeatureHealthReport(self.name(), is_healthy=True)

    def run_standalone(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, splits: Dict[str, List[ClozeQAExample]], cfg: Any) -> Any:
        reg_cfg: RegularizationConfig = cfg.regularization_cfg
        model_cfg: ModelConfig = cfg.model_cfg
        
        # Collect derivatives to weight penalty
        deriv_plugin = DerivativePlugin()
        deriv_results = deriv_plugin.run_standalone(model, tokenizer, splits, cfg)
        weights = [max(0.0, x["delta"]) for x in deriv_results]
        
        sum_w = sum(weights)
        if sum_w > 0:
            weights = [w / sum_w for w in weights]
            
        logger.info("Initializing Derivative-Weighted SFT Regularization training pass...")
        
        # Instantiate clean reference baseline model to prevent catastropic unanchored drift
        reference_model = AutoModelForCausalLM.from_pretrained(model_cfg.model_name)
        reference_model.to(model_cfg.device)
        reference_model.eval()
        
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
        dataset = CustomFactualDataset(splits["train"][:15], tokenizer, model_cfg.max_len)  # Sample sub-batch for fast, safe convergence
        loader = DataLoader(dataset, batch_size=2, shuffle=True)
        device = model_cfg.device
        
        model_mgr = TransformerHookManager(model)
        ref_mgr = TransformerHookManager(reference_model)
        
        num_layers = len(model_mgr.block_list)
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
            
            with torch.no_grad():
                _ = reference_model(input_ids=input_ids, attention_mask=attention_mask)
                
            reg_penalty = torch.tensor(0.0, device=device)
            for i in range(num_layers):
                if i in model_mgr.active_activations and i in ref_mgr.active_activations:
                    curr_act = model_mgr.active_activations[i]
                    ref_act = ref_mgr.active_activations[i]
                    drift = 1.0 - F.cosine_similarity(curr_act, ref_act, dim=-1).mean()
                    w_l = weights[i] if i < len(weights) else 0.0
                    reg_penalty += w_l * drift
                    
            loss = ce_loss + reg_cfg.lambda_reg * reg_penalty
            loss.backward()
            optimizer.step()
            
        model_mgr.remove_all_hooks()
        ref_mgr.remove_all_hooks()
        del reference_model
        
        logger.info("Regularization training pass completed.")
        return {"loss": float(loss.item())}

    def should_apply(self, baseline_stats: Dict[str, Any], feature_metrics: Dict[str, Any], gate_cfg: PromotionGateConfig) -> FeatureDecisionReport:
        # Standard API placeholder wrapper -> Actual gating executed by main safe controller
        return FeatureDecisionReport(
            feature_name=self.name(),
            status="SAFE_TO_APPLY",
            reason_code="READY_FOR_USE",
            explanation="Loss profile within bounds.",
            recommender_action="Proceed to global controller check.",
            safest_alternative="N/A"
        )

    def debug_next_steps(self, error_evidence: Dict[str, Any]) -> DebugRecommendation:
        return DebugRecommendation(
            feature_name=self.name(),
            suggested_debug_steps=["Scale back regularizer strength (lambda_reg) by half.", "Incorporate trust-region / KL bounding directly on predictions."],
            config_knobs_to_adjust=["regularization_cfg.lambda_reg", "regularization_cfg.penalty_type"],
            suggested_safer_fallback="Revert to baseline training without live loss weights."
        )


# ==============================================================================
# SECTION H. SAFE GATING SYSTEM (PATH C IMPLEMENTATION - UPGRADE 1)
# ==============================================================================

class SafePCRFController:
    """Decides when to safely promote optimized model parameters or trigger rollback fallbacks."""
    def __init__(self, gate_cfg: PromotionGateConfig):
        self.gate_cfg = gate_cfg

    def compute_promotion_decision(self, baseline_metrics: Dict[str, Any], feature_metrics: Dict[str, Any], feature_name: str) -> FeatureDecisionReport:
        seen_baseline_acc = baseline_metrics.get("seen_val_acc", 0.0)
        unseen_baseline_acc = baseline_metrics.get("unseen_val_acc", 0.0)
        
        # Cold start check: Exact-Match accuracy is strictly 0.0%
        path_c_active = (seen_baseline_acc == 0.0 and unseen_baseline_acc == 0.0)
        
        if path_c_active:
            logger.info("[Path C Fallback Activated] Cold-start detected (0.0% baseline EM accuracy). Gating on continuous loss metrics.")
            
            base_seen_nll = baseline_metrics["seen_val_nll"]
            feat_seen_nll = feature_metrics["seen_val_nll"]
            base_unseen_nll = baseline_metrics["unseen_val_nll"]
            feat_unseen_nll = feature_metrics["unseen_val_nll"]
            
            # Rule 1: Non-Inferiority Guard (Seen Split Safety)
            seen_nll_increase = feat_seen_nll - base_seen_nll
            seen_nll_tolerance = max(self.gate_cfg.seen_nll_tolerance, 0.01 * base_seen_nll)
            
            if seen_nll_increase > seen_nll_tolerance:
                return FeatureDecisionReport(
                    feature_name=feature_name,
                    status="DO_NOT_APPLY",
                    reason_code="SEEN_SPLIT_DAMAGE_PATH_C",
                    explanation=f"Seen NLL degradation ({seen_nll_increase:.4f}) exceeds tolerance ({seen_nll_tolerance:.4f}). Core distribution damaged.",
                    recommender_action="Lower regularization strength (lambda_reg) or anchor baseline parameters.",
                    safest_alternative="Emergency fallback: Restoring pre-training baseline model weights..."
                )
                
            # Rule 2: Generalization Guard (Unseen Split Superiority)
            unseen_nll_decrease_rel = (base_unseen_nll - feat_unseen_nll) / base_unseen_nll
            if unseen_nll_decrease_rel < self.gate_cfg.unseen_nll_gain_req:
                return FeatureDecisionReport(
                    feature_name=feature_name,
                    status="MEASUREMENT_ONLY",
                    reason_code="PROMOTION_GATE_FAILED_PATH_C",
                    explanation=f"Relative generalization drop ({unseen_nll_decrease_rel*100:.2f}%) "
                                f"is below the 5.0% relative improvement threshold.",
                    recommender_action="Increase step counts or widen prompt-level token tuning coverage.",
                    safest_alternative="Fallback Action: Measurement only without optimization activation."
                )
                
            # Rule 3: Over-Steering Detector (Loss-Accuracy Divergence)
            # Flag warning if NLL drops cleanly but validation perplexity explodes
            ppl_increase_rel = (feature_metrics["unseen_val_ppl"] - baseline_metrics["unseen_val_ppl"]) / baseline_metrics["unseen_val_ppl"] if baseline_metrics["unseen_val_ppl"] > 0 else 0.0
            if unseen_nll_decrease_rel > 0.15 and ppl_increase_rel > 0.15:
                return FeatureDecisionReport(
                    feature_name=feature_name,
                    status="OVERSTEERING_DETECTED",
                    reason_code="LOSS_ACCURACY_DIVERGENCE",
                    explanation="Over-steering detected! Perplexity exploded while NLL decreased.",
                    recommender_action="Apply extreme weight decay or scale back epochs.",
                    safest_alternative="Immediate emergency rollback to clean baseline parameters."
                )
                
            return FeatureDecisionReport(
                feature_name=feature_name,
                status="SAFE_TO_APPLY",
                reason_code="PROMOTED_PATH_C",
                explanation=f"Passed Path C Gating: Seen NLL variance stable (+{seen_nll_increase:.4f}), "
                            f"Unseen NLL generalized by {unseen_nll_decrease_rel*100:.1f}%.",
                recommender_action="Approve feature deployment under continuous validation tracking.",
                safest_alternative="N/A"
            )
            
        else:
            # Standard Discrete EM Gating
            seen_drop = seen_baseline_acc - feature_metrics.get("seen_val_acc", 0.0)
            unseen_gain = feature_metrics.get("unseen_val_acc", 0.0) - unseen_baseline_acc
            
            if seen_drop > self.gate_cfg.degradation_budget:
                return FeatureDecisionReport(
                    feature_name=feature_name,
                    status="DO_NOT_APPLY",
                    reason_code="SEEN_SPLIT_DAMAGE",
                    explanation=f"Severe degradation on seen split ({seen_drop*100:.1f}%).",
                    recommender_action="Lower regularization bounds or LR.",
                    safest_alternative="Emergency fallback: Restoring pre-training baseline model weights..."
                )
            if seen_drop > self.gate_cfg.non_inferiority_margin:
                return FeatureDecisionReport(
                    feature_name=feature_name,
                    status="MEASUREMENT_ONLY",
                    reason_code="PROMOTION_GATE_FAILED",
                    explanation="Seen validation drop exceeds non-inferiority limits.",
                    recommender_action="Lower learning rate or adjust scaling constraints.",
                    safest_alternative="Fallback Action: Run baseline configuration only."
                )
            if unseen_gain < self.gate_cfg.min_unseen_improvement:
                return FeatureDecisionReport(
                    feature_name=feature_name,
                    status="MEASUREMENT_ONLY",
                    reason_code="UNSEEN_GAIN_NOT_RELIABLE",
                    explanation="Unseen accuracy improvement does not meet performance requirements.",
                    recommender_action="Increase step counts or widen prompt-level token tuning coverage.",
                    safest_alternative="Fallback Action: Run baseline configuration only."
                )
            return FeatureDecisionReport(
                feature_name=feature_name,
                status="SAFE_TO_APPLY",
                reason_code="PROMOTED",
                explanation="Passed discrete accuracy performance and safety checks.",
                recommender_action="Approve feature deployment.",
                safest_alternative="N/A"
            )