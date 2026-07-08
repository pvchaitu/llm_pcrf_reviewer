# Baseline-Only Evaluation Report

## Execution Mode
- Run Mode: full
- PCRF Components Executed: Yes
- SFT Candidate Regularization Executed: Yes
- Protected Router Executed: Yes

## Dataset Source
- Dataset Source: External File
- Dataset File: another-dataset.csv

## Dataset Partition Counts
- Train Split: 100
- Seen Validation Split: 40
- Unseen Validation Split: 40
- OOD Split: 20
- Total Rows Audited: 200

## Baseline Metrics
- model_name: Qwen/Qwen2.5-0.5B-Instruct
- seen_val_acc: 0.675
- unseen_val_acc: 0.675
- seen_val_nll: 11.064453125
- unseen_val_nll: 9.292279411764707
- seen_val_ppl: 63860.297507269155
- unseen_val_ppl: 10853.896422306496

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
| 101 | seen_val | JSON payload: { 'event': 'FailedLogin', 'username': 'administrator', 'ip... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 102 | seen_val | JSON payload: { 'event': 'FailedLogin', 'username': 'sam_dev', 'ip': '19... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 103 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'dev_test_bot', 'pu... | What is the risk of this event occurring? <br>R... | high | What is the risk of this event occurring? <br>R... | NO | YES |
| 104 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'owner': 'ops_lead_44', 'pub... | What is the risk of this event occurring? <br>R... | low | What is the risk of this event occurring? <br>R... | NO | YES |
| 105 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'AdministratorAc... | What is the risk of this event occurring? <br>R... | medium | What is the risk of this event occurring? <br>R... | NO | YES |
| 106 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', 'policy': 'ReadOnlyAccess'... | What is the risk of this IAM policy modificatio... | medium | What is the risk of this IAM policy modificatio... | NO | YES |
| 107 | seen_val | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '45.33.102.88'... | low<br><br>What is the risk level of this incid... | high | low<br><br>What is the risk level of this incid... | NO | YES |
| 108 | seen_val | JSON payload: { 'event': 'PortScanDetected', 'source_ip': '10.0.2.99', '... | low<br><br>What is the risk level of this incid... | low | low<br><br>What is the risk level of this incid... | YES | NO |
| 109 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'jenkins_agent_05', 'key... | low<br><br>What is the risk level of this event... | low | low<br><br>What is the risk level of this event... | YES | NO |
| 110 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user': 'unverified_root', 'key_... | low<br><br>What is the risk level of this event... | high | low<br><br>What is the risk level of this event... | NO | YES |
| 111 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Fetch ... | 'GET', 'url': '/api/v1/clusters | get | 'GET', 'url': '/api/v1/clusters | YES | NO |
| 112 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Delete... | 'delete', 'id': 12345 | delete | 'delete', 'id': 12345 | YES | NO |
| 113 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Create... | 'POST', 'data': { 'server_gateway_token': | post | 'POST', 'data': { 'server_gateway_token': | YES | NO |
| 114 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Retrie... | 'GET', 'url': '/api/credit-balance | get | 'GET', 'url': '/api/credit-balance | YES | NO |
| 115 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Regist... | 'GET', 'url': '/webhooks/new-endpoints | post | 'GET', 'url': '/webhooks/new-endpoints | NO | YES |
| 116 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'path': '/backup/storage/directories | delete | 'delete', 'path': '/backup/storage/directories | YES | NO |
| 117 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'List a... | 'GET', 'url': '/api/v1/deploy | get | 'GET', 'url': '/api/v1/deploy | YES | NO |
| 118 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Provis... | 'POST', 'data': {} } To extract the API | post | 'POST', 'data': {} } To extract the API | YES | NO |
| 119 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Erase ... | 'delete', 'data': {} } To extract the API | delete | 'delete', 'data': {} } To extract the API | YES | NO |
| 120 | seen_val | Extract the API action (get/post/delete) from this routing rule: 'Fetch ... | 'GET', 'url': '/api/system-baseline-m | get | 'GET', 'url': '/api/system-baseline-m | YES | NO |
| 121 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | admin | 'admin' } The user role is set to admin. | YES | NO |
| 122 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | editor | 'admin' } The user role is set to admin. | NO | YES |
| 123 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 124 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already provided in the | admin | 'admin' } The user role is already provided in the | YES | NO |
| 125 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 126 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 127 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is set to admin. | admin | 'admin' } The user role is set to admin. | YES | NO |
| 128 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | editor | 'viewer' } The user role is viewer. Here's | NO | YES |
| 129 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. Here's | YES | NO |
| 130 | seen_val | Extract the user role (admin/editor/viewer) from this permission string:... | 'admin' } The user role is already specified in... | admin | 'admin' } The user role is already specified in... | YES | NO |
| 131 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'payment successful', 'am... | approved | 'approved', 'reason': 'payment successful', 'am... | YES | NO |
| 132 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'rejected', 'reason': 'user rejected payment re... | declined | 'rejected', 'reason': 'user rejected payment re... | NO | YES |
| 133 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'CVV verification mismatch | declined | 'declined', 'reason': 'CVV verification mismatch | YES | NO |
| 134 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'batch capture successful... | approved | 'approved', 'reason': 'batch capture successful... | YES | NO |
| 135 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'risk limit exceeded' | declined | 'declined', 'reason': 'risk limit exceeded' | YES | NO |
| 136 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'user cancelled billing c... | declined | 'declined', 'reason': 'user cancelled billing c... | YES | NO |
| 137 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': '' } Here is the extracted | approved | 'approved', 'reason': '' } Here is the extracted | YES | NO |
| 138 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'block detected in payment | declined | 'declined', 'reason': 'block detected in payment | YES | NO |
| 139 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'pending', 'reason': 'gateway error', 'details | approved | 'pending', 'reason': 'gateway error', 'details | NO | YES |
| 140 | seen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'network connection timeout' | declined | 'declined', 'reason': 'network connection timeout' | YES | NO |
| 141 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'Electronics', 'product_category': 'Apparel', | electronics | 'Electronics', 'product_category': 'Apparel', | YES | NO |
| 142 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | apparel | 'electronics', 'category': 'apparel', 'sub | YES | NO |
| 143 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 144 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 145 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 146 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'Electronics', 'category': 'Apparel', ' | apparel | 'Electronics', 'category': 'Apparel', ' | YES | NO |
| 147 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 148 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'category': 'apparel', 'sub | home | 'electronics', 'category': 'apparel', 'sub | NO | YES |
| 149 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | apparel | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 150 | unseen_val | Extract the product department (electronics/apparel/home) from this item... | 'electronics', 'product_category': 'apparel', ' | electronics | 'electronics', 'product_category': 'apparel', ' | YES | NO |
| 151 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 52 } The heart | bradycardia | 'normal', 'rate': 52 } The heart | NO | YES |
| 152 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 112 } The | tachycardia | 'normal', 'rate': 112 } The | NO | YES |
| 153 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 72 } The heart | normal | 'normal', 'rate': 72 } The heart | YES | NO |
| 154 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 48 } The heart | bradycardia | 'normal', 'rate': 48 } The heart | NO | YES |
| 155 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 125 } The | tachycardia | 'normal', 'rate': 125 } The | NO | YES |
| 156 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 80 } The heart | normal | 'normal', 'rate': 80 } The heart | YES | NO |
| 157 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 55 } The heart | bradycardia | 'normal', 'rate': 55 } The heart | NO | YES |
| 158 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 105 } The | tachycardia | 'normal', 'rate': 105 } The | NO | YES |
| 159 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 65 } The heart | normal | 'normal', 'rate': 65 } The heart | YES | NO |
| 160 | unseen_val | Extract the heart rate status (normal/bradycardia/tachycardia) from this... | 'normal', 'rate': 50 } The heart | bradycardia | 'normal', 'rate': 50 } The heart | NO | YES |
| 161 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | public | 'private', 'description': 'Allow all traffic on... | NO | YES |
| 162 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '10.0 | private | 'private', 'cidr': '10.0 | YES | NO |
| 163 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '192. | private | 'private', 'cidr': '192. | YES | NO |
| 164 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | NO | YES |
| 165 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'cidr': '172. | private | 'private', 'cidr': '172. | YES | NO |
| 166 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'description': 'Allow all traffic on... | private | 'private', 'description': 'Allow all traffic on... | YES | NO |
| 167 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'public' } The security group access level is p... | public | 'public' } The security group access level is p... | YES | NO |
| 168 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'public', 'cidr': '0.0. | public | 'public', 'cidr': '0.0. | YES | NO |
| 169 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'private', 'rule_id': '18', ' | private | 'private', 'rule_id': '18', ' | YES | NO |
| 170 | unseen_val | Extract the security group access level (public/private) from this rule:... | 'public' } The security group access level is p... | public | 'public' } The security group access level is p... | YES | NO |
| 171 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'billing address postcode... | declined | 'declined', 'reason': 'billing address postcode... | YES | NO |
| 172 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': '' } The transaction stat... | approved | 'approved', 'reason': '' } The transaction stat... | YES | NO |
| 173 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'card expired' } | declined | 'declined', 'reason': 'card expired' } | YES | NO |
| 174 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'no reason provided'} The | declined | 'approved', 'reason': 'no reason provided'} The | NO | YES |
| 175 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'message': 'Batch captured successf... | approved | 'approved', 'message': 'Batch captured successf... | YES | NO |
| 176 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'Insufficient credit limit | declined | 'declined', 'reason': 'Insufficient credit limit | YES | NO |
| 177 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'message': 'Transaction successful.... | approved | 'approved', 'message': 'Transaction successful.... | YES | NO |
| 178 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'capture approved'} The t... | approved | 'approved', 'reason': 'capture approved'} The t... | YES | NO |
| 179 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'declined', 'reason': 'card stolen' } | declined | 'declined', 'reason': 'card stolen' } | YES | NO |
| 180 | unseen_val | Extract the transaction status (approved/declined) from this gateway log... | 'approved', 'reason': 'authorized by merchant o... | approved | 'approved', 'reason': 'authorized by merchant o... | YES | NO |
| 181 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 182 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high oxygen pressure, | stable | 'unstable', 'reason': 'high oxygen pressure, | YES | NO |
| 183 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 184 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 185 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 186 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 187 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 188 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 189 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 190 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 191 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 192 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 193 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 194 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high oxygen pressure, | stable | 'unstable', 'reason': 'high oxygen pressure, | YES | NO |
| 195 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 196 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 197 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 198 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 199 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | unstable | 'unstable', 'reason': 'high pressure or high | YES | NO |
| 200 | ood | Extract the engine combustion state (stable/unstable) from this rocket t... | 'unstable', 'reason': 'high pressure or high | stable | 'unstable', 'reason': 'high pressure or high | YES | NO |
