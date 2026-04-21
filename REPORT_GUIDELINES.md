# Project 3 Report Writing Guidelines

This document provides guidance for writing the research paper-style report required for Project 3.

## Report Requirements

- **Length**: 4+ pages (minimum), single-spaced, 11-pt Times New Roman
- **Format**: PDF
- **Filename**: `Project3_[TeamName]_Report.pdf`
- **Figure Limit**: Figures count toward page limit; include 2-4 figures

## Required Sections

### 1. Abstract (0.25–0.5 page)
A concise summary of the problem, method, and key results that is understandable to someone unfamiliar with the project.

**Should Include:**
- Problem statement
- Methods used (LSTM baseline + Transformer)
- Main quantitative results (e.g., "BERT achieved 93% accuracy vs. LSTM's 86%")
- Key insight or implication

**Example structure:**
"Clinical trial abstracts contain structured information crucial for evidence-based medicine. We present an automated sentence classification system using PubMed RCT 20k dataset to classify sentences into rhetorical roles (Background, Objective, Methods, Results, Conclusions). We compare a baseline LSTM model with F1=0.85 to a fine-tuned BERT model with F1=0.92, demonstrating that transformer-based approaches significantly outperform recurrent architectures for this biomedical NLP task."

---

### 2. Introduction (0.75–1 page)
Clinical/medical background, motivation, and why this problem matters in healthcare.

**Should Include:**
- **Clinical background**: Why is sentence classification of clinical trials important?
  - Example: "Systematic reviews require manual extraction of key information from thousands of abstracts..."
- **Clinical use case**: Who benefits from this solution?
  - Example: "Clinical decision support systems, evidence synthesis platforms, or systematic review automation..."
- **Problem statement**: What is the specific challenge?
  - Example: "Although structured abstracts exist, extracting and organizing information remains labor-intensive..."
- **Project goals**: Clear, measurable objectives
  - Example: "Our goal is to develop models that automatically classify abstract sentences with >90% accuracy..."

**Suggested length breakdown:**
- Clinical motivation (3-4 sentences)
- Problem identification (2-3 sentences)
- Project objectives (2-3 sentences)

---

### 3. Literature Review (0.75–1 page)

Review of existing research related to the medical problem or clinical task.

**Requirements:**
- Minimum of 7 citations for this section (total minimum 15 citations across report)
- Discuss relevant ML methods, prior work, and state-of-the-art
- Highlight gap that this project addresses

**Topics to Cover:**
- Prior work on biomedical NLP (cite papers using PubMed data, abstract classification, etc.)
- RNN/LSTM approaches in NLP (general context)
- Transformer models and BERT (motivation for baseline comparison)
- Recent advances in domain-specific language models (e.g., BioClinicalBERT, PubMedBERT)
- Challenges in clinical NLP (domain terminology, class imbalance, etc.)

**Suggested Structure:**
1. "Early approaches to biomedical NLP relied on..." (historical context)
2. "Recent work has adopted transformer-based models..." (state-of-the-art)
3. "However, comparative studies between RNN and transformer approaches..." (gap)
4. "This project bridges this gap by..." (your contribution)

**Citation Format**: Use consistent format (APA, IEEE, or other academic standard)

---

### 4. Methods & Data (1–1.5 pages)

#### 4.1 Data Description
- **Source**: PubMed RCT 20k (Diversity of an open Hugging Face dataset)
- **Size**: ~180k train, ~30k validation, ~30k test sentences
- **Classes**: Background, Objective, Methods, Results, Conclusions (5-way classification)
- **Characteristics**: 
  - Structured medical abstracts from clinical trials
  - Balanced or imbalanced class distribution (cite your EDA findings)
  - Average sentence length (cite from EDA)
- **Preprocessing**: Document steps taken
  - Lowercasing, punctuation handling, whitespace normalization
  - Justification: "Lowercasing improves generalization to out-of-distribution text..."
- **Train/Validation/Test Split**: Already provided by dataset (80/10/10 or actual split)

#### 4.2 System Architecture
Include a high-level description of your pipeline:
- Data loading → Preprocessing → Tokenization → Model → Evaluation
- Consider including a figure (flowchart or architecture diagram)

#### 4.3 Implementation Details

