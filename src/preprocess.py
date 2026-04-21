"""
Text preprocessing utilities for biomedical text.
"""

import re
import string
from typing import List


def clean_text(text: str) -> str:
    """
    Clean and preprocess text for NLP tasks.

    Args:
        text: Input text string

    Returns:
        Cleaned text string
    """
    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove punctuation (keep some biomedical-relevant characters)
    # Keep: - (for compound words), / (for ratios), % (for percentages)
    punctuation_to_remove = string.punctuation.replace('-', '').replace('/', '').replace('%', '')
    text = text.translate(str.maketrans('', '', punctuation_to_remove))

    return text


def preprocess_sentences(sentences: List[str]) -> List[str]:
    """
    Apply preprocessing to a list of sentences.

    Args:
        sentences: List of sentence strings

    Returns:
        List of preprocessed sentence strings
    """
    return [clean_text(sentence) for sentence in sentences]


def get_sentence_lengths(sentences: List[str]) -> List[int]:
    """
    Get the lengths of sentences (number of words).

    Args:
        sentences: List of sentence strings

    Returns:
        List of sentence lengths
    """
    return [len(sentence.split()) for sentence in sentences]