# Project 3 Completion Checklist

Use this checklist to ensure your project meets all rubric requirements for submission.

## Report Submission

### Report Format & Content
- [ ] **File Format**: Report saved as PDF (not Word, Google Doc, etc.)
- [ ] **Filename**: Named `Project3_[TeamName]_Report.pdf`
- [ ] **Length**: At least 4 pages, single-spaced, 11-pt Times New Roman
- [ ] **Header**: Includes team member names, roles, GitHub link, submission date
- [ ] **Figures**: 2-4 figures included (confusion matrices, model comparison, class distribution)

### Required Sections
- [ ] **Abstract** (0.25-0.5 page)
  - [ ] Problem statement included
  - [ ] Methods mentioned (LSTM + Transformer)
  - [ ] Key quantitative results (accuracy/F1 scores)
  - [ ] Main insight/implication stated
  - [ ] Understandable to non-specialist reader

- [ ] **Introduction** (0.75-1 page)
  - [ ] Clinical/medical background explained
  - [ ] Why this problem matters in healthcare
  - [ ] Clinical use case and beneficiary population identified
  - [ ] Clear project goals and objectives stated
  - [ ] Why ML is needed for this task

- [ ] **Literature Review** (0.75-1 page)
  - [ ] **Minimum 7 citations in this section**
  - [ ] Discusses prior work on biomedical NLP
  - [ ] Covers RNN/LSTM approaches in NLP
  - [ ] Discusses Transformer models and BERT
  - [ ] Mentions domain-specific models if applicable (BioClinicalBERT, PubMedBERT)
  - [ ] Identifies gap that this project addresses
  - [ ] Positions project relative to existing approaches
  - [ ] Proper academic citations (APA, IEEE, or consistent format)

- [ ] **Methods & Data** (1-1.5 pages)
  - [ ] **Data Description**:
    - [ ] Dataset source clearly identified (PubMed RCT 20k)
    - [ ] Dataset size stated (~180k train, ~30k val, ~30k test)
    - [ ] 5 classes clearly defined
    - [ ] Data characteristics described (structured abstracts, balanced, medical vocabulary)
    - [ ] Train/validation/test split explained
  - [ ] **System Architecture**:
    - [ ] High-level pipeline described (loading → preprocessing → tokenization → model → evaluation)
    - [ ] Architecture diagram or flowchart included (optional but helpful)
  - [ ] **Implementation Details**:
    - [ ] **LSTM Baseline**:
      - [ ] Architecture clearly described (embedding → bidirectional LSTM → classification head)
      - [ ] Hyperparameters listed and justified:
        - [ ] Vocabulary size and why
        - [ ] Embedding dimension (e.g., 128) and rationale
        - [ ] Hidden dimensions (e.g., 256) and motivation
        - [ ] Num layers (e.g., 2) and justification
        - [ ] Dropout rate (e.g., 0.3) and effect
        - [ ] Batch size and learning rate rationale
        - [ ] Optimizer choice explained
    - [ ] **Transformer Model**:
      - [ ] Base model identified (bert-base-uncased or alternative)
      - [ ] Why this base model was chosen
      - [ ] Fine-tuning strategy described (full vs. partial)
      - [ ] Hyperparameters listed:
        - [ ] Max sequence length (512) and why
        - [ ] Batch size (why smaller than LSTM?)
        - [ ] Learning rate (2e-5) and standard justification
        - [ ] Epochs and rationale
        - [ ] Optimizer (AdamW) and why
  - [ ] **Preprocessing**:
    - [ ] Text cleaning steps explained (lowercasing, punctuation handling, normalization)
    - [ ] Justification for each preprocessing decision
    - [ ] Unknown token handling for LSTM documented
    - [ ] Padding/truncation strategy described
  - [ ] **Evaluation Strategy**:
    - [ ] Metrics explained (accuracy, precision, recall, F1-score, confusion matrix)
    - [ ] Validation approach described (use of validation set during training)
    - [ ] Test set held completely separate

