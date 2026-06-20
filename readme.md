# PCRF Transformer Reliability Suite v1

An enterprise-grade, information-theoretic AI safety and governance framework designed to measure, diagnose, and optimize Causal Language Models (CLMs) using **Probability Derivatives for Causal Reliability Flow (PCRF)** and **Causal Decay Loss V2 (CDL)**.

This library treats causal transformers not as opaque statistical engines, but as measurable, governed, series-reliability physical systems. It provides machine learning platform engineers, safety officers, and enterprise developers with a rigorous, mathematically sound validation pipeline to ensure post-regularization updates improve generalization without introducing silent regressions in production.

---

## 1. Core Features & Theoretical Foundations

The PCRF framework implements four major research tracks to identify and resolve model degradation:

*   **Track (a) - Structural PCRF Monitor:** Models the transformer's hidden layers as a series reliability chain. It maps representation vector drift under tiny embedding perturbations to continuous survival probabilities ($r_l$), evaluating systemic bottleneck points using analytical Birnbaum component importance.
*   **Track (b) - Derivative Estimation Engine:** Conducts empirical perturbation-based layer evaluations to measure how output target generation likelihood changes under downstream hidden state modifications.
*   **Track (c) - Safe Regularization (CDL v2):** Implements an anchor-regularized loss function that optimizes parameters strictly on high-impact boundary layers while maintaining logit-margin boundaries, token KL divergence, and greedy decoding alignment constraints.
*   **Track (d) - Curriculum Curation:** Prioritizes training samples by combining token-level difficulty (NLL) with systemic error sensitivity to curate a high-impact, cascade-risk replay buffer.

---

## 2. Hardware Requirements & VM Architecture Blueprints

To avoid Out-of-Memory Exceptions (OOME) during activation capturing hooks execution, the library runs a pre-computation hardware audit. Based on the selected model size, configure your Google Cloud Platform (GCP) Compute Engine or JupyterLab instances according to these specifications:

### Blueprint A: Sub-500M Parameter Models
*   **Optimal GCP Machine Type:** n1-standard-8 (8 vCPUs, 30 GB Host RAM)
*   **Hardware Accelerator:** 1x NVIDIA Tesla T4 (16 GB VRAM)
*   **Architectural Reason:** Light parameter footprints run cleanly inside the T4's memory boundaries. The 30 GB host memory handles parallel model downloads and tensor tokenization caches without hitting system swap limitations.

### Blueprint B: 500M to 3B Parameter Models
*   **Optimal GCP Machine Type:** g2-standard-8 (8 vCPUs, 32 GB Host RAM)
*   **Hardware Accelerator:** 1x NVIDIA L4 (24 GB VRAM)
*   **Architectural Reason:** Mid-tier generative models require faster matrix calculation paths and larger activation memory pools. The L4's Ada Lovelace architecture provides FP8 and FP16 speedups, preventing memory fragmentation during dynamic forward passes.

### Blueprint C: 3B+ Parameter Models
*   **Optimal GCP Machine Type:** a2-highgpu-1g (12 vCPUs, 85 GB Host RAM)
*   **Hardware Accelerator:** 1x NVIDIA A100 (40 GB VRAM)
*   **Architectural Reason:** High-dimensional sequence spaces require immense tensor processing speeds and wide memory bandwidth to avoid activation memory crashes during forward hook operations.

---

## 3. System Setup & Installation

Follow these steps to establish an isolated virtual environment and install the required dependencies:

### Step 1: Clone and Navigate to the Directory
Use your local system terminal to copy the repository files and navigate into the root directory of the project.

### Step 2: Establish a Clean Python Virtual Environment
It is highly recommended to use Python 3.10+ to ensure library compatibility. Activate the virtual environment using your terminal interface:
*   On Linux/macOS, source the environment activation script located within the environment folder.
*   On Windows, execute the command batch file located under the Scripts subdirectory of your environment folder.

### Step 3: Upgrade Package Installer & Install Dependencies
Using your active environment terminal, upgrade the Python package installer and pull the verified distribution libraries:
*   Install PyTorch (CUDA-enabled matched to your GPU runtime environment).
*   Install Hugging Face Transformers and Tokenizers.
*   Install System Utility Libraries (such as psutil for hardware profiling).

---

## 4. Custom Integration: Adapting to Your Models & Data

