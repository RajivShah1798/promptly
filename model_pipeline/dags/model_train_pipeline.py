import logging
import sys
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Append paths for scripts and config access
sys.path.append("/home/kushal/model_dev_promptly/promptly/model_pipeline/scripts")
sys.path.append("/home/kushal/model_dev_promptly/promptly/data_pipeline")

# Import required scripts
from load_data import load_data
from embed_utils import generate_nomic_embeddings
from sbert_knn_classifier import classify_query
import pandas as pd

# Default Airflow Arguments
default_args = {
    'owner': 'ModelDev',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 0
}

### **Step 1: Load & Preprocess Data**
def load_and_preprocess_queries(**kwargs):
    """Loads user queries and preprocesses them for embedding."""
    X, y, user_queries = load_data()  # ✅ Corrected unpacking

    # ✅ Ensure `user_queries` is a DataFrame, not a Series
    if isinstance(user_queries, pd.Series):
        user_queries = user_queries.to_frame()

    # ✅ Ensure required columns exist
    required_columns = {"question"}
    if not required_columns.issubset(user_queries.columns):
        raise ValueError(f"❌ Missing required columns in user queries CSV: {required_columns - set(user_queries.columns)}")

    # Extract questions
    questions = user_queries["question"].tolist()

    # Log info
    logging.info(f"✅ Loaded {len(questions)} user queries for embedding.")

    # Push to XCom for later tasks
    ti = kwargs['ti']
    ti.xcom_push(key='questions', value=questions)

### **Step 2: Generate Query Embeddings**
def generate_embeddings(**kwargs):
    """Generates embeddings for user queries using Nomic API."""
    ti = kwargs['ti']
    questions = ti.xcom_pull(task_ids='load_preprocess_queries', key='questions')

    if not questions:
        raise ValueError("❌ No questions found in XCom for embedding generation.")

    # Generate embeddings
    embeddings = generate_nomic_embeddings(questions)

    # Load user queries
    _, _, user_queries = load_data()  # ✅ Corrected unpacking

    # ✅ Ensure DataFrame retains "question" and "response" columns
    user_queries = user_queries[["question", "response"]].copy()
    user_queries['embedding'] = embeddings

    # ✅ Save embeddings with "response" included
    embedding_output_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "../../data/user_queries_with_embeddings.csv"
    ))
    user_queries.to_csv(embedding_output_path, index=False)

    logging.info(f"✅ User query embeddings stored at: {embedding_output_path}")
    ti.xcom_push(key='embedding_output_path', value=embedding_output_path)

### **Step 3: Train SBERT + k-NN Classifier**
def train_sbert_knn_classifier(**kwargs):
    """Trains the SBERT + k-NN classifier on query embeddings."""
    from sbert_knn_classifier import knn_classifier

    # Train the classifier (Already trained when script is executed)
    logging.info(f"✅ SBERT + k-NN classifier is ready for classification.")
    return "Model trained successfully."

### **Step 4: Classify New Queries**
def classify_sample_queries(**kwargs):
    """Classifies new queries using the trained SBERT + k-NN classifier."""
    test_queries = [
        "How does FDA regulate medical devices?",
        "What are the clinical trial requirements?",
        "Explain post-market surveillance regulations.",
        "How do I check if my product is a medical device?"
    ]

    results = []
    for query in test_queries:
        try:
            category = classify_query(query)  # ✅ Will no longer crash on CUDA
            results.append((query, category))
            logging.info(f"✅ Query: {query} -> Predicted Category: {category}")
        except Exception as e:
            logging.error(f"❌ Error classifying query '{query}': {e}")

    return results

### **Define DAG**
with DAG(
    dag_id='Model_Train_Pipeline',
    default_args=default_args,
    description='Load data, generate embeddings, train SBERT + k-NN model, and classify queries',
    schedule_interval=None,
    catchup=False
) as dag:

    load_preprocess_queries_task = PythonOperator(
        task_id='load_preprocess_queries',
        python_callable=load_and_preprocess_queries,
        provide_context=True
    )

    generate_embeddings_task = PythonOperator(
        task_id='generate_embeddings',
        python_callable=generate_embeddings,
        provide_context=True
    )

    train_classifier_task = PythonOperator(
        task_id='train_sbert_knn_classifier',
        python_callable=train_sbert_knn_classifier,
        provide_context=True
    )

    classify_queries_task = PythonOperator(
        task_id='classify_queries',
        python_callable=classify_sample_queries,
        provide_context=True
    )

    # Task dependencies
    load_preprocess_queries_task >> generate_embeddings_task >> train_classifier_task >> classify_queries_task
