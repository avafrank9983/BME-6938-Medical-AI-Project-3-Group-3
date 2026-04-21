"""
Tokenization utilities for both LSTM and transformer models.
"""

import torch
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data.utils import get_tokenizer
from transformers import AutoTokenizer
from typing import List, Dict, Tuple, Any
from collections import Counter


class LSTMTTokenizer:
    """Tokenizer for LSTM model with custom vocabulary."""

    def __init__(self, vocab_size: int = 30000, min_freq: int = 2):
        """
        Initialize LSTM tokenizer.

        Args:
            vocab_size: Maximum vocabulary size
            min_freq: Minimum frequency for words to be included
        """
        self.vocab_size = vocab_size
        self.min_freq = min_freq
        self.tokenizer = get_tokenizer('basic_english')
        self.vocab = None
        self.special_tokens = ['<pad>', '<unk>', '<sos>', '<eos>']

    def build_vocab(self, texts: List[str]) -> None:
        """
        Build vocabulary from training texts.

        Args:
            texts: List of text strings
        """
        def yield_tokens():
            for text in texts:
                yield self.tokenizer(text)

        self.vocab = build_vocab_from_iterator(
            yield_tokens(),
            specials=self.special_tokens,
            max_tokens=self.vocab_size,
            min_freq=self.min_freq
        )

        # Set default index for unknown tokens
        self.vocab.set_default_index(self.vocab['<unk>'])

    def encode(self, text: str, max_length: int = 128) -> List[int]:
        """
        Encode text to token IDs.

        Args:
            text: Input text
            max_length: Maximum sequence length

        Returns:
            List of token IDs
        """
        tokens = self.tokenizer(text)
        token_ids = self.vocab(tokens)

        # Truncate or pad
        if len(token_ids) > max_length:
            token_ids = token_ids[:max_length]
        else:
            token_ids.extend([self.vocab['<pad>']] * (max_length - len(token_ids)))

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