To utilize this framework for your own enterprise products, you must configure the system configuration files and format your dataset according to the rules detailed below.

### 4.1 Custom LLM Integration
You can plug in any causal autoregressive language model hosted on the Hugging Face Hub or stored locally on your network.
*   **Model Identification:** Modify the model name configuration variable with the Hugging Face directory path (such as Qwen/Qwen2.5-1.5B or standard GPT base profiles).
*   **Instrumentation Adaptation:** The library automatically scans the internal architecture of the model to locate layer blocks (such as attention layers, multi-layer perceptrons, or residual stream blocks). If you use a custom proprietary architecture, ensure your module lists are declared under standard block containers (e.g., an array named blocks, layers, or h) to enable automated forward hook registration.
*   **Precision and Device Mapping:** Configure the target execution device (CPU or CUDA) and enable float16/bfloat16 precision to fit representation capture steps within active VRAM envelopes.

### 4.2 Prompt Engineering & Target Aligned Formats
To prevent the "redundancy trap" and "continuation bias" where correct models score 0% due to formatting mismatches, follow these strict prompt and target completion guidelines:

*   **Prompt Completion Strategy:** Structure prompts so the expected completion sits at the very end of the sequence as a direct continuation.
*   **Target Minimization:** Keep target answers to the absolute semantic core (preferably a single word or a short, simple normalized phrase). Avoid grammatical redundancies. For example, instead of prompt "What is the capital of France?" with target "Paris, France", use prompt "The official capital city of France is" with target "Paris".
*   **Instruction Aligned Outputs:** If using an Instruct-tuned or Chat-tuned model, configure the tokenizer to apply the corresponding Chat Template wrapper, ensuring system instructions (e.g., "Respond with only one word") are passed as pre-tokens.

---

## 5. Dataset Schema & Split Rules

To derive the benefits of the PCRF safety gating and curriculum curation pipelines, your custom dataset must be compiled into a structured format (such as a CSV file or list of objects) containing exactly four dataset splits: `train`, `seen_val`, `unseen_val`, and `ood_test`.

### 5.1 Dataset Schema Specifications

| Property/Column Name | Expected Data Type | Description |
|---|---|---|
| **ID** | Integer | A unique numeric index assigned to each query row. |
| **Prompt** | String | The input text block fed to the model (e.g., "The chemical symbol for Gold is"). |
| **Target** | String | The exact expected semantic completion (e.g., "Au"). |
| **Task Type** | String | Category label used to group errors (e.g., "factual", "scientific", "code"). |
| **Is Critical** | Binary (0 or 1) | If set to 1, this represents a mission-critical, high-priority prompt where any regression under regularization is completely unacceptable. |
| **Criticality Weight** | Decimal | Multiplier representing the business impact of this query. Critical queries should be assigned weights between 3.0 and 5.0, while standard queries default to 1.0. |

### 5.2 Splitting Rules and Definitions

#### Split A: Train Set (Target of Curriculum Optimization)
The raw dataset pool used for candidate model regularized SFT tuning. It must contain representing samples across all target domains.

#### Split B: Seen Validation Set (CATALOG OF ANCHORS)
*   **Definition:** A curated subset containing prompts that are conceptually identical to, or heavily overlap with, the Train Set.
*   **Role in PCRF:** This acts as your "catastrophic forgetting" benchmark. The safety controller uses the Seen Validation set to ensure the model does not degrade on core knowledge it previously processed successfully.

#### Split C: Unseen Validation Set (GENERALIZATION FRONTIER)
*   **Definition:** Conceptually related to the training tasks but containing completely novel parameters, variables, or entities that the model has never processed before.
*   **Role in PCRF:** This is your primary metric of reliability improvement. The safety controller requires the candidate model to show validation loss or exact-match improvements on this split before promoting it.

#### Split D: Out-Of-Distribution (OOD) Test Set (BREAKING POINT MAP)
*   **Definition:** Queries originating from completely different conceptual domains, advanced topics, or edge-case structures.
*   **Role in PCRF:** This set is used to run stress-testing on the structural monitoring plugins, allowing your team to map out the ultimate representational breaking points of the network under extreme conceptual drift.

---

## 6. Running the Experiment Suite on Your Custom Pipeline

To run the full evaluation and tuning pipeline on your custom configurations:

