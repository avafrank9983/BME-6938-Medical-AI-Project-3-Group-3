"""
Training script for both LSTM and transformer models.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import argparse
import os
from transformers import Trainer, TrainingArguments

from data_loader import load_pubmed_rct_data
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

```
# Device setup
device = torch.device(device if torch.cuda.is_available() else "cpu")
model.to(device)

# Create results directory (outside src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

best_val_loss = float('inf')

for epoch in range(num_epochs):
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

        if (i + 1) % 50 == 0:
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

    print(f"Epoch {epoch+1}: Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
    print(f"Val Metrics: {val_metrics}")

    # Save best model
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        save_path = os.path.join(RESULTS_DIR, "lstm_model.pth")
        torch.save(model.state_dict(), save_path)
        print(f"Saved best model to {save_path}")
```

def train_transformer_model(model, train_dataset, val_dataset, config: dict):

```
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
```

def main():
parser = argparse.ArgumentParser(description='Train NLP models for PubMed RCT classification')
parser.add_argument('--model', type=str, choices=['lstm', 'transformer'], default='lstm')
parser.add_argument('--epochs', type=int, default=10)
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--learning_rate', type=float, default=0.001)
parser.add_argument('--max_length', type=int, default=128)
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--debug', action='store_true')

```
args = parser.parse_args()

set_seed(args.seed)

print("Loading dataset...")
dataset = load_pubmed_rct_data()

if args.debug:
    print("Using debug subset")
    dataset['train'] = dataset['train'].select(range(2000))
    dataset['validation'] = dataset['validation'].select(range(500))

if args.model == 'lstm':
    print("Preparing LSTM data...")
    tokenizer = LSTMTTokenizer()
    train_loader, val_loader, test_loader = prepare_lstm_data(
        tokenizer, dataset, args.max_length
    )

    model = LSTMClassifier(vocab_size=tokenizer.vocab_size)

    print("Training LSTM model...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    train_lstm_model(
        model,
        train_loader,
        val_loader,
        args.epochs,
        args.learning_rate,
        device
    )

elif args.model == 'transformer':
    print("Preparing transformer data...")
    tokenizer = TransformerTokenizer()
    train_dataset, val_dataset, test_dataset = prepare_transformer_data(
        tokenizer, dataset, args.max_length
    )

    model = create_transformer_model()

    config = get_model_config("bert-base-uncased", num_labels=5)
    config['num_train_epochs'] = args.epochs
    config['per_device_train_batch_size'] = args.batch_size
    config['per_device_eval_batch_size'] = args.batch_size

    print("Training transformer model...")
    train_transformer_model(model, train_dataset, val_dataset, config)

print("Training completed!")
```

if **name** == '**main**':
main()
