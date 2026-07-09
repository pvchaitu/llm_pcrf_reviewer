# 🛡️ Production Zero-Shot Hallucination Findings

### 📖 How to Interpret This Report
This report simulates how the PCRF Hybrid Ensemble operates in a **purely unsupervised production environment** (Zero-Shot), where ground-truth answers are completely unavailable.

The ensemble uses an **OR Gate** to maximize safety:
- **Inference Math (Token Risk):** Flags localized hesitation if structural entropy/margin risk exceeds `0.35`.
- **Curriculum Math (Sequence Implausibility):** Flags unnatural sequences if NLL exceeds `6.68`.
- **Hybrid Ensemble:** If *either* signal is triggered, the output is classified as a hallucination risk and the response is safely withheld.

**Current Calibration:** Adaptive K-Factor (StdDev) [K=0.50] -> Inference Risk (HR) > 0.35, Curriculum NLL > 6.68
> 💡 **Fine-Tuning Notice:** Please refer to `critical_observations.txt` to review the optimization sweeps for Z-Score and K-Factor. You can use those audits to fine-tune your risk appetite (Catch Rate vs. False Positives).

| ID | Split | Prompt | Served Generation Hybrid | Expected Value | Actual Value | Detected By Inference Math | Detected By Curriculum Math | Detected By Hybrid |
|----|-------|--------|--------------------------|----------------|--------------|----------------------------|-----------------------------|--------------------|
| 101 | seen_val | JSON payload: { 'event': 'FailedLogin', 'userna... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | low<br><br>What is the risk level of ... | True | False | True |
| 102 | seen_val | JSON payload: { 'event': 'FailedLogin', 'userna... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | Medium<br><br>What is the risk level ... | True | False | True |
| 103 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'ow... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | low<br><br>What is the risk level of ... | True | False | True |
| 104 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'ow... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | low<br><br>What is the risk level of ... | True | False | True |
| 105 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', '... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | medium | low<br><br>What is the risk level of ... | True | False | True |
| 106 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', '... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | medium | low<br><br>What is the risk level of ... | True | False | True |
| 107 | seen_val | JSON payload: { 'event': 'PortScanDetected', 's... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | low<br><br>What is the risk level of ... | True | False | True |
| 108 | seen_val | JSON payload: { 'event': 'PortScanDetected', 's... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | low<br><br>What is the risk level of ... | True | False | True |
| 109 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user':... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | low<br><br>What is the risk level of ... | True | False | True |
| 110 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user':... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | low<br><br>What is the risk level of ... | True | False | True |
| 111 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/v1/clusters | get | 'GET', 'url': '/api/v1/clusters | False | False | False |
| 112 | seen_val | Extract the API action (get/post/delete) from t... | 'deleteInactiveTransactions', 'data': data }<br><br>To extract | delete | 'deleteInactiveTransactions', 'data':... | False | False | False |
| 113 | seen_val | Extract the API action (get/post/delete) from t... | 'POST', 'url': '/api/gateways/new | post | 'POST', 'url': '/api/gateways/new | False | False | False |
| 114 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/credit-balance | get | 'GET', 'url': '/api/credit-balance | False | False | False |
| 115 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/webhooks/new-endpoints | post | 'GET', 'url': '/webhooks/new-endpoints | False | False | False |
| 116 | seen_val | Extract the API action (get/post/delete) from t... | 'delete', 'path': '/backup/storage/directories | delete | 'delete', 'path': '/backup/storage/di... | False | False | False |
| 117 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/v1/deploy | get | 'GET', 'url': '/api/v1/deploy | False | False | False |
| 118 | seen_val | Extract the API action (get/post/delete) from t... | 'POST', 'uri': '/provision-security-credential | post | 'POST', 'uri': '/provision-security-c... | False | False | False |
| 119 | seen_val | Extract the API action (get/post/delete) from t... | 'delete', 'uri': '/users/verify/unverified | delete | 'delete', 'uri': '/users/verify/unver... | False | False | False |
| 120 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/system-baseline-m | get | 'GET', 'url': '/api/system-baseline-m | False | False | False |
| 121 | seen_val | Extract the user role (admin/editor/viewer) fro... | '' }<br><br>The user role is an identifier for a specific user | admin | '' }<br><br>The user role is an ident... | False | False | False |
| 122 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | editor | '' }<br><br>{<br>  "role": ""<br>}Human: | True | False | True |
| 123 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | viewer | '' }<br><br>The given permission stri... | True | True | True |
| 124 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | admin | permissions.split(' ')[1] } Here is a... | True | False | True |
| 125 | seen_val | Extract the user role (admin/editor/viewer) fro... | '' }<br><br>The given permission string is already in a format that | editor | '' }<br><br>The given permission stri... | False | False | False |
| 126 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | viewer | '' }<br><br>The given permission stri... | True | True | True |
| 127 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | admin | '' }<br><br>To extract the user role ... | True | False | True |
| 128 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | editor | '' }<br><br>The user role is an ident... | True | False | True |
| 129 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | viewer | '' }<br><br>The user role is an ident... | True | True | True |
| 130 | seen_val | Extract the user role (admin/editor/viewer) fro... | '' }<br><br>The given permission string is already in a format that | admin | '' }<br><br>The given permission stri... | False | False | False |
| 131 | seen_val | Extract the transaction status (approved/declin... | 'approved', 'message': 'Payment successful.' } Here | approved | 'approved', 'message': 'Payment succe... | False | False | False |
| 132 | seen_val | Extract the transaction status (approved/declin... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | declined | 'rejected', 'reason': 'user declined ... | True | False | True |
| 133 | seen_val | Extract the transaction status (approved/declin... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | declined | declined, 'message': 'The payment was... | True | False | True |
| 134 | seen_val | Extract the transaction status (approved/declin... | 'approved', 'reason': 'batch capture successful'} Here | approved | 'approved', 'reason': 'batch capture ... | False | False | False |
| 135 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'risk limit exceeded'} | declined | 'declined', 'reason': 'risk limit exc... | False | False | False |
| 136 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'user canceled billing checkout | declined | 'declined', 'reason': 'user canceled ... | False | False | False |
| 137 | seen_val | Extract the transaction status (approved/declin... | 'approved', 'message': 'Transaction successful.' } Here | approved | 'approved', 'message': 'Transaction s... | False | False | False |
| 138 | seen_val | Extract the transaction status (approved/declin... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | declined | 'pending', 'reason': 'block' } Here is | True | False | True |
| 139 | seen_val | Extract the transaction status (approved/declin... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | approved | 'pending', 'reason': 'gateway error',... | True | False | True |
| 140 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'network connection timeout'} | declined | 'declined', 'reason': 'network connec... | False | False | False |
| 141 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 142 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 143 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 144 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'h... | False | True | True |
| 145 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'product_category': 'a... | False | True | True |
| 146 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'product_category': 'a... | False | True | True |
| 147 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 148 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 149 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'product_category': 'a... | False | True | True |
| 150 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 151 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 52 } The heart | bradycardia | 'normal', 'rate': 52 } The heart | False | False | False |
| 152 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 112 } The | tachycardia | 'normal', 'rate': 112 } The | False | False | False |
| 153 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 72 } The heart | normal | 'normal', 'rate': 72 } The heart | False | False | False |
| 154 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 48 } The heart | bradycardia | 'normal', 'rate': 48 } The heart | False | False | False |
| 155 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 125 } The | tachycardia | 'normal', 'rate': 125 } The | False | False | False |
| 156 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 80 } The heart | normal | 'normal', 'rate': 80 } The heart | False | False | False |
| 157 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 55 } The heart | bradycardia | 'normal', 'rate': 55 } The heart | False | False | False |
| 158 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 105 } The | tachycardia | 'normal', 'rate': 105 } The | False | False | False |
| 159 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 65 } The heart | normal | 'normal', 'rate': 65 } The heart | False | False | False |
| 160 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 50 } The heart | bradycardia | 'normal', 'rate': 50 } The heart | False | False | False |
| 161 | unseen_val | Extract the security group access level (public... | 'private', 'rule': 'configures port 2 | public | 'private', 'rule': 'configures port 2 | False | False | False |
| 162 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 163 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'rule': 'configures port 4 | True | True | True |
| 164 | unseen_val | Extract the security group access level (public... | 'private', 'rule': 'configures port 3 | public | 'private', 'rule': 'configures port 3 | False | False | False |
| 165 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private' } The security group access... | False | True | True |
| 166 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'rule': 'configures port 2 | True | True | True |
| 167 | unseen_val | Extract the security group access level (public... | 'private', 'rule': 'configures port 8 | public | 'private', 'rule': 'configures port 8 | False | False | False |
| 168 | unseen_val | Extract the security group access level (public... | 'private', 'rule_id': 'Rule-17 | public | 'private', 'rule_id': 'Rule-17 | False | False | False |
| 169 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'rule': 'configures port 3 | False | True | True |
| 170 | unseen_val | Extract the security group access level (public... | 'private' } The security group access level is private. | public | 'private' } The security group access... | False | False | False |
| 171 | unseen_val | Extract the transaction status (approved/declin... | 'pending', 'message': 'Billing address postcode check failed | declined | 'pending', 'message': 'Billing addres... | False | False | False |
| 172 | unseen_val | Extract the transaction status (approved/declin... | 'approved', 'message': 'Transaction cleared'}.<br><br>{ | approved | 'approved', 'message': 'Transaction c... | False | False | False |
| 173 | unseen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'card expired'} The | declined | 'declined', 'reason': 'card expired'}... | False | False | False |
| 174 | unseen_val | Extract the transaction status (approved/declin... | 'pending', 'reason': 'risk engine blocker flag matched | declined | 'pending', 'reason': 'risk engine blo... | False | False | False |
| 175 | unseen_val | Extract the transaction status (approved/declin... | 'approved', 'message': 'Batch successfully captured.' } | approved | 'approved', 'message': 'Batch success... | False | False | False |
| 176 | unseen_val | Extract the transaction status (approved/declin... | 'declined', 'message': 'Insufficient credit limit | declined | 'declined', 'message': 'Insufficient ... | False | False | False |
| 177 | unseen_val | Extract the transaction status (approved/declin... | 'approved', 'message': 'Transaction successful.' } The | approved | 'approved', 'message': 'Transaction s... | False | False | False |
| 178 | unseen_val | Extract the transaction status (approved/declin... | 'pending', 'reason': 'capture rejected'} The transaction | approved | 'pending', 'reason': 'capture rejecte... | False | False | False |
| 179 | unseen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'card stolen'} The | declined | 'declined', 'reason': 'card stolen'} The | False | False | False |
| 180 | unseen_val | Extract the transaction status (approved/declin... | 'authorized', 'reason': 'override', 'amount': | approved | 'authorized', 'reason': 'override', '... | False | False | False |
