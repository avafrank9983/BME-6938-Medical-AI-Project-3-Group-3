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
        0: 'Background',
        1: 'Objective',
        2: 'Methods',
        3: 'Results',
        4: 'Conclusions'
    }


def get_label_to_id() -> Dict[str, int]:
    """
    Get the mapping from class names to class indices.

    Returns:
        Dictionary mapping class names to class indices
    """
    return {
        'Background': 0,
        'Objective': 1,
        'Methods': 2,
        'Results': 3,
        'Conclusions': 4
    }