1.  **Configure Paths:** Point the script's input data loaders to your newly prepared CSV file or dataset folder.
2.  **Adjust Thresholds:** Calibrate the non-inferiority margins and degradation budgets inside the safety controller config block to match your corporate risk tolerance.
3.  **Execute the Runner:** Invoke the Python interpreter on the main module, specifying your target model, output directories, and deterministic random seed variables.
4.  **Confirm Output Generation:** Ensure the execution completes without system swap stalls and verifies that the validation trace and debug report are successfully written to disk.

---

## 7. Artifact Architecture & Productized Deliverables

Following execution, the library generates two distinct categories of files. **Debug & Validation Outputs** are kept strictly minimal to prevent directory clutter during research runs, while **Customer Implementation Outputs** provide stable, productized files meant for direct consumption by your downstream production pipelines.

### Category A: Debug & Validation Outputs (Strictly Minimized)
*   `validation_trace.csv`: The centralized diagnostic trace tracking every single validation query across the seen and unseen splits. It records inputs, generated texts, transition states (`wrong -> correct`, `correct -> wrong`), target logit probabilities, and entropy changes.
*   `pcrf_debug_report.txt`: A clean, structured, human-readable log file outlining the executive metrics summary, statistical bootstrapping confidence checks, and a root-cause analysis of any critical regressions.

### Category B: Productized Customer Implementation Outputs
*   `per_module_derivatives.csv`: Exports the calculated empirical sensitivity delta (`delta_prob`), clean probability (`clean_mean_target_prob`), and perturbed probability (`perturbed_mean_target_prob`) for each layer block [1].
*   `structural_pcrf_summary.json`: Captures the continuous layer reliability scores ($r_l$), total system chain reliability ($R_{\text{sys}}$), and the layer-wise structural entropy profile ($S_l$) [1].
*   `layer_intervention_plan.csv`: A derivative file mapping which layers are flagged for PEFT (LoRA) or CDL regularized parameter updates based on their sensitivity and Birnbaum derivatives [1].
*   `curriculum_scores.csv`: The prioritized ranking of your training dataset used to feed your data-replay samplers.
*   `pcrf_configuration.json`: Stores all verified safety parameters, KL bounds, and target layer indexes to standardize the runtime execution pipeline [1].

---

## 8. Gating Decisions & Fallback Policy

The Safe PCRF Controller evaluates the candidate model against strict performance thresholds before permitting promotion to production:

```
                          ┌───────────────────────────┐
                          │   Evaluation Evaluation   │
                          └─────────────┬─────────────┘
                                        │
                         Is Baseline EM Acc == 0.0%?
                                        │
                        ┌───────────────┴───────────────┐
                        │ YES                           │ NO
                        ▼                               ▼
           ┌─────────────────────────┐     ┌─────────────────────────┐
           │      PATH C GATING      │     │      PATH A GATING      │
           │  (Continuous Loss/NLL)  │     │  (Discrete Exact Match) │
           └────────────┬────────────┘     └────────────┬────────────┘
                        │                               │
             Satisfies All Rules?            Satisfies All Rules?
                        │                               │
                  ┌─────┴─────┐                   ┌─────┴─────┐
                  │           │                   │           │
                  ▼           ▼                   ▼           ▼
               PROMPT      REJECT              PROMPT      REJECT
```

### Path A: Discrete Exact Match (EM) Gating
Used when the baseline model has some existing semantic accuracy on the validation split:
*   **Rule 1 (Unseen Generalization):** Requires at least a $+2.0\%$ improvement on the Unseen Validation set.
*   **Rule 2 (Seen Non-Inferiority):** Restricts Seen Validation degradation to a maximum of $1.0\%$.
*   **Rule 3 (Zero Regressions):** Rejects the update immediately if any `correct -> wrong` transitions occur on any critical, high-priority prompt.

### Path C: Continuous Loss/NLL Gating
Activated automatically under "cold-start" conditions where baseline EM accuracy is $0.0\%$:
*   **Rule 1 (Seen NLL Guard):** Restricts seen validation NLL degradation to a maximum of $+0.05$ (or $+1\%$ of baseline), preventing core task regression.
*   **Rule 2 (Unseen NLL Improvement):** Mandates at least a $5.0\%$ relative improvement (decrease) in unseen validation NLL.
*   **Rule 3 (Statistical Bootstrap Guard):** Generates a bootstrapped 95% confidence interval on the NLL delta across three evaluation runs. The NLL delta must be statistically negative to ensure the improvement is consistent and not due to statistical noise.
*   **Rule 4 (Over-steering Interceptor):** Rejects the update if the candidate model's unseen NLL decreases but its validation perplexity (PPL) simultaneously explodes by $>15\%$, indicating a loss of generative stability.

