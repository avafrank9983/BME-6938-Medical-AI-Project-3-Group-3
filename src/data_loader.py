"""
Data loading module for PubMed RCT 20k dataset.
"""

from datasets import load_dataset
from typing import Dict, Any


def load_pubmed_rct_data() -> Dict[str, Any]:
    """
    Load the PubMed RCT 20k dataset from Hugging Face.

    Returns:
        Dict containing train, validation, and test splits
    """
    dataset = load_dataset("armanc/pubmed-rct20k")

    return {
        'train': dataset['train'],
        'validation': dataset['validation'],
        'test': dataset['test']
    }


def get_class_labels() -> Dict[int, str]:
    """
    Get the mapping from class indices to class names.

    Returns:
        Dictionary mapping class indices to class names
    """
    return {
        0: 'background',
        1: 'objective',
        2: 'methods',
        3: 'results',
        4: 'conclusions'
    }


def get_label_to_id() -> Dict[str, int]:
    """
    Get the mapping from class names to class indices.

    Returns:
        Dictionary mapping class names to class indices
    """
    return {
        'background': 0,
        'objective': 1,
        'methods': 2,
        'results': 3,
        'conclusions': 4
    }