**Baseline Model (LSTM):**
- Architecture: Embedding → Bidirectional LSTM → Dropout → Dense → Softmax
- **Hyperparameters**:
  - Vocab size: X (justify based on preprocessing)
  - Embedding dimension: 128 (why this choice?)
  - Hidden dimension: 256 (why this depth?)
  - Num layers: 2 (reasoning?)
  - Dropout: 0.3 (reasoning: helps prevent overfitting on small dataset)
  - Batch size: 32
  - Learning rate: 0.001 (why this rate?)
  - Optimizer: Adam
  - Loss function: CrossEntropyLoss

**Transformer Model (BERT):**
- Base model: `bert-base-uncased` or domain-specific variant (justify choice)
- Fine-tuning strategy: Freeze early layers (how many?) or full fine-tuning?
- **Hyperparameters**:
  - Max sequence length: 512 (why not shorter?)
  - Batch size: 16 (why smaller than LSTM?)
  - Learning rate: 2e-5 (standard for fine-tuning)
  - Num epochs: 5
  - Warmup steps: X
  - Optimizer: AdamW
  - Loss function: CrossEntropyLoss

**Feature Engineering/Preprocessing Decisions:**
- Why keep `-`, `/`, `%` in text? (biomedical relevance)
- Why lowercase? (domain practice)
- How handle unknown tokens? (OOV strategy for LSTM)

**Validation Strategy:**
- No cross-validation (already pre-split)
- Use validation set for:
  - Early stopping (if implemented)
  - Hyperparameter selection
- Final evaluation on held-out test set

**Tools & Libraries:**
- PyTorch for modeling framework
- Hugging Face Transformers for BERT
- Hugging Face Datasets for data loading
- scikit-learn for metrics
- Matplotlib/Seaborn for visualization

---

### 5. Results & Evaluation (1–1.5 pages)

#### 5.1 Quantitative Results
Present metrics in clear tables:

| Model | Accuracy | Precision (weighted) | Recall (weighted) | F1-score (weighted) |
|-------|----------|----------------------|-------------------|-------------------|
| LSTM Baseline | 0.86 | 0.86 | 0.86 | 0.85 |
| BERT (fine-tuned) | 0.93 | 0.93 | 0.93 | 0.92 |

**Per-Class Performance Table:**

| Class | LSTM F1 | BERT F1 | Sample Count |
|-------|---------|---------|--------------|
| Background | 0.82 | 0.91 | 45,000 |
| Objective | 0.80 | 0.89 | 45,000 |
| Methods | 0.88 | 0.95 | 45,000 |
| Results | 0.87 | 0.94 | 45,000 |
| Conclusions | 0.83 | 0.90 | 45,000 |

#### 5.2 Visualizations (include 2-4 figures)

1. **Confusion Matrix** (LSTM and BERT side-by-side)
   - Shows which classes are confused with each other
   - Example caption: "LSTM tends to confuse Background with Objective, while BERT shows improved separation of all classes."

2. **Class Distribution** (if applicable)
   - Bar plot showing train/validation/test split sizes per class
   - Caption: "PubMed RCT 20k maintains balanced class distributions across all splits."

3. **Training Curves** (optional)
   - Accuracy and loss over epochs for LSTM and BERT
   - Caption: "LSTM converges quickly but plateaus at lower accuracy; BERT shows steady improvement."

4. **Model Comparison**
   - Bar plot comparing accuracy, F1, precision, recall
   - Caption: "BERT outperforms LSTM across all metrics, suggesting that pre-trained contextual embeddings better capture abstract structure."

#### 5.3 Qualitative Analysis

**Successful Predictions:**
- Show 2-3 examples where both models predict correctly
- Explain what linguistic/contextual cues led to correct classification
- Example: "The sentence 'This study enrolled 100 patients...' is correctly classified as Methods because it contains methodologically relevant keywords (enrolled, patients, numbers)."

**Failure Cases:**
- Document common error patterns:
  - "Background vs. Objective confusion (5% of LSTM errors, 1% of BERT errors): Often occurs when results describe study hypotheses..."
  - "Long sequences causing errors in LSTM due to vanishing gradients..."
  - "Rare medical terminology causing misclassification..."
  - "Negation handling: Sentences with 'no significant difference' sometimes misclassified..."

#### 5.4 Clinical Relevance
- Are the predictive words/phrases medically meaningful?
- How do results reflect genuine ambiguity in clinical abstracts?
- What practical benefits would this system provide in real clinical workflows?

Example: "BERT's superior performance on Methods and Results classes is clinically significant because these categories contain actionable information for clinical decision-making. The 7% improvement in F1-score translates to approximately 2,100 correctly classified sentences per 30,000-sentence corpus, meaningfully reducing the manual annotation burden for systematic reviews."

