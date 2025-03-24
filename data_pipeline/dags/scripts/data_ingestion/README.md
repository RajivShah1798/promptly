# Data Generation Pipeline for Fine-Tuning

## Overview
Our product automates the generation of high-quality conversational datasets for fine-tuning large language models (LLMs). By leveraging a robust data pipeline and document processing techniques, we ensure efficient and secure handling of data while maintaining privacy and accuracy.

## Pipeline Workflow

### 1. Document Processing and PII Redaction
1. **Ingestion**: We initiate the process by running our data pipeline DAGs on the available documents.
2. **PII Detection and Redaction**: Using PII detection methods, we identify and redact sensitive information to ensure data privacy.
3. **Storage**: Cleaned documents are securely stored in **Supabase**, which also functions as our Retrieval-Augmented Generation (RAG) database.

### 2. Document Chunking and Embedding
1. **Semantic Chunking**: Processed documents undergo **Markdown semantic chunking** to divide them into meaningful sections.
2. **Embedding Creation**: We generate embeddings for each chunk using **Nomic embeddings** to facilitate fast and accurate document retrieval.

### 3. Synthetic Conversation Generation
1. **Contextual Generation**: Using the **LLaMA 3.2 8B** model, we create a set of synthetic conversations by:
   - Utilizing document chunks from **Supabase** as context.
   - Generating queries and responses.
   - Identifying and linking relevant document chunks to each conversation.
2. **Storage**: The generated conversations are stored in **Supabase** for future use.

### 4. Fine-Tuning Preparation
1. **Dataset Creation**: The generated conversations are compiled and added to the Supabase database.
2. **Model Fine-Tuning**: This dataset is used to fine-tune our LLM, enhancing its contextual understanding and response accuracy.

## Technology Stack
- **Data Pipeline**: Airflow DAGs
- **PII Detection**: Custom PII redaction methods
- **Storage & RAG**: Supabase
- **Chunking**: Markdown semantic chunking
- **Embeddings**: Nomic embeddings
- **LLM Model**: LLaMA 3.2 8B

## Usage
1. Ensure the document source is accessible and ingested via the pipeline.
2. Run the data pipeline DAGs to process and store cleaned documents.
3. Generate synthetic conversations using the LLaMA 3.2 8B model.
4. Use the resulting dataset to fine-tune our target LLM for improved performance.

## Future Improvements
- Integrate multi-modal document support.
- Optimize conversation generation for greater diversity and contextual depth.

