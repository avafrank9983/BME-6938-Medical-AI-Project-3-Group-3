"""
Training script for both LSTM and transformer models.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import argparse
import os
from tqdm import tqdm
from transformers import Trainer, TrainingArguments
import numpy as np

from data_loader import load_pubmed_rct_data, get_label_to_id
from preprocess import preprocess_sentences
from tokenizer_utils import LSTMTTokenizer, TransformerTokenizer
from data_utils import prepare_lstm_data, prepare_transformer_data
from model_lstm import LSTMClassifier
from model_transformer import create_transformer_model, get_model_config
from utils import set_seed, compute_metrics


def train_lstm_model(model: nn.Module,
                    train_loader: DataLoader,
                    val_loader: DataLoader,
                    num_epochs: int = 10,
                    learning_rate: float = 0.001,
                    device: str = 'cuda'):
    """
    Train LSTM baseline model for sentence classification.
    
    Implements standard supervised learning with validation monitoring:
    - Forward pass through model
    - Backward pass with gradient computation
    - Weight updates using Adam optimizer
    - Validation loss tracking for early stopping
    - Best model checkpointing based on validation performance
    
    The model uses Cross-Entropy Loss appropriate for multi-class (5-way) classification.
    Dropout regularization during training helps prevent overfitting on this moderate-sized dataset.

    Args:
        model (nn.Module): Initialized LSTM classifier model
        train_loader (DataLoader): Training data batches (sentences & labels)
        val_loader (DataLoader): Validation data batches for monitoring
        num_epochs (int): Number of passes through training data (default: 10)
        learning_rate (float): Adam optimizer learning rate, default 0.001
                              (slower than typical deep learning; appropriate for small model)
        device (str): 'cuda' for GPU or 'cpu' for CPU (default: 'cuda')
                      automatically falls back to CPU if GPU unavailable

    Returns:
        None (model saved to results/lstm_model.pth)
        
    Side Effects:
        - Creates results/ directory if not present
        - Saves best model checkpoint to results/lstm_model.pth
        - Prints training progress to console (loss every 50 batches, metrics every epoch)
        
    Training Details:
        - Uses CrossEntropyLoss (standard for multi-class classification)
        - Adam optimizer with learning rate 0.001
        - Validation monitored each epoch; best model saved
        - Early stopping possible if validation loss plateaus (future enhancement)
    """
    # USE DEVICE PROPERLY
    device = torch.device(device if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_val_loss = float('inf')

    for epoch in range(num_epochs):
        # Training
        model.train()
        train_loss = 0.0

        for i, (batch_x, batch_y) in enumerate(train_loader):
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

            # ADD PROGRESS PRINTING
            if (i + 1) % 50 == 0:  # Print every 50 batches
                print(f"Epoch {epoch+1}, Batch {i+1}, Loss: {loss.item():.4f}")

        train_loss /= len(train_loader)

        # Validation
        model.eval()
        val_loss = 0.0
        val_preds = []
        val_labels = []

        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                val_loss += loss.item()

                preds = torch.argmax(outputs, dim=1)
                val_preds.extend(preds.cpu().numpy())
                val_labels.extend(batch_y.cpu().numpy())

        val_loss /= len(val_loader)
        val_metrics = compute_metrics(val_labels, val_preds)

        print(f'Epoch {epoch+1}: Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')
        print(f'Val Metrics: {val_metrics}')

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'results/lstm_model.pth')
            print('Saved best model')


def train_transformer_model(model, train_dataset, val_dataset, config: dict):
    """
    Train fine-tuned transformer model using Hugging Face Trainer API.
    
    The Trainer API abstracts common PyTorch training patterns and provides:
    - Distributed training support (if multiple GPUs available)
    - Mixed precision training (FP16 on GPU for memory efficiency)
    - Automatic gradient accumulation (effective larger batch sizes)
    - Learning rate scheduling (linear warmup then linear decay)
    - Validation point evaluation
    - Best model checkpointing
    - Logging and progress tracking
    
    Fine-tuning strategy for BERT:
    - Start with bert-base-uncased pre-trained weights (general English)
    - Update all layers based on domain data (PubMed abstracts)
    - Learning rate 2e-5 chosen to prevent catastrophic forgetting of pre-training
    - 5 epochs sufficient; longer training risks overfitting to domain
    - Weight decay (L2 regularization) helps with generalization

    Args:
        model: Pre-initialized transformer model (from create_transformer_model())
        train_dataset: Hugging Face Dataset object with training sentences and labels
                      (must have 'input_ids', 'attention_mask', 'label' columns)
        val_dataset: Hugging Face Dataset object for validation (same schema)
        config (dict): Training configuration dict with parameters:
                      - output_dir: checkpoint directory
                      - learning_rate: fine-tuning LR (typically 2e-5 for BERT)
                      - per_device_train_batch_size: batch size for GPU memory
                      - num_train_epochs: passes through data
                      - weight_decay: L2 regularization coefficient
                      - etc. (see get_model_config() for full options)

    Returns:
        None (model saved to output_dir from config)
        
    Side Effects:
        - Saves model and tokenizer to output_dir
        - Generates training logs and metrics files
        - Creates checkpoint directories for each evaluation epoch
        
    Trainer Features Used:
        - Automatic validation at end of each epoch
        - Best model selection based on eval F1-score
        - Learning rate scheduling with warmup
        - Gradient accumulation (if batch_size < effective_batch_size)
    """
    training_args = TrainingArguments(**config)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model()


def main():
    parser = argparse.ArgumentParser(description='Train NLP models for PubMed RCT classification')
    parser.add_argument('--model', type=str, choices=['lstm', 'transformer'],
                       default='lstm', help='Model type to train')
    parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--max_length', type=int, default=128, help='Maximum sequence length')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--debug', action='store_true', help='Use small dataset subset for debugging')

    args = parser.parse_args()

    # Set seed for reproducibility
    set_seed(args.seed)

    # Load data
    print("Loading dataset...")
    dataset = load_pubmed_rct_data()

    # USE A SMALL SUBSET FOR DEBUGGING
    if args.debug:
        print("Using debug subset: 2000 train, 500 val samples")
        dataset['train'] = dataset['train'].select(range(2000))
        dataset['validation'] = dataset['validation'].select(range(500))

    if args.model == 'lstm':
        # Prepare LSTM data
        print("Preparing LSTM data...")
        tokenizer = LSTMTTokenizer()
        train_loader, val_loader, test_loader = prepare_lstm_data(
            tokenizer, dataset, args.max_length
        )

        # Create model
        vocab_size = tokenizer.vocab_size
        model = LSTMClassifier(vocab_size=vocab_size)

        # Train model
        print("Training LSTM model...")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        train_lstm_model(
            model, train_loader, val_loader,
            args.epochs, args.learning_rate, device
        )

    elif args.model == 'transformer':
        # Prepare transformer data
        print("Preparing transformer data...")
        tokenizer = TransformerTokenizer()
        train_dataset, val_dataset, test_dataset = prepare_transformer_data(
            tokenizer, dataset, args.max_length
        )

        # Create model
        model = create_transformer_model()

        # Get training config
        config = get_model_config("bert-base-uncased", num_labels=5)
        config['num_train_epochs'] = args.epochs
        config['per_device_train_batch_size'] = args.batch_size
        config['per_device_eval_batch_size'] = args.batch_size

        # Train model
        print("Training transformer model...")
        train_transformer_model(model, train_dataset, val_dataset, config)

    print("Training completed!")


if __name__ == '__main__':
    main()