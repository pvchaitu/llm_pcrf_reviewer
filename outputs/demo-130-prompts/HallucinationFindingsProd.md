# 🛡️ Production Zero-Shot Hallucination Findings

### 📖 How to Interpret This Report
This report simulates how the PCRF Hybrid Ensemble operates in a **purely unsupervised production environment** (Zero-Shot), where ground-truth answers are completely unavailable.

The ensemble uses an **OR Gate** to maximize safety:
- **Inference Math (Token Risk):** Flags localized hesitation if structural entropy/margin risk exceeds `0.39`.
- **Curriculum Math (Sequence Implausibility):** Flags unnatural sequences if NLL exceeds `5.88`.
- **Hybrid Ensemble:** If *either* signal is triggered, the output is classified as a hallucination risk and the response is safely withheld.

**Current Calibration:** Adaptive K-Factor (StdDev) [K=0.50] -> Inference Risk (HR) > 0.39, Curriculum NLL > 5.88
> 💡 **Fine-Tuning Notice:** Please refer to `critical_observations.txt` to review the optimization sweeps for Z-Score and K-Factor. You can use those audits to fine-tune your risk appetite (Catch Rate vs. False Positives).

| ID | Split | Prompt | Served Generation Hybrid | Expected Value | Actual Value | Detected By Inference Math | Detected By Curriculum Math | Detected By Hybrid |
|----|-------|--------|--------------------------|----------------|--------------|----------------------------|-----------------------------|--------------------|
| 81 | seen_val | Complete with one word only: The official capit... | Seoul. <br><br>The official capital city of South Korea is Seoul | Seoul | Seoul. <br><br>The official capital c... | False | False | False |
| 82 | seen_val | Complete with one word only: The official capit... | Oslo. <br><br>The official capital city of Norway is Oslo. | Oslo | Oslo. <br><br>The official capital ci... | False | False | False |
| 83 | seen_val | Complete with one word only: The official capit... | Stockholm. <br><br>The official capital city of Sweden is Stockholm. | Stockholm | Stockholm. <br><br>The official capit... | False | False | False |
| 84 | seen_val | Complete with one word only: The official capit... | __________. Zurich<br><br>The official capital city of Switzerland is | Bern | __________. Zurich<br><br>The officia... | False | False | False |
| 85 | seen_val | Complete with one word only: The official capit... | Warsaw. <br><br>The official capital city of Poland is Warsaw, | Warsaw | Warsaw. <br><br>The official capital ... | False | False | False |
| 86 | seen_val | Complete with one word only: The noble element ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Neon | ____. <br>A. Iron<br>B. Gold<br>C | True | True | True |
| 87 | seen_val | Complete with one word only: The volatile eleme... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Sulfur | ____. <br>A. Sodium<br>B. Magnesium | True | False | True |
| 88 | seen_val | Complete with one word only: The chemical molec... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Oxygen | called an oxygen molecule. <br><br>Th... | True | True | True |
| 89 | seen_val | Complete with one word only: The yellow dwarf s... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Sun | Sun. <br><br>The sun is a star, and it's | True | False | True |
| 90 | seen_val | Complete with one word only: Mechanical acousti... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Vacuum | medium. The sound waves that travel t... | True | True | True |
| 91 | seen_val | Complete with one word only: The globally recog... | Rowling and published in the United Kingdom by Bloomsbury Publishing | Rowling | Rowling and published in the United K... | False | False | False |
| 92 | seen_val | Complete with one word only: The legendary clas... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Homer | who?<br>The answer is Homer.Human res... | True | False | True |
| 93 | seen_val | Complete with one word only: To achieve multipl... | stone. <br><br>To achieve multiple goals simultaneously is to accomplish... | stone | stone. <br><br>To achieve multiple go... | False | False | False |
| 94 | seen_val | Complete with one word only: A graphical diagra... | words. <br><br>A) Visual<br>B) Textual | words | words. <br><br>A) Visual<br>B) Textual | False | False | False |
| 95 | seen_val | Complete with one word only: An advice warning ... | basket. This means that you should diversify your investments across | basket | basket. This means that you should di... | False | False | False |
| 96 | seen_val | Complete with one word only: To enforce unique ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Set | technique known as __________. <br><b... | True | True | True |
| 97 | seen_val | Complete with one word only: The hypermedia syn... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | HTML | called __________. HTML<br><br>The an... | True | False | True |
| 98 | seen_val | Complete with one word only: An execution failu... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Bug | (n) ________.<br>A. Error<br>B. Fault | False | True | True |
| 99 | seen_val | Complete with one word only: A standardized tex... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | JSON | called a(n) ________.<br>A. Standardi... | True | True | True |
| 100 | seen_val | Complete with one word only: The active keyword... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | import | ____________.<br>The active keyword u... | True | False | True |
| 101 | unseen_val | Complete with one word only: The official capit... | Vienna. <br><br>Austria, officially known as the Kingdom of | Vienna | Vienna. <br><br>Austria, officially k... | False | False | False |
| 102 | unseen_val | Complete with one word only: The classical Roma... | Caesar. <br><br>Translate to Spanish.<br><br>El general romano cl | Caesar | Caesar. <br><br>Translate to Spanish.... | False | False | False |
| 103 | unseen_val | Complete with one word only: The pioneer lunar ... | Armstrong. <br><br>The answer is:<br><br>Neil Armstrong<br><br>This sent... | Armstrong | Armstrong. <br><br>The answer is:<br>... | False | False | False |
| 104 | unseen_val | Complete with one word only: The theoretical ph... | Einstein. He is known for his work on the theory of | Einstein | Einstein. He is known for his work on... | False | False | False |
| 105 | unseen_val | Complete with one word only: The historical exp... | Columbus. <br><br>The historical explorer who reached the Bahamas landmass | Columbus | Columbus. <br><br>The historical expl... | False | False | False |
| 106 | unseen_val | Complete with one word only: Mammalian red bloo... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Oxygen | substances in the body. They have a t... | False | True | True |
| 107 | unseen_val | Complete with one word only: The organic cellul... | called meiosis. <br><br>The correct answer is:<br><br>meiosis | Mitosis | called meiosis. <br><br>The correct a... | False | False | False |
| 108 | unseen_val | Complete with one word only: The primary comman... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Brain | __________. spinal cord<br><br>The pr... | True | True | True |
| 109 | unseen_val | Complete with one word only: The dual-helix mac... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | DNA | the ________ of life.<br>A. Cell memb... | True | True | True |
| 110 | unseen_val | Complete with one word only: The dense celestia... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Black Hole | black hole. <br><br>The answer is:<br... | True | False | True |
| 111 | unseen_val | Complete with one word only: An unexpected, com... | ordinary. The phrase "out of the ordinary" means something | blue | ordinary. The phrase "out of the ordi... | False | False | False |
| 112 | unseen_val | Complete with one word only: To prematurely lea... | bag. This can lead to serious consequences, including legal action | bag | bag. This can lead to serious consequ... | False | False | False |
| 113 | unseen_val | Complete with one word only: A state of intense... | nine. The person feels a sense of euphoria and el | nine | nine. The person feels a sense of eup... | False | False | False |
| 114 | unseen_val | Complete with one word only: When working in an... | water. You are not sure what to do or how to | water | water. You are not sure what to do or... | False | False | False |
| 115 | unseen_val | Complete with one word only: An extremely dynam... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | wire | -action character. A live-action char... | True | False | True |
| 116 | unseen_val | Complete with one word only: The specialized da... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Tree | (n) ________.<br>tree<br>binary tree<... | True | True | True |
| 117 | unseen_val | Complete with one word only: A networking layou... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Star | common approach to network design. Th... | True | True | True |
| 118 | unseen_val | Complete with one word only: The routing index ... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | DNS | called the ____.<br>A. Routing Index ... | True | True | True |
| 119 | unseen_val | Complete with one word only: A formal logical i... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | API | example of a(n) ________.<br>A. Inter... | False | True | True |
| 120 | unseen_val | Complete with one word only: The physical block... | ⚠️ Hallucination Risk Detected — Response Withheld for Safety | Sector | (n) ________.<br>disk surface<br><br>... | True | True | True |
