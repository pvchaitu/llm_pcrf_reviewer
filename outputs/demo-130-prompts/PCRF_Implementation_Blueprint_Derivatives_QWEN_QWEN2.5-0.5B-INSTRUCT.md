# PCRF Implementation Blueprint: Parameter Sensitivity-Damped Optimization for QWEN_QWEN2.5-0.5B-INSTRUCT
This blueprint was programmatically generated because the Derivatives track was verified as safe (`SAFE_TO_APPLY`).

**🔍 Run Observation:** Your model demonstrated stable structural gradients with 0.00378 (Avg Sensitivity). This makes it an ideal candidate for layer-specific learning rate damping.

Configure your SFT optimization loop to adapt learning rates scaled inversely by sensitivity layer coordinates:

```python
import csv
import torch

def create_pcrf_optimizer(model, base_lr=1e-5, damping_factor=10.0, csv_path="per_module_derivatives.csv"):
    sensitivities = {}
    with open(csv_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensitivities[int(row["layer_id"])] = float(row["empirical_delta_prob"])
            
    # Apply parameterized learning rate scales per layer block
    params_group = []
    for name, param in model.named_parameters():
        matched_layer = None
        for i in range(32): # Inspect layers dynamically
            if f"layers.{i}." in name:
                matched_layer = i
                break
        if matched_layer is not None and matched_layer in sensitivities:
            # Dampen rate based on empirical sensitivity magnitude
            lr_scale = 1.0 / (1.0 + damping_factor * abs(sensitivities[matched_layer]))
            params_group.append({"params": param, "lr": base_lr * lr_scale})
        else:
            params_group.append({"params": param, "lr": base_lr})
            
    return torch.optim.AdamW(params_group)
```
