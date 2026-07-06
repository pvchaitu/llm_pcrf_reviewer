# Baseline-Only Evaluation Report

## Execution Mode
- Run Mode: baseline
- PCRF Components Executed: No
- SFT Candidate Regularization Executed: No
- Protected Router Executed: No

## Dataset Source
- Dataset Source: External File
- Dataset File: customer-demo-grade-500-prompt.csv

## Dataset Partition Counts
- Train Split: 200
- Seen Validation Split: 125
- Unseen Validation Split: 125
- OOD Split: 50
- Total Rows Audited: 500

## Baseline Metrics
- model_name: Qwen/Qwen2.5-0.5B-Instruct
- seen_val_acc: 0.824
- unseen_val_acc: 0.368
- seen_val_nll: 2.3784375
- unseen_val_nll: 3.368046875
- seen_val_ppl: 10.788033385918167
- unseen_val_ppl: 29.021788486435117

## Baseline Prompt / Generation Hallucination Audit

Baseline row audit includes train, seen validation, unseen validation, and OOD prompts where available. This gives a complete view of baseline hallucination exposure before PCRF governance.

| ID | Split | Prompt | Baseline Generation | Expected Value | Actual Value | Match? | Hallucinated? |
|----|--------|---------|---------|---------|---------|---------|---------|
| 1 | train | Train 1: The capital of France is | Paris. It's the largest city in Europe and one of | Paris | Paris. It's the largest city in Europe and one of | YES | NO |
| 2 | train | Train 2: The currency of Japan is | the yen. It is also known as Yen, or | Yen | the yen. It is also known as Yen, or | YES | NO |
| 3 | train | Train 3: The chemical symbol for gold is | Au. Which of the following statements about gol... | Au | Au. Which of the following statements about gol... | YES | NO |
| 4 | train | Train 4: The author of Hamlet is | a famous playwright, and the author of Romeo an... | Shakespeare | a famous playwright, and the author of Romeo an... | NO | YES |
| 5 | train | Train 5: The default HTTPS port is | 443, which means that all traffic on this | 443 | 443, which means that all traffic on this | YES | NO |
| 6 | train | Train 6: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 7 | train | Train 7: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 8 | train | Train 8: The largest planet in the solar system is | Jupiter, which has a diameter of approximately 142 | Jupiter | Jupiter, which has a diameter of approximately 142 | YES | NO |
| 9 | train | Train 9: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 10 | train | Train 10: The currency of Japan is | the yen. It is the world's most widely used cur... | Yen | the yen. It is the world's most widely used cur... | YES | NO |
| 11 | train | Train 11: The chemical symbol for gold is | Au. Which of the following statements about gol... | Au | Au. Which of the following statements about gol... | YES | NO |
| 12 | train | Train 12: The author of Hamlet is | a man who was born in which country?<br>Answer ... | Shakespeare | a man who was born in which country?<br>Answer ... | NO | YES |
| 13 | train | Train 13: The default HTTPS port is | 443, which means that all traffic on this | 443 | 443, which means that all traffic on this | YES | NO |
| 14 | train | Train 14: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 15 | train | Train 15: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 16 | train | Train 16: The largest planet in the solar system is | Jupiter, which has a diameter of approximately 79, | Jupiter | Jupiter, which has a diameter of approximately 79, | YES | NO |
| 17 | train | Train 17: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 18 | train | Train 18: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 19 | train | Train 19: The chemical symbol for gold is | Au. True or False?<br>To determine whether the ... | Au | Au. True or False?<br>To determine whether the ... | YES | NO |
| 20 | train | Train 20: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 21 | train | Train 21: The default HTTPS port is | 443, which means that all traffic on the | 443 | 443, which means that all traffic on the | YES | NO |
| 22 | train | Train 22: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 23 | train | Train 23: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 24 | train | Train 24: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 25 | train | Train 25: The capital of France is | Paris. It was founded in the 13th century | Paris | Paris. It was founded in the 13th century | YES | NO |
| 26 | train | Train 26: The currency of Japan is | the yen, and it's worth about $1.3 | Yen | the yen, and it's worth about $1.3 | YES | NO |
| 27 | train | Train 27: The chemical symbol for gold is | Au. True or False?<br>To determine whether the ... | Au | Au. True or False?<br>To determine whether the ... | YES | NO |
| 28 | train | Train 28: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 29 | train | Train 29: The default HTTPS port is | 443, which means that all traffic on the | 443 | 443, which means that all traffic on the | YES | NO |
| 30 | train | Train 30: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A | UDP | the ___ method to resolve domain names.<br>A. A | NO | YES |
| 31 | train | Train 31: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 32 | train | Train 32: The largest planet in the solar system is | Jupiter, which has a diameter of approximately 14. | Jupiter | Jupiter, which has a diameter of approximately 14. | YES | NO |
| 33 | train | Train 33: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 34 | train | Train 34: The currency of Japan is | the yen, and it's worth about 100 | Yen | the yen, and it's worth about 100 | YES | NO |
| 35 | train | Train 35: The chemical symbol for gold is | Au. Which of the following statements about gol... | Au | Au. Which of the following statements about gol... | YES | NO |
| 36 | train | Train 36: The author of Hamlet is | a famous playwright, and the play is also known... | Shakespeare | a famous playwright, and the play is also known... | NO | YES |
| 37 | train | Train 37: The default HTTPS port is | 443, which means that the user can access | 443 | 443, which means that the user can access | YES | NO |
| 38 | train | Train 38: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 39 | train | Train 39: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 40 | train | Train 40: The largest planet in the solar system is | Jupiter, which has a diameter of approximately 139 | Jupiter | Jupiter, which has a diameter of approximately 139 | YES | NO |
| 41 | train | Train 41: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 42 | train | Train 42: The currency of Japan is | the yen, and it's worth about $1.3 | Yen | the yen, and it's worth about $1.3 | YES | NO |
| 43 | train | Train 43: The chemical symbol for gold is | Au. Which of the following statements about gol... | Au | Au. Which of the following statements about gol... | YES | NO |
| 44 | train | Train 44: The author of Hamlet is | a famous playwright, and the play is also known... | Shakespeare | a famous playwright, and the play is also known... | NO | YES |
| 45 | train | Train 45: The default HTTPS port is | 443, which means that the user can access | 443 | 443, which means that the user can access | YES | NO |
| 46 | train | Train 46: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 47 | train | Train 47: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 48 | train | Train 48: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 49 | train | Train 49: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 50 | train | Train 50: The currency of Japan is | the yen, which is a type of ( ) currency. | Yen | the yen, which is a type of ( ) currency. | YES | NO |
| 51 | train | Train 51: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 52 | train | Train 52: The author of Hamlet is | ______.<br>A. Shakespeare<br>B. Dickens<br>C. | Shakespeare | ______.<br>A. Shakespeare<br>B. Dickens<br>C. | YES | NO |
| 53 | train | Train 53: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 54 | train | Train 54: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A... | UDP | the ___ method to resolve domain names.<br>A. A... | NO | YES |
| 55 | train | Train 55: The headquarters of Microsoft is in | which city?<br>A. Beijing<br>B. Shanghai<br>C | Redmond | which city?<br>A. Beijing<br>B. Shanghai<br>C | NO | YES |
| 56 | train | Train 56: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 57 | train | Train 57: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 58 | train | Train 58: The currency of Japan is | the yen, and it's worth approximately $1.2 | Yen | the yen, and it's worth approximately $1.2 | YES | NO |
| 59 | train | Train 59: The chemical symbol for gold is | ____<br>A. Au<br>B. Ag<br>C. | Au | ____<br>A. Au<br>B. Ag<br>C. | YES | NO |
| 60 | train | Train 60: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 61 | train | Train 61: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 62 | train | Train 62: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 63 | train | Train 63: The headquarters of Microsoft is in | which city?<br>A. Beijing<br>B. Shanghai<br>C | Redmond | which city?<br>A. Beijing<br>B. Shanghai<br>C | NO | YES |
| 64 | train | Train 64: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 65 | train | Train 65: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 66 | train | Train 66: The currency of Japan is | the yen, and it's worth about $1.2 | Yen | the yen, and it's worth about $1.2 | YES | NO |
| 67 | train | Train 67: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 68 | train | Train 68: The author of Hamlet is | a famous playwright, and the author of Romeo an... | Shakespeare | a famous playwright, and the author of Romeo an... | NO | YES |
| 69 | train | Train 69: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 70 | train | Train 70: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 71 | train | Train 71: The headquarters of Microsoft is in | which city?<br>A. New York<br>B. London | Redmond | which city?<br>A. New York<br>B. London | NO | YES |
| 72 | train | Train 72: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 73 | train | Train 73: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 74 | train | Train 74: The currency of Japan is | the yen, and it's worth about $1.2 | Yen | the yen, and it's worth about $1.2 | YES | NO |
| 75 | train | Train 75: The chemical symbol for gold is | Au. Is the following statement true or false? G... | Au | Au. Is the following statement true or false? G... | YES | NO |
| 76 | train | Train 76: The author of Hamlet is | a famous playwright, and the play is also known... | Shakespeare | a famous playwright, and the play is also known... | NO | YES |
| 77 | train | Train 77: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 78 | train | Train 78: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 79 | train | Train 79: The headquarters of Microsoft is in | which city?<br>A. Beijing<br>B. Shanghai<br>C | Redmond | which city?<br>A. Beijing<br>B. Shanghai<br>C | NO | YES |
| 80 | train | Train 80: The largest planet in the solar system is | Jupiter, which has a diameter of approximately 142 | Jupiter | Jupiter, which has a diameter of approximately 142 | YES | NO |
| 81 | train | Train 81: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 82 | train | Train 82: The currency of Japan is | the yen, and it's worth about $1.3 | Yen | the yen, and it's worth about $1.3 | YES | NO |
| 83 | train | Train 83: The chemical symbol for gold is | Au. Is the following statement true or false? G... | Au | Au. Is the following statement true or false? G... | YES | NO |
| 84 | train | Train 84: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 85 | train | Train 85: The default HTTPS port is | 443, which means that all traffic on the | 443 | 443, which means that all traffic on the | YES | NO |
| 86 | train | Train 86: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 87 | train | Train 87: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 88 | train | Train 88: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 89 | train | Train 89: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 90 | train | Train 90: The currency of Japan is | the yen, and it's worth about $1.2 | Yen | the yen, and it's worth about $1.2 | YES | NO |
| 91 | train | Train 91: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 92 | train | Train 92: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 93 | train | Train 93: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 94 | train | Train 94: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 95 | train | Train 95: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 96 | train | Train 96: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 97 | train | Train 97: The capital of France is | Paris. It was founded in the 12th century | Paris | Paris. It was founded in the 12th century | YES | NO |
| 98 | train | Train 98: The currency of Japan is | the yen, and it's worth about $1.2 | Yen | the yen, and it's worth about $1.2 | YES | NO |
| 99 | train | Train 99: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 100 | train | Train 100: The author of Hamlet is | a man who was born in which country?<br>Answer:... | Shakespeare | a man who was born in which country?<br>Answer:... | NO | YES |
| 101 | train | Train 101: The default HTTPS port is | 443, but it's not always the case | 443 | 443, but it's not always the case | YES | NO |
| 102 | train | Train 102: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A | UDP | the ___ method to resolve domain names.<br>A. A | NO | YES |
| 103 | train | Train 103: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 104 | train | Train 104: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 105 | train | Train 105: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 106 | train | Train 106: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 107 | train | Train 107: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 108 | train | Train 108: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 109 | train | Train 109: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 110 | train | Train 110: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A | UDP | the ___ method to resolve domain names.<br>A. A | NO | YES |
| 111 | train | Train 111: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 112 | train | Train 112: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 113 | train | Train 113: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 114 | train | Train 114: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 115 | train | Train 115: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 116 | train | Train 116: The author of Hamlet is | a famous playwright, and the author of Romeo an... | Shakespeare | a famous playwright, and the author of Romeo an... | NO | YES |
| 117 | train | Train 117: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 118 | train | Train 118: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 119 | train | Train 119: The headquarters of Microsoft is in | which city?<br>A. Beijing<br>B. Shanghai<br>C | Redmond | which city?<br>A. Beijing<br>B. Shanghai<br>C | NO | YES |
| 120 | train | Train 120: The largest planet in the solar system is | Jupiter, which has a diameter of approximately 79, | Jupiter | Jupiter, which has a diameter of approximately 79, | YES | NO |
| 121 | train | Train 121: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 122 | train | Train 122: The currency of Japan is | the yen, and it's worth about $3.5 | Yen | the yen, and it's worth about $3.5 | YES | NO |
| 123 | train | Train 123: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 124 | train | Train 124: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 125 | train | Train 125: The default HTTPS port is | 443, which means that if you are using | 443 | 443, which means that if you are using | YES | NO |
| 126 | train | Train 126: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 127 | train | Train 127: The headquarters of Microsoft is in | which city?<br>A. New York<br>B. London | Redmond | which city?<br>A. New York<br>B. London | NO | YES |
| 128 | train | Train 128: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 129 | train | Train 129: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 130 | train | Train 130: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 131 | train | Train 131: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 132 | train | Train 132: The author of Hamlet is | a famous playwright, and the play is also known... | Shakespeare | a famous playwright, and the play is also known... | NO | YES |
| 133 | train | Train 133: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 134 | train | Train 134: The DNS protocol primarily uses | the ___ address to identify hosts.<br>A. IP<br>B | UDP | the ___ address to identify hosts.<br>A. IP<br>B | NO | YES |
| 135 | train | Train 135: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 136 | train | Train 136: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 137 | train | Train 137: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 138 | train | Train 138: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 139 | train | Train 139: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 140 | train | Train 140: The author of Hamlet is | a famous playwright, and the play is also known... | Shakespeare | a famous playwright, and the play is also known... | NO | YES |
| 141 | train | Train 141: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 142 | train | Train 142: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 143 | train | Train 143: The headquarters of Microsoft is in | which city?<br>Answer Choices:<br>- A: New York | Redmond | which city?<br>Answer Choices:<br>- A: New York | NO | YES |
| 144 | train | Train 144: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 145 | train | Train 145: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 146 | train | Train 146: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 147 | train | Train 147: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 148 | train | Train 148: The author of Hamlet is | a famous playwright, and the play is also known... | Shakespeare | a famous playwright, and the play is also known... | NO | YES |
| 149 | train | Train 149: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 150 | train | Train 150: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A | UDP | the ___ method to resolve domain names.<br>A. A | NO | YES |
| 151 | train | Train 151: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 152 | train | Train 152: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 153 | train | Train 153: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 154 | train | Train 154: The currency of Japan is | the yen, and it's worth about $2.3 | Yen | the yen, and it's worth about $2.3 | YES | NO |
| 155 | train | Train 155: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 156 | train | Train 156: The author of Hamlet is | a famous playwright, and the play is also known... | Shakespeare | a famous playwright, and the play is also known... | NO | YES |
| 157 | train | Train 157: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 158 | train | Train 158: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 159 | train | Train 159: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 160 | train | Train 160: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 161 | train | Train 161: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 162 | train | Train 162: The currency of Japan is | the yen, and it's worth about $3.5 | Yen | the yen, and it's worth about $3.5 | YES | NO |
| 163 | train | Train 163: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 164 | train | Train 164: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 165 | train | Train 165: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 166 | train | Train 166: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 167 | train | Train 167: The headquarters of Microsoft is in | which city?<br>A. Beijing<br>B. Shanghai<br>C | Redmond | which city?<br>A. Beijing<br>B. Shanghai<br>C | NO | YES |
| 168 | train | Train 168: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 169 | train | Train 169: The capital of France is | Paris, the largest city in Europe. It has a pop... | Paris | Paris, the largest city in Europe. It has a pop... | YES | NO |
| 170 | train | Train 170: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 171 | train | Train 171: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 172 | train | Train 172: The author of Hamlet is | a man who was born in which country?<br>Answer:... | Shakespeare | a man who was born in which country?<br>Answer:... | NO | YES |
| 173 | train | Train 173: The default HTTPS port is | 443, and the default HTTP port is | 443 | 443, and the default HTTP port is | YES | NO |
| 174 | train | Train 174: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 175 | train | Train 175: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 176 | train | Train 176: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 177 | train | Train 177: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 178 | train | Train 178: The currency of Japan is | the yen, and it's worth about $2.3 | Yen | the yen, and it's worth about $2.3 | YES | NO |
| 179 | train | Train 179: The chemical symbol for gold is | Au. True or False?<br>A. True<br>B. | Au | Au. True or False?<br>A. True<br>B. | YES | NO |
| 180 | train | Train 180: The author of Hamlet is | a man who was born in which country?<br>Answer:... | Shakespeare | a man who was born in which country?<br>Answer:... | NO | YES |
| 181 | train | Train 181: The default HTTPS port is | 443, but it can be changed to any | 443 | 443, but it can be changed to any | YES | NO |
| 182 | train | Train 182: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 183 | train | Train 183: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 184 | train | Train 184: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 185 | train | Train 185: The capital of France is | Paris, the largest city in Europe. It has a pop... | Paris | Paris, the largest city in Europe. It has a pop... | YES | NO |
| 186 | train | Train 186: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 187 | train | Train 187: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 188 | train | Train 188: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 189 | train | Train 189: The default HTTPS port is | 443, but it can be changed to any | 443 | 443, but it can be changed to any | YES | NO |
| 190 | train | Train 190: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 191 | train | Train 191: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 192 | train | Train 192: The largest planet in the solar system is | ____<br>A. Venus<br>B. Mars<br>C. | Jupiter | ____<br>A. Venus<br>B. Mars<br>C. | NO | YES |
| 193 | train | Train 193: The capital of France is | Paris. It was founded in the 8th century by | Paris | Paris. It was founded in the 8th century by | YES | NO |
| 194 | train | Train 194: The currency of Japan is | the yen, and it's worth about $2.5 | Yen | the yen, and it's worth about $2.5 | YES | NO |
| 195 | train | Train 195: The chemical symbol for gold is | Au. Is this statement correct?<br>A. Correct<br>B | Au | Au. Is this statement correct?<br>A. Correct<br>B | YES | NO |
| 196 | train | Train 196: The author of Hamlet is | a famous playwright, and the play was written i... | Shakespeare | a famous playwright, and the play was written i... | NO | YES |
| 197 | train | Train 197: The default HTTPS port is | 443, but it can be changed to any | 443 | 443, but it can be changed to any | YES | NO |
| 198 | train | Train 198: The DNS protocol primarily uses | the ___ method to resolve domain names.<br>A. A- | UDP | the ___ method to resolve domain names.<br>A. A- | NO | YES |
| 199 | train | Train 199: The headquarters of Microsoft is in | Redmond, Washington. It has a large office buil... | Redmond | Redmond, Washington. It has a large office buil... | YES | NO |
| 200 | train | Train 200: The largest planet in the solar system is | ____<br>A. Mercury<br>B. Venus<br>C. | Jupiter | ____<br>A. Mercury<br>B. Venus<br>C. | NO | YES |
| 201 | seen_val | Seen Validation 1: The capital of Germany is | Berlin. <br><br>What is the next sentence?<br>O... | Berlin | Berlin. <br><br>What is the next sentence?<br>O... | YES | NO |
| 202 | seen_val | Seen Validation 2: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 203 | seen_val | Seen Validation 3: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 204 | seen_val | Seen Validation 4: The author of Odyssey is | a Greek poet and playwright. A) 正确 B | Homer | a Greek poet and playwright. A) 正确 B | NO | YES |
| 205 | seen_val | Seen Validation 5: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 206 | seen_val | Seen Validation 6: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 207 | seen_val | Seen Validation 7: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 208 | seen_val | Seen Validation 8: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 209 | seen_val | Seen Validation 9: The author of Odyssey is | a Greek poet and playwright. A) True B) False | Homer | a Greek poet and playwright. A) True B) False | NO | YES |
| 210 | seen_val | Seen Validation 10: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 211 | seen_val | Seen Validation 11: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 212 | seen_val | Seen Validation 12: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 213 | seen_val | Seen Validation 13: The currency of United Kingdom is | the Pound Sterling (GBP). The pound sterling wa... | Pound | the Pound Sterling (GBP). The pound sterling wa... | YES | NO |
| 214 | seen_val | Seen Validation 14: The author of Odyssey is | a Greek poet and playwright. A) True B) False | Homer | a Greek poet and playwright. A) True B) False | NO | YES |
| 215 | seen_val | Seen Validation 15: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 216 | seen_val | Seen Validation 16: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 217 | seen_val | Seen Validation 17: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 218 | seen_val | Seen Validation 18: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 219 | seen_val | Seen Validation 19: The author of Odyssey is | a Greek poet and playwright. A) 正确 B | Homer | a Greek poet and playwright. A) 正确 B | NO | YES |
| 220 | seen_val | Seen Validation 20: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 221 | seen_val | Seen Validation 21: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 222 | seen_val | Seen Validation 22: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 223 | seen_val | Seen Validation 23: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 224 | seen_val | Seen Validation 24: The author of Odyssey is | a man named Homer. He was born in the city of | Homer | a man named Homer. He was born in the city of | YES | NO |
| 225 | seen_val | Seen Validation 25: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 226 | seen_val | Seen Validation 26: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 227 | seen_val | Seen Validation 27: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 228 | seen_val | Seen Validation 28: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 229 | seen_val | Seen Validation 29: The author of Odyssey is | a Greek poet and playwright. He was born in Ath... | Homer | a Greek poet and playwright. He was born in Ath... | NO | YES |
| 230 | seen_val | Seen Validation 30: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 231 | seen_val | Seen Validation 31: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 232 | seen_val | Seen Validation 32: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 233 | seen_val | Seen Validation 33: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 234 | seen_val | Seen Validation 34: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 235 | seen_val | Seen Validation 35: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 236 | seen_val | Seen Validation 36: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 237 | seen_val | Seen Validation 37: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 238 | seen_val | Seen Validation 38: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 239 | seen_val | Seen Validation 39: The author of Odyssey is | a Greek poet and playwright. A) 正确 B | Homer | a Greek poet and playwright. A) 正确 B | NO | YES |
| 240 | seen_val | Seen Validation 40: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 241 | seen_val | Seen Validation 41: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 242 | seen_val | Seen Validation 42: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 243 | seen_val | Seen Validation 43: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 244 | seen_val | Seen Validation 44: The author of Odyssey is | a man named Homer. He was born in the city of | Homer | a man named Homer. He was born in the city of | YES | NO |
| 245 | seen_val | Seen Validation 45: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 246 | seen_val | Seen Validation 46: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 247 | seen_val | Seen Validation 47: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 248 | seen_val | Seen Validation 48: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 249 | seen_val | Seen Validation 49: The author of Odyssey is | a Greek poet and playwright. A) 正确 B | Homer | a Greek poet and playwright. A) 正确 B | NO | YES |
| 250 | seen_val | Seen Validation 50: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 251 | seen_val | Seen Validation 51: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 252 | seen_val | Seen Validation 52: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 253 | seen_val | Seen Validation 53: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 254 | seen_val | Seen Validation 54: The author of Odyssey is | a Greek poet and playwright. A) 正确 B | Homer | a Greek poet and playwright. A) 正确 B | NO | YES |
| 255 | seen_val | Seen Validation 55: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 256 | seen_val | Seen Validation 56: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 257 | seen_val | Seen Validation 57: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 258 | seen_val | Seen Validation 58: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 259 | seen_val | Seen Validation 59: The author of Odyssey is | a Greek poet and playwright. A) 正确 B | Homer | a Greek poet and playwright. A) 正确 B | NO | YES |
| 260 | seen_val | Seen Validation 60: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 261 | seen_val | Seen Validation 61: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 262 | seen_val | Seen Validation 62: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 263 | seen_val | Seen Validation 63: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 264 | seen_val | Seen Validation 64: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 265 | seen_val | Seen Validation 65: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 266 | seen_val | Seen Validation 66: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 267 | seen_val | Seen Validation 67: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 268 | seen_val | Seen Validation 68: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 269 | seen_val | Seen Validation 69: The author of Odyssey is | a man who was born in the year ________.<br>A | Homer | a man who was born in the year ________.<br>A | NO | YES |
| 270 | seen_val | Seen Validation 70: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 271 | seen_val | Seen Validation 71: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 272 | seen_val | Seen Validation 72: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 273 | seen_val | Seen Validation 73: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 274 | seen_val | Seen Validation 74: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 275 | seen_val | Seen Validation 75: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 276 | seen_val | Seen Validation 76: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 277 | seen_val | Seen Validation 77: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 278 | seen_val | Seen Validation 78: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 279 | seen_val | Seen Validation 79: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 280 | seen_val | Seen Validation 80: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 281 | seen_val | Seen Validation 81: The capital of Germany is | Berlin. It was founded in the year 192 | Berlin | Berlin. It was founded in the year 192 | YES | NO |
| 282 | seen_val | Seen Validation 82: The capital of Italy is | Rome. It was founded by the Romans in the 7 | Rome | Rome. It was founded by the Romans in the 7 | YES | NO |
| 283 | seen_val | Seen Validation 83: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 284 | seen_val | Seen Validation 84: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 285 | seen_val | Seen Validation 85: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 286 | seen_val | Seen Validation 86: The capital of Germany is | Berlin. It was founded in the year 192 | Berlin | Berlin. It was founded in the year 192 | YES | NO |
| 287 | seen_val | Seen Validation 87: The capital of Italy is | Rome. It was founded by the Romans in the 6 | Rome | Rome. It was founded by the Romans in the 6 | YES | NO |
| 288 | seen_val | Seen Validation 88: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 289 | seen_val | Seen Validation 89: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 290 | seen_val | Seen Validation 90: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 291 | seen_val | Seen Validation 91: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 292 | seen_val | Seen Validation 92: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 293 | seen_val | Seen Validation 93: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 294 | seen_val | Seen Validation 94: The author of Odyssey is | a man who has been in the business for over 1 | Homer | a man who has been in the business for over 1 | NO | YES |
| 295 | seen_val | Seen Validation 95: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 296 | seen_val | Seen Validation 96: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 297 | seen_val | Seen Validation 97: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 298 | seen_val | Seen Validation 98: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 299 | seen_val | Seen Validation 99: The author of Odyssey is | a man named Homer. He was born in the city of | Homer | a man named Homer. He was born in the city of | YES | NO |
| 300 | seen_val | Seen Validation 100: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 301 | seen_val | Seen Validation 101: The capital of Germany is | Berlin. It's the largest city in Europe and one of | Berlin | Berlin. It's the largest city in Europe and one of | YES | NO |
| 302 | seen_val | Seen Validation 102: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 303 | seen_val | Seen Validation 103: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 304 | seen_val | Seen Validation 104: The author of Odyssey is | a man who has been in the business for over 5 | Homer | a man who has been in the business for over 5 | NO | YES |
| 305 | seen_val | Seen Validation 105: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 306 | seen_val | Seen Validation 106: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 307 | seen_val | Seen Validation 107: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 308 | seen_val | Seen Validation 108: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 309 | seen_val | Seen Validation 109: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 310 | seen_val | Seen Validation 110: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 311 | seen_val | Seen Validation 111: The capital of Germany is | Berlin. It was founded in the year 187 | Berlin | Berlin. It was founded in the year 187 | YES | NO |
| 312 | seen_val | Seen Validation 112: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 313 | seen_val | Seen Validation 113: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 314 | seen_val | Seen Validation 114: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 315 | seen_val | Seen Validation 115: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 316 | seen_val | Seen Validation 116: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 317 | seen_val | Seen Validation 117: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 318 | seen_val | Seen Validation 118: The currency of United Kingdom is | the Pound Sterling (GBP). It is a unit of measu... | Pound | the Pound Sterling (GBP). It is a unit of measu... | YES | NO |
| 319 | seen_val | Seen Validation 119: The author of Odyssey is | a Greek poet and playwright. A) 正确 B | Homer | a Greek poet and playwright. A) 正确 B | NO | YES |
| 320 | seen_val | Seen Validation 120: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 321 | seen_val | Seen Validation 121: The capital of Germany is | Berlin. It was founded in the year ________.<br>A | Berlin | Berlin. It was founded in the year ________.<br>A | YES | NO |
| 322 | seen_val | Seen Validation 122: The capital of Italy is | Rome. It was founded by the Romans in the 8 | Rome | Rome. It was founded by the Romans in the 8 | YES | NO |
| 323 | seen_val | Seen Validation 123: The currency of United Kingdom is | the Pound Sterling (GBP). It is also known as B... | Pound | the Pound Sterling (GBP). It is also known as B... | YES | NO |
| 324 | seen_val | Seen Validation 124: The author of Odyssey is | a man who has been in the military for many years. | Homer | a man who has been in the military for many years. | NO | YES |
| 325 | seen_val | Seen Validation 125: The chemical symbol for silver is | ____<br>A. Ag<br>B. Au<br>C. | Ag | ____<br>A. Ag<br>B. Au<br>C. | YES | NO |
| 326 | unseen_val | Unseen Validation 1: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 327 | unseen_val | Unseen Validation 2: The Docker packaging artifact is called a | container. A container is a lightweight, execut... | container | container. A container is a lightweight, execut... | YES | NO |
| 328 | unseen_val | Unseen Validation 3: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 329 | unseen_val | Unseen Validation 4: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 330 | unseen_val | Unseen Validation 5: The protocol used for secure web traffic is | not the same as the one used for insecure web t... | HTTPS | not the same as the one used for insecure web t... | NO | YES |
| 331 | unseen_val | Unseen Validation 6: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the depl... | kube-scheduler | by the Kubernetes API server to manage the depl... | NO | YES |
| 332 | unseen_val | Unseen Validation 7: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 333 | unseen_val | Unseen Validation 8: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 334 | unseen_val | Unseen Validation 9: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 335 | unseen_val | Unseen Validation 10: The protocol used for secure web traffic is | not the same as the one used for secure email. ... | HTTPS | not the same as the one used for secure email. ... | NO | YES |
| 336 | unseen_val | Unseen Validation 11: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 337 | unseen_val | Unseen Validation 12: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 338 | unseen_val | Unseen Validation 13: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 339 | unseen_val | Unseen Validation 14: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 340 | unseen_val | Unseen Validation 15: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 341 | unseen_val | Unseen Validation 16: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 342 | unseen_val | Unseen Validation 17: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 343 | unseen_val | Unseen Validation 18: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 344 | unseen_val | Unseen Validation 19: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 345 | unseen_val | Unseen Validation 20: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 346 | unseen_val | Unseen Validation 21: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 347 | unseen_val | Unseen Validation 22: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 348 | unseen_val | Unseen Validation 23: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 349 | unseen_val | Unseen Validation 24: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 350 | unseen_val | Unseen Validation 25: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. TLS<br>C | HTTPS | called ____<br>A. SSL<br>B. TLS<br>C | NO | YES |
| 351 | unseen_val | Unseen Validation 26: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 352 | unseen_val | Unseen Validation 27: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 353 | unseen_val | Unseen Validation 28: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 354 | unseen_val | Unseen Validation 29: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 355 | unseen_val | Unseen Validation 30: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 356 | unseen_val | Unseen Validation 31: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 357 | unseen_val | Unseen Validation 32: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 358 | unseen_val | Unseen Validation 33: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 359 | unseen_val | Unseen Validation 34: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 360 | unseen_val | Unseen Validation 35: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 361 | unseen_val | Unseen Validation 36: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 362 | unseen_val | Unseen Validation 37: The Docker packaging artifact is called a | container, and the container image is also know... | container | container, and the container image is also know... | YES | NO |
| 363 | unseen_val | Unseen Validation 38: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 364 | unseen_val | Unseen Validation 39: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 365 | unseen_val | Unseen Validation 40: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 366 | unseen_val | Unseen Validation 41: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 367 | unseen_val | Unseen Validation 42: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 368 | unseen_val | Unseen Validation 43: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 369 | unseen_val | Unseen Validation 44: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 370 | unseen_val | Unseen Validation 45: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 371 | unseen_val | Unseen Validation 46: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 372 | unseen_val | Unseen Validation 47: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 373 | unseen_val | Unseen Validation 48: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 374 | unseen_val | Unseen Validation 49: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 375 | unseen_val | Unseen Validation 50: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 376 | unseen_val | Unseen Validation 51: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 377 | unseen_val | Unseen Validation 52: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 378 | unseen_val | Unseen Validation 53: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 379 | unseen_val | Unseen Validation 54: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 380 | unseen_val | Unseen Validation 55: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 381 | unseen_val | Unseen Validation 56: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 382 | unseen_val | Unseen Validation 57: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 383 | unseen_val | Unseen Validation 58: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 384 | unseen_val | Unseen Validation 59: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 385 | unseen_val | Unseen Validation 60: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 386 | unseen_val | Unseen Validation 61: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 387 | unseen_val | Unseen Validation 62: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 388 | unseen_val | Unseen Validation 63: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 389 | unseen_val | Unseen Validation 64: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 390 | unseen_val | Unseen Validation 65: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. TLS<br>C | HTTPS | called ____<br>A. SSL<br>B. TLS<br>C | NO | YES |
| 391 | unseen_val | Unseen Validation 66: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 392 | unseen_val | Unseen Validation 67: The Docker packaging artifact is called a | container, and the container image is also know... | container | container, and the container image is also know... | YES | NO |
| 393 | unseen_val | Unseen Validation 68: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 394 | unseen_val | Unseen Validation 69: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 395 | unseen_val | Unseen Validation 70: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 396 | unseen_val | Unseen Validation 71: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 397 | unseen_val | Unseen Validation 72: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 398 | unseen_val | Unseen Validation 73: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 399 | unseen_val | Unseen Validation 74: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 400 | unseen_val | Unseen Validation 75: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 401 | unseen_val | Unseen Validation 76: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 402 | unseen_val | Unseen Validation 77: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 403 | unseen_val | Unseen Validation 78: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 404 | unseen_val | Unseen Validation 79: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 405 | unseen_val | Unseen Validation 80: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 406 | unseen_val | Unseen Validation 81: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 407 | unseen_val | Unseen Validation 82: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 408 | unseen_val | Unseen Validation 83: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 409 | unseen_val | Unseen Validation 84: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 410 | unseen_val | Unseen Validation 85: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 411 | unseen_val | Unseen Validation 86: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 412 | unseen_val | Unseen Validation 87: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 413 | unseen_val | Unseen Validation 88: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 414 | unseen_val | Unseen Validation 89: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 415 | unseen_val | Unseen Validation 90: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 416 | unseen_val | Unseen Validation 91: The Kubernetes scheduler component is called | the "master" in Kubernetes. It manages the sche... | kube-scheduler | the "master" in Kubernetes. It manages the sche... | NO | YES |
| 417 | unseen_val | Unseen Validation 92: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 418 | unseen_val | Unseen Validation 93: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 419 | unseen_val | Unseen Validation 94: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 420 | unseen_val | Unseen Validation 95: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 421 | unseen_val | Unseen Validation 96: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 422 | unseen_val | Unseen Validation 97: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 423 | unseen_val | Unseen Validation 98: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 424 | unseen_val | Unseen Validation 99: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 425 | unseen_val | Unseen Validation 100: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 426 | unseen_val | Unseen Validation 101: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the depl... | kube-scheduler | by the Kubernetes API server to manage the depl... | NO | YES |
| 427 | unseen_val | Unseen Validation 102: The Docker packaging artifact is called a | container. A container is a lightweight, execut... | container | container. A container is a lightweight, execut... | YES | NO |
| 428 | unseen_val | Unseen Validation 103: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 429 | unseen_val | Unseen Validation 104: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 430 | unseen_val | Unseen Validation 105: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 431 | unseen_val | Unseen Validation 106: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 432 | unseen_val | Unseen Validation 107: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 433 | unseen_val | Unseen Validation 108: The Apache Kafka storage abstraction is a | key to understanding the power of distributed s... | topic | key to understanding the power of distributed s... | NO | YES |
| 434 | unseen_val | Unseen Validation 109: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 435 | unseen_val | Unseen Validation 110: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 436 | unseen_val | Unseen Validation 111: The Kubernetes scheduler component is called | the "scheduler" because it schedules pods to ru... | kube-scheduler | the "scheduler" because it schedules pods to ru... | NO | YES |
| 437 | unseen_val | Unseen Validation 112: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 438 | unseen_val | Unseen Validation 113: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 439 | unseen_val | Unseen Validation 114: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 440 | unseen_val | Unseen Validation 115: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 441 | unseen_val | Unseen Validation 116: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 442 | unseen_val | Unseen Validation 117: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 443 | unseen_val | Unseen Validation 118: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem. It... | topic | key component of the Apache Kafka ecosystem. It... | NO | YES |
| 444 | unseen_val | Unseen Validation 119: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 445 | unseen_val | Unseen Validation 120: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 446 | unseen_val | Unseen Validation 121: The Kubernetes scheduler component is called | by the Kubernetes API server to manage the sche... | kube-scheduler | by the Kubernetes API server to manage the sche... | NO | YES |
| 447 | unseen_val | Unseen Validation 122: The Docker packaging artifact is called a | container, and it's the smallest unit of softwa... | container | container, and it's the smallest unit of softwa... | YES | NO |
| 448 | unseen_val | Unseen Validation 123: The Apache Kafka storage abstraction is a | key component of the Apache Kafka ecosystem, pr... | topic | key component of the Apache Kafka ecosystem, pr... | NO | YES |
| 449 | unseen_val | Unseen Validation 124: The cloud object storage service on AWS is | a great option for storing and managing data. H... | S3 | a great option for storing and managing data. H... | NO | YES |
| 450 | unseen_val | Unseen Validation 125: The protocol used for secure web traffic is | called ____<br>A. SSL<br>B. HTTPS<br>C | HTTPS | called ____<br>A. SSL<br>B. HTTPS<br>C | YES | NO |
| 451 | ood | OOD Challenge 1: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 452 | ood | OOD Challenge 2: In machine learning, a model predicting its training da... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 453 | ood | OOD Challenge 3: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 454 | ood | OOD Challenge 4: In transformer models, the mechanism relating tokens is | not always clear. The following are some exampl... | attention | not always clear. The following are some exampl... | NO | YES |
| 455 | ood | OOD Challenge 5: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 456 | ood | OOD Challenge 6: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 457 | ood | OOD Challenge 7: In machine learning, a model predicting its training da... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 458 | ood | OOD Challenge 8: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 459 | ood | OOD Challenge 9: In transformer models, the mechanism relating tokens is | not clear. I am trying to understand how the mo... | attention | not clear. I am trying to understand how the mo... | NO | YES |
| 460 | ood | OOD Challenge 10: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 461 | ood | OOD Challenge 11: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 462 | ood | OOD Challenge 12: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 463 | ood | OOD Challenge 13: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 464 | ood | OOD Challenge 14: In transformer models, the mechanism relating tokens is | often a sequence of operations. The first opera... | attention | often a sequence of operations. The first opera... | NO | YES |
| 465 | ood | OOD Challenge 15: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 466 | ood | OOD Challenge 16: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 467 | ood | OOD Challenge 17: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 468 | ood | OOD Challenge 18: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 469 | ood | OOD Challenge 19: In transformer models, the mechanism relating tokens is | often a sequence of operations. The first opera... | attention | often a sequence of operations. The first opera... | NO | YES |
| 470 | ood | OOD Challenge 20: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 471 | ood | OOD Challenge 21: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 472 | ood | OOD Challenge 22: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 473 | ood | OOD Challenge 23: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 474 | ood | OOD Challenge 24: In transformer models, the mechanism relating tokens is | often a sequence of operations. The first opera... | attention | often a sequence of operations. The first opera... | NO | YES |
| 475 | ood | OOD Challenge 25: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 476 | ood | OOD Challenge 26: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 477 | ood | OOD Challenge 27: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 478 | ood | OOD Challenge 28: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 479 | ood | OOD Challenge 29: In transformer models, the mechanism relating tokens is | often a sequence of operations. The first opera... | attention | often a sequence of operations. The first opera... | NO | YES |
| 480 | ood | OOD Challenge 30: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 481 | ood | OOD Challenge 31: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 482 | ood | OOD Challenge 32: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 483 | ood | OOD Challenge 33: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 484 | ood | OOD Challenge 34: In transformer models, the mechanism relating tokens is | often a sequence of operations. The first opera... | attention | often a sequence of operations. The first opera... | NO | YES |
| 485 | ood | OOD Challenge 35: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 486 | ood | OOD Challenge 36: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 487 | ood | OOD Challenge 37: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 488 | ood | OOD Challenge 38: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 489 | ood | OOD Challenge 39: In transformer models, the mechanism relating tokens is | often a sequence of operations. The first opera... | attention | often a sequence of operations. The first opera... | NO | YES |
| 490 | ood | OOD Challenge 40: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 491 | ood | OOD Challenge 41: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 492 | ood | OOD Challenge 42: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 493 | ood | OOD Challenge 43: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 494 | ood | OOD Challenge 44: In transformer models, the mechanism relating tokens is | not always clear. The following are some exampl... | attention | not always clear. The following are some exampl... | NO | YES |
| 495 | ood | OOD Challenge 45: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
| 496 | ood | OOD Challenge 46: In quantum computing, a basic information unit is a | qubit. A qubit can be in one of two | qubit | qubit. A qubit can be in one of two | YES | NO |
| 497 | ood | OOD Challenge 47: In machine learning, a model predicting its training d... | called overfitting. Overfitting occurs when the... | overfitting | called overfitting. Overfitting occurs when the... | YES | NO |
| 498 | ood | OOD Challenge 48: In information theory, uncertainty is measured using | the entropy of a probability distribution. The ... | entropy | the entropy of a probability distribution. The ... | YES | NO |
| 499 | ood | OOD Challenge 49: In transformer models, the mechanism relating tokens is | not clear. The following are some examples of h... | attention | not clear. The following are some examples of h... | NO | YES |
| 500 | ood | OOD Challenge 50: In reliability engineering, Birnbaum importance measures | are used to assess the impact of a single failu... | sensitivity | are used to assess the impact of a single failu... | NO | YES |
