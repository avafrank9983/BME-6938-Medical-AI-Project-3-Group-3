"""Data preparation utilities."""
import torch
from torch.utils.data import DataLoader, TensorDataset
from src.tokenizer_utils import LSTMTTokenizer
from src.preprocess import preprocess_sentences

LABEL_TO_ID = {"background":0,"objective":1,"methods":2,"results":3,"conclusions":4}

def prepare_lstm_data(tokenizer, dataset, max_length=128, batch_size=32):
    train_texts = preprocess_sentences(dataset["train"]["text"])
    train_labels = [LABEL_TO_ID[l] for l in dataset["train"]["label"]]
    val_texts = preprocess_sentences(dataset["validation"]["text"])
    val_labels = [LABEL_TO_ID[l] for l in dataset["validation"]["label"]]
    test_texts = preprocess_sentences(dataset["test"]["text"])
    test_labels = [LABEL_TO_ID[l] for l in dataset["test"]["label"]]
    print("Building vocabulary...")
    tokenizer.build_vocab(train_texts)
    print(f"Vocab size: {tokenizer.vocab_size}")
    def make_loader(texts, labels, shuffle=False):
        encoded = tokenizer.batch_encode(texts, max_length)
        tensor_labels = torch.tensor(labels, dtype=torch.long)
        ds = TensorDataset(encoded, tensor_labels)
        return DataLoader(ds, batch_size=batch_size, shuffle=shuffle, num_workers=0)
    return make_loader(train_texts,train_labels,shuffle=True),make_loader(val_texts,val_labels),make_loader(test_texts,test_labels)

def prepare_transformer_data(tokenizer, dataset, max_length=128):
    def convert_labels(examples):
        examples["label"] = [LABEL_TO_ID[l] for l in examples["label"]]
        return examples
    def tokenize_function(examples):
        texts = preprocess_sentences(examples["text"])
        return tokenizer.tokenizer(texts, truncation=True, padding="max_length", max_length=max_length)
    print("Tokenizing...")
    train_ds = dataset["train"].map(convert_labels,batched=True).map(tokenize_function,batched=True)
    val_ds = dataset["validation"].map(convert_labels,batched=True).map(tokenize_function,batched=True)
    test_ds = dataset["test"].map(convert_labels,batched=True).map(tokenize_function,batched=True)
    cols = ["input_ids","attention_mask","label"]
    for ds in [train_ds,val_ds,test_ds]: ds.set_format(type="torch",columns=cols)
    return train_ds, val_ds, test_ds