- [ ] **Results & Evaluation** (1-1.5 pages)
  - [ ] **Quantitative Results**:
    - [ ] Performance table showing LSTM and BERT side-by-side
    - [ ] Metrics reported: accuracy, precision, recall, F1-score (at minimum)
    - [ ] Per-class breakdown provided
    - [ ] Confusion matrix results interpreted
    - [ ] Statistical confidence discussed if applicable
    - [ ] Tables are clear and labeled with captions
  - [ ] **Visualizations** (2-4 figures):
    - [ ] Confusion matrix (or matrices if comparing models)
    - [ ] Model comparison chart (e.g., bar plot of metrics)
    - [ ] Class distribution (optional but informative)
    - [ ] Training curves or other relevant plots (optional)
    - [ ] All figures have descriptive captions
    - [ ] All figures referenced in text
  - [ ] **Qualitative Analysis**:
    - [ ] Successful predictions examples given with explanation
    - [ ] Common error patterns identified and categorized
    - [ ] Failure modes discussed (ambiguity, long sequences, rare terms, class confusion)
    - [ ] Discussion of how LSTM vs BERT errors differ
  - [ ] **Clinical Relevance**:
    - [ ] Predictive words/phrases identified and checked for medical meaningfulness
    - [ ] Genuine ambiguity in data acknowledged
    - [ ] Practical benefits for clinical workflows discussed
    - [ ] Limitations for real-world deployment addressed

- [ ] **Discussion & Limitations** (0.75-1 page)
  - [ ] **Interpretation**:
    - [ ] Results explained in context of clinical problem
    - [ ] Why BERT outperforms LSTM analyzed
    - [ ] Performance adequacy for deployment discussed
    - [ ] Practical implications outlined
  - [ ] **Limitations**:
    - [ ] Dataset limitations acknowledged (English-only, PubMed-specific, structured format)
    - [ ] Generalization concerns raised (other clinical domains, temporal drift)
    - [ ] Model assumptions discussed
    - [ ] Potential overfitting or underfitting issues mentioned
  - [ ] **Ethical Considerations**:
    - [ ] Bias in training data addressed
    - [ ] Fairness across classes discussed 
    - [ ] Data privacy considerations mentioned
    - [ ] Potential for model misuse discussed
    - [ ] Patient safety implications considered
  - [ ] **Future Work**:
    - [ ] Extensions to unstructured text mentioned
    - [ ] Alternative models or ensemble approaches discussed
    - [ ] Real-world deployment challenges outlined
    - [ ] Suggested improvements listed

- [ ] **References**
  - [ ] **Minimum 15 total citations** (≥7 in Literature Review, ≥15 overall)
  - [ ] Consistent citation format used (APA, IEEE, etc.)
  - [ ] All sources peer-reviewed or reputable
  - [ ] Dataset paper cited
  - [ ] LSTM/RNN foundational papers cited
  - [ ] BERT/Transformer papers cited
  - [ ] Biomedical NLP literature cited
  - [ ] All citations in text appear in references (no orphans)

---

## GitHub Repository Requirements

### Repository Organization
- [ ] Repository is **PUBLIC** (not private)
- [ ] Repository link included in report
- [ ] Clean folder structure matching documentation
- [ ] Meaningful commit history (not squashed into single commit)
- [ ] Team member names and roles in README

### Code Quality

#### Documentation
- [ ] **README.md includes**:
  - [ ] Project title and one-sentence summary  
  - [ ] Clinical context section
  - [ ] Dataset description with link and citation
  - [ ] Quick start installation instructions
  - [ ] Step-by-step run instructions with expected commands
  - [ ] Expected runtime estimates
  - [ ] Project structure explanation
  - [ ] Team member names and roles
  - [ ] Dependencies listed
  - [ ] License information
- [ ] **Code documentation**:
  - [ ] All functions have docstrings
  - [ ] Docstrings explain purpose, arguments, returns
  - [ ] Complex logic has inline comments
  - [ ] Type hints added to functions (Python 3.6+)
- [ ] **requirements.txt**:
  - [ ] Pinned package versions (e.g., `torch>=2.0.0`)
  - [ ] All dependencies listed
  - [ ] No unnecessary packages included

