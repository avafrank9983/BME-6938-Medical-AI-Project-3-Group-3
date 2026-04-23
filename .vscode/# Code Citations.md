# Code Citations

## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/skumarlabs/nlp/blob/51b542cee9954162047410aeb13dfe45c8452a24/contractions.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/gopher408/nordstrom.3/blob/9d8328181b98c9b816d621b156ed5708eab52503/banter_nltk.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/gopher408/nordstrom.3/blob/9d8328181b98c9b816d621b156ed5708eab52503/banter_nltk.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/gopher408/nordstrom.3/blob/9d8328181b98c9b816d621b156ed5708eab52503/banter_nltk.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/gopher408/nordstrom.3/blob/9d8328181b98c9b816d621b156ed5708eab52503/banter_nltk.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        
```


## License: unknown
https://github.com/gopher408/nordstrom.3/blob/9d8328181b98c9b816d621b156ed5708eab52503/banter_nltk.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```


## License: unknown
https://github.com/gopher408/nordstrom.3/blob/9d8328181b98c9b816d621b156ed5708eab52503/banter_nltk.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```


## License: unknown
https://github.com/jazoza/architecturality/blob/29407ec3c1724834763445d9498e5cc67d0caae8/Twitter_MINING/word2vec-tweets-visualize.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```


## License: unknown
https://github.com/alhakimiakrm/Quill/blob/c18a4055b9a09405de8cbcbdf1f8dcb0f631f5d0/Code/main.py

```
Perfect! Let me continue creating all remaining essential files. I'll work through them systematically.

## Step 13: Create `data_loader.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/data_loader.py
"""
Data loading utilities for PubMed RCT dataset.

Handles:
- Loading dataset from Hugging Face
- Label mapping and class information
- Dataset statistics and info
- Data validation
"""

from datasets import load_dataset
from typing import Dict


def load_pubmed_rct_data():
    """
    Load PubMed RCT dataset from Hugging Face.

    Returns:
        Dataset object with 'train', 'validation', 'test' splits
    """
    print("Loading PubMed RCT dataset from Hugging Face...")
    dataset = load_dataset("armanc/pubmed-rct20k")
    return dataset


def get_class_labels() -> Dict[int, str]:
    """
    Get mapping of label indices to class names.

    Returns:
        Dictionary mapping label index to class name
    """
    labels = {
        0: "BACKGROUND",
        1: "OBJECTIVE",
        2: "METHODS",
        3: "RESULTS",
        4: "CONCLUSIONS"
    }
    return labels


def get_reverse_labels() -> Dict[str, int]:
    """
    Get mapping of class names to label indices.

    Returns:
        Dictionary mapping class name to label index
    """
    labels = get_class_labels()
    return {v: k for k, v in labels.items()}


def print_dataset_info(dataset):
    """
    Print dataset statistics and information.

    Args:
        dataset: Loaded dataset
    """
    labels = get_class_labels()
    
    print("\n" + "="*70)
    print("DATASET INFORMATION")
    print("="*70)
    
    for split in ['train', 'validation', 'test']:
        if split in dataset:
            split_data = dataset[split]
            print(f"\n{split.upper()} SET:")
            print(f"  Total samples: {len(split_data)}")
            
            # Label distribution
            label_counts = {}
            for example in split_data:
                label = example['label']
                label_counts[label] = label_counts.get(label, 0) + 1
            
            print(f"  Label distribution:")
            for label_idx in sorted(label_counts.keys()):
                count = label_counts[label_idx]
                pct = 100 * count / len(split_data)
                print(f"    {labels[label_idx]:12} : {count:8d} ({pct:5.1f}%)")
    
    print("\n" + "="*70)
````

## Step 14: Create `preprocess.py`

````python
# filepath: /workspaces/BME-6938-Medical-AI-Project-3-Group-3/src/preprocess.py
"""
Text preprocessing utilities for NLP pipeline.

Handles:
- Text normalization (lowercasing, whitespace)
- Punctuation handling
- Special character removal
- Text cleaning for consistency

Note: For LSTM, we keep most punctuation as it can be meaningful.
For Transformer, the tokenizer handles most preprocessing.
"""

import re
from typing import List, Union


def preprocess_sentences(texts: Union[List[str], str], lowercase: bool = True) -> Union[List[str], str]:
    """
    Preprocess text(s) for model input.

    Args:
        texts: Single text or list of texts
        lowercase: Whether to convert to lowercase

    Returns:
        Preprocessed text(s) in same format as input
    """
    def clean_text(text: str) -> str:
        """Clean single text sample."""
        if not isinstance(text, str):
            return ""
        
        # Lowercase if requested
        if lowercase:
            text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    # Handle single text or list
    if isinstance(texts, str):
        return clean_text(texts)
    else:
        return [clean_text(text) for text in texts]


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text: Input text
        keep_punctuation: Whether to keep standard punctuation

    Returns:
        Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:\-\(\)]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    return text


def expand_contractions(text: str) -> str:
    """
    Expand common contractions in text.

    Args:
        text: Input text

    Returns:
        Text with contractions expanded
    """
    contractions_dict = {
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "won't": "will not",
        "wouldn't": "would not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "it
```

