import logging
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.rag.rag_utils import get_documents_from_folder, read_document, check_for_pii, redact_pii, chunk_text, embed_and_store_chunks
from airflow import configuration as conf
from scripts.rag.validate_schema import validate_rag_schema
from scripts.upload_data_GCS import upload_docs_data_to_gcs

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

task_upload_processed_data_to_GCS = PythonOperator(
    task_id='view_and_upload_to_GCS',
    python_callable=upload_docs_data_to_gcs,
    op_args=[embed_and_store_task.output],
    op_kwargs={
        'bucket_name': 'promptly-chat',
        'destination_blob_name': 'training_documents/preprocessed_docs_chunk_data.csv'
    },
    provide_context=True,
    dag=dag,
)

# send_success_email_dag = PythonOperator(
#     task_id="send_success_email",
#     python_callable=send_success_email,
#     provide_context = True,
#     dag=dag,
# )

# Define task dependencies
fetch_documents_task >> read_documents_task >> check_pii_task >> redact_pii_task >> chunk_text_task >> task_validate_schema >> embed_and_store_task >> task_upload_processed_data_to_GCS

# Run DAG from CLI
if __name__ == "__main__":
    dag.cli()
