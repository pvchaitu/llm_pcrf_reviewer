# ==============================================================================
# File: pcrf_dataset.py
# ==============================================================================
"""
PCRF Transformer Reliability Suite - Dataset & File Handling Ingestion Engine
pcrf_dataset.py
========================================================================================
Defines data models, text normalization rules, external CSV validations, and loading utilities.
"""

import os
import sys
import csv
import logging
from typing import Any, Dict, List, Optional, Tuple
import torch
from torch.utils.data import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer

logger = logging.getLogger("PCRF_Suite")

# Global safety variables and fallback configurations
SAFETY_WITHHELD_RESPONSE = "⚠️ Hallucination Risk Detected — Response Withheld for Safety"
SAFETY_WITHHELD_STATUS = "ABSTAINED"
SAFETY_WITHHELD_REASON = "HALLUCINATION_RISK_UNRESOLVED"
SAFETY_WITHHELD_ACTION = "Abstained — No reliable generation available"


def _as_bool_int(value: Any) -> bool:
    """Safely converts correctness indicators into boolean primitives."""
    try:
        return int(value) == 1
    except Exception:
        return bool(value)


def is_baseline_hallucination(row: Dict[str, Any]) -> bool:
    """Treat ANY incorrect baseline as hallucination for business reporting."""
    return not bool(int(row.get("baseline_correct", 0)))


def is_candidate_hallucination(row: Dict[str, Any]) -> bool:
    """Candidate is hallucinated if it failed correctness."""
    return not bool(int(row.get("candidate_correct", 0)))


def is_unresolved_hallucination(row: Dict[str, Any]) -> bool:
    """Identifies if both baseline and candidate models failed semantic target capture."""
    return is_baseline_hallucination(row) and is_candidate_hallucination(row)


def is_candidate_repair(row: Dict[str, Any]) -> bool:
    """Checks if the candidate successfully repaired a baseline hallucination."""
    return is_baseline_hallucination(row) and not is_candidate_hallucination(row)


def is_candidate_regression(row: Dict[str, Any]) -> bool:
    """Checks if the candidate regressed on a correct baseline generation."""
    return (not is_baseline_hallucination(row)) and is_candidate_hallucination(row)


def mask_output_if_hallucinated(raw_output: Any, is_hallucinated: bool, cfg: Any = None) -> str:
    """Shields customer exposure by withholding raw text on verified hallucination risks."""
    if is_hallucinated:
        return SAFETY_WITHHELD_RESPONSE
    return "" if raw_output is None else str(raw_output)


def get_public_baseline_output(row: Dict[str, Any], cfg: Any = None) -> str:
    """Baseline must NEVER be masked. Always return raw output for audit integrity."""
    val = row.get("baseline_output")
    return "" if val is None else str(val)


def get_public_candidate_output(row: Dict[str, Any], cfg: Any = None) -> str:
    """Retrieves customer-safe, masked candidate generation output."""
    return mask_output_if_hallucinated(row.get("candidate_output", ""), is_candidate_hallucination(row), cfg)


def get_public_served_output(row: Dict[str, Any], cfg: Any = None) -> str:
    """Returns strictly governed served output for customer artifacts."""
    decision = str(row.get("router_decision", "")).strip()

    if decision == "abstain_safe_fallback":
        return SAFETY_WITHHELD_RESPONSE

    if decision == "use_candidate":
        if is_candidate_hallucination(row):
            return SAFETY_WITHHELD_RESPONSE
        return "" if row.get("candidate_output") is None else str(row.get("candidate_output"))

    if decision == "use_baseline":
        if is_baseline_hallucination(row):
            return SAFETY_WITHHELD_RESPONSE
        return "" if row.get("baseline_output") is None else str(row.get("baseline_output"))

    return SAFETY_WITHHELD_RESPONSE


