# Promptly-Tuned: Fine-Tuning Qwen2.5-0.5B-Instruct for Technical Query Responses


This folder contains the code and documentation for fine-tuning the `Qwen/Qwen2.5-0.5B-Instruct` model from Hugging Face to improve its ability to respond to technical queries related to IT software systems. The fine-tuned model, named `promptly-tuned`, is designed to assist developers, engineers, and technical managers by providing accurate, context-aware responses based on conversation data stored in a Supabase database.

The project leverages LoRA (Low-Rank Adaptation) for efficient fine-tuning and evaluates performance against the baseline model using ROUGE scores. The fine-tuned model is hosted on Hugging Face at [rajiv8197/promptly-tuned](https://huggingface.co/rajiv8197/promptly-tuned).

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Dataset](#dataset)
- [Fine-Tuning Process](#fine-tuning-process)
- [Evaluation](#evaluation)
- [Usage](#usage)
- [Results](#results)

---

## Overview

This project fine-tunes the `Qwen/Qwen2.5-0.5B-Instruct` language model to enhance its performance in answering technical questions for IT software systems. The training data is sourced from a Supabase database containing conversation records, including queries, responses, and associated context chunks. The fine-tuning process uses LoRA for efficiency, and the results are compared against the baseline model using ROUGE metrics.

The fine-tuned model is optimized for:
- Providing factual, context-driven responses.
- Supporting developers and engineers with technical queries.
- Avoiding speculative or negative answers.

---

## Features

- **Model**: Fine-tuned `Qwen/Qwen2.5-0.5B-Instruct` with LoRA.
- **Data Source**: Conversation data fetched from Supabase.
- **Training**: Efficient fine-tuning with gradient accumulation.
- **Evaluation**: ROUGE-1, ROUGE-2, and ROUGE-L scores for quantitative analysis.
- **Deployment**: Model pushed to Hugging Face Hub (`rajiv8197/promptly-tuned`).
- **Monitoring**: Integrated with Weights & Biases (W&B) for training logs.

---

## Requirements

- Python 3.10+
- NVIDIA GPU with CUDA support (recommended for training)
- Kaggle or compatible environment with GPU acceleration
- Supabase account with API credentials
- Hugging Face account and token
- Weights & Biases (W&B) account and API key

---

## Installation

1. **Install dependencies**:
   ```bash
   pip install supabase transformers datasets torch peft accelerate wandb huggingface_hub rouge_score
    ```
2. **Set Up Environment Variables**: 
Create a .env file or configure secrets in your environment (e.g., Kaggle Secrets):
    ```
    SUPABASE_URL=your-supabase-url
    SUPABASE_KEY=your-supabase-key
    NOMIC_API_KEY=your-nomic-api-key
    HUGGINGFACE_TOKEN=your-hf-token
    WANDB_API_KEY=your-wandb-api-key
    ```

---

## Dataset

The dataset is sourced from a Supabase table named `conversations`, which includes:
- `query`: The user’s technical question.
- `response`: The expected answer.
- `conversation_document_chunks`: Related context chunks from documents.

Currently we have manually generated some examples based on available documents. In future, this finetuning will be driven by user interaction with the service.

### Preprocessing
- Data is fetched using the Supabase Python client.
- The dataset is split into training (80%), validation (10%), and test (10%) sets.
- Queries are formatted with a system prompt, context, and response, tokenized with padding/truncation to a max length of 1024 tokens.
- Labels are masked with `-100` before the assistant’s response to focus training on response generation.

### Dataset Size (Current)
- Total samples: 69
- Training: 55
- Validation: 6
- Test: 8

---

## Fine-Tuning Process

### Model
- **Base Model**: `Qwen/Qwen2.5-0.5B-Instruct`
- **Adaptation**: LoRA with `r=16`, `lora_alpha=32`, targeting `q_proj` and `v_proj` layers.

### Training Configuration
- **Batch Size**: 1 (with gradient accumulation steps = 8)
- **Learning Rate**: 2e-4
- **Epochs**: 3
- **Optimizer**: Default (AdamW)
- **Precision**: Full precision (fp16 disabled)
- **Output Directory**: `./promptly-finetune`
- **Hub Model ID**: `rajiv8197/promptly-tuned`

### Steps
1. Fetch conversation data from Supabase.
2. Split dataset into train, validation, and test sets.
3. Tokenize inputs with context and responses using the model’s tokenizer.
4. Fine-tune the model with LoRA using the `Trainer` from Hugging Face.
5. Save the best model based on validation loss and push to Hugging Face Hub.

---

## Evaluation

### Metrics
- **ROUGE-1**: Measures unigram overlap.
- **ROUGE-2**: Measures bigram overlap.
- **ROUGE-L**: Measures longest common subsequence.

### Methodology
- The baseline (`Qwen/Qwen2.5-0.5B-Instruct`) and fine-tuned models generate responses for test queries.
- Responses are compared against ground truth using the `rouge_score` library.
- Quantitative results are averaged; qualitative examples are provided for the first 3 test samples.

---

## Usage

### Loading the Fine-Tuned Model
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "rajiv8197/promptly-tuned"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

model.eval()
```

---

## Results

### Quantitative Results (ROUGE Scores)

| Example ID | Baseline ROUGE-1 | Baseline ROUGE-2 | Baseline ROUGE-L | Fine-Tuned ROUGE-1 | Fine-Tuned ROUGE-2 | Fine-Tuned ROUGE-L |
|------------|------------------|------------------|------------------|--------------------|--------------------|--------------------|
| 0          | 0.5244           | 0.5215           | 0.5244           | 0.5029             | 0.5000             | 0.5029             |
| 1          | 0.8397           | 0.8372           | 0.8397           | 0.8730             | 0.8710             | 0.8730             |
| 2          | 0.7629           | 0.7579           | 0.7629           | 0.7957             | 0.7912             | 0.7957             |
| 3          | 0.4828           | 0.4792           | 0.4828           | 0.7955             | 0.7931             | 0.7955             |
| 4          | 0.7143           | 0.7083           | 0.7143           | 0.8434             | 0.8395             | 0.8434             |
| 5          | 0.5656           | 0.5636           | 0.5656           | 0.8681             | 0.8671             | 0.8681             |
| 6          | 0.2342           | 0.2293           | 0.2342           | 0.3700             | 0.3636             | 0.3700             |
| 7          | 0.8163           | 0.8138           | 0.8163           | 0.9023             | 0.9008             | 0.9023             |
| Average    | 0.6175           | 0.6139           | 0.6175           | 0.7438             | 0.7408             | 0.7438             |