#### Code Organization
- [ ] **src/ folder properly organized**:
  - [ ] `data_loader.py`: Dataset loading with clear function names
  - [ ] `preprocess.py`: Text preprocessing utilities
  - [ ] `tokenizer_utils.py`: Tokenization for both model types
  - [ ] `model_lstm.py`: LSTM implementation
  - [ ] `model_transformer.py`: Transformer/BERT implementation
  - [ ] `train.py`: Training orchestration
  - [ ] `evaluate.py`: Evaluation and metrics
  - [ ] `utils.py`: Reproducibility utilities
- [ ] Each module has a clear single responsibility
- [ ] No hard-coded paths (use config arguments)
- [ ] Proper error handling with informative messages

#### Reproducibility
- [ ] Random seeds set in `utils.py`
- [ ] [`set_seed()` function called at start of training](src/utils.py#L1)
- [ ] CUDA determinism enabled (even if slower)
- [ ] Data splits are deterministic
- [ ] Model initialization is seeded
- [ ] Comments explaining reproducibility approach

#### Code Style
- [ ] PEP 8 compliance (flake8 or similar)
- [ ] Meaningful variable names (no `x`, `df2`, `temp`)
- [ ] Function names are descriptive and lowercase with underscores
- [ ] Class names are PascalCase
- [ ] No print statements for debugging (use logging instead)
- [ ] Consistent indentation (4 spaces)

### Notebooks

#### EDA Notebook (exploratory-data-analysis)
- [ ] Dataset overview (size, shape, data types)
- [ ] Label/class distribution visualization
- [ ] Sentence length statistics and histogram
- [ ] Vocabulary analysis (unique tokens, top N tokens)
- [ ] Sample sentences from each class
- [ ] Class imbalance analysis
- [ ] Preprocessing impact (before/after comparison)
- [ ] Key insights documented
- [ ] Markdown cells explaining findings
- [ ] All cells have been executed and outputs visible

#### Demo Notebook
- [ ] Model loading code documented
- [ ] Example inference on sample sentences
- [ ] Confidence scores/probabilities shown
- [ ] Prediction visualization
- [ ] Error examples with analysis
- [ ] Comparison of LSTM vs BERT predictions
- [ ] Markdown explanation of findings
- [ ] All cells executed successfully

### Deliverable Files
- [ ] `results/` directory contains trained models
- [ ] `results/metrics.json` with evaluation results
- [ ] `figures/` directory with visualizations
- [ ] `.gitignore` excludes large files (models, data)
- [ ] No large files accidentally committed
- [ ] Clear README describing how to reproduce

---

## Model Implementation Specifics

### LSTM Model Checklist
- [ ] Embedding layer properly initialized
- [ ] Bidirectional LSTM implemented (not unidirectional)
- [ ] Dropout layer included for regularization
- [ ] Output layer maps to 5 classes
- [ ] Handles variable length sequences (padding)
- [ ] Vocabulary size documented
- [ ] Special tokens handled (UNK, PAD)
- [ ] Model architecture matches documentation
- [ ] Hyperparameters justified in code comments

### Transformer Model Checklist
- [ ] BERT base model loaded from Hugging Face
- [ ] Tokenizer matches model (`bert-base-uncased` uses WordPiece)
- [ ] Classification head added for 5 classes
- [ ] Fine-tuning strategy clearly implemented
- [ ] Appropriate learning rate for fine-tuning (2e-5)
- [ ] Training uses mixed precision if available
- [ ] Model saved with config and tokenizer
- [ ] Evaluation uses correct tokenization
- [ ] Hyperparameters match documentation

### Model Comparison
- [ ] Both models use same train/val/test splits
- [ ] Same preprocessing applied to both
- [ ] Fair comparison: different hyperparameters justified
- [ ] Runtime/efficiency compared
- [ ] Per-class performance compared
- [ ] Error patterns analyzed for both
- [ ] Discussion of why BERT might outperform LSTM

---

## Evaluation Metrics & Analysis

### Metrics Computation
- [ ] Accuracy calcul ated correctly
- [ ] Precision computed (weighted or macro, specified)
- [ ] Recall computed correctly
- [ ] F1-score computed (weighted average + macro average)
- [ ] Confusion matrix generated
- [ ] Metrics generated on held-out test set

### Error Analysis
- [ ] Confusion matrix visualized
- [ ] Most common errors identified
- [ ] Error categories defined (e.g., Background vs. Objective)
- [ ] Representative examples provided
- [ ] Per-class performance disparities noted
- [ ] Systematic errors investigated
- [ ] Qualitative patterns documented

### Class Imbalance Handling
- [ ] Class distribution analyzed
- [ ] If imbalanced: addressed with class weights or sampling
- [ ] Per-class metrics reported (not just overall accuracy)
- [ ] Macro-F1 computed (unweighted average across classes)
- [ ] Discussion of imbalance effects (if applicable)

---

## Reproducibility & Testing

### Before Final Submission
- [ ] Clone repository fresh (simulate student perspective)
- [ ] Run `pip install -r requirements.txt` successfully
- [ ] Run `python src/train.py --model lstm --epochs 1` (quick verification)
- [ ] Verify model checkpoint created in `results/`
- [ ] Run evaluation script successfully
- [ ] Run EDA notebook (check outputs)\
- [ ] Run demo notebook (check outputs)
- [ ] Confirm metrics match documentation

### Git Best Practices
- [ ] Meaningful commit messages (not "fix" or "asdf")
- [ ] Commits from all team members (if applicable)
- [ ] Clean history (no accidental files commits)
- [ ] No credentials committed (.gitignore used)
- [ ] Tags or releases for final submission (optional)

---

## Submission Checklist (Final)

### Canvas Submission
- [ ] One team member designated for final upload
- [ ] Report PDF uploaded with correct filename
- [ ] GitHub link provided in submission comments
- [ ] GitHub link also in report itself
- [ ] Peer evaluations completed by deadline
- [ ] All team members names in report

### Report File
- [ ] Saved as PDF (not Google Drive link)
- [ ] Filename: `Project3_[TeamName]_Report.pdf`
- [ ] File size reasonable (<20MB)
- [ ] No corruption (opens in PDF viewer)

### GitHub Repository
- [ ] Repository is public and accessible
- [ ] README complete and accurate
- [ ] Code is clean and documented
- [ ] All necessary files present
- [ ] No private data or credentials in repo

### Team Contributions Documented
- [ ] Each team member's role listed
- [ ] Specific contributions documented
- [ ] Peer evaluations submitted

---

## Grading Rubric Reference

### Report Scoring (60 points)
| Section | Points | Your Score | Notes |
|---------|--------|-----------|-------|
| Introduction | 10 | | Clinical motivation + use case |
| Literature Review | 10 | | Minimum 10 citations, synthesis |
| Methods & Data | 15 | | Dataset described, algorithm justified |
| Results & Evaluation | 10 | | Metrics + visualizations + baselines |
| Discussion & Limitations | 15 | | Interpretation + ethics + limitations |
| **Total Report** | **60** | | |

### Repository Scoring (40 points)
| Component | Points | Your Score | Notes |
|-----------|--------|-----------|-------|
| Code Organization & Quality | 10 | | Structure, docs, style |
| README & Documentation | 10 | | Completeness, clarity |
| EDA Notebook | 10 | | Dataset analysis, insights |
| Demo Notebook | 10 | | Model loading, inference |
| **Total Repository** | **40** | | |

### Overall Score
| Aspect | Score | Status |
|--------|-------|--------|
| Report (60 pts) | __ / 60 | |
| Repository (40 pts) | __ / 40 | |
| **Total** | **__ / 100** | |

---

## Tips for Success

1. **Start Early**: Writing a 4+ page report takes time; don't rush at last minute
2. **Literature Review**: Aim for 15+ quality citations from peer-reviewed sources
3. **Figures**: Use high-quality visualizations; confusion matrix and model comparison are essential
4. **Code Comments**: Document your thinking; future you and evaluators will appreciate it
5. **Reproducibility**: Test the repo from scratch before submission
6. **Clinical Context**: Connect every technical choice back to the clinical problem
7. **Peer Review**: Have teammates review report before submission
8. **Error Analysis**: Spend time understanding failures, not just successes

---

## Questions?

See [REPORT_GUIDELINES.md](REPORT_GUIDELINES.md) for detailed writing guidance.