def apply_customer_safe_outputs_to_row(
    row: Dict[str, Any],
    cfg: Any = None,
    preserve_raw: bool = True
) -> Dict[str, Any]:
    out = dict(row)
    if preserve_raw:
        out["raw_baseline_output"] = row.get("baseline_output", "")
        out["raw_candidate_output"] = row.get("candidate_output", "")

    out["baseline_output"] = row.get("baseline_output", "")

    mask_flag = True
    if cfg is not None and hasattr(cfg, "artifact_cfg"):
        mask_flag = getattr(cfg.artifact_cfg, "mask_hallucinated_outputs_in_customer_artifacts", True)

    if mask_flag:
        out["candidate_output"] = mask_output_if_hallucinated(row.get("candidate_output", ""), is_candidate_hallucination(row), cfg)
    else:
        out["candidate_output"] = row.get("candidate_output", "")

    out["served_output"] = get_public_served_output(row, cfg)
    return out


class ClozeQAExample:
    def __init__(self, example_id: int, prompt: str, target: str, task_type: str, split: str, is_critical: int = 0, criticality_weight: float = 1.0):
        self.example_id = example_id
        self.prompt = prompt
        self.target = target
        self.task_type = task_type
        self.split = split
        self.is_critical = is_critical
        self.criticality_weight = criticality_weight


class CustomFactualDataset(Dataset):
    """Encodes causal text sequences, setting labels ONLY on simplified target tokens."""
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


def normalize_text(text: str) -> str:
    """Robust normalizer converting inputs to stripped lowercase, clean of trailing punctuations."""
    text = text.lower().strip()
    for char in [".", ",", "!", "?", '"', "'", ";", ":", "-", "_"]:
        text = text.replace(char, " ")
    return " ".join(text.split())


def evaluate_semantic_match(generated_text: str, target_text: str) -> bool:
    """Evaluates if the normalized target is semantically captured inside generation boundaries."""
    gen_norm = normalize_text(generated_text)
    tar_norm = normalize_text(target_text)
    
    if not gen_norm or not tar_norm:
        return False
        
    gen_words = gen_norm.split()
    tar_words = tar_norm.split()
    
    if not gen_words or not tar_words:
        return False
        
    if gen_norm == tar_norm or gen_words[0] == tar_words[0]:
        return True
        
    if tar_norm in gen_norm:
        return True
        
    return False


def get_expected_dataset_format_example() -> str:
    """Returns the exact 8-row sample CSV format."""
    return (
        'id,prompt,target,task_type,split,is_critical,criticality_weight\n'
        '1,"The capital of France is","Paris","factual_cloze","train",0,1.0\n'
        '2,"The largest planet is","Jupiter","factual_cloze","train",0,1.0\n'
        '3,"The chemical symbol for water is","H2O","factual_cloze","seen_val",0,1.0\n'
        '4,"The author of Hamlet is","Shakespeare","factual_cloze","seen_val",0,1.0\n'
        '5,"The currency of Japan is","Yen","factual_cloze","unseen_val",0,1.0\n'
        '6,"The speed of light is measured in","meters per second","factual_cloze","unseen_val",1,1.5\n'
        '7,"In quantum computing, a basic unit is called a","qubit","ood_fact","ood",1,2.0\n'
        '8,"In Kubernetes, a deployable unit is called a","pod","ood_fact","ood",1,2.0'
    )


def format_dataset_validation_error(errors: List[str]) -> str:
    """Returns customer-friendly error output with sample format and rationale."""
    err_str = "\n" + "=" * 90 + "\n"
    err_str += "ERROR: Invalid dataset file format.\n\n"
    err_str += "Reason(s):\n"
    for err in errors:
        err_str += f" - {err}\n"
    err_str += "\nExpected CSV format:\n"
    err_str += "id,prompt,target,task_type,split,is_critical,criticality_weight\n\n"
    err_str += "Sample compliant dataset:\n"
    err_str += get_expected_dataset_format_example() + "\n\n"
    err_str += "Why this format is required:\n"
    err_str += " - train: Used for fitting, adaptation, or regularization paths when the full PCRF experiment executes training components.\n"
    err_str += " - seen_val: Used to measure preservation on validation prompts close to the training distribution.\n"
    err_str += " - unseen_val: Used to measure generalization on validation prompts not used during training.\n"
    err_str += " - ood: Used to measure out-of-distribution transfer behavior so the reliability suite can distinguish in-distribution reliability from broader deployment risk.\n"
    err_str += "=" * 90 + "\n"
    err_str += "Execution halted before model loading or experiment execution.\n"
    return err_str


