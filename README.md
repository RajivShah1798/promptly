# Promptly
## Introduction
Promptly is a simple online service that helps you quickly find answers in your documents whether those are PDFs, text files, or other kinds of files. Imagine having a virtual assistant who has read all your paperwork and can instantly tell you what’s inside each document.
1) **Upload Your Files:** You can upload documents (like PDFs or text files) through Promptly.
2) **Ask Questions:** Whenever you want information, just type in your question.
3) **Get Accurate Answers:** Promptly will search through the documents you’ve uploaded and give you a direct answer, almost like an expert who has read everything.

---

## Current Problems:
🚫 Manual Document Analysis – Professionals spend hours searching and summarizing documents.  
🚫 Keyword Search Limitations – Basic search tools fail to provide context-aware answers.  
🚫 Scalability Issues – Many solutions struggle with large document volumes.  

---

## Proposed Solutions:
✅ Persistent Multi-Document Memory – Users can create chatbot instances that retain knowledge.  
✅ Cross-Document Referencing – AI synthesizes insights across multiple files.  
✅ Role-Based Customization – Chatbot adapts to different roles (Legal, Finance, IT, HR).  
✅ On-Premise & Cloud Deployment – Enterprise-friendly with security and compliance in mind 

---

## Business Value Proposition
🏢 For Teams & Enterprises – A centralized AI knowledge assistant for fast and reliable document retrieval.  
📖 For Individuals – A personal AI assistant for organizing and querying private notes and study materials.  

--- 
## Project Directory Structure

```
├── assets/
│   ├── process_user_queries_dag.png  # User Query Pipeline Worflow Diagram
│   ├── rag_data_pipeline_dag.png  # Data Pipeline Workflow Diagram
│
├── data_pipeline/
│   ├── dags/
│   │   ├── dataPipeline.py  # User Queries DAG
│   │   ├── rag_data_pipeline.py  # Document Processing DAG
│   │   ├── scripts/
│   │   │   ├── email_utils.py  # Email notifications
│   │   │   ├── upload_data_GCS.py  # GCS Uploading
│   │   │   ├── data_preprocessing/
│   │   │   │   ├── check_pii_data.py  # PII Detection
│   │   │   │   ├── validate_schema.py  # Schema Validation
│   │   │   │   ├── data_utils.py  # Query Cleaning Functions
│   │   │   ├── supadb/
│   │   │   │   ├── supabase_utils.py  # Supabase Integration
│   │   │   ├── rag/
│   │   │   │   ├── validate_schema.py  # Schema Validation
│   │   │   │   ├── rag_utils.py  # Chunking & Embeddings
│   │   ├── tests/
│   │   │   ├── test_data_pii_redact.py  # Unit tests for PII detection and redaction
│   │   │   ├── test_rag_pipeline.py  # Unit tests for the RAG document chunking pipeline
│   │   │   ├── test_user_queries.py  # Unit tests for the user queries processing pipeline
│   ├── config.py  # API Keys & Configurations
│   ├── README.md  # Data Pipeline Documentation
│
├── data/
│   ├── rag_documents/  # Original PDFs & Text Files
│   ├── preprocessed_docs_chunks.csv/  # Cleaned & Chunked Data
│   ├── preprocessed_user_data.csv  # Processed User Queries
│
├── .dvc/  # DVC Configuration
├── .gitignore
├── .dvcignore
├── README.md  # Project Overview
├── requirements.txt  # Dependencies
```
---

## Data Source
### 1. User Queries
- Source: Retrieved from the conversations table in Supabase.
- Description: This table contains user-generated queries, which we have pre-filled with custom data to simulate various interaction scenarios.

### 2. Documents
- Source: Focused on IT specifications, we have curated data from publicly available requirements documents.
- Description: We have selectively gathered documents that provide detailed IT specifications, particularly from the PURE dataset, which comprises 79 publicly available natural language requirements documents collected from the web.
- Reference: [https://zenodo.org/records/5195084](https://zenodo.org/records/5195084)

---

## System Architecture

### 1. Data Pipeline:
- Readme continues [here](./data_pipeline/README.md)

### 2. Model Training and Deployment Pipeline
- Work in Progress

### 3. Data Drift Detection
- Work in Progress


### Project proposal [View Here](https://docs.google.com/document/d/1ZARzFI9JG95JxkLO9lD2LJZfr6xIisEh2SVzuhyPN3M/edit?usp=sharing)

## **Contact**

For any questions or issues, reach out to the Promptly team:

- **Ronak Vadhaiya** - vadhaiya.r@northeastern.edu
- **Sagar Bilwal** - bilwal.sagar@northeastern.edu
- **Kushal Shankar** - kushalshankar03@gmail.com
- **Rajiv Shah** - shah.rajiv1702@gmail.com
