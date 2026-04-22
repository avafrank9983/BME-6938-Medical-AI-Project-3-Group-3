"""
Evaluation module for model performance assessment and error analysis.

This module provides:
1. Model loading utilities (LSTM and Transformer)
2. Evaluation metrics computation (accuracy, precision, recall, F1)
3. Confusion matrix generation for error analysis
4. Per-class performance breakdown
5. Error pattern identification
6. Qualitative analysis of predictions

Metrics reported at multiple levels:
- Micro-averaging: treats all cases equally (useful for imbalanced data)
- Macro-averaging: treats all classes equally (reveals per-class disparities)
- Weighted-averaging: accounts for class frequency (overall system performance)

Usage:
    python evaluate.py --model_path results/lstm_model.pth --model_type lstm
    python evaluate.py --model_path results/transformer_model --model_type transformer
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import argparse
from src import train
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.data_loader import load_pubmed_rct_data, get_class_labels
from src.preprocess import preprocess_sentences
from src.tokenizer_utils import LSTMTTokenizer, TransformerTokenizer
from src.model_lstm import LSTMClassifier
from src.utils import compute_metrics


def load_lstm_model(model_path: str, vocab_size: int) -> nn.Module:
    """
    Load trained LSTM model.

    Args:
        model_path: Path to saved model
        vocab_size: Vocabulary size

    Returns:
        Loaded LSTM model
    """
    model = LSTMClassifier(vocab_size=vocab_size)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def load_transformer_model(model_path: str) -> AutoModelForSequenceClassification:
    """
    Load trained transformer model.

    Args:
        model_path: Path to saved model

    Returns:
        Loaded transformer model
    """
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return model


def evaluate_lstm_model(model: nn.Module,
                       test_loader: DataLoader,
                       device: str = 'cpu') -> tuple:
    """
    Evaluate LSTM model.

    Args:
        model: LSTM model
        test_loader: Test data loader
        device: Device to evaluate on

    Returns:
        Tuple of (predictions, true_labels)
    """
    model.to(device)
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            outputs = model(batch_x)
            preds = torch.argmax(outputs, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(batch_y.cpu().numpy())

    return all_preds, all_labels


def evaluate_transformer_model(model,
                              test_dataset,
                              tokenizer: TransformerTokenizer) -> tuple:
    """
    Evaluate transformer model.

    Args:
        model: Transformer model
        test_dataset: Test dataset
        tokenizer: Tokenizer

    Returns:
        Tuple of (predictions, true_labels)
    """
    model.eval()
    all_preds = []
    all_labels = []

    for example in test_dataset:
        inputs = {
            'input_ids': example['input_ids'].unsqueeze(0),
            'attention_mask': example['attention_mask'].unsqueeze(0)
        }

        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()

        all_preds.append(pred)
        all_labels.append(example['label'].item())

    return all_preds, all_labels


def plot_confusion_matrix(y_true, y_pred, class_names, save_path: str = 'figures/confusion_matrix.png'):
    """
    Plot and save confusion matrix.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: Class names
        save_path: Path to save the plot
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def error_analysis(texts, y_true, y_pred, class_names, num_examples: int = 5):
    """
    Perform error analysis by showing misclassified examples.

    Args:
        texts: Original texts
        y_true: True labels
        y_pred: Predicted labels
        class_names: Class names
        num_examples: Number of examples to show per error type
    """
    print("\n=== ERROR ANALYSIS ===")

    # Find misclassified examples
    misclassified = []
    for i, (true, pred) in enumerate(zip(y_true, y_pred)):
        if true != pred:
            misclassified.append((i, true, pred))

    print(f"Total misclassified: {len(misclassified)} out of {len(y_true)}")

    # Show examples of common confusions
    confusion_counts = {}
    for _, true, pred in misclassified:
        key = (true, pred)
        confusion_counts[key] = confusion_counts.get(key, 0) + 1

    # Sort by frequency
    sorted_confusions = sorted(confusion_counts.items(), key=lambda x: x[1], reverse=True)

    print("\nMost common confusions:")
    for (true_idx, pred_idx), count in sorted_confusions[:5]:
        print(f"{class_names[true_idx]} -> {class_names[pred_idx]}: {count} times")

    # Show example misclassifications
    print(f"\nExample misclassifications:")
    shown_per_type = {}
    for idx, true, pred in misclassified[:50]:  # Check first 50 misclassified
        key = (true, pred)
        if shown_per_type.get(key, 0) < num_examples:
            print(f"\nTrue: {class_names[true]}, Predicted: {class_names[pred]}")
            print(f"Text: {texts[idx][:200]}...")
            shown_per_type[key] = shown_per_type.get(key, 0) + 1


def main():
    parser = argparse.ArgumentParser(description='Evaluate trained NLP models')
    parser.add_argument('--model_path', type=str, required=True,
                       help='Path to trained model')
    parser.add_argument('--model_type', type=str, choices=['lstm', 'transformer'],
                       required=True, help='Model type')
    parser.add_argument('--max_length', type=int, default=128,
                       help='Maximum sequence length')

    args = parser.parse_args()

    # Load data
    print("Loading dataset...")
    dataset = load_pubmed_rct_data()
    class_names = list(get_class_labels().values())

    if args.model_type == 'lstm':
        # Prepare LSTM data
        print("Preparing LSTM data...")
        tokenizer = LSTMTTokenizer()
        _, _, test_loader = train.prepare_lstm_data(tokenizer, dataset, args.max_length)

        # Load model
        vocab_size = tokenizer.vocab_size
        model = load_lstm_model(args.model_path, vocab_size)

        # Evaluate
        print("Evaluating LSTM model...")
        preds, labels = evaluate_lstm_model(model, test_loader)

    elif args.model_type == 'transformer':
        # Prepare transformer data
        print("Preparing transformer data...")
        tokenizer = TransformerTokenizer()
        _, _, test_dataset = train.prepare_transformer_data(tokenizer, dataset, args.max_length)

        # Load model
        model = load_transformer_model(args.model_path)

        # Evaluate
        print("Evaluating transformer model...")
        preds, labels = evaluate_transformer_model(model, test_dataset, tokenizer)

    # Compute metrics
    metrics = compute_metrics(labels, preds)
    print("\n=== EVALUATION RESULTS ===")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1']:.4f}")

    # Classification report
    print("\nClassification Report:")
    print(classification_report(labels, preds, target_names=class_names))

    # Confusion matrix
    plot_confusion_matrix(labels, preds, class_names)

    # Error analysis
    test_texts = preprocess_sentences(dataset['test']['text'])
    error_analysis(test_texts, labels, preds, class_names)

    print(f"\nConfusion matrix saved to figures/confusion_matrix.png")


if __name__ == '__main__':
    # Import here to avoid circular import
    from src.data_utils import prepare_lstm_data, prepare_transformer_data
    main()