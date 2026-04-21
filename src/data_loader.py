"""
Data loading module for PubMed RCT 20k dataset.
"""

from datasets import load_dataset
from typing import Dict, Any


def load_pubmed_rct_data() -> Dict[str, Any]:
    """
    Load the PubMed RCT 20k dataset from Hugging Face.
    
    This function loads the PubMed RCT 20k dataset which contains ~180k train,
    ~30k validation, and ~30k test sentences labeled with rhetorical roles.

    Returns:
        Dict containing 'train', 'validation', 'test' dataset splits
        
    Example:
        >>> data = load_pubmed_rct_data()
        >>> print(data['train'][0])  # First training example
    """
    dataset = load_dataset("armanc/pubmed-rct20k")

    return {
        'train': dataset['train'],
        'validation': dataset['validation'],
        'test': dataset['test']
    }


def get_class_labels() -> Dict[str, str]:
    """
    Get the mapping from class names to display names.
    
    Returns:
        Dictionary mapping class names (lowercase) to display names (capitalized)
    """
    return {
        'background': 'Background',
        'objective': 'Objective',
        'methods': 'Methods',
        'results': 'Results',
        'conclusions': 'Conclusions'
    }


def get_label_to_id() -> Dict[str, int]:
    """
    Get the mapping from class names to class indices.
    
    This is used for training models to convert string labels to numeric indices.

    Returns:
        Dictionary mapping class names (lowercase) to integer indices (0-4)
    """
    return {
        'background': 0,
        'objective': 1,
        'methods': 2,
        'results': 3,
        'conclusions': 4
    }