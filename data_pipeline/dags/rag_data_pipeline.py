import logging
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.data_utils import get_documents_from_folder, read_document, check_for_pii, redact_pii, chunk_text, embed_and_store_chunks
from airflow import configuration as conf

conf.set('core', 'enable_xcom_pickling', 'True')

logging.basicConfig(level=logging.INFO)

# Define default arguments for the DAG
default_args = {
    'owner': 'Sagar',
    'start_date': datetime(2025, 1, 15),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'Document_Processing_Pipeline',
    default_args=default_args,
    description='DAG for processing documents (PDF & TXT), checking PII, chunking, and storing embeddings',
    schedule_interval=None,
    catchup=False,
)

# Folder containing the documents
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_FOLDER = base_dir+"/data/rag_documents"

# Fetch document list
fetch_documents_task = PythonOperator(
    task_id="fetch_documents",
    python_callable=get_documents_from_folder,
    op_args=[DATA_FOLDER],
    provide_context=True,
    dag=dag,
)

# Read documents
read_documents_task = PythonOperator(
    task_id="read_documents",
    python_callable=read_document,
    op_args=[fetch_documents_task.output],
    provide_context=True,
    dag=dag,
)

# Check for PII
check_pii_task = PythonOperator(
    task_id="check_for_pii",
    python_callable=check_for_pii,
    op_args=[read_documents_task.output],
    provide_context=True,
    dag=dag,
)

# Redact PII if found
redact_pii_task = PythonOperator(
    task_id="redact_pii",
    python_callable=redact_pii,
    op_args=[read_documents_task.output, check_pii_task.output],
    provide_context=True,
    dag=dag,
)

# Chunk text
chunk_text_task = PythonOperator(
    task_id="chunk_text",
    python_callable=chunk_text,
    op_args=[redact_pii_task.output],
    provide_context=True,
    dag=dag,
)

# Embed text and store in Supabase
embed_and_store_task = PythonOperator(
    task_id="embed_and_store_chunks",
    python_callable=embed_and_store_chunks,
    op_args=[chunk_text_task.output],
    provide_context=True,
    dag=dag,
)

# Define task dependencies
fetch_documents_task >> read_documents_task >> check_pii_task >> redact_pii_task >> chunk_text_task >> embed_and_store_task

# Run DAG from CLI
if __name__ == "__main__":
    dag.cli()
