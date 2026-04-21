"""
Transformer model implementation using Hugging Face.
"""

from transformers import AutoModelForSequenceClassification, AutoConfig


def create_transformer_model(model_name: str = "bert-base-uncased",
                              num_labels: int = 5) -> AutoModelForSequenceClassification:
    """
    Create a transformer model for sequence classification.

    Args:
        model_name: Hugging Face model name
        num_labels: Number of output classes

    Returns:
        Pre-trained transformer model for classification
    """
    config = AutoConfig.from_pretrained(model_name, num_labels=num_labels)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, config=config)
    return model


def get_model_config(model_name: str, num_labels: int = 5) -> dict:
    """
    Get TrainingArguments-compatible configuration for transformer training.
    Note: model_name is accepted as an arg but NOT passed to TrainingArguments
    (it is used upstream in create_transformer_model).

    Args:
        model_name: Model name (used by create_transformer_model, not TrainingArguments)
        num_labels: Number of classes

    Returns:
        Training configuration dictionary compatible with TrainingArguments
    """
    return {
        'output_dir': './results/transformer_model',
        'eval_strategy': 'epoch',
        'save_strategy': 'epoch',
        'learning_rate': 2e-5,
        'per_device_train_batch_size': 16,
        'per_device_eval_batch_size': 16,
        'num_train_epochs': 5,
        'weight_decay': 0.01,
        'load_best_model_at_end': True,
        'metric_for_best_model': 'f1',
        'greater_is_better': True,
        'logging_dir': './results/logs',
        'logging_steps': 100,
        'save_total_limit': 2,
    }
