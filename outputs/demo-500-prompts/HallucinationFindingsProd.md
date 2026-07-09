# 🛡️ Production Zero-Shot Hallucination Findings

### 📖 How to Interpret This Report
This report simulates how the PCRF Hybrid Ensemble operates in a **purely unsupervised production environment** (Zero-Shot), where ground-truth answers are completely unavailable.

The ensemble uses an **OR Gate** to maximize safety:
- **Inference Math (Token Risk):** Flags localized hesitation if structural entropy/margin risk exceeds `0.34`.
- **Curriculum Math (Sequence Implausibility):** Flags unnatural sequences if NLL exceeds `7.69`.
- **Hybrid Ensemble:** If *either* signal is triggered, the output is classified as a hallucination risk and the response is safely withheld.

**Current Calibration:** Adaptive K-Factor (StdDev) [K=0.50] -> Inference Risk (HR) > 0.34, Curriculum NLL > 7.69
> 💡 **Fine-Tuning Notice:** Please refer to `critical_observations.txt` to review the optimization sweeps for Z-Score and K-Factor. You can use those audits to fine-tune your risk appetite (Catch Rate vs. False Positives).

| ID | Split | Prompt | Served Generation Hybrid | Expected Value | Actual Value | Detected By Inference Math | Detected By Curriculum Math | Detected By Hybrid |
|----|-------|--------|--------------------------|----------------|--------------|----------------------------|-----------------------------|--------------------|
| 201 | seen_val | JSON payload: { 'event': 'FailedLogin', 'userna... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | low<br><br>What is the risk level of ... | True | False | True |
| 202 | seen_val | JSON payload: { 'event': 'FailedLogin', 'userna... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | low<br><br>What is the risk level of ... | True | False | True |
| 203 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'ow... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | What is the risk of this event occurr... | True | False | True |
| 204 | seen_val | JSON payload: { 'event': 'S3BucketCreated', 'ow... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | What is the risk of this event occurr... | True | False | True |
| 205 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', '... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | medium | What is the risk of this event occurr... | True | True | True |
| 206 | seen_val | JSON payload: { 'event': 'IAMPolicyModified', '... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | medium | What is the risk of this event occurr... | True | False | True |
| 207 | seen_val | JSON payload: { 'event': 'PortScanDetected', 's... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | low<br><br>What is the risk level of ... | True | False | True |
| 208 | seen_val | JSON payload: { 'event': 'PortScanDetected', 's... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | low<br><br>What is the risk level of ... | True | False | True |
| 209 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user':... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | low | low<br><br>What is the risk level of ... | True | False | True |
| 210 | seen_val | JSON payload: { 'event': 'SSHKeyAdded', 'user':... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | high | low<br><br>What is the risk level of ... | True | False | True |
| 211 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/v1/clusters | get | 'GET', 'url': '/api/v1/clusters | False | False | False |
| 212 | seen_val | Extract the API action (get/post/delete) from t... | 'deleteInactiveTransactions', 'data': { 'transactionId | delete | 'deleteInactiveTransactions', 'data':... | False | False | False |
| 213 | seen_val | Extract the API action (get/post/delete) from t... | 'POST', 'url': '/api/gateways/new | post | 'POST', 'url': '/api/gateways/new | False | False | False |
| 214 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/credit-balance | get | 'GET', 'url': '/api/credit-balance | False | False | False |
| 215 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/webhooks/new-endpoints | post | 'GET', 'url': '/webhooks/new-endpoints | False | False | False |
| 216 | seen_val | Extract the API action (get/post/delete) from t... | 'delete', 'path': '/backup/storage/directories | delete | 'delete', 'path': '/backup/storage/di... | False | False | False |
| 217 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/v1/deploy | get | 'GET', 'url': '/api/v1/deploy | False | False | False |
| 218 | seen_val | Extract the API action (get/post/delete) from t... | 'POST', 'uri': '/api/credential_sets/new | post | 'POST', 'uri': '/api/credential_sets/new | False | False | False |
| 219 | seen_val | Extract the API action (get/post/delete) from t... | 'delete', 'uri': '/users/verify/unverified | delete | 'delete', 'uri': '/users/verify/unver... | False | False | False |
| 220 | seen_val | Extract the API action (get/post/delete) from t... | 'GET', 'url': '/api/system-baseline-m | get | 'GET', 'url': '/api/system-baseline-m | False | False | False |
| 221 | seen_val | Extract the user role (admin/editor/viewer) fro... | 'admin', 'permissions': ['assign_groups', 'modify | admin | 'admin', 'permissions': ['assign_grou... | False | False | False |
| 222 | seen_val | Extract the user role (admin/editor/viewer) fro... | 'admin', 'permissions': ['can modify files and edit | editor | 'admin', 'permissions': ['can modify ... | False | False | False |
| 223 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | viewer | '' }<br><br>The given permission stri... | True | False | True |
| 224 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | admin | 'admin', 'permissions': ['root_level_... | True | False | True |
| 225 | seen_val | Extract the user role (admin/editor/viewer) fro... | 'admin', 'permissions': ['save_adjustment_parameters'] | editor | 'admin', 'permissions': ['save_adjust... | False | False | False |
| 226 | seen_val | Extract the user role (admin/editor/viewer) fro... | 'viewer' } The user role is viewer. Here's | viewer | 'viewer' } The user role is viewer. H... | False | False | False |
| 227 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | admin | 'admin', 'permissions': ['create_bill... | True | False | True |
| 228 | seen_val | Extract the user role (admin/editor/viewer) fro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | editor | '' }<br><br>The user role is an ident... | True | False | True |
| 229 | seen_val | Extract the user role (admin/editor/viewer) fro... | 'viewer', 'permissions': ['canObserveNetworkThrough | viewer | 'viewer', 'permissions': ['canObserve... | False | False | False |
| 230 | seen_val | Extract the user role (admin/editor/viewer) fro... | 'admin', 'permissions': ['edit_user_access_groups', | admin | 'admin', 'permissions': ['edit_user_a... | False | False | False |
| 231 | seen_val | Extract the transaction status (approved/declin... | 'approved', 'message': 'Payment successful.' } Here | approved | 'approved', 'message': 'Payment succe... | False | False | False |
| 232 | seen_val | Extract the transaction status (approved/declin... | 'rejected', 'reason': 'user declined payment request'} | declined | 'rejected', 'reason': 'user declined ... | False | False | False |
| 233 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'CVV verification mismatch | declined | 'declined', 'reason': 'CVV verificati... | False | False | False |
| 234 | seen_val | Extract the transaction status (approved/declin... | 'approved', 'reason': 'batch capture successful'} Here | approved | 'approved', 'reason': 'batch capture ... | False | False | False |
| 235 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'risk limit exceeded'} | declined | 'declined', 'reason': 'risk limit exc... | False | False | False |
| 236 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'user canceled billing checkout | declined | 'declined', 'reason': 'user canceled ... | False | False | False |
| 237 | seen_val | Extract the transaction status (approved/declin... | 'approved', 'message': 'Transaction successful.' } Here | approved | 'approved', 'message': 'Transaction s... | False | False | False |
| 238 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'block detected in payment | declined | 'declined', 'reason': 'block detected... | False | False | False |
| 239 | seen_val | Extract the transaction status (approved/declin... | 'pending', 'message': '', 'data': {} } | approved | 'pending', 'message': '', 'data': {} } | False | False | False |
| 240 | seen_val | Extract the transaction status (approved/declin... | 'declined', 'reason': 'network connection timeout'} | declined | 'declined', 'reason': 'network connec... | False | False | False |
| 241 | seen_val | To accomplish multiple milestones at the exact ... | stone. This is a common strategy used by many people who | stone | stone. This is a common strategy used... | False | False | False |
| 242 | seen_val | To avoid placing all your financial capital in ... | basket. Instead, diversify your investments to spread the risk | basket | basket. Instead, diversify your inves... | False | False | False |
| 243 | seen_val | To accidentally reveal highly confidential orga... | bag. This is a common occurrence in many organizations, and | bag | bag. This is a common occurrence in m... | False | False | False |
| 244 | seen_val | Being in a state of supreme, ecstatic joy or ex... | nine. It’s the feeling that you are surrounded by all | nine | nine. It’s the feeling that you are s... | False | False | False |
| 245 | seen_val | Feeling entirely awkward, uncomfortable, and ph... | water. It’s not just embarrassing but also humiliating. The | water | water. It’s not just embarrassing but... | False | False | False |
| 246 | seen_val | An unpredictable, incredibly dynamic, and highl... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | wire | action film director. This type of pe... | True | False | True |
| 247 | seen_val | An entirely random, highly surprising, and comp... | ordinary. It's a situation that has never happened before, | blue | ordinary. It's a situation that has n... | False | False | False |
| 248 | seen_val | Pursuing a completely incorrect strategy or lin... | tree. The goal should be to find a way to solve | tree | tree. The goal should be to find a wa... | False | False | False |
| 249 | seen_val | Facing a very difficult, painful, or awkward si... | bullet. The act of biting the bullet can be done in | bullet | bullet. The act of biting the bullet ... | False | False | False |
| 250 | seen_val | Wishing a theater actor excellent performance f... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | leg | promise. The actor breaks the promise... | True | False | True |
| 251 | seen_val | To accidentally expose a highly guarded organiz... | beans. This is an example of which type of logical fall | beans | beans. This is an example of which ty... | False | False | False |
| 252 | seen_val | Executing an operational workflow that is incre... | cake. However, when it comes to creating a workflow for | cake | cake. However, when it comes to creat... | False | False | False |
| 253 | seen_val | Resolving an architectural software bottleneck ... | head. The software that I am working on has a very | head | head. The software that I am working ... | False | False | False |
| 254 | seen_val | To accept the negative consequences of your pre... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | music | reality that you are not a good perso... | True | True | True |
| 255 | seen_val | Feeling mildly sick, fatigued, or physically un... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | weather | care of a doctor. The doctor will exa... | True | False | True |
| 256 | seen_val | To completely cease working on a development pi... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | day | day. The development pipeline is a se... | True | False | True |
| 257 | seen_val | Complaining about unfixable, past execution err... | milk. This is a common complaint from users of the Microsoft | milk | milk. This is a common complaint from... | False | False | False |
| 258 | seen_val | Avoiding speaking about the central, most criti... | bush. It’s not just a matter of being polite and | bush | bush. It’s not just a matter of being... | False | False | False |
| 259 | seen_val | To initiate a highly difficult, tense, or awkwa... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | ice | rules of social etiquette. The most a... | True | False | True |
| 260 | seen_val | Adding angry, volatile statements to an ongoing... | fire. The problem of conflict resolution in organizations has been a | fire | fire. The problem of conflict resolut... | False | False | False |
| 261 | seen_val | The system of rules and practices that governs ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | OS | ____.<br>A. Network File System<br>B.... | True | False | True |
| 262 | seen_val | The widely-used server operating system based o... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Linux | ____.<br>A. Windows Server 2016 | True | False | True |
| 263 | seen_val | The default web server software suite designed ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Apache | known as<br>A. Tomcat<br>B. IIS | True | False | True |
| 264 | seen_val | The high-performance reverse proxy and routing ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Nginx | a powerful tool for managing traffic ... | True | False | True |
| 265 | seen_val | The lightweight operating system-level containe... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Docker | ____<br>KVM<br>Xen<br>QEMU<br>V | True | False | True |
| 266 | seen_val | The cluster container orchestration engine deve... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Kubernetes | called Kubernetes. It was first relea... | True | False | True |
| 267 | seen_val | The Amazon Web Services virtual machine server ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | EC2 | a type of software that allows you to... | True | False | True |
| 268 | seen_val | In databases, storing unstructured records acro... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | NoSQL | a common practice. Which of the follo... | True | False | True |
| 269 | seen_val | The structural design schema defining relationa... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | schema | ____.<br>A. Data Definition Language<... | True | False | True |
| 270 | seen_val | CSS style sheets acronym stands for Cascading S... | Sheets. It is a set of rules that define the appearance | Sheets | Sheets. It is a set of rules that def... | False | False | False |
| 271 | seen_val | API programming layout acronym stands for Appli... | Interface. It is a set of rules and conventions that define | Interface | Interface. It is a set of rules and c... | False | False | False |
| 272 | seen_val | URL locate path acronym stands for Uniform Reso... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Locator | Locator. It is a string that represen... | True | False | True |
| 273 | seen_val | JSON data block acronym stands for JavaScript O... | Notation. It is a format used to represent structured data | Notation | Notation. It is a format used to repr... | False | False | False |
| 274 | seen_val | XML document layout acronym stands for Extensib... | Language. It is a markup language that allows documents to be | Language | Language. It is a markup language tha... | False | False | False |
| 275 | seen_val | SDK development toolkit acronym stands for Soft... | Kit. It is a collection of software components that developers can | Kit | Kit. It is a collection of software c... | False | False | False |
| 276 | seen_val | IDE coding interface acronym stands for Integra... | Environment. It is a software development environment that allows develo... | Environment | Environment. It is a software develop... | False | False | False |
| 277 | seen_val | CPU computer brain acronym stands for Central P... | Unit. It is the core of a computer and it is | Unit | Unit. It is the core of a computer an... | False | False | False |
| 278 | seen_val | RAM memory hardware acronym stands for Random A... | Memory. It is a type of computer memory that allows data | Memory | Memory. It is a type of computer memo... | False | False | False |
| 279 | seen_val | ROM startup hardware acronym stands for Read Only | Memory. It is a type of memory that stores data in | Memory | Memory. It is a type of memory that s... | False | False | False |
| 280 | seen_val | SSH terminal connection acronym stands for Secure | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Shell | Terminal Connection. It is a protocol... | True | False | True |
| 281 | seen_val | FTP network upload acronym stands for File Tran... | Protocol. It is a protocol used to transfer files between two | Protocol | Protocol. It is a protocol used to tr... | False | False | False |
| 282 | seen_val | SMTP email delivery acronym stands for Simple M... | Protocol. It is a protocol used to transfer emails between mail | Protocol | Protocol. It is a protocol used to tr... | False | False | False |
| 283 | seen_val | Running matching loops or blocks inside themsel... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | recursion | nesting. In this article, we will dis... | True | False | True |
| 284 | seen_val | An error or flaw in the underlying code logic i... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | bug | (n) ________.<br>A. Error<br>B. Bug | True | False | True |
| 285 | seen_val | Isolating and resolving structural flaws in a c... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | debugging | :<br><br>A) Debugging<br>B) Testing<b... | True | False | True |
| 286 | seen_val | The central computer hardware component respons... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | CPU | ____.<br>A. Arithmetic Logic Unit<br>... | True | False | True |
| 287 | seen_val | The fast volatile memory layer loaded during ac... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | RAM | called ____.<br>A. Page Table<br>B. S... | True | True | True |
| 288 | seen_val | The non-volatile chip storing fundamental start... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | ROM | called a(n) ________.<br>A. ROM<br>B | True | True | True |
| 289 | seen_val | The terminal connection protocol allowing secur... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | SSH | ____<br>SSH<br>FTP<br>HTTP<br>TELNET<... | True | False | True |
| 290 | seen_val | The internet routing directory system that maps... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | DNS | called ____.<br>DNS<br>FTP<br>HTTP<br... | True | False | True |
| 291 | seen_val | The structured query language command used to f... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | SELECT | ____<br>A. SELECT<br>B. INSERT<br>C. | True | False | True |
| 292 | seen_val | The structured query language command used to i... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | INSERT | ____.<br>A. INSERT<br>B. UPDATE<br>C. | True | False | True |
| 293 | seen_val | The structured query language command used to a... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | UPDATE | ____.<br>A. INSERT<br>B. UPDATE<br>C. | True | True | True |
| 294 | seen_val | The structured query language command used to d... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | DELETE | ____.<br>A. DELETE<br>B. DROP<br>C. | True | False | True |
| 295 | seen_val | The local virtual network interface loopback ad... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | 127.0.0.1 | ____.<br>A. 127.0.0 | True | False | True |
| 296 | seen_val | The standard network port utilized for insecure... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | 80 | :<br>A. 80<br>B. 44 | True | False | True |
| 297 | seen_val | The standard network port utilized for secure H... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | 443 | :<br>A. 443<br>B. 8 | True | False | True |
| 298 | seen_val | The Python script keyword used to pull in exter... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | import | ____<br>A. from<br>B. import<br>C. | True | False | True |
| 299 | seen_val | The Python script keyword used to define a new ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | class | ____<br>A. def<br>B. class<br>C. | True | False | True |
| 300 | seen_val | The Python script keyword used to declare a new... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | def | ____<br>A. def<br>B. class<br>C. | True | False | True |
| 301 | seen_val | The Python script keyword used to emit values b... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | return | called a function argument. The synta... | True | True | True |
| 302 | seen_val | The Python loop keyword used to iterate over fi... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | for | ____<br>A. for<br>B. while<br>C. | True | False | True |
| 303 | seen_val | The Python loop keyword used to run loops while... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | while | :<br>A. for<br>B. while<br>C. if | True | False | True |
| 304 | seen_val | The Python logical boolean variable indicating ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | True | `True` if the number is positive, and... | True | False | True |
| 305 | seen_val | The Python logical boolean variable indicating ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | False | ____<br>A. True<br>B. False<br>C. | True | False | True |
| 306 | seen_val | The Git code versioning command used to save ch... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | commit | commit. ____<br>A. Correct<br>B. Inco... | True | False | True |
| 307 | seen_val | The Git code versioning command used to send ch... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | push | push. The following commands are exam... | True | False | True |
| 308 | seen_val | The Git code versioning command used to fetch c... | fetch. The syntax for this command is:<br><br>```<br>git | pull | fetch. The syntax for this command is... | False | False | False |
| 309 | seen_val | Relational database records are structurally or... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | database | table. The data in the table is calle... | True | False | True |
| 310 | seen_val | The physical database schema detailing model la... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | schema | foundation of a database system. Whic... | True | False | True |
| 311 | seen_val | In CSS layouts, style rules are applied using C... | Sheets (CSS). This means that the styles for a particular | Sheets | Sheets (CSS). This means that the sty... | False | False | False |
| 312 | seen_val | In web protocols, the standard layout formattin... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | HTML | known as ____.<br>A. HTML<br>B. CSS | True | False | True |
| 313 | seen_val | In web protocols, the API interaction framework... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | API | HTTP client. Is this statement correc... | True | False | True |
| 314 | seen_val | In web protocols, the location path of resource... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | URL | crucial part. Which of the following ... | True | False | True |
| 315 | seen_val | In web protocols, the structured text format us... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | JSON | known as:<br>A. HTML<br>B. XML<br>C | True | True | True |
| 316 | seen_val | In web protocols, the extensible markup documen... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | XML | ____.<br>HTML<br>XML<br>XHTML<br>MIME | True | False | True |
| 317 | seen_val | The software development tools bundle provided ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | SDK | example of a(n) ________.<br>A. Softw... | True | True | True |
| 318 | seen_val | The unified development software editor workspa... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | IDE | area where developers can create and ... | True | False | True |
| 319 | seen_val | The primary network protocol standardizing pack... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | IP | ____<br>A. TCP<br>B. IP<br>C. | True | False | True |
| 320 | seen_val | The file transfer protocol standardizing file u... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | FTP | ____<br>FTP<br>HTTP<br>SMTP<br>SNMP<b... | True | False | True |
| 321 | seen_val | The file transfer protocol standardizing files ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | FTP | FTP, which stands for File Transfer P... | True | False | True |
| 322 | seen_val | The file transfer protocol standardizing files ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | FTP | FTP, which stands for File Transfer P... | True | False | True |
| 323 | seen_val | The file transfer protocol standardizing folder... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | FTP | FTP.<br>A. Correct<br>B. Incorrect<br... | True | False | True |
| 324 | seen_val | The file transfer protocol standardizing folder... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | FTP | FTP.<br>A. Correct<br>B. Incorrect<br... | True | False | True |
| 325 | seen_val | The file transfer protocol standardizing folder... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | FTP | FTP. A. 正确 B. 错误 | True | False | True |
| 326 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'Electronics', 'product_category': 'A... | False | True | True |
| 327 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 328 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'product_category': 'a... | False | True | True |
| 329 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 330 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 331 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'Electronics', 'category': 'Apparel', ' | False | True | True |
| 332 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 333 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 334 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 335 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 336 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 337 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'product_category': 'a... | False | True | True |
| 338 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 339 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 340 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'product_category': 'a... | False | True | True |
| 341 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 342 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'product_category': 'a... | False | True | True |
| 343 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'product_category': 'a... | False | True | True |
| 344 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 345 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 346 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'product_category': 'a... | False | True | True |
| 347 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 348 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'product_category': 'a... | False | True | True |
| 349 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 350 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'category': 'apparel',... | False | True | True |
| 351 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'product_category': 'a... | False | True | True |
| 352 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'product_category': 'a... | False | True | True |
| 353 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 354 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 355 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 356 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 357 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 358 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 359 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 360 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 361 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 362 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 363 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | home | 'electronics', 'category': 'apparel',... | False | True | True |
| 364 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | apparel | 'electronics', 'category': 'apparel',... | False | True | True |
| 365 | unseen_val | Extract the product department (electronics/app... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | electronics | 'electronics', 'product_category': 'a... | False | True | True |
| 366 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 52 } The heart | bradycardia | 'normal', 'rate': 52 } The heart | False | False | False |
| 367 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 112 } The | tachycardia | 'normal', 'rate': 112 } The | False | False | False |
| 368 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 72 } The heart | normal | 'normal', 'rate': 72 } The heart | False | False | False |
| 369 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 48 } The heart | bradycardia | 'normal', 'rate': 48 } The heart | False | False | False |
| 370 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 125 } The | tachycardia | 'normal', 'rate': 125 } The | False | False | False |
| 371 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 80 } The heart | normal | 'normal', 'rate': 80 } The heart | False | False | False |
| 372 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 55 } The heart | bradycardia | 'normal', 'rate': 55 } The heart | False | False | False |
| 373 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 105 } The | tachycardia | 'normal', 'rate': 105 } The | False | False | False |
| 374 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 65 } The heart | normal | 'normal', 'rate': 65 } The heart | False | False | False |
| 375 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 50 } The heart | bradycardia | 'normal', 'rate': 50 } The heart | False | False | False |
| 376 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 118 } The | tachycardia | 'normal', 'rate': 118 } The | False | False | False |
| 377 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 75 } The heart | normal | 'normal', 'rate': 75 } The heart | False | False | False |
| 378 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 58 } The heart | bradycardia | 'normal', 'rate': 58 } The heart | False | False | False |
| 379 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 130 } The | tachycardia | 'normal', 'rate': 130 } The | False | False | False |
| 380 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 85 } The heart | normal | 'normal', 'rate': 85 } The heart | False | False | False |
| 381 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 45 } The heart | bradycardia | 'normal', 'rate': 45 } The heart | False | False | False |
| 382 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 115 } The | tachycardia | 'normal', 'rate': 115 } The | False | False | False |
| 383 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 90 } The heart | normal | 'normal', 'rate': 90 } The heart | False | False | False |
| 384 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 53 } The heart | bradycardia | 'normal', 'rate': 53 } The heart | False | False | False |
| 385 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 110 } The | tachycardia | 'normal', 'rate': 110 } The | False | False | False |
| 386 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 70 } The heart | normal | 'normal', 'rate': 70 } The heart | False | False | False |
| 387 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 51 } The heart | bradycardia | 'normal', 'rate': 51 } The heart | False | False | False |
| 388 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 122 } The | tachycardia | 'normal', 'rate': 122 } The | False | False | False |
| 389 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 68 } The heart | normal | 'normal', 'rate': 68 } The heart | False | False | False |
| 390 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 49 } The heart | bradycardia | 'normal', 'rate': 49 } The heart | False | False | False |
| 391 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 108 } The | tachycardia | 'normal', 'rate': 108 } The | False | False | False |
| 392 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 78 } The heart | normal | 'normal', 'rate': 78 } The heart | False | False | False |
| 393 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 56 } The heart | bradycardia | 'normal', 'rate': 56 } The heart | False | False | False |
| 394 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 120 } The | tachycardia | 'normal', 'rate': 120 } The | False | False | False |
| 395 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 74 } The heart | normal | 'normal', 'rate': 74 } The heart | False | False | False |
| 396 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 57 } The heart | bradycardia | 'normal', 'rate': 57 } The heart | False | False | False |
| 397 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 128 } The | tachycardia | 'normal', 'rate': 128 } The | False | False | False |
| 398 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 88 } The heart | normal | 'normal', 'rate': 88 } The heart | False | False | False |
| 399 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 54 } The heart | bradycardia | 'normal', 'rate': 54 } The heart | False | False | False |
| 400 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 116 } The | tachycardia | 'normal', 'rate': 116 } The | False | False | False |
| 401 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 82 } The heart | normal | 'normal', 'rate': 82 } The heart | False | False | False |
| 402 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 47 } The heart | bradycardia | 'normal', 'rate': 47 } The heart | False | False | False |
| 403 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 124 } The | tachycardia | 'normal', 'rate': 124 } The | False | False | False |
| 404 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 76 } The heart | normal | 'normal', 'rate': 76 } The heart | False | False | False |
| 405 | unseen_val | Extract the heart rate status (normal/bradycard... | 'normal', 'rate': 59 } The heart | bradycardia | 'normal', 'rate': 59 } The heart | False | False | False |
| 406 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 407 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 408 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 409 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 410 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '172. | False | True | True |
| 411 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 412 | unseen_val | Extract the security group access level (public... | 'public', 'cidr': '0.0. | public | 'public', 'cidr': '0.0. | False | False | False |
| 413 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 414 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 415 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 416 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 417 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 418 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '172. | False | True | True |
| 419 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '172. | False | True | True |
| 420 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 421 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '172. | False | True | True |
| 422 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 423 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 424 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 425 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 426 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 427 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 428 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 429 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 430 | unseen_val | Extract the security group access level (public... | 'private', 'protocol': 'tcp', 'source': | public | 'private', 'protocol': 'tcp', 'source': | False | False | False |
| 431 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 432 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 433 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 434 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 435 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 436 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 437 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 438 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 439 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 440 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 441 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 442 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 443 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 444 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | public | 'private', 'cidr': '0.0. | False | True | True |
| 445 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 446 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 447 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '192. | False | True | True |
| 448 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
| 449 | unseen_val | Extract the security group access level (public... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | private | 'private', 'cidr': '10.0 | False | True | True |
| 450 | unseen_val | Extract the security group access level (public... | 'private', 'cidr': '0.0. | public | 'private', 'cidr': '0.0. | False | False | False |
