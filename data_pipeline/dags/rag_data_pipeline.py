import logging
import os
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.email_utils import send_success_email
from scripts.supadb.supabase_utils import push_to_dvc
from scripts.rag.rag_utils import get_documents_from_folder, read_document, chunk_text, embed_and_store_chunks
from scripts.data_preprocessing.check_pii_data import check_for_pii, redact_pii
from airflow import configuration as conf
from scripts.rag.validate_schema import validate_rag_schema
from scripts.upload_data_GCS import upload_docs_data_to_gcs

conf.set('core', 'enable_xcom_pickling', 'True')

logging.basicConfig(level=logging.INFO)

# Define default arguments for the DAG
default_args = {
    'owner': 'Sagar',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0, # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5), # Delay before retries
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
    op_args=[check_pii_task.output],
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

# Validate Schema
task_validate_schema = PythonOperator(
    task_id='validate_schema',
    python_callable=validate_rag_schema,
    op_args=[chunk_text_task.output],
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

# Upload to GCS
task_upload_processed_data_to_GCS = PythonOperator(
    task_id='view_and_upload_to_GCS',
    python_callable=upload_docs_data_to_gcs,
    op_args=[embed_and_store_task.output],
    op_kwargs={
        'bucket_name': 'promptly-chat',
        'destination_blob_name': 'training_documents/preprocessed_docs_chunks.csv'
    },
    provide_context=True,
    dag=dag,
)

# Push Data to DVC once ready
push_data_to_DVC = PythonOperator(
    task_id='push_data_to_dvc',
    python_callable=push_to_dvc,
    op_args=[embed_and_store_task.output, "/data/preprocessed_docs_chunks.csv", True],
    provide_context = True,
    dag=dag,
)

# Send success email on completion
send_success_email_dag = PythonOperator(
    task_id="send_success_email",
    python_callable=send_success_email,
    op_args=[task_upload_processed_data_to_GCS.output, push_data_to_DVC.output],
    provide_context = True,
    dag=dag,
)

# Define task dependencies
fetch_documents_task >> read_documents_task >> check_pii_task >> redact_pii_task >> chunk_text_task >> task_validate_schema >> embed_and_store_task
embed_and_store_task >> task_upload_processed_data_to_GCS
embed_and_store_task >> push_data_to_DVC 
push_data_to_DVC >> send_success_email_dag

# Run DAG from CLI
if __name__ == "__main__":
    dag.cli()