---

### 6. Discussion & Limitations (0.75–1 page)

#### 6.1 Interpretation
- **What do results tell us?** Compare models and discuss why BERT outperforms LSTM
  - Pre-trained representations capture biomedical language better
  - Attention mechanisms help with long-range dependencies
- **Is the performance adequate for clinical deployment?** Discuss.
  - "93% accuracy may not be sufficient for direct clinical deployment without human review..."
  - "In systematic review workflows, even 5-10% errors could impact meta-analysis results..."

#### 6.2 Limitations
- **Dataset limitations**: 
  - Limited to structured abstracts (may not generalize to unstructured clinical notes)
  - PubMed abstracts may differ from other clinical texts (EHRs, case reports)
  - English-only data
  - Potential class imbalance (if present)
- **Model assumptions**:
  - Sequential nature of LSTM assumes causal dependency (may oversimplify)
  - BERT assumes transformer architecture is optimal (other architectures not tested)
- **Generalization concerns**:
  - How would models perform on other clinical domains?
  - Temporal generalization: Would models trained on 2017 papers perform on 2025 abstracts?
  - Cross-lingual applicability?

#### 6.3 Ethical Considerations

**Address:**
- **Bias in training data**: Does PubMed contain over-representation of certain medical specialties?
- **Fairness**: Do models perform equally well across classes? (Check per-class F1 scores)
- **Data privacy**: Are abstracts anonymized? (Usually yes for PubMed, but document)
- **Model misuse**: Could misclassification harm clinical decisions?
  - Example: "Misclassifying a Results section as Background could lead to incorrect interpretation of study findings in a clinical review..."
- **Patient safety implications**: What guarantees are needed before deployment?

#### 6.4 Future Work
- Expand to unstructured clinical text (EHRs, case notes, radiology reports)
- Fine-tune domain-specific models (BioClinicalBERT, PubMedBERT)
- Implement ensemble methods combining LSTM and BERT
- Add error correction via human-in-the-loop active learning
- Multi-language support for international research synthesis
- Real-time integration with clinical decision support systems

---

### 7. References (minimum 15 citations)

**Academic standard format** (APA shown below):

```
Dernoncourt, F., & Lee, J. Y. (2017). PubMed 200k RCT: A dataset for sequential sentence 
  classification in medical abstracts. In Proceedings of the 2017 international conference 
  on digital health (pp. 198-206). ACM.

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of deep 
  bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805.

Lee, J., Yoon, W., Kim, S., Kim, D., Kim, S., So, C. H., & Kang, J. (2020). BioBERT: 
  a pre-trained biomedical language representation model for biomedical text mining. 
  Bioinformatics, 36(4), 1234-1240.

[Additional 12+ citations...]
```

**Sources to include:**
- Dataset paper(s)
- LSTM/RNN foundational papers (e.g., Hochreiter & Schmidhuber on LSTMs)
- BERT and Transformer papers (Vaswani et al., Devlin et al.)
- Biomedical NLP papers (Lee et al. on BioBERT, PubMedBERT, etc.)
- Related sentence classification tasks
- Evaluation metrics and methodological papers

---

## Writing Tips

1. **Use past tense** for methods and results: "We trained the LSTM model..." not "We train..."
2. **Be specific**: Don't just say "the model performed well"; say "achieved 93% accuracy on the test set"
3. **Support claims with data**: Every statement about performance should cite results
4. **Use figures**: A picture/table saves hundreds of words
5. **Define acronyms**: First mention should define (e.g., "recurrent neural networks (RNNs)")
6. **Justify choices**: Explain WHY you chose hyperparameters, not just WHAT they are
7. **Acknowledge limitations**: Honest discussion of limitations strengthens the paper
8. **Connect to clinical relevance**: Regularly remind reader why this matters for healthcare

---

## Submission Checklist

- [ ] 4+ pages, single-spaced, 11-pt Times New Roman
- [ ] All 7 sections included (Abstract, Intro, Lit Review, Methods, Results, Discussion, References)
- [ ] ≥10 citations in Literature Review, ≥15 total citations
- [ ] 2-4 figures with descriptive captions
- [ ] Team member names and roles listed
- [ ] GitHub repository link included
- [ ] Addresses ethical considerations
- [ ] Discusses clinical relevance
- [ ] Includes error analysis and model comparison
- [ ] Saved as `Project3_[TeamName]_Report.pdf`

