"""
Utility functions for reproducibility and helpers.
"""

import torch
import numpy as np
import random
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from typing import Dict, Any


def set_seed(seed: int = 42):
    """
    Set random seed for reproducibility.

    Args:
        seed: Random seed value
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def compute_metrics(y_true, y_pred) -> Dict[str, float]:
    """
    Compute classification metrics.

    Args:
        y_true: True labels
        y_pred: Predicted labels

    Returns:
        Dictionary with accuracy, precision, recall, f1
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted'
    )

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }


def format_metrics(metrics: Dict[str, float]) -> str:
    """
    Format metrics for display.

    Args:
        metrics: Metrics dictionary

    Returns:
        Formatted string
    """
    return (f"Accuracy: {metrics['accuracy']:.4f}, "
            f"Precision: {metrics['precision']:.4f}, "
            f"Recall: {metrics['recall']:.4f}, "
            f"F1: {metrics['f1']:.4f}")


def save_metrics(metrics: Dict[str, float], filepath: str):
    """
    Save metrics to file.

    Args:
        metrics: Metrics dictionary
        filepath: Path to save file
    """
    with open(filepath, 'w') as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value:.4f}\n")


def load_metrics(filepath: str) -> Dict[str, float]:
    """
    Load metrics from file.

    Args:
        filepath: Path to metrics file

    Returns:
        Metrics dictionary
    """
    metrics = {}
    with open(filepath, 'r') as f:
        for line in f:
            key, value = line.strip().split(': ')
            metrics[key] = float(value)
    return metrics