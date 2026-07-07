# Baseline-Only Evaluation Report

## Execution Mode
- Run Mode: baseline
- PCRF Components Executed: No
- SFT Candidate Regularization Executed: No
- Protected Router Executed: No

## Dataset Source
- Dataset Source: Built-in Mock Cloze Dataset
- Dataset File: N/A

## Dataset Partition Counts
- Train Split: 80
- Seen Validation Split: 20
- Unseen Validation Split: 20
- OOD Split: 10
- Total Rows Audited: 130

## Baseline Metrics
- model_name: Qwen/Qwen2.5-0.5B-Instruct
- seen_val_acc: 0.55
- unseen_val_acc: 0.5
- seen_val_nll: 4.615767045454546
- unseen_val_nll: 5.252333207563921
- seen_val_ppl: 101.06532050345386
- unseen_val_ppl: 191.0114182290873

## Baseline Prompt / Generation Hallucination Audit

Baseline row audit includes train, seen validation, unseen validation, and OOD prompts where available. This gives a complete view of baseline hallucination exposure before PCRF governance.

| ID | Split | Prompt | Baseline Generation | Expected Value | Actual Value | Match? | Hallucinated? |
|----|--------|---------|---------|---------|---------|---------|---------|
| 1 | train | Complete with one word only: The official capital city of France is | Paris. <br><br>Paris, the French capital, is a ... | Paris | Paris. <br><br>Paris, the French capital, is a ... | YES | NO |
| 2 | train | Complete with one word only: The official capital city of Germany is | Berlin. Berlin is the capital city of Germany, ... | Berlin | Berlin. Berlin is the capital city of Germany, ... | YES | NO |
| 3 | train | Complete with one word only: The official capital city of Italy is | __________. Rome<br><br>The official capital ci... | Rome | __________. Rome<br><br>The official capital ci... | YES | NO |
| 4 | train | Complete with one word only: The official capital city of Spain is | Madrid. <br><br>Madrid, officially known as the... | Madrid | Madrid. <br><br>Madrid, officially known as the... | YES | NO |
| 5 | train | Complete with one word only: The official capital city of Japan is | __________. Tokyo<br><br>What is the answer? To... | Tokyo | __________. Tokyo<br><br>What is the answer? To... | YES | NO |
| 6 | train | Complete with one word only: The official capital city of China is | ________.<br>Beijing<br><br>The official capita... | Beijing | ________.<br>Beijing<br><br>The official capita... | YES | NO |
| 7 | train | Complete with one word only: The official capital city of Egypt is | Cairo. <br><br>Cairo is the capital city of Egypt, | Cairo | Cairo. <br><br>Cairo is the capital city of Egypt, | YES | NO |
| 8 | train | Complete with one word only: The official capital city of Greece is | ________.<br>Athens<br><br>The official capital... | Athens | ________.<br>Athens<br><br>The official capital... | YES | NO |
| 9 | train | Complete with one word only: The official capital city of Portugal is | Lisbon. <br><br>Lisbon<br>Portugal's capital, | Lisbon | Lisbon. <br><br>Lisbon<br>Portugal's capital, | YES | NO |
| 10 | train | Complete with one word only: The official capital city of Russia is | __________. Moscow<br><br>The answer is Moscow.... | Moscow | __________. Moscow<br><br>The answer is Moscow.... | YES | NO |
| 11 | train | Complete with one word only: The official capital city of India is | __________. New Delhi<br><br>The official capit... | Delhi | __________. New Delhi<br><br>The official capit... | YES | NO |
| 12 | train | Complete with one word only: The official capital city of England is | ________.<br>London<br><br>The official capital... | London | ________.<br>London<br><br>The official capital... | YES | NO |
| 13 | train | Complete with one word only: The official capital city of Canada is | ____.<br>A. Ottawa<br>B. Toronto<br>C. | Ottawa | ____.<br>A. Ottawa<br>B. Toronto<br>C. | YES | NO |
| 14 | train | Complete with one word only: The official capital city of Brazil is | ____.<br>Rio de Janeiro<br><br>The official cap... | Brasilia | ____.<br>Rio de Janeiro<br><br>The official cap... | NO | YES |
| 15 | train | Complete with one word only: The official capital city of Mexico is | ____.<br>Mexico City<br><br>The official capita... | Mexico | ____.<br>Mexico City<br><br>The official capita... | YES | NO |
| 16 | train | Complete with one word only: The official capital city of Argentina is | Buenos Aires. <br><br>Buenos Aires<br><br>Trans... | Buenos Aires | Buenos Aires. <br><br>Buenos Aires<br><br>Trans... | YES | NO |
| 17 | train | Complete with one word only: The official capital city of Australia is | ________.<br>Sydney<br><br>The official capital... | Canberra | ________.<br>Sydney<br><br>The official capital... | NO | YES |
| 18 | train | Complete with one word only: The official capital city of Sweden is | ________.<br>Stockholm<br><br>The official capi... | Stockholm | ________.<br>Stockholm<br><br>The official capi... | YES | NO |
| 19 | train | Complete with one word only: The official capital city of Turkey is | Ankara. <br><br>A) Istanbul<br>B) Izmir | Ankara | Ankara. <br><br>A) Istanbul<br>B) Izmir | YES | NO |
| 20 | train | Complete with one word only: The official capital city of Thailand is | __________. Bangkok<br><br>The answer is: Bangkok. | Bangkok | __________. Bangkok<br><br>The answer is: Bangkok. | YES | NO |
| 21 | train | Complete with one word only: The official capital city of Vietnam is | __________. Hanoi<br><br>The official capital c... | Hanoi | __________. Hanoi<br><br>The official capital c... | YES | NO |
| 22 | train | Complete with one word only: The official capital city of Peru is | ____.<br>Cortés<br><br>The official capital cit... | Lima | ____.<br>Cortés<br><br>The official capital cit... | NO | YES |
| 23 | train | Complete with one word only: The official capital city of Chile is | Santiago. <br><br>Santiago de Chile, officially... | Santiago | Santiago. <br><br>Santiago de Chile, officially... | YES | NO |
| 24 | train | Complete with one word only: The official capital city of Colombia is | ____.<br>Bogotá<br><br>The official capital cit... | Bogota | ____.<br>Bogotá<br><br>The official capital cit... | NO | YES |
| 25 | train | Complete with one word only: The official capital city of Belgium is | __________. Bruges<br><br>What is the main idea of | Brussels | __________. Bruges<br><br>What is the main idea of | NO | YES |
| 26 | train | Complete with one word only: The official capital city of Austria is | __________. Vienna<br><br>What does the sentenc... | Vienna | __________. Vienna<br><br>What does the sentenc... | YES | NO |
| 27 | train | Complete with one word only: The official capital city of Poland is | Warsaw. <br><br>A) Capital<br>B) City<br>C | Warsaw | Warsaw. <br><br>A) Capital<br>B) City<br>C | YES | NO |
| 28 | train | Complete with one word only: The official capital city of Finland is | __________. Helsinki<br><br>The official capita... | Helsinki | __________. Helsinki<br><br>The official capita... | YES | NO |
| 29 | train | Complete with one word only: The official capital city of Ireland is | ________.<br>Dublin<br><br>The official capital... | Dublin | ________.<br>Dublin<br><br>The official capital... | YES | NO |
| 30 | train | Complete with one word only: The official capital city of Kenya is | Nairobi. <br><br>Nairobi, the capital city of K... | Nairobi | Nairobi. <br><br>Nairobi, the capital city of K... | YES | NO |
| 31 | train | Complete with one word only: The official capital city of Nigeria is | Lagos. Lagos is the largest city in Nigeria and... | Abuja | Lagos. Lagos is the largest city in Nigeria and... | NO | YES |
| 32 | train | Complete with one word only: The official capital city of South Africa is | __________. Cape Town<br><br>The official capit... | Pretoria | __________. Cape Town<br><br>The official capit... | NO | YES |
| 33 | train | Complete with one word only: The official capital city of New Zealand is | ________.<br>Wellington<br><br>The official cap... | Wellington | ________.<br>Wellington<br><br>The official cap... | YES | NO |
| 34 | train | Complete with one word only: The official capital city of Saudi Arabia is | Riyadh. <br><br>Riyadh is the largest city in S... | Riyadh | Riyadh. <br><br>Riyadh is the largest city in S... | YES | NO |
| 35 | train | Complete with one word only: The official capital city of Ukraine is | __________. Kiev<br><br>The official capital ci... | Kyiv | __________. Kiev<br><br>The official capital ci... | NO | YES |
| 36 | train | Complete with one word only: The official capital city of Netherlands is | __________. Amsterdam<br><br>The official capit... | Amsterdam | __________. Amsterdam<br><br>The official capit... | YES | NO |
| 37 | train | Complete with one word only: The official capital city of Switzerland is | __________. Zurich<br><br>What does the sentenc... | Bern | __________. Zurich<br><br>What does the sentenc... | NO | YES |
| 38 | train | Complete with one word only: The official capital city of Denmark is | ________.<br>Copenhagen<br><br>The official cap... | Copenhagen | ________.<br>Copenhagen<br><br>The official cap... | YES | NO |
| 39 | train | Complete with one word only: The official capital city of Norway is | ________.<br>Stockholm<br><br>The official capi... | Oslo | ________.<br>Stockholm<br><br>The official capi... | NO | YES |
| 40 | train | Complete with one word only: The official capital city of Indonesia is | Jakarta. <br><br>A) Capital<br>B) Largest<br>C | Jakarta | Jakarta. <br><br>A) Capital<br>B) Largest<br>C | YES | NO |
| 41 | train | Complete with one word only: The element with atomic number 1 is | ____. <br>A. Iron<br>B. Gold<br>C | Hydrogen | ____. <br>A. Iron<br>B. Gold<br>C | NO | YES |
| 42 | train | Complete with one word only: The element with atomic number 2 is | __________. <br>A) Sodium<br>B) Iron | Helium | __________. <br>A) Sodium<br>B) Iron | NO | YES |
| 43 | train | Complete with one word only: The element with atomic number 6 is | __________. <br>A) Sodium<br>B) Iron | Carbon | __________. <br>A) Sodium<br>B) Iron | NO | YES |
| 44 | train | Complete with one word only: The element with atomic number 7 is | ____. <br>A. Iron<br>B. Gold<br>C | Nitrogen | ____. <br>A. Iron<br>B. Gold<br>C | NO | YES |
| 45 | train | Complete with one word only: The element with atomic number 8 is | __________. <br>A) Sodium<br>B) Iron | Oxygen | __________. <br>A) Sodium<br>B) Iron | NO | YES |
| 46 | train | Complete with one word only: Water is chemically composed of oxygen and | hydrogen. <br><br>A) Hydrogen<br>B) Oxygen | Hydrogen | hydrogen. <br><br>A) Hydrogen<br>B) Oxygen | YES | NO |
| 47 | train | Complete with one word only: The planet sitting closest to our solar sys... | called __________. Mercury<br><br>What is the a... | Mercury | called __________. Mercury<br><br>What is the a... | YES | NO |
| 48 | train | Complete with one word only: The planet with the highest surface tempera... | __________. <br>A) Mercury<br>B) Venus | Venus | __________. <br>A) Mercury<br>B) Venus | YES | NO |
| 49 | train | Complete with one word only: The planet historically referred to as the ... | now known as Mars. <br><br>The ancient Roman go... | Mars | now known as Mars. <br><br>The ancient Roman go... | YES | NO |
| 50 | train | Complete with one word only: The largest gas giant orbiting inside our s... | __________. Saturn.<br>The answer is Saturn.Human | Jupiter | __________. Saturn.<br>The answer is Saturn.Human | NO | YES |
| 51 | train | Complete with one word only: Photosynthesis in organic plant structures ... | oxygen. <br><br>A) Correct<br>B) Incorrect<br><... | Oxygen | oxygen. <br><br>A) Correct<br>B) Incorrect<br><... | YES | NO |
| 52 | train | Complete with one word only: The standard electrical metric measuring op... | called ____.<br>A. Voltage<br>B. Current<br>C | Ohm | called ____.<br>A. Voltage<br>B. Current<br>C | NO | YES |
| 53 | train | Complete with one word only: The physical force driving planetary orbits is | ___________.<br><br>A) gravity  <br>B) friction | Gravity | ___________.<br><br>A) gravity  <br>B) friction | YES | NO |
| 54 | train | Complete with one word only: The chemical compound representing standard... | __________. Sodium chloride.<br>The answer is: ... | NaCl | __________. Sodium chloride.<br>The answer is: ... | YES | NO |
| 55 | train | Complete with one word only: A liquid solution with a pH rating signific... | example of which type of solution?<br><br>a) Ac... | Acid | example of which type of solution?<br><br>a) Ac... | YES | NO |
| 56 | train | Complete with one word only: A liquid solution with a pH rating signific... | (n) ___________.<br>sodium hydroxide | Base | (n) ___________.<br>sodium hydroxide | NO | YES |
| 57 | train | Complete with one word only: The basic physical container of all organic... | __________. <br>A. Cell<br>B. Organism | Cell | __________. <br>A. Cell<br>B. Organism | YES | NO |
| 58 | train | Complete with one word only: The atmospheric gas primarily responsible f... | __________. carbon dioxide<br>Answer:<br><br>ca... | Carbon | __________. carbon dioxide<br>Answer:<br><br>ca... | YES | NO |
| 59 | train | Complete with one word only: The core organ driving blood circulation in... | __________.<br>heart<br><br>The heart is the pr... | Heart | __________.<br>heart<br><br>The heart is the pr... | YES | NO |
| 60 | train | Complete with one word only: Light waves travel significantly faster tha... | sound. <br><br>A) Faster<br>B) Slower | Sound | sound. <br><br>A) Faster<br>B) Slower | YES | NO |
| 61 | train | Complete with one word only: In operating systems, a scheduled execution... | process. A thread is an independent unit of wor... | Process | process. A thread is an independent unit of wor... | YES | NO |
| 62 | train | Complete with one word only: In deep learning, structural parameters are... | a loss function to minimize the error between t... | Descent | a loss function to minimize the error between t... | NO | YES |
| 63 | train | Complete with one word only: To store keyed associative records with rap... | data structure that is __________. <br><br>a) h... | Map | data structure that is __________. <br><br>a) h... | NO | YES |
| 64 | train | Complete with one word only: A sequential queue data structure operates ... | FIFO. <br><br>A linked list is a linear data st... | FIFO | FIFO. <br><br>A linked list is a linear data st... | YES | NO |
| 65 | train | Complete with one word only: A sequential stack data structure operates ... | LIFO. This means that the most recently added e... | LIFO | LIFO. This means that the most recently added e... | YES | NO |
| 66 | train | Complete with one word only: The digital counting framework representing... | called _________. binary<br><br>The answer to t... | Binary | called _________. binary<br><br>The answer to t... | YES | NO |
| 67 | train | Complete with one word only: The primary volatile memory utilized for ra... | ________.<br>Answer:<br><br>cache<br><br>The pr... | RAM | ________.<br>Answer:<br><br>cache<br><br>The pr... | NO | YES |
| 68 | train | Complete with one word only: The foundational processing unit executing ... | ________.<br>A. CPU<br>B. Memory<br>C | CPU | ________.<br>A. CPU<br>B. Memory<br>C | YES | NO |
| 69 | train | Complete with one word only: The technical engineering pipeline of locat... | called a(n) ________.<br>A. Debugging | Debugging | called a(n) ________.<br>A. Debugging | YES | NO |
| 70 | train | Complete with one word only: In class structures, an operational memory ... | __________. <br>A) register<br>B) buffer | Object | __________. <br>A) register<br>B) buffer | NO | YES |
| 71 | train | Complete with one word only: The network transmission protocol used to s... | __________.<br>A. HTTP<br>B. HTTPS<br>C | HTTPS | __________.<br>A. HTTP<br>B. HTTPS<br>C | YES | NO |
| 72 | train | Complete with one word only: A software routine that invokes itself to s... | called a(n) ________.<br>recursive algorithm<br... | Recursion | called a(n) ________.<br>recursive algorithm<br... | NO | YES |
| 73 | train | Complete with one word only: The version control directive committing in... | add .gitignore. <br><br>The version control dir... | commit | add .gitignore. <br><br>The version control dir... | YES | NO |
| 74 | train | Complete with one word only: The relational database directive used to f... | __________.<br>A. SELECT<br>B. INSERT<br>C | SELECT | __________.<br>A. SELECT<br>B. INSERT<br>C | YES | NO |
| 75 | train | Complete with one word only: An auxiliary database lookup catalog built ... | example of ____.<br>A. Indexing<br>B. Query | Index | example of ____.<br>A. Indexing<br>B. Query | YES | NO |
| 76 | train | Complete with one word only: The fundamental internet routing system sta... | ___ protocol.<br>A. TCP<br>B. IP<br>C | IP | ___ protocol.<br>A. TCP<br>B. IP<br>C | YES | NO |
| 77 | train | Complete with one word only: In balanced search trees, a terminal node l... | (n) _______ node. To determine the correct answ... | Leaf | (n) _______ node. To determine the correct answ... | NO | YES |
| 78 | train | Complete with one word only: The reserved programming keyword used to de... | __________. <br><br>a) class<br>b) def | class | __________. <br><br>a) class<br>b) def | YES | NO |
| 79 | train | Complete with one word only: The reserved programming keyword used to in... | __________. <br><br>a) def<br>b) while | def | __________. <br><br>a) def<br>b) while | YES | NO |
| 80 | train | Complete with one word only: The computational scale measuring worst-cas... | notation. <br><br>Big O notation describes the ... | Notation | notation. <br><br>Big O notation describes the ... | YES | NO |
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
| 121 | ood | Complete with one word only: In mathematical topology, topological manif... | characteristic. A manifold is a topological spa... | Manifold | characteristic. A manifold is a topological spa... | YES | NO |
| 122 | ood | Complete with one word only: In wave equations, particles exhibit simult... | duality. This phenomenon is observed in various... | Duality | duality. This phenomenon is observed in various... | YES | NO |
| 123 | ood | Complete with one word only: In molecular structures, compounds sharing ... | known as ____. <br>A. Ionic compounds<br>B. | Isomers | known as ____. <br>A. Ionic compounds<br>B. | NO | YES |
| 124 | ood | Complete with one word only: In ecological geology, the mechanical drift... | tectonics. The process involves the movement of t | Tectonics | tectonics. The process involves the movement of t | YES | NO |
| 125 | ood | Complete with one word only: In ancient law, the primary eye-for-an-eye ... | Hammurabi. The code stipulated that if a person | Hammurabi | Hammurabi. The code stipulated that if a person | YES | NO |
| 126 | ood | Complete with one word only: In early Mesopotamian clay scripts, the cla... | Gilgamesh. The story begins with Gilgamesh, | Gilgamesh | Gilgamesh. The story begins with Gilgamesh, | YES | NO |
| 127 | ood | Complete with one word only: In multi-linear algebra, a multi-dimensiona... | matrix of the form $\begin{bmatrix}a_{ | Tensor | matrix of the form $\begin{bmatrix}a_{ | NO | YES |
| 128 | ood | Complete with one word only: In scientific taxonomy, species modificatio... | selection. <br><br>A) Artificial<br>B) Natural<... | Selection | selection. <br><br>A) Artificial<br>B) Natural<... | YES | NO |
| 129 | ood | Complete with one word only: In mathematical logic, a clean self-contrad... | ____.<br>In mathematical logic, a clean self-co... | Paradox | ____.<br>In mathematical logic, a clean self-co... | NO | YES |
| 130 | ood | Complete with one word only: In deep history, the foundational Bronze Ag... | Hammurabi. The Code of Hammurabi was a | Hammurabi | Hammurabi. The Code of Hammurabi was a | YES | NO |
