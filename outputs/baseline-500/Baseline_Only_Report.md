# Baseline-Only Evaluation Report

## Execution Mode
- Run Mode: baseline
- PCRF Components Executed: No
- SFT Candidate Regularization Executed: No
- Protected Router Executed: No

## Dataset Source
- Dataset Source: External File
- Dataset File: new-customer-demo-500-prompt.csv

## Dataset Partition Counts
- Train Split: 200
- Seen Validation Split: 125
- Unseen Validation Split: 125
- OOD Split: 50
- Total Rows Audited: 500

## Baseline Metrics
- model_name: Qwen/Qwen2.5-0.5B-Instruct
- seen_val_acc: 0.68
- unseen_val_acc: 0.56
- seen_val_nll: 5.157656669616699
- unseen_val_nll: 8.998390557939913
- seen_val_ppl: 173.75680855699622
- unseen_val_ppl: 8090.052972582302

## Baseline Prompt / Generation Hallucination Audit

Baseline row audit includes train, seen validation, unseen validation, and OOD prompts where available. This gives a complete view of baseline hallucination exposure before PCRF governance.

| ID | Split | Prompt | Baseline Generation | Expected Value | Actual Value | Match? | Hallucinated? |
|----|--------|---------|---------|---------|---------|---------|---------|
| 1 | train | JSON payload: { 'event': 'FailedLogin', 'username': 'root', 'ip': '198.5... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 2 | train | JSON payload: { 'event': 'FailedLogin', 'username': 'johndoe', 'ip': '19... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 3 | train | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'dev_user_99', 'pub... | What is the risk of this event occurring? <br>R... | high | What is the risk of this event occurring? <br>R... | NO | YES |
| 4 | train | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'ops_manager_22', '... | What is the risk of this event occurring? <br>R... | low | What is the risk of this event occurring? <br>R... | NO | YES |
| 5 | train | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'AdministratorAc... | What is the risk of this event occurring? <br>R... | high | What is the risk of this event occurring? <br>R... | NO | YES |
| 6 | train | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'ReadOnlyAccess'... | What is the risk of this event occurring? <br>R... | low | What is the risk of this event occurring? <br>R... | NO | YES |
| 7 | train | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '45.33.102.55'... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 8 | train | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '10.0.2.14', '... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 9 | train | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'jenkins_agent_01', 'key... | low<br><br>What is the risk level of this event... | medium | low<br><br>What is the risk level of this event... | NO | YES |
| 10 | train | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'master_backup_bot', 'ke... | low<br><br>What is the risk level of this event... | low | low<br><br>What is the risk level of this event... | YES | NO |
| 11 | train | JSON payload: { 'event': 'FailedLogin', 'username': 'admin_crm', 'ip': '... | What is the risk of this event? <br>Risk level: | medium | What is the risk of this event? <br>Risk level: | NO | YES |
| 12 | train | JSON payload: { 'event': 'FailedLogin', 'username': 'staff_dev', 'ip': '... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 13 | train | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'marketing_external... | low<br><br>What is the risk level of this event... | high | low<br><br>What is the risk level of this event... | NO | YES |
| 14 | train | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'finance_lead', 'pu... | low. Severity of the risk: medium.<br><br>What ... | low | low. Severity of the risk: medium.<br><br>What ... | YES | NO |
| 15 | train | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'BillingAccess',... | What is the risk of this event occurring? <br>R... | medium | What is the risk of this event occurring? <br>R... | NO | YES |
| 16 | train | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'SecurityAuditOn... | What is the risk level of this IAM policy modif... | low | What is the risk level of this IAM policy modif... | NO | YES |
| 17 | train | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '185.190.140.2... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 18 | train | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '192.168.10.15... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 19 | train | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'temporary_contractor', ... | low<br><br>What is the risk level of this event... | medium | low<br><br>What is the risk level of this event... | NO | YES |
| 20 | train | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'ceo_laptop_device', 'ke... | low<br><br>What is the risk level of this event... | low | low<br><br>What is the risk level of this event... | YES | NO |
| 21 | train | Extract the API action (get/post/delete) from this routing rule: 'Fetch ... | 'GET' } To extract the API action from the given | get | 'GET' } To extract the API action from the given | YES | NO |
| 22 | train | Extract the API action (get/post/delete) from this routing rule: 'Delete... | 'delete', 'data': {} } The provided JSON object | delete | 'delete', 'data': {} } The provided JSON object | YES | NO |
| 23 | train | Extract the API action (get/post/delete) from this routing rule: 'Create... | 'POST', 'data': { 'client_id': ' | post | 'POST', 'data': { 'client_id': ' | YES | NO |
| 24 | train | Extract the API action (get/post/delete) from this routing rule: 'Retrie... | 'GET', 'url': '/api/transactions' } | get | 'GET', 'url': '/api/transactions' } | YES | NO |
| 25 | train | Extract the API action (get/post/delete) from this routing rule: 'Regist... | 'POST', 'data': { 'mobile_gateway_id': | post | 'POST', 'data': { 'mobile_gateway_id': | YES | NO |
| 26 | train | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'resource': 'configurationBaselineRev... | delete | 'delete', 'resource': 'configurationBaselineRev... | YES | NO |
| 27 | train | Extract the API action (get/post/delete) from this routing rule: 'List a... | 'GET', 'uri': '/containers/{containerId}/ | get | 'GET', 'uri': '/containers/{containerId}/ | YES | NO |
| 28 | train | Extract the API action (get/post/delete) from this routing rule: 'Provis... | 'POST', 'data': { 'name': 'John | post | 'POST', 'data': { 'name': 'John | YES | NO |
| 29 | train | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'uri': '/api/billing/direct | delete | 'delete', 'uri': '/api/billing/direct | YES | NO |
| 30 | train | Extract the API action (get/post/delete) from this routing rule: 'Fetch ... | 'GET', 'url': '/compliance-checklist/' | get | 'GET', 'url': '/compliance-checklist/' | YES | NO |
| 31 | train | Extract the API action (get/post/delete) from this routing rule: 'Retrie... | 'GET', 'url': '/api/heartbeat-telemetry | get | 'GET', 'url': '/api/heartbeat-telemetry | YES | NO |
| 32 | train | Extract the API action (get/post/delete) from this routing rule: 'Delete... | 'delete_orphaned_volumes_from_host_server' } | delete | 'delete_orphaned_volumes_from_host_server' } | YES | NO |
| 33 | train | Extract the API action (get/post/delete) from this routing rule: 'Submit... | 'get', 'url': '/api/submit/client-access | post | 'get', 'url': '/api/submit/client-access | NO | YES |
| 34 | train | Extract the API action (get/post/delete) from this routing rule: 'Load a... | 'GET', 'url': '/api/v1/transactions | get | 'GET', 'url': '/api/v1/transactions | YES | NO |
| 35 | train | Extract the API action (get/post/delete) from this routing rule: 'Push l... | 'GET', 'url': '/api/system-baseline-profile | post | 'GET', 'url': '/api/system-baseline-profile | NO | YES |
| 36 | train | Extract the API action (get/post/delete) from this routing rule: 'Purge ... | 'GET', 'uri': '/purge-deprecated-session | delete | 'GET', 'uri': '/purge-deprecated-session | NO | YES |
| 37 | train | Extract the API action (get/post/delete) from this routing rule: 'Reques... | 'GET', 'url': '/api/network/interfaces/latest' | get | 'GET', 'url': '/api/network/interfaces/latest' | YES | NO |
| 38 | train | Extract the API action (get/post/delete) from this routing rule: 'Publis... | 'POST', 'data': {} } To extract the API | post | 'POST', 'data': {} } To extract the API | YES | NO |
| 39 | train | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'database': 'staging', 'cluster | delete | 'delete', 'database': 'staging', 'cluster | YES | NO |
| 40 | train | Extract the API action (get/post/delete) from this routing rule: 'Load b... | 'GET', 'uri': '/metrics/load-balancer-in | get | 'GET', 'uri': '/metrics/load-balancer-in | YES | NO |
| 41 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already provided in the | admin | 'admin' } The user role is already provided in the | YES | NO |
| 42 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 43 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 44 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The provided permission string is alr... | admin | 'admin' } The provided permission string is alr... | YES | NO |
| 45 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 46 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 47 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | admin | 'admin' } The user role is set to admin. | YES | NO |
| 48 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | editor | 'admin' } The user role is set to admin. | NO | YES |
| 49 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 50 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already specified in... | admin | 'admin' } The user role is already specified in... | YES | NO |
| 51 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'editor' } The user role is set to `editor | editor | 'editor' } The user role is set to `editor | YES | NO |
| 52 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 53 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already provided in the | admin | 'admin' } The user role is already provided in the | YES | NO |
| 54 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | editor | 'admin' } The user role is set to admin. | NO | YES |
| 55 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 56 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | admin | 'admin' } The user role is set to admin. | YES | NO |
| 57 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 58 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 59 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already provided in the | admin | 'admin' } The user role is already provided in the | YES | NO |
| 60 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 61 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'payment successful', 'am... | approved | 'approved', 'reason': 'payment successful', 'am... | YES | NO |
| 62 | train | Extract the transaction status (approved/declined) from this gateway log... | 'rejected', 'reason': 'insufficient credit' } | declined | 'rejected', 'reason': 'insufficient credit' } | NO | YES |
| 63 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'credit card verification... | declined | 'declined', 'reason': 'credit card verification... | YES | NO |
| 64 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'funds captured successfu... | approved | 'approved', 'reason': 'funds captured successfu... | YES | NO |
| 65 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'fraud filter triggered | declined | 'declined', 'reason': 'fraud filter triggered | YES | NO |
| 66 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'verified', 'order_id | approved | 'approved', 'reason': 'verified', 'order_id | YES | NO |
| 67 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'card has expired' | declined | 'declined', 'reason': 'card has expired' | YES | NO |
| 68 | train | Extract the transaction status (approved/declined) from this gateway log... | 'pending_capture', 'reason': 'payment authorize... | approved | 'pending_capture', 'reason': 'payment authorize... | NO | YES |
| 69 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': '' } The transaction stat... | declined | 'approved', 'reason': '' } The transaction stat... | NO | YES |
| 70 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'digital wallet authentic... | approved | 'approved', 'reason': 'digital wallet authentic... | YES | NO |
| 71 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'Charge limit exceeded for | declined | 'declined', 'reason': 'Charge limit exceeded for | YES | NO |
| 72 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'address postcode verify ... | declined | 'declined', 'reason': 'address postcode verify ... | YES | NO |
| 73 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'payment completed succes... | approved | 'approved', 'reason': 'payment completed succes... | YES | NO |
| 74 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'chargeback rejected by | declined | 'declined', 'reason': 'chargeback rejected by | YES | NO |
| 75 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'token validated and clea... | approved | 'approved', 'reason': 'token validated and clea... | YES | NO |
| 76 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'user cancelled checkout ... | declined | 'declined', 'reason': 'user cancelled checkout ... | YES | NO |
| 77 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'invoice archived' } The | approved | 'approved', 'reason': 'invoice archived' } The | YES | NO |
| 78 | train | Extract the transaction status (approved/declined) from this gateway log... | 'pending', 'reason': 'suspicious billing ip | declined | 'pending', 'reason': 'suspicious billing ip | NO | YES |
| 79 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'merchant manual override... | approved | 'approved', 'reason': 'merchant manual override... | YES | NO |
| 80 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'network connection dropp... | declined | 'declined', 'reason': 'network connection dropp... | YES | NO |
| 81 | train | To accomplish multiple milestones at the exact same moment is to kill tw... | stone. This is a common strategy used by many p... | stone | stone. This is a common strategy used by many p... | YES | NO |
| 82 | train | To avoid placing all your financial capital in a single volatile asset, ... | basket. Instead, diversify your investments acr... | basket | basket. Instead, diversify your investments acr... | YES | NO |
| 83 | train | To accidentally reveal highly confidential organization blueprints is to... | bag. This is a common occurrence in many organi... | bag | bag. This is a common occurrence in many organi... | YES | NO |
| 84 | train | Being in a state of supreme, ecstatic joy or extreme mental happiness is... | nine. This feeling can come from many different... | nine | nine. This feeling can come from many different... | YES | NO |
| 85 | train | Feeling entirely awkward, uncomfortable, and physically out of place is ... | water. It can be very embarrassing to feel this... | water | water. It can be very embarrassing to feel this... | YES | NO |
| 86 | train | An unpredictable, incredibly dynamic, and highly energetic person is des... | action film director. This type of person can b... | wire | action film director. This type of person can b... | NO | YES |
| 87 | train | An entirely random, highly surprising, and completely unexpected event i... | ordinary. It's a situation that has never happe... | blue | ordinary. It's a situation that has never happe... | NO | YES |
| 88 | train | Pursuing a completely incorrect strategy or line of logic is barking up ... | tree. The goal should be to find a way to solve | tree | tree. The goal should be to find a way to solve | YES | NO |
| 89 | train | Facing a very difficult, painful, or awkward situation with brave compos... | bullet. The act of biting the bullet can be don... | bullet | bullet. The act of biting the bullet can be don... | YES | NO |
| 90 | train | Wishing a theater actor excellent performance fortune right before a sho... | promise. The actor breaks the promise and gets ... | leg | promise. The actor breaks the promise and gets ... | NO | YES |
| 91 | train | To accidentally expose a highly guarded organizational secret is to spil... | beans. This is an example of which type of logi... | beans | beans. This is an example of which type of logi... | YES | NO |
| 92 | train | Executing an operational workflow that is incredibly straightforward is ... | cake. However, when it comes to creating a work... | cake | cake. However, when it comes to creating a work... | YES | NO |
| 93 | train | Resolving an architectural software bottleneck with absolute precision i... | head. The software that I am working on has a very | head | head. The software that I am working on has a very | YES | NO |
| 94 | train | To accept the negative consequences of your previous incorrect actions i... | reality that you are not a good person. This st... | music | reality that you are not a good person. This st... | NO | YES |
| 95 | train | Feeling mildly sick, fatigued, or physically under the weather is to be ... | care of a doctor. The doctor will examine you a... | weather | care of a doctor. The doctor will examine you a... | NO | YES |
| 96 | train | To completely cease working on a development pipeline for the evening is... | day. The development pipeline is a series of st... | day | day. The development pipeline is a series of st... | YES | NO |
| 97 | train | Complaining about unfixable, past execution errors is crying over spilled | milk. This is a common complaint from users of ... | milk | milk. This is a common complaint from users of ... | YES | NO |
| 98 | train | Avoiding speaking about the central, most critical problem in a meeting ... | bush. It’s not just a matter of being polite or | bush | bush. It’s not just a matter of being polite or | YES | NO |
| 99 | train | To initiate a highly difficult, tense, or awkward discussion with collea... | rules of social etiquette. The most appropriate... | ice | rules of social etiquette. The most appropriate... | NO | YES |
| 100 | train | Adding angry, volatile statements to an ongoing administrative dispute i... | fire. The problem of conflict resolution in org... | fire | fire. The problem of conflict resolution in org... | YES | NO |
| 101 | train | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '185.190.140.4... | low<br><br>What is the risk level of this incid... | medium | low<br><br>What is the risk level of this incid... | NO | YES |
| 102 | train | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'ops_agent_12', 'key_str... | low<br><br>What is the risk level of this event... | low | low<br><br>What is the risk level of this event... | YES | NO |
| 103 | train | JSON payload: { 'event': 'FailedLogin', 'username': 'root', 'ip': '198.5... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 104 | train | JSON payload: { 'event': 'FailedLogin', 'username': 'sam', 'ip': '192.16... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 105 | train | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'dev_test_user', 'p... | What is the risk of this event occurring? <br>R... | high | What is the risk of this event occurring? <br>R... | NO | YES |
| 106 | train | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'ops_admin_4', 'pub... | What is the risk of this event occurring? <br>R... | low | What is the risk of this event occurring? <br>R... | NO | YES |
| 107 | train | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'AdministratorAc... | What is the risk of this event occurring? <br>R... | medium | What is the risk of this event occurring? <br>R... | NO | YES |
| 108 | train | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'ReadOnlyAccess'... | What is the risk of this IAM policy modificatio... | medium | What is the risk of this IAM policy modificatio... | NO | YES |
| 109 | train | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '45.33.102.12'... | low<br><br>What is the risk level of this incid... | medium | low<br><br>What is the risk level of this incid... | NO | YES |
| 110 | train | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '10.0.2.19', '... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 111 | train | Extract the API action (get/post/delete) from this routing rule: 'Delete... | 'delete', 'data': {} } To extract the API | delete | 'delete', 'data': {} } To extract the API | YES | NO |
| 112 | train | Extract the API action (get/post/delete) from this routing rule: 'Create... | 'POST', 'url': '/api/webhooks/server/ | post | 'POST', 'url': '/api/webhooks/server/ | YES | NO |
| 113 | train | Extract the API action (get/post/delete) from this routing rule: 'Retrie... | 'GET', 'url': '/api/system-balance-profile | get | 'GET', 'url': '/api/system-balance-profile | YES | NO |
| 114 | train | Extract the API action (get/post/delete) from this routing rule: 'Regist... | 'GET', 'url': '/webhooks/gateways | post | 'GET', 'url': '/webhooks/gateways | NO | YES |
| 115 | train | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'GET' } To extract the API action from a given | delete | 'GET' } To extract the API action from a given | NO | YES |
| 116 | train | Extract the API action (get/post/delete) from this routing rule: 'List a... | 'GET', 'url': '/api/system/deployments | get | 'GET', 'url': '/api/system/deployments | YES | NO |
| 117 | train | Extract the API action (get/post/delete) from this routing rule: 'Provis... | 'POST', 'data': {} } To extract the API | post | 'POST', 'data': {} } To extract the API | YES | NO |
| 118 | train | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'data': {} } To extract the API | delete | 'delete', 'data': {} } To extract the API | YES | NO |
| 119 | train | Extract the API action (get/post/delete) from this routing rule: 'Fetch ... | 'GET', 'uri': '/api/system-baseline-m | get | 'GET', 'uri': '/api/system-baseline-m | YES | NO |
| 120 | train | Extract the API action (get/post/delete) from this routing rule: 'Submit... | 'POST', 'data': { 'transaction_id': ' | post | 'POST', 'data': { 'transaction_id': ' | YES | NO |
| 121 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already provided in the | admin | 'admin' } The user role is already provided in the | YES | NO |
| 122 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | editor | 'admin' } The user role is set to admin. | NO | YES |
| 123 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 124 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The provided permission string is alr... | admin | 'admin' } The provided permission string is alr... | YES | NO |
| 125 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 126 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 127 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | admin | 'admin' } The user role is set to admin. | YES | NO |
| 128 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | editor | 'admin' } The user role is set to admin. | NO | YES |
| 129 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 130 | train | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | admin | 'viewer' } The user role is viewer. Here's | NO | YES |
| 131 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'payment successful', 'am... | approved | 'approved', 'reason': 'payment successful', 'am... | YES | NO |
| 132 | train | Extract the transaction status (approved/declined) from this gateway log... | 'rejected', 'reason': 'user rejected payment re... | declined | 'rejected', 'reason': 'user rejected payment re... | NO | YES |
| 133 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'CVV verification mismatch | declined | 'declined', 'reason': 'CVV verification mismatch | YES | NO |
| 134 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'batch capture successful... | approved | 'approved', 'reason': 'batch capture successful... | YES | NO |
| 135 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'risk limit exceeded' | declined | 'declined', 'reason': 'risk limit exceeded' | YES | NO |
| 136 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'user cancelled billing c... | declined | 'declined', 'reason': 'user cancelled billing c... | YES | NO |
| 137 | train | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': '' } Here is the extracted | approved | 'approved', 'reason': '' } Here is the extracted | YES | NO |
| 138 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'block detected in payment | declined | 'declined', 'reason': 'block detected in payment | YES | NO |
| 139 | train | Extract the transaction status (approved/declined) from this gateway log... | 'pending', 'reason': 'gateway error', 'details | approved | 'pending', 'reason': 'gateway error', 'details | NO | YES |
| 140 | train | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'network connection timeout' | declined | 'declined', 'reason': 'network connection timeout' | YES | NO |
| 141 | train | The system of rules and practices that governs a local network file stor... | ____.<br>A. Network File System<br>B. Local Area | OS | ____.<br>A. Network File System<br>B. Local Area | NO | YES |
| 142 | train | The widely-used server operating system based on Linux open source codeb... | ____.<br>A. Windows Server 2016 | Linux | ____.<br>A. Windows Server 2016 | NO | YES |
| 143 | train | The default web server software suite designed by the Apache foundation is | known as ____.<br>A. Tomcat<br>B. I | Apache | known as ____.<br>A. Tomcat<br>B. I | NO | YES |
| 144 | train | The high-performance reverse proxy and routing load balancer engine is | a powerful tool for managing traffic on your ne... | Nginx | a powerful tool for managing traffic on your ne... | NO | YES |
| 145 | train | The lightweight operating system-level container virtualization framewor... | ____<br>KVM<br>Xen<br>QEMU<br>V | Docker | ____<br>KVM<br>Xen<br>QEMU<br>V | NO | YES |
| 146 | train | The cluster container orchestration engine developed originally by Googl... | called<br>A. Kubernetes<br>B. Docker<br>C. | Kubernetes | called<br>A. Kubernetes<br>B. Docker<br>C. | YES | NO |
| 147 | train | The Amazon Web Services virtual machine server hosting cloud instance is | a type of cloud computing service that allows u... | EC2 | a type of cloud computing service that allows u... | NO | YES |
| 148 | train | In databases, storing unstructured records across distributed document s... | a common practice. Which of the following state... | NoSQL | a common practice. Which of the following state... | NO | YES |
| 149 | train | The structural design schema defining relational table layout constraint... | ____.<br>A. Data Definition Language<br>B. Data... | schema | ____.<br>A. Data Definition Language<br>B. Data... | NO | YES |
| 150 | train | CSS style sheets acronym stands for Cascading Style | Sheets. It is a set of rules that define the ap... | Sheets | Sheets. It is a set of rules that define the ap... | YES | NO |
| 151 | train | API programming layout acronym stands for Application Programming | Interface. A. Correct B. Incorrect<br>Answer:<b... | Interface | Interface. A. Correct B. Incorrect<br>Answer:<b... | YES | NO |
| 152 | train | URL locate path acronym stands for Uniform Resource | Locator. It is a string that represents the loc... | Locator | Locator. It is a string that represents the loc... | YES | NO |
| 153 | train | JSON data block acronym stands for JavaScript Object | Notation. It is a format used to represent and ... | Notation | Notation. It is a format used to represent and ... | YES | NO |
| 154 | train | XML document layout acronym stands for Extensible Markup | Language. It is a markup language that allows d... | Language | Language. It is a markup language that allows d... | YES | NO |
| 155 | train | SDK development toolkit acronym stands for Software Development | Kit. It is a collection of software components ... | Kit | Kit. It is a collection of software components ... | YES | NO |
| 156 | train | IDE coding interface acronym stands for Integrated Development | Environment. It is a software development envir... | Environment | Environment. It is a software development envir... | YES | NO |
| 157 | train | CPU computer brain acronym stands for Central Processing | Unit. It is the core of a computer and it is | Unit | Unit. It is the core of a computer and it is | YES | NO |
| 158 | train | RAM memory hardware acronym stands for Random Access | Memory. It is a type of computer memory that al... | Memory | Memory. It is a type of computer memory that al... | YES | NO |
| 159 | train | ROM startup hardware acronym stands for Read Only | Memory. It is a type of memory that stores data in | Memory | Memory. It is a type of memory that stores data in | YES | NO |
| 160 | train | SSH terminal connection acronym stands for Secure | Terminal Connection. It is a protocol that allo... | Shell | Terminal Connection. It is a protocol that allo... | NO | YES |
| 161 | train | FTP network upload acronym stands for File Transfer | Protocol. It is a protocol used to transfer fil... | Protocol | Protocol. It is a protocol used to transfer fil... | YES | NO |
| 162 | train | SMTP email delivery acronym stands for Simple Mail Transfer | Protocol. It is a protocol used to transfer ema... | Protocol | Protocol. It is a protocol used to transfer ema... | YES | NO |
| 163 | train | Running matching loops or blocks inside themselves in programming is called | nesting. In this article, we will discuss the s... | recursion | nesting. In this article, we will discuss the s... | NO | YES |
| 164 | train | An error or flaw in the underlying code logic is called a | (n) ________.<br>A. Error<br>B. Bug | bug | (n) ________.<br>A. Error<br>B. Bug | YES | NO |
| 165 | train | Isolating and resolving structural flaws in a codebase is called | :<br><br>A) Code review<br>B) Code optimization... | debugging | :<br><br>A) Code review<br>B) Code optimization... | NO | YES |
| 166 | train | The central computer hardware component responsible for active processin... | ____.<br>A. Arithmetic Logic Unit (ALU)<br>B | CPU | ____.<br>A. Arithmetic Logic Unit (ALU)<br>B | NO | YES |
| 167 | train | The fast volatile memory layer loaded during active task runtime is | called ____.<br>A. Page Table<br>B. Stack Pointer | RAM | called ____.<br>A. Page Table<br>B. Stack Pointer | NO | YES |
| 168 | train | The non-volatile chip storing fundamental startup firmware instructions is | called a(n) ____.<br>A. ROM<br>B. | ROM | called a(n) ____.<br>A. ROM<br>B. | YES | NO |
| 169 | train | The terminal connection protocol allowing secure remote administrative s... | ____<br>SSH<br>HTTP<br>FTP<br>TELNET<br>Answer | SSH | ____<br>SSH<br>HTTP<br>FTP<br>TELNET<br>Answer | YES | NO |
| 170 | train | The internet routing directory system that maps domain names to IPs is | called ____.<br>A. DNS<br>B. FTP<br>C | DNS | called ____.<br>A. DNS<br>B. FTP<br>C | YES | NO |
| 171 | train | The structured query language command used to fetch rows from tables is | ____<br>A. SELECT<br>B. INSERT<br>C. | SELECT | ____<br>A. SELECT<br>B. INSERT<br>C. | YES | NO |
| 172 | train | The structured query language command used to insert new database rows is | ____<br>A. INSERT<br>B. UPDATE<br>C. | INSERT | ____<br>A. INSERT<br>B. UPDATE<br>C. | YES | NO |
| 173 | train | The structured query language command used to alter existing database ro... | ____.<br>A. INSERT<br>B. UPDATE<br>C. | UPDATE | ____.<br>A. INSERT<br>B. UPDATE<br>C. | YES | NO |
| 174 | train | The structured query language command used to delete existing database r... | ____<br>A. DELETE<br>B. INSERT<br>C. | DELETE | ____<br>A. DELETE<br>B. INSERT<br>C. | YES | NO |
| 175 | train | The local virtual network interface loopback address is | ____.<br>A. 127.0.0 | 127.0.0.1 | ____.<br>A. 127.0.0 | NO | YES |
| 176 | train | The standard network port utilized for insecure HTTP web traffic is | :<br>A. 80<br>B. 44 | 80 | :<br>A. 80<br>B. 44 | YES | NO |
| 177 | train | The standard network port utilized for secure HTTPS web traffic is | :<br>A. 443<br>B. 8 | 443 | :<br>A. 443<br>B. 8 | YES | NO |
| 178 | train | The Python script keyword used to pull in external modules is | ____<br>A. from<br>B. import<br>C. | import | ____<br>A. from<br>B. import<br>C. | YES | NO |
| 179 | train | The Python script keyword used to define a new class block is | ____<br>A. def<br>B. class<br>C. | class | ____<br>A. def<br>B. class<br>C. | YES | NO |
| 180 | train | The Python script keyword used to declare a new function block is | ____<br>A. def<br>B. class<br>C. | def | ____<br>A. def<br>B. class<br>C. | YES | NO |
| 181 | train | The Python script keyword used to emit values back from functions is | ____<br>A. def<br>B. return<br>C. | return | ____<br>A. def<br>B. return<br>C. | YES | NO |
| 182 | train | The Python loop keyword used to iterate over fixed sequences is | ____<br>A. for<br>B. while<br>C. | for | ____<br>A. for<br>B. while<br>C. | YES | NO |
| 183 | train | The Python loop keyword used to run loops while conditions hold true is | :<br>A. for<br>B. while<br>C. if | while | :<br>A. for<br>B. while<br>C. if | YES | NO |
| 184 | train | The Python logical boolean variable indicating positivity is | `True` if the number is positive, and `False | True | `True` if the number is positive, and `False | YES | NO |
| 185 | train | The Python logical boolean variable indicating negativity is | ____<br>A. True<br>B. False<br>C. | False | ____<br>A. True<br>B. False<br>C. | YES | NO |
| 186 | train | The Git code versioning command used to save changes locally is git | commit. ____<br>A. Correct<br>B. Incorrect | commit | commit. ____<br>A. Correct<br>B. Incorrect | YES | NO |
| 187 | train | The Git code versioning command used to send changes to remote hosts is git | push. The following are the steps for using thi... | push | push. The following are the steps for using thi... | YES | NO |
| 188 | train | The Git code versioning command used to fetch changes from remote hosts ... | fetch. The syntax for this command is:<br><br>`... | pull | fetch. The syntax for this command is:<br><br>`... | NO | YES |
| 189 | train | Relational database records are structurally organized and stored inside a | table. The data in the table is called a record, | database | table. The data in the table is called a record, | NO | YES |
| 190 | train | The physical database schema detailing model layouts is the | foundation of a database system. Which of the f... | schema | foundation of a database system. Which of the f... | NO | YES |
| 191 | train | In CSS layouts, style rules are applied using Cascading Style | Sheets (CSS). This means that the styles for a ... | Sheets | Sheets (CSS). This means that the styles for a ... | YES | NO |
| 192 | train | In web protocols, the standard layout formatting framework is | known as ____.<br>A. HTML<br>B. CSS | HTML | known as ____.<br>A. HTML<br>B. CSS | YES | NO |
| 193 | train | In web protocols, the API interaction framework is called an | HTTP/HTTPS protocol. A. Correct B. Incorrect | API | HTTP/HTTPS protocol. A. Correct B. Incorrect | NO | YES |
| 194 | train | In web protocols, the location path of resources is a | crucial part. Which of the following statements... | URL | crucial part. Which of the following statements... | NO | YES |
| 195 | train | In web protocols, the structured text format used for data exchanges is | known as:<br>A. HTML<br>B. XML<br>C | JSON | known as:<br>A. HTML<br>B. XML<br>C | NO | YES |
| 196 | train | In web protocols, the extensible markup document layout format is | ____.<br>HTML<br>XML<br>XHTML<br>MIME | XML | ____.<br>HTML<br>XML<br>XHTML<br>MIME | YES | NO |
| 197 | train | The software development tools bundle provided to programmers is an | example of a(n) ________.<br>A. Software | SDK | example of a(n) ________.<br>A. Software | NO | YES |
| 198 | train | The unified development software editor workspace is an | important part of the development environment. ... | IDE | important part of the development environment. ... | YES | NO |
| 199 | train | The primary network protocol standardizing packet layout constraints is | ____<br>A. TCP<br>B. IP<br>C. | IP | ____<br>A. TCP<br>B. IP<br>C. | YES | NO |
| 200 | train | The file transfer protocol standardizing file uploads is | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | YES | NO |
| 201 | seen_val | JSON payload: { 'event': 'FailedLogin', 'username': 'administrator', 'ip... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 202 | seen_val | JSON payload: { 'event': 'FailedLogin', 'username': 'sam_dev', 'ip': '19... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 203 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'dev_test_bot', 'pu... | What is the risk of this event occurring? <br>R... | high | What is the risk of this event occurring? <br>R... | NO | YES |
| 204 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'ops_lead_44', 'pub... | What is the risk of this event occurring? <br>R... | low | What is the risk of this event occurring? <br>R... | NO | YES |
| 205 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'AdministratorAc... | What is the risk of this event occurring? <br>R... | medium | What is the risk of this event occurring? <br>R... | NO | YES |
| 206 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'ReadOnlyAccess'... | What is the risk of this IAM policy modificatio... | medium | What is the risk of this IAM policy modificatio... | NO | YES |
| 207 | seen_val | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '45.33.102.88'... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 208 | seen_val | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '10.0.2.99', '... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 209 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'jenkins_agent_05', 'key... | low<br><br>What is the risk level of this event... | low | low<br><br>What is the risk level of this event... | YES | NO |
| 210 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'unverified_root', 'key_... | low<br><br>What is the risk level of this event... | high | low<br><br>What is the risk level of this event... | NO | YES |
| 211 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Fetch ... | 'GET', 'url': '/api/v1/clusters | get | 'GET', 'url': '/api/v1/clusters | YES | NO |
| 212 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Delete... | 'delete', 'id': 12345 | delete | 'delete', 'id': 12345 | YES | NO |
| 213 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Create... | 'POST', 'data': { 'server_gateway_token': | post | 'POST', 'data': { 'server_gateway_token': | YES | NO |
| 214 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Retrie... | 'GET', 'url': '/api/credit-balance | get | 'GET', 'url': '/api/credit-balance | YES | NO |
| 215 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Regist... | 'GET', 'url': '/webhooks/new-endpoints | post | 'GET', 'url': '/webhooks/new-endpoints | NO | YES |
| 216 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'path': '/backup/storage/directories | delete | 'delete', 'path': '/backup/storage/directories | YES | NO |
| 217 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'List a... | 'GET', 'url': '/api/v1/deploy | get | 'GET', 'url': '/api/v1/deploy | YES | NO |
| 218 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Provis... | 'POST', 'data': {} } To extract the API | post | 'POST', 'data': {} } To extract the API | YES | NO |
| 219 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'data': {} } To extract the API | delete | 'delete', 'data': {} } To extract the API | YES | NO |
| 220 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Fetch ... | 'GET', 'url': '/api/system-baseline-m | get | 'GET', 'url': '/api/system-baseline-m | YES | NO |
| 221 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | admin | 'admin' } The user role is set to admin. | YES | NO |
| 222 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | editor | 'admin' } The user role is set to admin. | NO | YES |
| 223 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 224 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already provided in the | admin | 'admin' } The user role is already provided in the | YES | NO |
| 225 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 226 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 227 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | admin | 'admin' } The user role is set to admin. | YES | NO |
| 228 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 229 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 230 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already specified in... | admin | 'admin' } The user role is already specified in... | YES | NO |
| 231 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'payment successful', 'am... | approved | 'approved', 'reason': 'payment successful', 'am... | YES | NO |
| 232 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'rejected', 'reason': 'user rejected payment re... | declined | 'rejected', 'reason': 'user rejected payment re... | NO | YES |
| 233 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'CVV verification mismatch | declined | 'declined', 'reason': 'CVV verification mismatch | YES | NO |
| 234 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'batch capture successful... | approved | 'approved', 'reason': 'batch capture successful... | YES | NO |
| 235 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'risk limit exceeded' | declined | 'declined', 'reason': 'risk limit exceeded' | YES | NO |
| 236 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'user cancelled billing c... | declined | 'declined', 'reason': 'user cancelled billing c... | YES | NO |
| 237 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': '' } Here is the extracted | approved | 'approved', 'reason': '' } Here is the extracted | YES | NO |
| 238 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'block detected in payment | declined | 'declined', 'reason': 'block detected in payment | YES | NO |
| 239 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'pending', 'reason': 'gateway error', 'details | approved | 'pending', 'reason': 'gateway error', 'details | NO | YES |
| 240 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'network connection timeout' | declined | 'declined', 'reason': 'network connection timeout' | YES | NO |
| 241 | seen_val | To accomplish multiple milestones at the exact same moment is to kill tw... | stone. This is a common strategy used by many p... | stone | stone. This is a common strategy used by many p... | YES | NO |
| 242 | seen_val | To avoid placing all your financial capital in a single volatile asset, ... | basket. Instead, diversify your investments acr... | basket | basket. Instead, diversify your investments acr... | YES | NO |
| 243 | seen_val | To accidentally reveal highly confidential organization blueprints is to... | bag. This is a common occurrence in many organi... | bag | bag. This is a common occurrence in many organi... | YES | NO |
| 244 | seen_val | Being in a state of supreme, ecstatic joy or extreme mental happiness is... | nine. This feeling can come from many different... | nine | nine. This feeling can come from many different... | YES | NO |
| 245 | seen_val | Feeling entirely awkward, uncomfortable, and physically out of place is ... | water. It can be very embarrassing to feel this... | water | water. It can be very embarrassing to feel this... | YES | NO |
| 246 | seen_val | An unpredictable, incredibly dynamic, and highly energetic person is des... | action film director. This type of person can b... | wire | action film director. This type of person can b... | NO | YES |
| 247 | seen_val | An entirely random, highly surprising, and completely unexpected event i... | ordinary. It's a situation that has never happe... | blue | ordinary. It's a situation that has never happe... | NO | YES |
| 248 | seen_val | Pursuing a completely incorrect strategy or line of logic is barking up ... | tree. The goal should be to find a way to solve | tree | tree. The goal should be to find a way to solve | YES | NO |
| 249 | seen_val | Facing a very difficult, painful, or awkward situation with brave compos... | bullet. The act of biting the bullet can be don... | bullet | bullet. The act of biting the bullet can be don... | YES | NO |
| 250 | seen_val | Wishing a theater actor excellent performance fortune right before a sho... | promise. The actor breaks the promise and gets ... | leg | promise. The actor breaks the promise and gets ... | NO | YES |
| 251 | seen_val | To accidentally expose a highly guarded organizational secret is to spil... | beans. This is an example of which type of logi... | beans | beans. This is an example of which type of logi... | YES | NO |
| 252 | seen_val | Executing an operational workflow that is incredibly straightforward is ... | cake. However, when it comes to creating a work... | cake | cake. However, when it comes to creating a work... | YES | NO |
| 253 | seen_val | Resolving an architectural software bottleneck with absolute precision i... | head. The software that I am working on has a very | head | head. The software that I am working on has a very | YES | NO |
| 254 | seen_val | To accept the negative consequences of your previous incorrect actions i... | reality that you are not a good person. This st... | music | reality that you are not a good person. This st... | NO | YES |
| 255 | seen_val | Feeling mildly sick, fatigued, or physically under the weather is to be ... | care of a doctor. The doctor will examine you a... | weather | care of a doctor. The doctor will examine you a... | NO | YES |
| 256 | seen_val | To completely cease working on a development pipeline for the evening is... | day. The development pipeline is a series of st... | day | day. The development pipeline is a series of st... | YES | NO |
| 257 | seen_val | Complaining about unfixable, past execution errors is crying over spilled | milk. This is a common complaint from users of ... | milk | milk. This is a common complaint from users of ... | YES | NO |
| 258 | seen_val | Avoiding speaking about the central, most critical problem in a meeting ... | bush. It’s not just a matter of being polite or | bush | bush. It’s not just a matter of being polite or | YES | NO |
| 259 | seen_val | To initiate a highly difficult, tense, or awkward discussion with collea... | rules of social etiquette. The most appropriate... | ice | rules of social etiquette. The most appropriate... | NO | YES |
| 260 | seen_val | Adding angry, volatile statements to an ongoing administrative dispute i... | fire. The problem of conflict resolution in org... | fire | fire. The problem of conflict resolution in org... | YES | NO |
| 261 | seen_val | The system of rules and practices that governs a local network file stor... | ____.<br>A. Network File System<br>B. Local Area | OS | ____.<br>A. Network File System<br>B. Local Area | NO | YES |
| 262 | seen_val | The widely-used server operating system based on Linux open source codeb... | ____.<br>A. Windows Server 2016 | Linux | ____.<br>A. Windows Server 2016 | NO | YES |
| 263 | seen_val | The default web server software suite designed by the Apache foundation is | known as ____.<br>A. Tomcat<br>B. I | Apache | known as ____.<br>A. Tomcat<br>B. I | NO | YES |
| 264 | seen_val | The high-performance reverse proxy and routing load balancer engine is | a powerful tool for managing traffic on your ne... | Nginx | a powerful tool for managing traffic on your ne... | NO | YES |
| 265 | seen_val | The lightweight operating system-level container virtualization framewor... | ____<br>KVM<br>Xen<br>QEMU<br>V | Docker | ____<br>KVM<br>Xen<br>QEMU<br>V | NO | YES |
| 266 | seen_val | The cluster container orchestration engine developed originally by Googl... | called<br>A. Kubernetes<br>B. Docker<br>C. | Kubernetes | called<br>A. Kubernetes<br>B. Docker<br>C. | YES | NO |
| 267 | seen_val | The Amazon Web Services virtual machine server hosting cloud instance is | a type of cloud computing service that allows u... | EC2 | a type of cloud computing service that allows u... | NO | YES |
| 268 | seen_val | In databases, storing unstructured records across distributed document s... | a common practice. Which of the following state... | NoSQL | a common practice. Which of the following state... | NO | YES |
| 269 | seen_val | The structural design schema defining relational table layout constraint... | ____.<br>A. Data Definition Language<br>B. Data... | schema | ____.<br>A. Data Definition Language<br>B. Data... | NO | YES |
| 270 | seen_val | CSS style sheets acronym stands for Cascading Style | Sheets. It is a set of rules that define the ap... | Sheets | Sheets. It is a set of rules that define the ap... | YES | NO |
| 271 | seen_val | API programming layout acronym stands for Application Programming | Interface. A. Correct B. Incorrect<br>Answer:<b... | Interface | Interface. A. Correct B. Incorrect<br>Answer:<b... | YES | NO |
| 272 | seen_val | URL locate path acronym stands for Uniform Resource | Locator. It is a string that represents the loc... | Locator | Locator. It is a string that represents the loc... | YES | NO |
| 273 | seen_val | JSON data block acronym stands for JavaScript Object | Notation. It is a format used to represent and ... | Notation | Notation. It is a format used to represent and ... | YES | NO |
| 274 | seen_val | XML document layout acronym stands for Extensible Markup | Language. It is a markup language that allows d... | Language | Language. It is a markup language that allows d... | YES | NO |
| 275 | seen_val | SDK development toolkit acronym stands for Software Development | Kit. It is a collection of software components ... | Kit | Kit. It is a collection of software components ... | YES | NO |
| 276 | seen_val | IDE coding interface acronym stands for Integrated Development | Environment. It is a software development envir... | Environment | Environment. It is a software development envir... | YES | NO |
| 277 | seen_val | CPU computer brain acronym stands for Central Processing | Unit. It is the core of a computer and it is | Unit | Unit. It is the core of a computer and it is | YES | NO |
| 278 | seen_val | RAM memory hardware acronym stands for Random Access | Memory. It is a type of computer memory that al... | Memory | Memory. It is a type of computer memory that al... | YES | NO |
| 279 | seen_val | ROM startup hardware acronym stands for Read Only | Memory. It is a type of memory that stores data in | Memory | Memory. It is a type of memory that stores data in | YES | NO |
| 280 | seen_val | SSH terminal connection acronym stands for Secure | Terminal Connection. It is a protocol that allo... | Shell | Terminal Connection. It is a protocol that allo... | NO | YES |
| 281 | seen_val | FTP network upload acronym stands for File Transfer | Protocol. It is a protocol used to transfer fil... | Protocol | Protocol. It is a protocol used to transfer fil... | YES | NO |
| 282 | seen_val | SMTP email delivery acronym stands for Simple Mail Transfer | Protocol. It is a protocol used to transfer ema... | Protocol | Protocol. It is a protocol used to transfer ema... | YES | NO |
| 283 | seen_val | Running matching loops or blocks inside themselves in programming is called | nesting. In this article, we will discuss the s... | recursion | nesting. In this article, we will discuss the s... | NO | YES |
| 284 | seen_val | An error or flaw in the underlying code logic is called a | (n) ________.<br>A. Error<br>B. Bug | bug | (n) ________.<br>A. Error<br>B. Bug | YES | NO |
| 285 | seen_val | Isolating and resolving structural flaws in a codebase is called | :<br><br>A) Code review<br>B) Code optimization... | debugging | :<br><br>A) Code review<br>B) Code optimization... | NO | YES |
| 286 | seen_val | The central computer hardware component responsible for active processin... | ____.<br>A. Arithmetic Logic Unit (ALU)<br>B | CPU | ____.<br>A. Arithmetic Logic Unit (ALU)<br>B | NO | YES |
| 287 | seen_val | The fast volatile memory layer loaded during active task runtime is | called ____.<br>A. Page Table<br>B. Stack Pointer | RAM | called ____.<br>A. Page Table<br>B. Stack Pointer | NO | YES |
| 288 | seen_val | The non-volatile chip storing fundamental startup firmware instructions is | called a(n) ____.<br>A. ROM<br>B. | ROM | called a(n) ____.<br>A. ROM<br>B. | YES | NO |
| 289 | seen_val | The terminal connection protocol allowing secure remote administrative s... | ____<br>SSH<br>HTTP<br>FTP<br>TELNET<br>Answer | SSH | ____<br>SSH<br>HTTP<br>FTP<br>TELNET<br>Answer | YES | NO |
| 290 | seen_val | The internet routing directory system that maps domain names to IPs is | called ____.<br>A. DNS<br>B. FTP<br>C | DNS | called ____.<br>A. DNS<br>B. FTP<br>C | YES | NO |
| 291 | seen_val | The structured query language command used to fetch rows from tables is | ____<br>A. SELECT<br>B. INSERT<br>C. | SELECT | ____<br>A. SELECT<br>B. INSERT<br>C. | YES | NO |
| 292 | seen_val | The structured query language command used to insert new database rows is | ____<br>A. INSERT<br>B. UPDATE<br>C. | INSERT | ____<br>A. INSERT<br>B. UPDATE<br>C. | YES | NO |
| 293 | seen_val | The structured query language command used to alter existing database ro... | ____.<br>A. INSERT<br>B. UPDATE<br>C. | UPDATE | ____.<br>A. INSERT<br>B. UPDATE<br>C. | YES | NO |
| 294 | seen_val | The structured query language command used to delete existing database r... | ____<br>A. DELETE<br>B. INSERT<br>C. | DELETE | ____<br>A. DELETE<br>B. INSERT<br>C. | YES | NO |
| 295 | seen_val | The local virtual network interface loopback address is | ____.<br>A. 127.0.0 | 127.0.0.1 | ____.<br>A. 127.0.0 | NO | YES |
| 296 | seen_val | The standard network port utilized for insecure HTTP web traffic is | :<br>A. 80<br>B. 44 | 80 | :<br>A. 80<br>B. 44 | YES | NO |
| 297 | seen_val | The standard network port utilized for secure HTTPS web traffic is | :<br>A. 443<br>B. 8 | 443 | :<br>A. 443<br>B. 8 | YES | NO |
| 298 | seen_val | The Python script keyword used to pull in external modules is | ____<br>A. from<br>B. import<br>C. | import | ____<br>A. from<br>B. import<br>C. | YES | NO |
| 299 | seen_val | The Python script keyword used to define a new class block is | ____<br>A. def<br>B. class<br>C. | class | ____<br>A. def<br>B. class<br>C. | YES | NO |
| 300 | seen_val | The Python script keyword used to declare a new function block is | ____<br>A. def<br>B. class<br>C. | def | ____<br>A. def<br>B. class<br>C. | YES | NO |
| 301 | seen_val | The Python script keyword used to emit values back from functions is | ____<br>A. def<br>B. return<br>C. | return | ____<br>A. def<br>B. return<br>C. | YES | NO |
| 302 | seen_val | The Python loop keyword used to iterate over fixed sequences is | ____<br>A. for<br>B. while<br>C. | for | ____<br>A. for<br>B. while<br>C. | YES | NO |
| 303 | seen_val | The Python loop keyword used to run loops while conditions hold true is | :<br>A. for<br>B. while<br>C. if | while | :<br>A. for<br>B. while<br>C. if | YES | NO |
| 304 | seen_val | The Python logical boolean variable indicating positivity is | `True` if the number is positive, and `False | True | `True` if the number is positive, and `False | YES | NO |
| 305 | seen_val | The Python logical boolean variable indicating negativity is | ____<br>A. True<br>B. False<br>C. | False | ____<br>A. True<br>B. False<br>C. | YES | NO |
| 306 | seen_val | The Git code versioning command used to save changes locally is git | commit. ____<br>A. Correct<br>B. Incorrect | commit | commit. ____<br>A. Correct<br>B. Incorrect | YES | NO |
| 307 | seen_val | The Git code versioning command used to send changes to remote hosts is git | push. The following are the steps for using thi... | push | push. The following are the steps for using thi... | YES | NO |
| 308 | seen_val | The Git code versioning command used to fetch changes from remote hosts ... | fetch. The syntax for this command is:<br><br>`... | pull | fetch. The syntax for this command is:<br><br>`... | NO | YES |
| 309 | seen_val | Relational database records are structurally organized and stored inside a | table. The data in the table is called a record, | database | table. The data in the table is called a record, | NO | YES |
| 310 | seen_val | The physical database schema detailing model layouts is the | foundation of a database system. Which of the f... | schema | foundation of a database system. Which of the f... | NO | YES |
| 311 | seen_val | In CSS layouts, style rules are applied using Cascading Style | Sheets (CSS). This means that the styles for a ... | Sheets | Sheets (CSS). This means that the styles for a ... | YES | NO |
| 312 | seen_val | In web protocols, the standard layout formatting framework is | known as ____.<br>A. HTML<br>B. CSS | HTML | known as ____.<br>A. HTML<br>B. CSS | YES | NO |
| 313 | seen_val | In web protocols, the API interaction framework is called an | HTTP/HTTPS protocol. A. Correct B. Incorrect | API | HTTP/HTTPS protocol. A. Correct B. Incorrect | NO | YES |
| 314 | seen_val | In web protocols, the location path of resources is a | crucial part. Which of the following statements... | URL | crucial part. Which of the following statements... | NO | YES |
| 315 | seen_val | In web protocols, the structured text format used for data exchanges is | known as:<br>A. HTML<br>B. XML<br>C | JSON | known as:<br>A. HTML<br>B. XML<br>C | NO | YES |
| 316 | seen_val | In web protocols, the extensible markup document layout format is | ____.<br>HTML<br>XML<br>XHTML<br>MIME | XML | ____.<br>HTML<br>XML<br>XHTML<br>MIME | YES | NO |
| 317 | seen_val | The software development tools bundle provided to programmers is an | example of a(n) ________.<br>A. Software | SDK | example of a(n) ________.<br>A. Software | NO | YES |
| 318 | seen_val | The unified development software editor workspace is an | important part of the development environment. ... | IDE | important part of the development environment. ... | YES | NO |
| 319 | seen_val | The primary network protocol standardizing packet layout constraints is | ____<br>A. TCP<br>B. IP<br>C. | IP | ____<br>A. TCP<br>B. IP<br>C. | YES | NO |
| 320 | seen_val | The file transfer protocol standardizing file uploads is | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | YES | NO |
| 321 | seen_val | The file transfer protocol standardizing files transfer is | ____<br>FTP<br>HTTP<br>SMTP<br>TCP<br>Answer: | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>TCP<br>Answer: | YES | NO |
| 322 | seen_val | The file transfer protocol standardizing files download is | ____<br>FTP<br>HTTP<br>SMTP<br>TCP<br>Answer: | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>TCP<br>Answer: | YES | NO |
| 323 | seen_val | The file transfer protocol standardizing folders upload is | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | YES | NO |
| 324 | seen_val | The file transfer protocol standardizing folders transfer is | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | YES | NO |
| 325 | seen_val | The file transfer protocol standardizing folders download is | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<br>Answer | YES | NO |
| 326 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'Electronics', 'product_category': 'Apparel', | electronics | 'Electronics', 'product_category': 'Apparel', | YES | NO |
| 327 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 328 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 329 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 330 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 331 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'Electronics', 'category': 'Apparel', ' | apparel | 'Electronics', 'category': 'Apparel', ' | YES | NO |
| 332 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 333 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 334 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | apparel | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 335 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 336 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 337 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 338 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | electronics | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 339 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 340 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 341 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 342 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 343 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 344 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | electronics | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 345 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 346 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 347 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 348 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 349 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 350 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | electronics | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 351 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 352 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | apparel | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 353 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 354 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 355 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 356 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 357 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 358 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 359 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | electronics | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 360 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 361 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 362 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | electronics | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 363 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 364 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 365 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 366 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 52 } The heart | bradycardia | 'normal', 'rate': 52 } The heart | NO | YES |
| 367 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 112 } The | tachycardia | 'normal', 'rate': 112 } The | NO | YES |
| 368 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 72 } The heart | normal | 'normal', 'rate': 72 } The heart | YES | NO |
| 369 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 48 } The heart | bradycardia | 'normal', 'rate': 48 } The heart | NO | YES |
| 370 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 125 } The | tachycardia | 'normal', 'rate': 125 } The | NO | YES |
| 371 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 80 } The heart | normal | 'normal', 'rate': 80 } The heart | YES | NO |
| 372 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 55 } The heart | bradycardia | 'normal', 'rate': 55 } The heart | NO | YES |
| 373 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 105 } The | tachycardia | 'normal', 'rate': 105 } The | NO | YES |
| 374 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 65 } The heart | normal | 'normal', 'rate': 65 } The heart | YES | NO |
| 375 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 50 } The heart | bradycardia | 'normal', 'rate': 50 } The heart | NO | YES |
| 376 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 118 } The | tachycardia | 'normal', 'rate': 118 } The | NO | YES |
| 377 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 75 } The heart | normal | 'normal', 'rate': 75 } The heart | YES | NO |
| 378 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 58 } The heart | bradycardia | 'normal', 'rate': 58 } The heart | NO | YES |
| 379 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 130 } The | tachycardia | 'normal', 'rate': 130 } The | NO | YES |
| 380 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 85 } The heart | normal | 'normal', 'rate': 85 } The heart | YES | NO |
| 381 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 45 } The heart | bradycardia | 'normal', 'rate': 45 } The heart | NO | YES |
| 382 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 115 } The | tachycardia | 'normal', 'rate': 115 } The | NO | YES |
| 383 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 90 } The heart | normal | 'normal', 'rate': 90 } The heart | YES | NO |
| 384 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 53 } The heart | bradycardia | 'normal', 'rate': 53 } The heart | NO | YES |
| 385 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 110 } The | tachycardia | 'normal', 'rate': 110 } The | NO | YES |
| 386 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 70 } The heart | normal | 'normal', 'rate': 70 } The heart | YES | NO |
| 387 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 51 } The heart | bradycardia | 'normal', 'rate': 51 } The heart | NO | YES |
| 388 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 122 } The | tachycardia | 'normal', 'rate': 122 } The | NO | YES |
| 389 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 68 } The heart | normal | 'normal', 'rate': 68 } The heart | YES | NO |
| 390 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 49 } The heart | bradycardia | 'normal', 'rate': 49 } The heart | NO | YES |
| 391 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 108 } The | tachycardia | 'normal', 'rate': 108 } The | NO | YES |
| 392 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 78 } The heart | normal | 'normal', 'rate': 78 } The heart | YES | NO |
| 393 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 56 } The heart | bradycardia | 'normal', 'rate': 56 } The heart | NO | YES |
| 394 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 120 } The | tachycardia | 'normal', 'rate': 120 } The | NO | YES |
| 395 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 74 } The heart | normal | 'normal', 'rate': 74 } The heart | YES | NO |
| 396 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 57 } The heart | bradycardia | 'normal', 'rate': 57 } The heart | NO | YES |
| 397 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 128 } The | tachycardia | 'normal', 'rate': 128 } The | NO | YES |
| 398 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 88 } The heart | normal | 'normal', 'rate': 88 } The heart | YES | NO |
| 399 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 54 } The heart | bradycardia | 'normal', 'rate': 54 } The heart | NO | YES |
| 400 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 116 } The | tachycardia | 'normal', 'rate': 116 } The | NO | YES |
| 401 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 82 } The heart | normal | 'normal', 'rate': 82 } The heart | YES | NO |
| 402 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 47 } The heart | bradycardia | 'normal', 'rate': 47 } The heart | NO | YES |
| 403 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 124 } The | tachycardia | 'normal', 'rate': 124 } The | NO | YES |
| 404 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 76 } The heart | normal | 'normal', 'rate': 76 } The heart | YES | NO |
| 405 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 59 } The heart | bradycardia | 'normal', 'rate': 59 } The heart | NO | YES |
| 406 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 407 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 408 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 409 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | NO | YES |
| 410 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '172. | private | 'private', 'cidr': '172. | YES | NO |
| 411 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | private | 'private', 'description': 'Allow all traffic on... | YES | NO |
| 412 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'public' } The security group access level is p... | public | 'public' } The security group access level is p... | YES | NO |
| 413 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'public', 'cidr': '0.0. | public | 'public', 'cidr': '0.0. | YES | NO |
| 414 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'rule_id': '18', ' | private | 'private', 'rule_id': '18', ' | YES | NO |
| 415 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'public' } The security group access level is p... | public | 'public' } The security group access level is p... | YES | NO |
| 416 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 417 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 418 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '172. | private | 'private', 'cidr': '172. | YES | NO |
| 419 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '172. | private | 'private', 'cidr': '172. | YES | NO |
| 420 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 421 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '172. | private | 'private', 'cidr': '172. | YES | NO |
| 422 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 423 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 424 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 425 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 426 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 427 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 428 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 429 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | private | 'private', 'description': 'Allow all traffic on... | YES | NO |
| 430 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 431 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 432 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | NO | YES |
| 433 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 434 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | NO | YES |
| 435 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 436 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | NO | YES |
| 437 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 438 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | NO | YES |
| 439 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 440 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | NO | YES |
| 441 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 442 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'protocol': 'tcp', 'source_address | public | 'private', 'protocol': 'tcp', 'source_address | NO | YES |
| 443 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 444 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 445 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | private | 'private', 'description': 'Allow all traffic on... | YES | NO |
| 446 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 447 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 448 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Port 590 | public | 'private', 'description': 'Port 590 | NO | YES |
| 449 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Port 590 | private | 'private', 'description': 'Port 590 | YES | NO |
| 450 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 451 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 452 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high oxygen pressure, | stable | 'unstable', 'reason': 'high oxygen pressure, | YES | NO |
| 453 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 454 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 455 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 456 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 457 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 458 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 459 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 460 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 461 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 462 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 463 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 464 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high oxygen pressure, | stable | 'unstable', 'reason': 'high oxygen pressure, | YES | NO |
| 465 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 466 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 467 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 468 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 469 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 470 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 471 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 472 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 473 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 474 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 475 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 476 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 477 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 478 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 479 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 480 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 481 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 482 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 483 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 484 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 485 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 486 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 487 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 488 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 489 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 490 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 491 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 492 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 493 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 494 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 495 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 496 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 497 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 498 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 499 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 500 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
