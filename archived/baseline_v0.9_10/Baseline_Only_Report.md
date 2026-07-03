# Baseline-Only Evaluation Report

## Execution Mode
- Run Mode: baseline
- PCRF Components Executed: No
- Candidate Regularization Executed: No
- Protected Router Executed: No

## Dataset Source
- Dataset Source: Built-in Mock Cloze Dataset
- Dataset File: N/A

## Dataset Partition Counts
- Train Split: 80
- Seen Validation Split: 20
- Unseen Validation Split: 20

## Baseline Metrics
- model_name: Qwen/Qwen2.5-0.5B-Instruct
- seen_val_acc: 0.55
- unseen_val_acc: 0.5
- seen_val_nll: 4.615767045454546
- unseen_val_nll: 5.252333207563921
- seen_val_ppl: 101.06532050345386
- unseen_val_ppl: 191.0114182290873

### Baseline Prompt / Generation Hallucination Audit

| ID | Split | Prompt | Baseline Generation | Expected Value | Actual Value | Match? | Hallucinated? |
|----|--------|---------|---------|---------|---------|---------|---------|
| 81 | seen_val | Complete with one word only: The official capital city of South Korea is | __________. Seoul<br><br>What is the answer? To... | Seoul | __________. Seoul<br><br>What is the answer? To... | YES | NO |
| 82 | seen_val | Complete with one word only: The official capital city of Norway is | ________.<br>Stockholm<br><br>The official capi... | Oslo | ________.<br>Stockholm<br><br>The official capi... | NO | YES |
| 83 | seen_val | Complete with one word only: The official capital city of Sweden is | ________.<br>Stockholm<br><br>The official capi... | Stockholm | ________.<br>Stockholm<br><br>The official capi... | YES | NO |
| 84 | seen_val | Complete with one word only: The official capital city of Switzerland is | __________. Zurich<br><br>What does the sentenc... | Bern | __________. Zurich<br><br>What does the sentenc... | NO | YES |
| 85 | seen_val | Complete with one word only: The official capital city of Poland is | Warsaw. <br><br>A) Capital<br>B) City<br>C | Warsaw | Warsaw. <br><br>A) Capital<br>B) City<br>C | YES | NO |
| 86 | seen_val | Complete with one word only: The noble element designated by atomic numb... | ____. <br>A. Gold<br>B. Silver<br>C | Neon | ____. <br>A. Gold<br>B. Silver<br>C | NO | YES |
| 87 | seen_val | Complete with one word only: The volatile element designated by atomic n... | __________. <br>A. Sodium<br>B. Magnesium | Sulfur | __________. <br>A. Sodium<br>B. Magnesium | NO | YES |
| 88 | seen_val | Complete with one word only: The chemical molecule animals must extract ... | called _____. oxygen<br><br>The chemical molecu... | Oxygen | called _____. oxygen<br><br>The chemical molecu... | YES | NO |
| 89 | seen_val | Complete with one word only: The yellow dwarf star supporting life at th... | ___.<br>A. Sun<br>B. Earth<br>C. | Sun | ___.<br>A. Sun<br>B. Earth<br>C. | YES | NO |
| 90 | seen_val | Complete with one word only: Mechanical acoustics are completely incapab... | medium. <br><br>A) Inertial<br>B) Elastic | Vacuum | medium. <br><br>A) Inertial<br>B) Elastic | NO | YES |
| 91 | seen_val | Complete with one word only: The globally recognized fantasy series Harr... | Rowling, and it has been adapted into a popular... | Rowling | Rowling, and it has been adapted into a popular... | YES | NO |
| 92 | seen_val | Complete with one word only: The legendary classical Greek epic poem The... | which ancient Greek poet? Homer. <br><br>The Od... | Homer | which ancient Greek poet? Homer. <br><br>The Od... | YES | NO |
| 93 | seen_val | Complete with one word only: To achieve multiple achievements concurrent... | stone. <br><br>A) Achieve<br>B) Conquer | stone | stone. <br><br>A) Achieve<br>B) Conquer | YES | NO |
| 94 | seen_val | Complete with one word only: A graphical diagram is capable of conveying... | words. <br><br>A) Visual<br>B) Digital<br>C | words | words. <br><br>A) Visual<br>B) Digital<br>C | YES | NO |
| 95 | seen_val | Complete with one word only: An advice warning against placing all finan... | basket. This means that you should diversify yo... | basket | basket. This means that you should diversify yo... | YES | NO |
| 96 | seen_val | Complete with one word only: To enforce unique constraints with no dupli... | technique known as __________. <br><br>A) Hashing | Set | technique known as __________. <br><br>A) Hashing | NO | YES |
| 97 | seen_val | Complete with one word only: The hypermedia syntax used to format layout... | called __________. HTML<br><br>The hypermedia s... | HTML | called __________. HTML<br><br>The hypermedia s... | YES | NO |
| 98 | seen_val | Complete with one word only: An execution failure originating from incor... | (n) ________.<br>A. Error<br>B. Fault | Bug | (n) ________.<br>A. Error<br>B. Fault | NO | YES |
| 99 | seen_val | Complete with one word only: A standardized text notation representing c... | called a(n) ________.<br>A. CAD<br>B | JSON | called a(n) ________.<br>A. CAD<br>B | NO | YES |
| 100 | seen_val | Complete with one word only: The active keyword used to bind external pa... | ____________.<br>module<br><br>The active keywo... | import | ____________.<br>module<br><br>The active keywo... | NO | YES |
| 101 | unseen_val | Complete with one word only: The official capital city of Austria is | __________. Vienna<br><br>What does the sentenc... | Vienna | __________. Vienna<br><br>What does the sentenc... | YES | NO |
| 102 | unseen_val | Complete with one word only: The classical Roman general who met his end... | Caesar. <br><br>A) Lucius Cornelius Sulla | Caesar | Caesar. <br><br>A) Lucius Cornelius Sulla | YES | NO |
| 103 | unseen_val | Complete with one word only: The pioneer lunar explorer who took the fir... | Armstrong. <br><br>A) John B<br>B) Robert C | Armstrong | Armstrong. <br><br>A) John B<br>B) Robert C | YES | NO |
| 104 | unseen_val | Complete with one word only: The theoretical physicist who revolutionize... | Einstein. <br><br>A) Correct  <br>B) Incorrect<... | Einstein | Einstein. <br><br>A) Correct  <br>B) Incorrect<... | YES | NO |
| 105 | unseen_val | Complete with one word only: The historical explorer who reached the Bah... | Columbus. <br><br>A) Invented B) Discovered C | Columbus | Columbus. <br><br>A) Invented B) Discovered C | YES | NO |
| 106 | unseen_val | Complete with one word only: Mammalian red blood cells are chemically re... | substances in the body. They have a unique stru... | Oxygen | substances in the body. They have a unique stru... | NO | YES |
| 107 | unseen_val | Complete with one word only: The organic cellular process separating chr... | called __________. meiosis<br><br>The organic c... | Mitosis | called __________. meiosis<br><br>The organic c... | NO | YES |
| 108 | unseen_val | Complete with one word only: The primary command center of the central n... | __________. spinal cord<br><br>The primary comm... | Brain | __________. spinal cord<br><br>The primary comm... | NO | YES |
| 109 | unseen_val | Complete with one word only: The dual-helix macromolecule housing core g... | called a(n) ________.<br>A. Chromosome | DNA | called a(n) ________.<br>A. Chromosome | NO | YES |
| 110 | unseen_val | Complete with one word only: The dense celestial body whose localized gr... | (n) ________.<br><br>A. black hole B. white | Black Hole | (n) ________.<br><br>A. black hole B. white | YES | NO |
| 111 | unseen_val | Complete with one word only: An unexpected, completely unpredictable eve... | ________.<br>boundaries. boundaries<br><br>An u... | blue | ________.<br>boundaries. boundaries<br><br>An u... | NO | YES |
| 112 | unseen_val | Complete with one word only: To prematurely leak sensitive details of a ... | bag. This can lead to significant risks, includ... | bag | bag. This can lead to significant risks, includ... | YES | NO |
| 113 | unseen_val | Complete with one word only: A state of intense mental ecstasy or extrem... | nine. The person feels a sense of euphoria and el | nine | nine. The person feels a sense of euphoria and el | YES | NO |
| 114 | unseen_val | Complete with one word only: When working in an uncomfortable, unfamilia... | water. You may be overwhelmed by the noise and ... | water | water. You may be overwhelmed by the noise and ... | YES | NO |
| 115 | unseen_val | Complete with one word only: An extremely dynamic, energetic, and unpred... | -action character. A live-action character can ... | wire | -action character. A live-action character can ... | NO | YES |
| 116 | unseen_val | Complete with one word only: The specialized data structure used to mode... | (n) ________.<br>tree<br>graph<br>array<br>list | Tree | (n) ________.<br>tree<br>graph<br>array<br>list | YES | NO |
| 117 | unseen_val | Complete with one word only: A networking layout topology organizing nod... | (n) ________.<br>cluster<br>mesh<br>tree<br>ring | Star | (n) ________.<br>cluster<br>mesh<br>tree<br>ring | NO | YES |
| 118 | unseen_val | Complete with one word only: The routing index directory that translates... | called ____.<br>A. Domain Name System<br>B. Rou... | DNS | called ____.<br>A. Domain Name System<br>B. Rou... | NO | YES |
| 119 | unseen_val | Complete with one word only: A formal logical interface allowing separat... | example of a(n) ________.<br>A. Protocol | API | example of a(n) ________.<br>A. Protocol | NO | YES |
| 120 | unseen_val | Complete with one word only: The physical block boundary used to seriali... | (n) ________.<br>disk surface<br><br>The physic... | Sector | (n) ________.<br>disk surface<br><br>The physic... | NO | YES |
