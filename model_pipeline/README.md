# Model Pipeline - Key Components and Workflow

## Overview
The pipeline automates the process of preparing data, fine-tuning, evaluating, and deploying a model for retrieval-augmented generation (RAG). The processed data is loaded directly into Supabase, and training is orchestrated via a Kaggle notebook triggered by GitHub Actions, with model artifacts uploaded to Hugging Face.

## Key Components

### 1. *Data Preparation*
The data preparation process leverages Supabase to store and retrieve processed data with chunked documents:
   - *Direct Data Loading*: Instead of using Airflow and BigQuery, data is stored in Supabase with pre-chunked documents for efficient retrieval.
   - *Metadata Management*: Each chunk is indexed with relevant metadata for fast lookups in the RAG system.
   - *Automated Updates*: Changes in the source documents trigger re-processing, ensuring data is always up-to-date.

### 2. *Model Training*
The model training workflow is designed for efficiency and reproducibility:
   - *Kaggle Notebook Execution*: GitHub Actions triggers a Kaggle notebook runner to start the training process.
   - *Training in Jupyter Notebook*: Most of the fine-tuning logic is implemented within a Jupyter notebook, allowing for interactive debugging and iterative improvements.
   - *Hugging Face Model Upload*: Once training is complete, the trained model is uploaded to Hugging Face for storage and deployment.

### 3. *Model Evaluation*
The evaluation system employs standard and custom metrics to ensure model performance:
   - *Standard Metrics*: BLEU, ROUGE (1, 2, L), and perplexity.
   - *Custom Metrics*: Relevance and Coverage to assess response quality in the RAG system.
   - *Bias Detection*: Evaluates responses using a 5-point rubric to ensure fairness and inclusivity.

### 4. *Model Deployment*
The deployment process is streamlined for ease of integration:
   - *Hugging Face Model Hub*: Models are stored as versions in Hugging Face, enabling easy access and rollback.
   - *Supabase Integration*: The fine-tuned model is loaded into the RAG system for real-time inference.
   - *Low-Latency API*: The deployed model serves API requests efficiently, supporting real-time applications.

### 5. *CI/CD Pipeline*
A GitHub Actions workflow automates the training and deployment cycle:
   - *Triggering*: The pipeline detects code updates and triggers the Kaggle notebook runner.
   - *End-to-End Integration*: Automates the data preparation, training, evaluation, and deployment process.
   - *Error Handling*: Implements robust error handling and logging for debugging.

### 6. *Notifications and Alerts*
Real-time updates keep stakeholders informed:
   - *GitHub Actions Notifications*: Alerts on training start, completion, and failures.
   - *Bias Detection Reports*: Periodic reports summarizing evaluation findings.
   - *Error Logs*: Detailed logs for debugging failures.

## Pipeline Directory Structure

model_pipeline/
├── README.md: Documentation of the model pipeline.
├── dags/ (not used, as Supabase is the main data source)
├── notebooks/
│   ├── train_model.ipynb: Jupyter notebook for fine-tuning the model.
│   ├── eval_model.ipynb: Jupyter notebook for evaluating model performance.
│   ├── bias_detection.ipynb: Notebook for analyzing and mitigating bias.
├── github_workflows/
│   ├── kaggle_train.yml: GitHub Actions workflow to trigger Kaggle notebook.
├── huggingface/
│   ├── upload_model.py: Script to upload trained model to Hugging Face.
├── supabase/
│   ├── fetch_data.py: Retrieves processed documents from Supabase.
│   ├── load_to_rag.py: Loads fine-tuned models into the RAG system.
├── tests/
│   ├── unit_tests.py: Unit tests for core pipeline functions.
│   ├── integration_tests.py: Tests for end-to-end workflow validation.
├── requirements.txt: Python dependencies required for execution.


## Key Features
   - *Direct integration with Supabase for data storage and retrieval*
   - *Kaggle notebook execution triggered via GitHub Actions*
   - *Automated model upload to Hugging Face for versioning and deployment*
   - *Custom and standard metrics for rigorous model evaluation*
   - *Bias detection and reporting to ensure fairness in generated responses*
   - *CI/CD pipeline for automated training and deployment cycles*

This pipeline is optimized for automation, scalability, and fairness, aligning with best practices in RAG model development and MLOps.