---

## 9. Dynamic Decay Curve & Trend Interpretation

The framework dynamically segments your chosen model's layers into three proportional sections: **Input Boundary** (first 15%), **Information Highway** (middle 70%), and **Output Boundary** (last 15%). By analyzing the average continuous survival probabilities ($r_l$) across these regions, the suite determines your model's structural health trend:

*   **U-Shaped Bottleneck Trend:** Reliability falls at the input and output boundaries but remains highly stable throughout the middle layers. This is the most common trend for dense generative models processing noisy data. **Action:** Freeze the middle layers; apply selective CDL regularization or PEFT tuning exclusively on the boundary layers.
*   **Monotonic Informational Decay Trend:** Reliability decreases steadily and cumulatively as layer index increases. This indicates representation corruption is cascading through the network depth. **Action:** Widen SFT regularization scope to include intermediate layers, or apply layer-wise skip-connection anchoring.
*   **Flat Representational Stability:** Reliability remains exceptionally high ($>95\%$) across all segments. This indicates highly coherent representations. **Action:** Broad SFT modifications are safe to perform.

---

## 10. Unique Value-Add of the PCRF Invention

Traditional AI evaluation approaches (like BLEU, ROUGE, or LLM-as-a-judge scoring) are **reactive**—they evaluate downstream outputs after text generation has already completed. This process is slow, computationally expensive, highly subjective, and unable to prevent failures in real-time.

The PCRF invention introduces a **preventative, white-box engineering paradigm** that adds unique value to your systems:

*   **Representational Telemetry (Knowing "Why"):** PCRF inspects the hidden vector spaces of your model during execution. It identifies exactly *how* information decays or becomes corrupted as it flows through the transformer blocks.
*   **Causal Bottleneck Attribution (Knowing "Where"):** By computing analytical Birnbaum derivatives ($D_R$) across the network depth, the framework pinpoints the exact layers or attention heads responsible for system failure, allowing your developers to debug structural errors.
*   **Pre-Generative Failure Interception (Knowing "When"):** Because representational decay ($R_{\text{sys}}$) can be measured during the forward pass, the system can detect an impending failure or adversarial exploit *before* the first output token is generated, allowing your gateway to safely route the query.

---

## 11. Step-by-Step Implementation Roadmap

Your development teams can directly implement these insights using the generated productized artifacts:

### Phase 1: Selective Boundary Layer Optimization
Open your dynamically generated `PCRF_Implementation_Blueprint_Regularization_*.md` file. Freeze the intermediate blocks (identified in `layer_intervention_plan.csv` as having low sensitivity) and apply your training gradients only to the early input and late projection layers. This reduces active backpropagation memory footprints by up to 50% while preventing catastrophic forgetting.

### Phase 2: Prioritized Dataset Sampler
Open your dynamically generated `PCRF_Implementation_Blueprint_Curriculum_*.md` file. Inject the provided weighted data-loading wrapper into your training pipelines. This code reads `curriculum_scores.csv` and uses a PyTorch weighted sampler to focus training epochs on high-priority, high-cascade-risk prompts. This allows your team to cut training times by up to 50% while maintaining target generalization boundaries.

### Phase 3: Live API Gateway "Canary" Router
Open your dynamically generated `PCRF_Implementation_Blueprint_Structural_PCRF_*.md` file. Implement the provided canary routing middleware in your production API gateways. For each user request, the gateway runs a low-overhead forward pass to compute the structural reliability index ($R_{\text{sys}}$). If $R_{\text{sys}}$ drops below your chosen safety threshold (configured in `pcrf_configuration.json`), the router intercepts the request and falls back to your frozen baseline model before any corrupted text reaches the user.

### Phase 4: Automated CI/CD Governance Safety Gates
Integrate the `SafePCRFController` class directly into your GitLab, GitHub, or Jenkins deployment pipelines. Configure the CI/CD runner to block any model release that fails to clear the continuous Path C non-inferiority and bootstrap validation checks on your validation trace. This provides an automated, mathematically rigorous barrier against performance regressions in production.