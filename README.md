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
├── assets/                     # Diagrams and visual assets
│   ├── process_user_queries_dag.png  # User Query Pipeline Workflow Diagram
│   ├── rag_data_pipeline_dag.png     # Data Pipeline Workflow Diagram
│   ├── Data Pipeline Architecture.png
│   ├── Model Training & Deployment Architecture.png
│   ├── Drift Detection.png
│   ├── pipeline_optimization.png
│
├── data_pipeline/              # Data processing and ingestion pipeline
│   ├── dags/                   # Airflow DAGs for pipeline orchestration
│   │   ├── dataPipeline.py     # User Queries DAG
│   │   ├── rag_data_pipeline.py # Document Processing DAG
│   │   ├── scripts/            # Scripts for data preprocessing and ingestion
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
│   ├── config.py               # API Keys & Configurations
│   ├── README.md               # Data Pipeline Documentation
│
├── model/                      # Model serving, testing, and deployment
│   ├── serve.py                # FastAPI server for serving the model
│   ├── deploy_server.py        # Deployment script for Google Cloud Vertex AI
│   ├── Dockerfile              # Docker configuration for containerizing the model server
│   ├── requirements.txt        # Python dependencies for the model
│   ├── tests/                  # Unit tests for the model and APIs
│   │   ├── api_test.py         # Test script for the REST API
│   │   └── sdk_test.py         # Test script for SDK integration
│   ├── README.md               # Model Directory Documentation
│
├── model_pipeline/             # Model training and fine-tuning pipeline
│   ├── training/               # Training scripts and notebooks
│   │   ├── promptly-finetuning.ipynb  # Model training Jupyter notebook
│   │   ├── README.md           # Training-specific documentation
│   ├── scripts/
│   │   ├── bias_detection.py   # Script for detecting bias while training the model
│   │   ├── load_data.py        # Load data from Supabase
│   │   ├── streamlit_ui.py     # Streamlit user interface for the app
│   ├── mlflow/
│   │   ├── Dockerfile          # Docker file for setting up MLflow in GCP Instance
│   ├── README.md               # Model Pipeline Documentation
│
├── data/                       # Data storage and processing
│   ├── rag_documents/          # Original PDFs & Text Files
│   ├── preprocessed_docs_chunks.csv  # Cleaned & Chunked Data
│   ├── preprocessed_user_data.csv    # Processed User Queries
│
├── .github/workflows/          # CI/CD workflows
│   ├── README.md               # GitHub Actions Documentation
│
├── .dvc/                       # DVC Configuration
├── .gitignore                  # Git ignore file
├── .dvcignore                  # DVC ignore file
├── requirements.txt            # Python dependencies
├── README.md                   # Global project documentation
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
![Data Pipeline Architecture](/assets/Data%20Pipeline%20Architecture.png)
- The data pipeline automates document ingestion, preprocessing, and storage in Supabase.
- For detailed documentation, refer to the [Data Pipeline README](./data_pipeline/README.md).

### 2. Model Training and Deployment Pipeline
![Model Training & Deployment Architecture](/assets/Model%20Training%20&%20Deployment%20Architecture.png)
- The model training pipeline handles fine-tuning and evaluation of the model. For more details, refer to the [Model Training README](./model_pipeline/README.md).
- The model serving is the deployment of model to Vertex AI. For more details, refer to the [Model Serving README](./model/README.md).

### 3. Data Drift Detection
![Data Drift Detection Architecture](/assets/Drift%20Detection.png)
- User dominance is verified to check if the drift is caused by a single user or skewed usage pattern.
- If drift is detected, it triggers downstream actions:
- Drift trend analysis to monitor changes over time.
- Model retraining is triggered automatically if needed.
- The entire process is automated via an Apache Airflow DAG, which runs once a day.
- Upon completion or detection, an email notification is sent to alert stakeholders.

---

## Key Features

1. **Cross-Document Retrieval:** Enables querying across multiple documents for context-aware answers.
2. **Fine-Tuned Model:** Uses a fine-tuned version of `Qwen/Qwen2.5-0.5B-Instruct` for text generation tasks.
3. **Cloud Deployment:** Supports deployment to Google Cloud Vertex AI for scalable inference.
4. **CI/CD Integration:** Automates model training and deployment using GitHub Actions.

---


### Project proposal [View Here](https://docs.google.com/document/d/1ZARzFI9JG95JxkLO9lD2LJZfr6xIisEh2SVzuhyPN3M/edit?usp=sharing)

## **Contact**

For any questions or issues, reach out to the Promptly team:

- **Ronak Vadhaiya** - vadhaiya.r@northeastern.edu
- **Sagar Bilwal** - bilwal.sagar@northeastern.edu
- **Rajiv Shah** - shah.rajiv1702@gmail.com
- **Kushal Shankar** - kushalshankar03@gmail.com