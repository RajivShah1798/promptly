# Promptly Data Pipeline

## Overview

Promptly is an AI-powered document-based Q&A system designed to retrieve answers from user-uploaded documents (PDFs, text files) using a **Retrieval-Augmented Generation (RAG) pipeline**. The system processes user queries, cleans and validates data, stores embeddings in Supabase, and utilizes **Google Cloud Storage (GCS), Airflow DAGs, and DVC** for **data processing, tracking, and versioning**.

This repository hosts the **data pipeline** for managing document processing, query handling, and RAG workflows.

---

## Data Pipeline - Key Components & Workflow

### 1. User Queries Processing Pipeline

The pipeline processes user queries from **Supabase** and prepares them for retrieval tasks:

- **Fetch Queries**: Retrieves queries from the Supabase database.
- **Validate Schema**: Ensures that queries match expected format.
- **Clean & Preprocess**: Tokenizes, lemmatizes, and removes noise.
- **Upload to GCS**: Saves processed queries as CSV files in GCS.
- **Push to DVC**: Enables version control for reproducibility.
- **Trigger Model Training** (if needed).
- **Send Notifications**: Sends a success email when tasks complete.

---

### 2. Document Processing & RAG Pipeline

This pipeline processes and indexes uploaded documents for retrieval:

- **Fetch Documents**: Collects uploaded PDFs & text files.
- **Read Documents**: Extracts text content using `pymupdf4llm`.
- **PII Detection & Redaction**: Uses **Presidio-based Named Entity Recognition (NER)** to identify and redact sensitive data.
- **Chunk Text**: Splits documents into structured sections.
- **Validate Schema**: Ensures processed text follows expected format.
- **Embed & Store**:
  - **Generate embeddings** using `Nomic`.
  - **Store in Supabase** (using `pgvector` for semantic search).
- **Upload to GCS**: Saves processed chunks for backup.
- **Push to DVC**: Ensures version control for document processing.
- **Send Notifications**: Triggers email alerts upon completion.

---

## Data Storage

The processed data is stored across multiple locations:

- **Google Cloud Storage (GCS)**: Stores raw & processed data.
- **Supabase**: Hosts document metadata & vector embeddings for retrieval.
- **DVC (Data Version Control)**: Tracks dataset versions for reproducibility.

---

## Airflow DAGs Overview

### 1. **User Queries DAG (Train_User_Queries)**

Processes user queries and prepares them for retrieval:

- `fetch_queries_task`: Retrieves queries from Supabase.
- `validate_schema`: Ensures data consistency.
- `clean_user_queries_task`: Cleans and preprocesses queries.
- `view_and_upload_to_GCS`: Saves processed data to GCS.
- `push_data_to_dvc`: Tracks query versions in DVC.
- `send_success_email`: Notifies of completion.

### 2. **Document Processing DAG (Document_Processing_Pipeline)**

Processes uploaded PDFs and prepares them for retrieval:

- `fetch_documents`: Retrieves documents.
- `read_documents`: Extracts text from PDFs/TXT files.
- `check_for_pii`: Detects sensitive information.
- `redact_pii`: Redacts or masks sensitive data.
- `chunk_text`: Splits text into meaningful chunks.
- `validate_schema`: Ensures chunked data structure is valid.
- `embed_and_store_chunks`: Generates embeddings and stores them in Supabase.
- `view_and_upload_to_GCS`: Uploads processed chunks to GCS.

---

## Project Directory Structure

```
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
│   │   │   │   ├── rag_utils.py  # Chunking & Embeddings
│   ├── config.py  # API Keys & Configurations
│   ├── README.md  # Project Documentation
│
├── data/
│   ├── raw_documents/  # Original PDFs & Text Files
│   ├── processed_documents/  # Cleaned & Chunked Data
│   ├── user_queries.csv  # Raw User Queries
│   ├── preprocessed_user_data.csv  # Processed Queries
│
├── .dvc/  # DVC Configuration
├── .gitignore
├── requirements.txt  # Dependencies
```

---

## **Setup & Deployment**

### **Prerequisites**

Ensure you have the following installed:

- **Google Cloud SDK** (`gcloud` CLI)
- **Python 3.8+**
- **DVC** (`pip install dvc[gdrive]`)
- **Airflow** (`pip install apache-airflow`)

### **1. Environment Setup**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/promptly-data-pipeline.git
   cd promptly-data-pipeline
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Google Cloud authentication:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
4. Initialize DVC:
   ```bash
   dvc init
   dvc remote add gcs_remote gs://promptly-chat
   dvc pull
   ```

### **2. Running Airflow DAGs**

1. Start Airflow:
   ```bash
   airflow db init
   airflow scheduler & airflow webserver
   ```
2. Trigger DAGs via the Airflow UI or CLI:
   ```bash
   airflow dags trigger Train_User_Queries
   airflow dags trigger Document_Processing_Pipeline
   ```

### **3. Monitoring & Logs**

- Check Airflow logs:
  ```bash
  airflow tasks logs <dag_id> <task_id>
  ```
- Supabase logs can be viewed via the web dashboard.

---

## **CI/CD & Model Versioning**

- **DVC tracks dataset versions** for reproducibility.
- **GitHub Actions** handles automated deployments.
- **MLflow (future enhancement)** for tracking model performance.

---

## **Contributing**

We welcome contributions to improve this pipeline! To contribute:

1. Fork this repository.
2. Create a new branch.
3. Commit changes and push them.
4. Submit a Pull Request.

---

## **License**

Distributed under the MIT License. See `LICENSE.txt` for more details.

---

## **Contact**

For any questions or issues, reach out to the Promptly team:

- **Ronak Vadhaiya** - vadhaiya.r@northeastern.edu
- **Sagar Bilwal** - bilwal.sagar@northeastern.edu
- **Kushal Shankar** - kushalshankar03@gmail.com
- **Rajiv Shah** - shah.rajiv1702@gmail.com
