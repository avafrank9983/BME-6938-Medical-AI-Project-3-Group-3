"""
Data preparation utilities for training and evaluation.
"""

import torch
from torch.utils.data import DataLoader, TensorDataset
from tokenizer_utils import LSTMTTokenizer, TransformerTokenizer
from preprocess import preprocess_sentences
from data_loader import get_label_to_id


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
    label_to_id = get_label_to_id()

    def create_dataloader(split_data, batch_size=32):
        texts = preprocess_sentences(split_data['text'])
        labels = [label_to_id[label] for label in split_data['label']]  # Convert string labels to integers

        # Build vocab if training
        if split_data == dataset['train']:
            tokenizer.build_vocab(texts)

        # Encode texts
        encoded_texts = tokenizer.batch_encode(texts, max_length)

        # Create dataset and dataloader
        tensor_dataset = TensorDataset(encoded_texts, torch.tensor(labels, dtype=torch.long))
        # ADD SPEED IMPROVEMENTS: num_workers and pin_memory
        dataloader = DataLoader(tensor_dataset, 
                              batch_size=batch_size, 
                              shuffle=(split_data == dataset['train']),
                              num_workers=4,  # Use multiple workers for data loading
                              pin_memory=True)  # Pin memory for faster GPU transfer

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