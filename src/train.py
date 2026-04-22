"""
Training script for LSTM and Transformer models.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import argparse
import os
from transformers import Trainer, TrainingArguments

from src.data_loader import load_pubmed_rct_data
from src.tokenizer_utils import LSTMTTokenizer, TransformerTokenizer
from src.data_utils import prepare_lstm_data, prepare_transformer_data
from src.model_lstm import LSTMClassifier
from src.model_transformer import create_transformer_model, get_model_config
from src.utils import set_seed, compute_metrics


def train_lstm_model(model, train_loader, val_loader, num_epochs=10, learning_rate=0.001, device="cuda"):

    device = torch.device(device if torch.cuda.is_available() else "cpu")
    model.to(device)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESULTS_DIR = os.path.join(BASE_DIR, "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_val_loss = float("inf")

    for epoch in range(num_epochs):

        model.train()
        train_loss = 0

        for i, (x, y) in enumerate(train_loader):
            x, y = x.to(device), y.to(device)

            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        train_loss /= len(train_loader)

        model.eval()
        val_loss = 0
        preds, labels = [], []

        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                out = model(x)
                loss = criterion(out, y)
                val_loss += loss.item()

                preds.extend(torch.argmax(out, 1).cpu().numpy())
                labels.extend(y.cpu().numpy())

        val_loss /= len(val_loader)
        metrics = compute_metrics(labels, preds)

        print(f"Epoch {epoch+1}: train={train_loss:.4f}, val={val_loss:.4f}")
        print(metrics)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_path = os.path.join(RESULTS_DIR, "lstm_model.pth")
            torch.save(model.state_dict(), save_path)
            print("Saved model:", save_path)


def train_transformer_model(model, train_dataset, val_dataset, config):

    args = TrainingArguments(**config)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["lstm", "transformer"], default="lstm")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--max_length", type=int, default=128)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    set_seed(args.seed)

    print("Loading dataset...")
    dataset = load_pubmed_rct_data()

    if args.debug:
        dataset["train"] = dataset["train"].select(range(2000))
        dataset["validation"] = dataset["validation"].select(range(500))

    if args.model == "lstm":

        tokenizer = LSTMTTokenizer()
        train_loader, val_loader, test_loader = prepare_lstm_data(
            tokenizer, dataset, args.max_length
        )

        model = LSTMClassifier(vocab_size=tokenizer.vocab_size)

        train_lstm_model(
            model,
            train_loader,
            val_loader,
            args.epochs,
            args.learning_rate,
        )

    else:

        tokenizer = TransformerTokenizer()
        train_dataset, val_dataset, test_dataset = prepare_transformer_data(
            tokenizer, dataset, args.max_length
        )

        model = create_transformer_model()

        config = get_model_config("bert-base-uncased", num_labels=5)
        config["num_train_epochs"] = args.epochs
        config["per_device_train_batch_size"] = args.batch_size
        config["per_device_eval_batch_size"] = args.batch_size

        train_transformer_model(model, train_dataset, val_dataset, config)


if __name__ == "__main__":
    main()