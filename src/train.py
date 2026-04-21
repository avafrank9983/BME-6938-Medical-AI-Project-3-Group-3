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
from tokenize import LSTMTTokenizer, TransformerTokenizer
from model_lstm import LSTMClassifier
from model_transformer import create_transformer_model, get_model_config
from utils import set_seed, compute_metrics
from evaluate import evaluate_model


def prepare_lstm_data(tokenizer: LSTMTTokenizer, dataset, max_length: int = 128):
    """
    Prepare data for LSTM training.

    Args:
        tokenizer: LSTM tokenizer
        dataset: Hugging Face dataset
        max_length: Maximum sequence length

    Returns:
        DataLoader objects for train/val/test
    """
    def create_dataloader(split_data, batch_size=32):
        texts = preprocess_sentences(split_data['text'])
        labels = split_data['label']

        # Build vocab if training
        if split_data == dataset['train']:
            tokenizer.build_vocab(texts)

        # Encode texts
        encoded_texts = tokenizer.batch_encode(texts, max_length)

        # Create dataset and dataloader
        tensor_dataset = TensorDataset(encoded_texts, torch.tensor(labels, dtype=torch.long))
        dataloader = DataLoader(tensor_dataset, batch_size=batch_size, shuffle=(split_data == dataset['train']))

        return dataloader

    train_loader = create_dataloader(dataset['train'])
    val_loader = create_dataloader(dataset['validation'])
    test_loader = create_dataloader(dataset['test'])

    return train_loader, val_loader, test_loader


def prepare_transformer_data(tokenizer: TransformerTokenizer, dataset, max_length: int = 128):
    """
    Prepare data for transformer training.

    Args:
        tokenizer: Transformer tokenizer
        dataset: Hugging Face dataset
        max_length: Maximum sequence length

    Returns:
        Dataset objects for train/val/test
    """
    def tokenize_function(examples):
        texts = preprocess_sentences(examples['text'])
        return tokenizer.tokenizer(
            texts,
            truncation=True,
            padding='max_length',
            max_length=max_length
        )

    # Tokenize datasets
    train_dataset = dataset['train'].map(tokenize_function, batched=True)
    val_dataset = dataset['validation'].map(tokenize_function, batched=True)
    test_dataset = dataset['test'].map(tokenize_function, batched=True)

    # Set format for PyTorch
    train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    val_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    test_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

    return train_dataset, val_dataset, test_dataset


def train_lstm_model(model: nn.Module,
                    train_loader: DataLoader,
                    val_loader: DataLoader,
                    num_epochs: int = 10,
                    learning_rate: float = 0.001,
                    device: str = 'cuda'):
    """
    Train LSTM model.

    Args:
        model: LSTM model
        train_loader: Training data loader
        val_loader: Validation data loader
        num_epochs: Number of training epochs
        learning_rate: Learning rate
        device: Device to train on
    """
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_val_loss = float('inf')

    for epoch in range(num_epochs):
        # Training
        model.train()
        train_loss = 0.0

        for batch_x, batch_y in tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}'):
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

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
    Train transformer model using Hugging Face Trainer.

    Args:
        model: Transformer model
        train_dataset: Training dataset
        val_dataset: Validation dataset
        config: Training configuration
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

    args = parser.parse_args()

    # Set seed for reproducibility
    set_seed(args.seed)

    # Load data
    print("Loading dataset...")
    dataset = load_pubmed_rct_data()

    if args.model == 'lstm':
        # Prepare LSTM data
        print("Preparing LSTM data...")
        tokenizer = LSTMTTokenizer()
        train_loader, val_loader, test_loader = prepare_lstm_data(
            tokenizer, dataset, args.max_length
        )

        # Create model
        vocab_size = len(tokenizer.vocab)
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