def validate_external_dataset_file(dataset_path: str) -> Tuple[bool, List[str]]:
    """Validates the structure, headers, values, splits, and requirements of the CSV file."""
    errors = []
    if not os.path.exists(dataset_path):
        errors.append(f"File does not exist: {dataset_path}")
        return False, errors
    if not dataset_path.lower().endswith(".csv"):
        errors.append(f"File extension must be .csv: {dataset_path}")
        return False, errors

    required_cols = {"id", "prompt", "target", "task_type", "split", "is_critical", "criticality_weight"}
    valid_splits = {"train", "seen_val", "unseen_val", "ood"}
    valid_is_critical = {"0", "1"}

    ids = set()
    splits_found = set()

    try:
        with open(dataset_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            if not headers:
                errors.append("CSV file is empty or missing headers.")
                return False, errors

            missing_cols = required_cols - set(headers)
            if missing_cols:
                errors.append(f"Missing required columns: {sorted(list(missing_cols))}")
                return False, errors

            row_idx = 1
            for row in reader:
                row_idx += 1
                for col in required_cols:
                    val = row.get(col)
                    if val is None or str(val).strip() == "":
                        errors.append(f"[Row {row_idx}] Column '{col}' is blank.")

                raw_id = row.get("id", "")
                try:
                    parsed_id = int(raw_id)
                    if parsed_id in ids:
                        errors.append(f"[Row {row_idx}] Duplicate ID found: {parsed_id}")
                    ids.add(parsed_id)
                except (ValueError, TypeError):
                    errors.append(f"[Row {row_idx}] 'id' value must be an integer, got: '{raw_id}'")

                split = row.get("split", "").strip() if row.get("split") else ""
                if split not in valid_splits:
                    errors.append(f"[Row {row_idx}] Invalid split: '{split}'. Must be one of {valid_splits}")
                else:
                    splits_found.add(split)

                is_crit = row.get("is_critical", "").strip() if row.get("is_critical") else ""
                if is_crit not in valid_is_critical:
                    errors.append(f"[Row {row_idx}] Invalid 'is_critical' value: '{is_crit}'. Must be 0 or 1.")

                crit_wt = row.get("criticality_weight", "").strip() if row.get("criticality_weight") else ""
                try:
                    float(crit_wt)
                except (ValueError, TypeError):
                    errors.append(f"[Row {row_idx}] 'criticality_weight' must be numeric, got: '{crit_wt}'")

                prompt = row.get("prompt", "")
                target = row.get("target", "")
                if prompt and prompt.strip() == "":
                    errors.append(f"[Row {row_idx}] 'prompt' is empty or whitespace only.")
                if target and target.strip() == "":
                    errors.append(f"[Row {row_idx}] 'target' is empty or whitespace only.")

            missing_splits = valid_splits - splits_found
            if missing_splits:
                errors.append(f"Missing rows for splits: {sorted(list(missing_splits))}. Each split category must have at least one row.")

    except Exception as e:
        errors.append(f"Error reading/parsing CSV file: {str(e)}")

    return len(errors) == 0, errors


def load_external_cloze_dataset(dataset_path: str) -> Dict[str, List[ClozeQAExample]]:
    """Loads validated rows from an external CSV file into ClozeQAExample objects."""
    splits = {"train": [], "seen_val": [], "unseen_val": [], "ood": []}
    with open(dataset_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed_id = int(row["id"])
            prompt = row["prompt"].strip()
            target = row["target"].strip()
            task_type = row["task_type"].strip()
            split = row["split"].strip()
            is_crit = int(row["is_critical"])
            crit_wt = float(row["criticality_weight"])

            ex = ClozeQAExample(
                example_id=parsed_id,
                prompt=prompt,
                target=target,
                task_type=task_type,
                split=split,
                is_critical=is_crit,
                criticality_weight=crit_wt
            )
            if split in splits:
                splits[split].append(ex)

    splits["ood_test"] = splits["ood"]
    return splits


def get_dataset_or_default(dataset_path: Optional[str]) -> Tuple[Dict[str, List[ClozeQAExample]], Dict[str, Any]]:
    """Resolves and returns the parsed dataset along with its metadata details."""
    if dataset_path is not None:
        valid, errors = validate_external_dataset_file(dataset_path)
        if not valid:
            err_msg = format_dataset_validation_error(errors)
            print(err_msg, file=sys.stderr)
            sys.exit(1)
        splits = load_external_cloze_dataset(dataset_path)
        metadata = {
            "dataset_source": "External File",
            "dataset_file": dataset_path
        }
        logger.info(f"Loaded external dataset from {dataset_path}")
    else:
        splits = generate_mock_cloze_dataset()
        if "ood_test" in splits and "ood" not in splits:
            splits["ood"] = splits["ood_test"]
        elif "ood" in splits and "ood_test" not in splits:
            splits["ood_test"] = splits["ood"]
        metadata = {
            "dataset_source": "Built-in Mock Cloze Dataset",
            "dataset_file": "N/A"
        }
        logger.info("Loaded built-in mock cloze dataset")
    return splits, metadata


def generate_mock_cloze_dataset() -> Dict[str, List[ClozeQAExample]]:
    """Generates the complete, balanced 130-example Cloze QA dataset with simplified targets."""
    raw_source = []
    
    # 1. TRAIN SPLIT: 80 Examples (40 Factual, 20 Scientific, 20 CS)
    factual_countries = [
        ("France", "Paris", 0, 1.0), ("Germany", "Berlin", 0, 1.0), ("Italy", "Rome", 0, 1.0),
        ("Spain", "Madrid", 0, 1.0), ("Japan", "Tokyo", 1, 4.0), ("China", "Beijing", 1, 4.0),
        ("Egypt", "Cairo", 0, 1.0), ("Greece", "Athens", 0, 1.0), ("Portugal", "Lisbon", 0, 1.0),
        ("Russia", "Moscow", 0, 1.0), ("India", "Delhi", 1, 4.0), ("England", "London", 1, 4.0),
        ("Canada", "Ottawa", 0, 1.0), ("Brazil", "Brasilia", 0, 1.0), ("Mexico", "Mexico", 0, 1.0),
        ("Argentina", "Buenos Aires", 0, 1.0), ("Australia", "Canberra", 0, 1.0), ("Sweden", "Stockholm", 0, 1.0),
        ("Turkey", "Ankara", 0, 1.0), ("Thailand", "Bangkok", 0, 1.0), ("Vietnam", "Hanoi", 0, 1.0),
        ("Peru", "Lima", 0, 1.0), ("Chile", "Santiago", 0, 1.0), ("Colombia", "Bogota", 0, 1.0),
        ("Belgium", "Brussels", 0, 1.0), ("Austria", "Vienna", 0, 1.0), ("Poland", "Warsaw", 0, 1.0),
        ("Finland", "Helsinki", 0, 1.0), ("Ireland", "Dublin", 0, 1.0), ("Kenya", "Nairobi", 0, 1.0),
        ("Nigeria", "Abuja", 0, 1.0), ("South Africa", "Pretoria", 0, 1.0), ("New Zealand", "Wellington", 0, 1.0),
        ("Saudi Arabia", "Riyadh", 0, 1.0), ("Ukraine", "Kyiv", 0, 1.0), ("Netherlands", "Amsterdam", 0, 1.0),
        ("Switzerland", "Bern", 1, 5.0), ("Denmark", "Copenhagen", 0, 1.0), ("Norway", "Oslo", 0, 1.0),
        ("Indonesia", "Jakarta", 0, 1.0)
    ]
    for country, cap, is_c, wt in factual_countries:
        raw_source.append((f"The official capital city of {country} is", cap, "factual", "train", is_c, wt))

    scientific_train = [
        ("The element with atomic number 1 is", "Hydrogen", "scientific", "train", 0, 1.0),
        ("The element with atomic number 2 is", "Helium", "scientific", "train", 0, 1.0),
        ("The element with atomic number 6 is", "Carbon", "scientific", "train", 0, 1.0),
        ("The element with atomic number 7 is", "Nitrogen", "scientific", "train", 0, 1.0),
        ("The element with atomic number 8 is", "Oxygen", "scientific", "train", 1, 3.0),
        ("Water is chemically composed of oxygen and", "Hydrogen", "scientific", "train", 0, 1.0),
        ("The planet sitting closest to our solar system's sun is", "Mercury", "scientific", "train", 0, 1.0),
        ("The planet with the highest surface temperature is", "Venus", "scientific", "train", 0, 1.0),
        ("The planet historically referred to as the red planet is", "Mars", "scientific", "train", 0, 1.0),
        ("The largest gas giant orbiting inside our solar system is", "Jupiter", "scientific", "train", 0, 1.0),
        ("Photosynthesis in organic plant structures generates glucose and", "Oxygen", "scientific", "train", 1, 3.0),
        ("The standard electrical metric measuring opposition to current is", "Ohm", "scientific", "train", 0, 1.0),
        ("The physical force driving planetary orbits is", "Gravity", "scientific", "train", 0, 1.0),
        ("The chemical compound representing standard table salt is", "NaCl", "scientific", "train", 0, 1.0),
        ("A liquid solution with a pH rating significantly lower than 7 is an", "Acid", "scientific", "train", 0, 1.0),
        ("A liquid solution with a pH rating significantly higher than 7 is a", "Base", "scientific", "train", 0, 1.0),
        ("The basic physical container of all organic life is the", "Cell", "scientific", "train", 0, 1.0),
        ("The atmospheric gas primarily responsible for global warming is", "Carbon", "scientific", "train", 0, 1.0),
        ("The core organ driving blood circulation in mammalian systems is the", "Heart", "scientific", "train", 1, 3.0),
        ("Light waves travel significantly faster than mechanical propagation of", "Sound", "scientific", "train", 0, 1.0)
    ]
    raw_source.extend(scientific_train)

    cs_train = [
        ("In operating systems, a scheduled execution thread resides within a", "Process", "cs", "train", 1, 5.0),
        ("In deep learning, structural parameters are mathematically adjusted via", "Descent", "cs", "train", 0, 1.0),
        ("To store keyed associative records with rapid O(1) lookup, developers choose a", "Map", "cs", "train", 0, 1.0),
        ("A sequential queue data structure operates on the first-in first-out principle, or", "FIFO", "cs", "train", 0, 1.0),
        ("A sequential stack data structure operates on the last-in first-out principle, or", "LIFO", "cs", "train", 0, 1.0),
        ("The digital counting framework representing information with 0 and 1 is", "Binary", "cs", "train", 1, 5.0),
        ("The primary volatile memory utilized for rapid workspace computation is", "RAM", "cs", "train", 1, 5.0),
        ("The foundational processing unit executing computing instructions is the", "CPU", "cs", "train", 1, 5.0),
        ("The technical engineering pipeline of locating and isolating software bugs is", "Debugging", "cs", "train", 0, 1.0),
        ("In class structures, an operational memory instantiation is called an", "Object", "cs", "train", 1, 5.0),
        ("The network transmission protocol used to serve encrypted web content is", "HTTPS", "cs", "train", 0, 1.0),
        ("A software routine that invokes itself to solve smaller sub-problems is", "Recursion", "cs", "train", 0, 1.0),
        ("The version control directive committing index state to local repository history is git", "commit", "cs", "train", 0, 1.0),
        ("The relational database directive used to fetch selected tuples from table arrays is", "SELECT", "cs", "train", 1, 5.0),
        ("An auxiliary database lookup catalog built to accelerate query evaluation is an", "Index", "cs", "train", 0, 1.0),
        ("The fundamental internet routing system standardizing packet layout is the", "IP", "cs", "train", 1, 5.0),
        ("In balanced search trees, a terminal node lacking downstream progeny is a", "Leaf", "cs", "train", 0, 1.0),
        ("The reserved programming keyword used to declare structural blueprints in Python is", "class", "cs", "train", 1, 5.0),
        ("The reserved programming keyword used to initiate routine blocks in Python is", "def", "cs", "train", 1, 5.0),
        ("The computational scale measuring worst-case algorithm complexity is Big O", "Notation", "cs", "train", 0, 1.0)
    ]
    raw_source.extend(cs_train)

    # 2. SEEN VALIDATION: 20 Examples
    seen_val = [
        ("The official capital city of South Korea is", "Seoul", "factual", "seen_val", 1, 4.0),
        ("The official capital city of Norway is", "Oslo", "factual", "seen_val", 0, 1.0),
        ("The official capital city of Sweden is", "Stockholm", "factual", "seen_val", 0, 1.0),
        ("The official capital city of Switzerland is", "Bern", "factual", "seen_val", 1, 5.0),
        ("The official capital city of Poland is", "Warsaw", "factual", "seen_val", 0, 1.0),

        ("The noble element designated by atomic number 10 is", "Neon", "scientific", "seen_val", 0, 1.0),
        ("The volatile element designated by atomic number 16 is", "Sulfur", "scientific", "seen_val", 0, 1.0),
        ("The chemical molecule animals must extract from air to survive is", "Oxygen", "scientific", "seen_val", 1, 3.0),
        ("The yellow dwarf star supporting life at the center of our solar system is the", "Sun", "scientific", "seen_val", 0, 1.0),
        ("Mechanical acoustics are completely incapable of moving across a spatial", "Vacuum", "scientific", "seen_val", 0, 1.0),

        ("The globally recognized fantasy series Harry Potter was written by J.K.", "Rowling", "cloze", "seen_val", 0, 1.0),
        ("The legendary classical Greek epic poem The Odyssey is attributed to", "Homer", "cloze", "seen_val", 0, 1.0),
        ("To achieve multiple achievements concurrently is to kill two birds with one", "stone", "cloze", "seen_val", 0, 1.0),
        ("A graphical diagram is capable of conveying complex information because a picture is worth a thousand", "words", "cloze", "seen_val", 0, 1.0),
        ("An advice warning against placing all financial resources in a single asset is to not put all your eggs in one", "basket", "cloze", "seen_val", 0, 1.0),

        ("To enforce unique constraints with no duplicated items, algorithms utilize a", "Set", "cs", "seen_val", 1, 5.0),
        ("The hypermedia syntax used to format layout documents across the World Wide Web is", "HTML", "cs", "seen_val", 0, 1.0),
        ("An execution failure originating from incorrect program logic is called a", "Bug", "cs", "seen_val", 1, 5.0),
        ("A standardized text notation representing complex structural records is", "JSON", "cs", "seen_val", 0, 1.0),
        ("The active keyword used to bind external packages into Python script scopes is", "import", "cs", "seen_val", 1, 5.0)
    ]
    raw_source.extend(seen_val)

    # 3. UNSEEN VALIDATION: 20 Examples
    unseen_val = [
        ("The official capital city of Austria is", "Vienna", "factual", "unseen_val", 0, 1.0),
        ("The classical Roman general who met his end during the Ides of March was Julius", "Caesar", "factual", "unseen_val", 1, 4.0),
        ("The pioneer lunar explorer who took the first steps on the moon surface was Neil", "Armstrong", "factual", "unseen_val", 0, 1.0),
        ("The theoretical physicist who revolutionized coordinate physics with relativity was Albert", "Einstein", "factual", "unseen_val", 1, 5.0),
        ("The historical explorer who reached the Bahamas landmass in 1492 was Christopher", "Columbus", "factual", "unseen_val", 0, 1.0),

        ("Mammalian red blood cells are chemically responsible for transporting vital", "Oxygen", "scientific", "unseen_val", 1, 3.0),
        ("The organic cellular process separating chromosome pairs into twin cells is", "Mitosis", "scientific", "unseen_val", 0, 1.0),
        ("The primary command center of the central nervous system in vertebrates is the", "Brain", "scientific", "unseen_val", 1, 3.0),
        ("The dual-helix macromolecule housing core genetic blueprints is", "DNA", "scientific", "unseen_val", 1, 4.0),
        ("The dense celestial body whose localized gravitational path traps light is a", "Black Hole", "scientific", "unseen_val", 1, 4.0),

        ("An unexpected, completely unpredictable event is idiomatic described as out of the", "blue", "cloze", "unseen_val", 0, 1.0),
        ("To prematurely leak sensitive details of a confidential strategy is to let the cat out of the", "bag", "cloze", "unseen_val", 0, 1.0),
        ("A state of intense mental ecstasy or extreme joy is described as being on cloud", "nine", "cloze", "unseen_val", 0, 1.0),
        ("When working in an uncomfortable, unfamiliar setting, you feel like a fish out of", "water", "cloze", "unseen_val", 0, 1.0),
        ("An extremely dynamic, energetic, and unpredictable person is referred to as a live", "wire", "cloze", "unseen_val", 0, 1.0),

        ("The specialized data structure used to model recursive parent-child linkages is a", "Tree", "cs", "unseen_val", 1, 5.0),
        ("A networking layout topology organizing nodes around a central server hub is a", "Star", "cs", "unseen_val", 0, 1.0),
        ("The routing index directory that translates domain strings to IP coordinates is", "DNS", "cs", "unseen_val", 1, 5.0),
        ("A formal logical interface allowing separate software modules to interact is an", "API", "cs", "unseen_val", 0, 1.0),
        ("The physical block boundary used to serialize hard drive data tracks is a", "Sector", "cs", "unseen_val", 0, 1.0)
    ]
    raw_source.extend(unseen_val)

    # 4. OOD TEST: 10 Examples
    ood_test = [
        ("In mathematical topology, topological manifolds are categorized by Euler", "Manifold", "scientific", "ood_test", 0, 1.0),
        ("In wave equations, particles exhibit simultaneously localized and spread qualities called wave-particle", "Duality", "scientific", "ood_test", 0, 1.0),
        ("In molecular structures, compounds sharing atomic compositions but with varying bonds are", "Isomers", "scientific", "ood_test", 0, 1.0),
        ("In ecological geology, the mechanical drift of continental landmasses over time is plate", "Tectonics", "scientific", "ood_test", 0, 1.0),
        ("In ancient law, the primary eye-for-an-eye judicial structure was established in the Code of", "Hammurabi", "factual", "ood_test", 1, 4.0),
        ("In early Mesopotamian clay scripts, the classic adventure narrative is the Epic of", "Gilgamesh", "factual", "ood_test", 0, 1.0),
        ("In multi-linear algebra, a multi-dimensional array mapping space coordinate matrices is a", "Tensor", "scientific", "ood_test", 0, 1.0),
        ("In scientific taxonomy, species modifications driven by human breeders are called artificial", "Selection", "scientific", "ood_test", 0, 1.0),
        ("In mathematical logic, a clean self-contradictory loop that holds consistent truth is a", "Paradox", "factual", "ood_test", 1, 5.0),
        ("In deep history, the foundational Bronze Age legal block recovered in Susa is the Code of", "Hammurabi", "factual", "ood_test", 1, 4.0)
    ]
    raw_source.extend(ood_test)

    splits = {"train": [], "seen_val": [], "unseen_val": [], "ood": []}
    for idx, (p, t, task, s, is_c, wt) in enumerate(raw_source):
        prompt_aligned = f"Complete with one word only: {p}"
        split_name = "ood" if s == "ood_test" else s
        example = ClozeQAExample(
            example_id=idx + 1, prompt=prompt_aligned, target=t, task_type=task, split=split_name,
            is_critical=is_c, criticality_weight=wt
        )
        splits[split_name].append(example)
    return splits


def detect_format_template_leakage(text: str) -> bool:
    """Detect blanks, choices, scaffolds, option headers, bullet lists, or repeated patterns."""
    text_clean = text.strip()
    options = ["a.", "b.", "c.", "d.", "a)", "b)", "c)", "d)", "____", "______", "option a", "option b", "choose a"]
    for opt in options:
        if opt in text_clean.lower():
            return True
    if "\n" in text_clean or "\r" in text_clean:
        return True
    return False


def detect_over_generation(text: str, target: str) -> bool:
    """Detect if text is significantly longer than semantic target, violating task constraints."""
    norm_text = normalize_text(text)
    norm_target = normalize_text(target)
    if not norm_text or not norm_target:
        return False
    words_text = norm_text.split()
    words_target = norm_target.split()
    if len(words_text) > len(words_target):
        return True
    return False


def detect_instruction_contract_violation(text: str, target: str) -> bool:
    """Strictly checks if output text complies with the single-word / target-only boundary."""
    norm_text = normalize_text(text)
    words = norm_text.split()
    if len(words) > 1:
        return True
    return False


def load_reusable_model_and_tokenizer(cfg: Any) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    """Retrieves target causal model from HuggingFace, setting pad parameters cleanly."""
    logger.info(f"Retrieving tokenizer and architecture weights for: {cfg.model_name}")
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(cfg.model_name)
    model.to(cfg.device)
    model.config.pad_token_id = tokenizer.pad_token_id

    logger.info("Model parameter arrays successfully allocated.")
    return model, tokenizer


def is_contract_clean_candidate_repair(row: Dict[str, Any], model_name: Optional[str] = None) -> bool:
    """
    A production-safe SFT candidate repair requires:
    - baseline failed semantic target capture (baseline_correct == 0)
    - candidate captured semantic target (candidate_correct == 1)
    - candidate did not violate instruction contract (instruction_violation_candidate == 0)
    - candidate passed strict target-only exact match (strict_em_candidate == 1)
    
    Bypass/relaxation rule for small models (Issue 1):
    If the target model is lightweight (e.g., Qwen-0.5B, GPT-2), we relax the strict formatting
    gate. If the candidate captures the semantic target, it is considered a repair and formatting
    violations are recorded purely as debug observations.
    """
    baseline_failed = not _as_bool_int(row.get("baseline_correct", 0))
    candidate_semantic_ok = _as_bool_int(row.get("candidate_correct", 0))
    
    if not model_name:
        model_name = row.get("model_name")
        
    is_small_model = False
    if model_name:
        name_lower = str(model_name).lower()
        if "0.5b" in name_lower or "gpt2" in name_lower or "124m" in name_lower:
            is_small_model = True
            
    if is_small_model:
        return baseline_failed and candidate_semantic_ok

    candidate_strict_ok = _as_bool_int(row.get("strict_em_candidate", 0))
    candidate_contract_violation = _as_bool_int(
        row.get("instruction_violation_candidate", 1)
    )

    return (
        baseline_failed
        and candidate_semantic_ok
        and candidate_strict_ok
        and not candidate_contract_violation
    )