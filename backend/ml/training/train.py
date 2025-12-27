# ml/training/train.py
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train():
    # Load dataset
    dataset = load_dataset("hate_speech_offensive")
    
    # Preprocess data
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=128
        )
    
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    
    # Prepare model
    model = AutoModelForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=3  # Adjust based on your dataset
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        push_to_hub=False,
        logging_dir='./logs',
        logging_steps=10,
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        compute_metrics=compute_metrics,
    )
    
    # Train the model
    trainer.train()
    
    # Save the model
    model.save_pretrained("./ml/models/content_moderation")
    tokenizer.save_pretrained("./ml/models/content_moderation")

if __name__ == "__main__":
    train()