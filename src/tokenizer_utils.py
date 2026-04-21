"""
Tokenization utilities for both LSTM and transformer models.
"""

import torch
import re
from typing import List, Dict, Tuple, Any
from collections import Counter


class LSTMTTokenizer:
    """Tokenizer for LSTM model with custom vocabulary."""

    def __init__(self, max_vocab_size: int = 30000, min_freq: int = 2):
        """
        Initialize LSTM tokenizer.

        Args:
            max_vocab_size: Maximum vocabulary size
            min_freq: Minimum frequency for words to be included
        """
        self.max_vocab_size = max_vocab_size
        self.min_freq = min_freq
        self.vocab = None
        self.special_tokens = ['<pad>', '<unk>', '<sos>', '<eos>']
        self.word_to_idx = {}
        self.idx_to_word = {}

    def _tokenize(self, text: str) -> List[str]:
        """
        Basic English tokenization.

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        # Simple tokenization: lowercase, split on whitespace and punctuation
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def build_vocab(self, texts: List[str]) -> None:
        """
        Build vocabulary from training texts.

        Args:
            texts: List of text strings
        """
        # Count word frequencies
        counter = Counter()
        for text in texts:
            tokens = self._tokenize(text)
            counter.update(tokens)

        # Build vocabulary with special tokens first
        self.word_to_idx = {token: idx for idx, token in enumerate(self.special_tokens)}

        # Add frequent words
        for word, freq in counter.most_common(self.max_vocab_size - len(self.special_tokens)):
            if freq >= self.min_freq:
                self.word_to_idx[word] = len(self.word_to_idx)

        # Build reverse mapping
        self.idx_to_word = {idx: word for word, idx in self.word_to_idx.items()}

        # Set default index for unknown tokens
        self.default_index = self.word_to_idx['<unk>']

    @property
    def vocab_size(self):
        """Get the vocabulary size."""
        return len(self.word_to_idx) if self.word_to_idx else 0

    def encode(self, text: str, max_length: int = 128) -> List[int]:
        """
        Encode text to token IDs.

        Args:
            text: Input text
            max_length: Maximum sequence length

        Returns:
            List of token IDs
        """
        if not self.word_to_idx:
            raise ValueError("Vocabulary not built. Call build_vocab() first.")

        tokens = self._tokenize(text)
        token_ids = [self.word_to_idx.get(token, self.word_to_idx['<unk>']) for token in tokens]

        # Add SOS and EOS tokens
        token_ids = [self.word_to_idx['<sos>']] + token_ids + [self.word_to_idx['<eos>']]

        # Truncate or pad
        if len(token_ids) > max_length:
            token_ids = token_ids[:max_length]
        else:
            token_ids.extend([self.word_to_idx['<pad>']] * (max_length - len(token_ids)))

        return token_ids

    def batch_encode(self, texts: List[str], max_length: int = 128) -> torch.Tensor:
        """
        Encode batch of texts.

        Args:
            texts: List of text strings
            max_length: Maximum sequence length

        Returns:
            Tensor of shape (batch_size, max_length)
        """
        encoded = [self.encode(text, max_length) for text in texts]
        return torch.tensor(encoded, dtype=torch.long)


class TransformerTokenizer:
    """Tokenizer wrapper for transformer models."""

    def __init__(self, model_name: str = "bert-base-uncased"):
        """
        Initialize transformer tokenizer.

        Args:
            model_name: Hugging Face model name
        """
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def encode(self, text: str, max_length: int = 128) -> Dict[str, torch.Tensor]:
        """
        Encode text for transformer model.

        Args:
            text: Input text
            max_length: Maximum sequence length

        Returns:
            Dictionary with input_ids and attention_mask
        """
        return self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=max_length,
            return_tensors='pt'
        )

    def batch_encode(self, texts: List[str], max_length: int = 128) -> Dict[str, torch.Tensor]:
        """
        Encode batch of texts.

        Args:
            texts: List of text strings
            max_length: Maximum sequence length

        Returns:
            Dictionary with input_ids and attention_mask
        """
        return self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors='pt'
        )