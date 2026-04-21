# Biomedical NLP: PubMed RCT Sentence Classification

## Project Overview

This repository implements a biomedical natural language processing (NLP) project for sentence-level classification of clinical trial abstracts from the PubMed RCT 20k dataset. The goal is to classify sentences into one of five rhetorical roles: Background, Objective, Methods, Results, and Conclusions.

## Clinical Relevance

Understanding the structure of clinical trial abstracts is crucial for:
- Automated literature review and evidence synthesis
- Clinical decision support systems
- Research methodology analysis
- Knowledge extraction from biomedical literature

## Dataset Description

**Dataset**: PubMed RCT 20k (Hugging Face: `armanc/pubmed-rct20k`)

- **Task**: Sentence-level classification into 5 classes
- **Classes**: Background, Objective, Methods, Results, Conclusions
- **Size**: ~180k train / ~30k validation / ~30k test sentences
- **Source**: Clinical trial abstracts from PubMed
- **Pre-built splits**: Yes (train, validation, test)

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/BME-6938-Medical-AI-Project-3-Group-3.git
   cd BME-6938-Medical-AI-Project-3-Group-3
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run Training and Evaluation

### Training

Train the baseline LSTM model:
```bash
python src/train.py --model lstm --epochs 10 --batch_size 32
```

Train the transformer model (BERT):
```bash
python src/train.py --model transformer --epochs 5 --batch_size 16
```

### Evaluation

Evaluate a trained model:
```bash
python src/evaluate.py --model_path results/lstm_model.pth --model_type lstm
python src/evaluate.py --model_path results/transformer_model --model_type transformer
```

### Jupyter Notebooks

Launch Jupyter Lab to explore the data and run demos:
```bash
jupyter lab
```

Then open:
- `notebooks/EDA.ipynb` - Exploratory data analysis
- `notebooks/demo.ipynb` - Model demonstration

## Project Structure

```
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   ├── data_loader.py      # Dataset loading using Hugging Face
│   ├── preprocess.py       # Text preprocessing functions
│   ├── tokenizer_utils.py  # Tokenization for both models
│   ├── data_utils.py       # Data preparation utilities
│   ├── model_lstm.py       # LSTM classifier implementation
│   ├── model_transformer.py # BERT-based classifier
│   ├── train.py            # Training script for both models
│   ├── evaluate.py         # Evaluation and metrics
│   └── utils.py            # Utilities (seeds, helpers)
├── notebooks/
│   ├── EDA.ipynb           # Exploratory data analysis
│   └── demo.ipynb          # Model demonstration
├── results/                # Trained models and logs
└── figures/                # Generated plots and figures
```

## Implementation Details

- **Framework**: PyTorch for modeling
- **Transformer**: Hugging Face Transformers with Trainer API
- **Baseline**: Custom LSTM with embedding layer
- **Evaluation**: Accuracy, Precision, Recall, F1-score, Confusion Matrix
- **Reproducibility**: Fixed random seeds, consistent splits

## Results Summary

### LSTM Model
- **Accuracy**: TBD
- **F1-Score**: TBD
- **Common Confusions**: TBD

### Transformer Model (BERT)
- **Accuracy**: TBD
- **F1-Score**: TBD
- **Common Confusions**: TBD

## Error Analysis

The evaluation script includes detailed error analysis showing:
- Misclassified examples
- Class confusion patterns
- Qualitative analysis of prediction errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and evaluation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this code in your research, please cite:

```
@misc{pubmed-rct-classification,
  title={Biomedical NLP: PubMed RCT Sentence Classification},
  author={Your Name},
  year={2024},
  publisher={GitHub},
  url={https://github.com/your-username/BME-6938-Medical-AI-Project-3-Group-3}
}
```
