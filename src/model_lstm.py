"""
LSTM model implementation for sentence-level biomedical text classification.

Architecture Overview:
    Input sequence of token IDs
        ↓
    Embedding Layer (learned word representations)
        ↓
    Bidirectional LSTM (capture context from both directions)
        ↓
    Dropout (regularization to prevent overfitting)
        ↓
    Fully Connected Layer (map to 5 output classes)
        ↓
    Softmax (probability distribution over classes)

Design Rationale:
- Bidirectional LSTM: medical text context from both left and right is critical
  (e.g., "enrolled in the study" needs both "enrolled" and "in the study")
- Stacked LSTMs: 2 layers provide sufficient capacity without excessive parameters
- Dropout: Essential regularization for domain-specific datasets (prevent overfitting)
- Shared embedding: Weight sharing improves generalization and reduces parameters

Hyperparameter Justification:
- embedding_dim=128: Balance between expressiveness and parameter count
  (too small → loses meaning, too large → overfits)
- hidden_dim=256: Sufficient to capture complex sentence structures
- num_layers=2: Depth enables hierarchy of representations (e.g., syntax → semantics)
- dropout=0.3: Aggressive regularization appropriate for moderate-sized biomedical dataset

Strengths:
- Handles variable-length sequences (via padding)
- Computationally efficient (can train on CPU if needed)
- Interpretable (can visualize hidden states)
- Sequential inductive bias matches sentence structure

Limitations:
- Long-range dependencies: LSTM struggles beyond 20-30 token spans (→ Transformer advantage)
- No pre-training: Must learn from task data alone (limited biomedical vocabulary capture)
- Context limited: Bidirectional scope limited to long-term memory capacity
"""

import torch
import torch.nn as nn
from typing import Tuple


class LSTMClassifier(nn.Module):
    """
    Bidirectional LSTM-based multi-class classifier for biomedical sentence classification.
    
    This model converts a sequence of tokens into a fixed-size representation using
    bidirectional LSTM, then predicts the rhetorical role (5 classes) of the sentence.
    
    Model Flow:
        Input Tokens (sequence)
            ↓
        Embedding lookup (vocab_size → embedding_dim)
            ↓
        Bidirectional LSTM (embedding_dim → 2*hidden_dim, num_layers stacks)
            ↓
        Last hidden state (2*hidden_dim due to bidirectionality)
            ↓
        Dropout (regularization, p=0.3)
            ↓
        Linear projection (2*hidden_dim → num_classes)
            ↓
        Logits for softmax (not include softmax; handled by CrossEntropyLoss)
    
    Attributes:
        embedding (nn.Embedding): Token embedding layer (shared weights across training)
        lstm (nn.LSTM): Bidirectional LSTM with num_layers stacked layers
        dropout (nn.Dropout): Regularization during training
        fc (nn.Linear): Classification head mapping hidden state to class probabilities
    """

    def __init__(self,
                 vocab_size: int,
                 embedding_dim: int = 128,
                 hidden_dim: int = 256,
                 num_layers: int = 2,
                 num_classes: int = 5,
                 dropout: float = 0.3):
        """
        Initialize LSTM classifier.
        
        Approach:
        - Embedding layer: Learns dense word vectors from training data
          Initialized randomly; updated during backprop
        - LSTM parameters: 4 gates per cell (input, forget, cell, output)
          Bidirectional doubles the hidden dimension
        - Linear layer: Maps combined forward+backward LSTM states to class logits
        - Weight initialization: Custom Xavier initialization for faster convergence

        Args:
            vocab_size (int): Number of unique tokens in vocabulary
                             (typically 10,000 for this dataset)
            embedding_dim (int): Dimension of learned token embeddings (default: 128)
                                Higher = more expressive but more parameters
            hidden_dim (int): LSTM hidden state dimension per direction (default: 256)
                             Total hidden = hidden_dim * 2 (bidirectional)
            num_layers (int): Number of stacked LSTM layers (default: 2)
                             More layers = more representation power but more parameters
            num_classes (int): Number of output classes for classification (default: 5)
                              Fixed to 5 for PubMed RCT task
            dropout (float): Dropout probability applied to LSTM outputs (default: 0.3)
                            Applied between layers; helps prevent overfitting
        
        Example:
            >>> model = LSTMClassifier(vocab_size=10000, embedding_dim=128, 
            ...                        hidden_dim=256, num_layers=2, num_classes=5)
            >>> input_ids = torch.randint(0, 10000, (32, 128))  # batch_size=32, seq_len=128
            >>> output = model(input_ids)  # shape: (32, 5)
        """
        super(LSTMClassifier, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=True
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # *2 for bidirectional

        # Initialize weights
        self._initialize_weights()

    def _initialize_weights(self):
        """Initialize model weights."""
        for name, param in self.named_parameters():
            if 'weight' in name:
                nn.init.xavier_uniform_(param)
            elif 'bias' in name:
                nn.init.constant_(param, 0.0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Args:
            x: Input tensor of shape (batch_size, seq_len)

        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        # Embedding
        embedded = self.embedding(x)  # (batch_size, seq_len, embedding_dim)

        # LSTM
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # lstm_out: (batch_size, seq_len, hidden_dim * 2)

        # Use the last hidden state
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)  # Concatenate bidirectional

        # Dropout and classification
        out = self.dropout(hidden)
        out = self.fc(out)
        return out