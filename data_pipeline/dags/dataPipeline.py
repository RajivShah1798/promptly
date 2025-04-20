# Import necessary libraries and modules
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow import configuration as conf

from datetime import datetime, timedelta
from scripts.supadb.supabase_utils import get_supabase_data, push_to_dvc
from scripts.email_utils import send_success_email, send_failure_email
from scripts.data_preprocessing.data_utils import clean_text
from scripts.data_preprocessing.validate_schema import validate_schema
from scripts.upload_data_GCS import view_and_upload_data
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


# Enable pickle support for XCom, allowing data to be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

logging.basicConfig(level=logging.INFO)

# Define default arguments for your DAG
default_args = {
    'owner': 'Ronak',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0, # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5), # Delay before retries
}

# Function to handle failur
def handle_failure(context):
    task_instance = context['task_instance']
    exception = task_instance.exception
    # Log or handle the exception as needed
    print(f"Task {task_instance.task_id} failed with exception: {exception}")
    try:
        send_failure_email(task_instance, exception)
        print("Failure email sent successfully!")
    except Exception as e:
        print(f"Error sending failure email: {e}")

# Create a DAG instance named 'Airflow_Lab1' with the defined default arguments
dag = DAG(
    'Train_User_Queries',
    default_args=default_args,
    description='Dag for processing User Queries stored in Supabase for Model Training',
    schedule_interval=None,  # Set the schedule interval or use None for manual triggering
    catchup=False,
)

# Define PythonOperators for each function
fetch_user_queries = PythonOperator(
    task_id="fetch_queries_task",
    python_callable=get_supabase_data,
    provide_context = True,
    dag=dag,
)

task_validate_schema = PythonOperator(
    task_id='validate_schema',
    python_callable=validate_schema,
    op_args=[fetch_user_queries.output],
    provide_context=True,
    dag=dag,
)

task_clean_queries = PythonOperator(
    task_id="clean_user_queries_task",
    python_callable=clean_text,
    op_args=[fetch_user_queries.output],
    provide_context = True,
    dag=dag,
)

task_view_and_upload_data = PythonOperator(
    task_id='view_and_upload_to_GCS',
    python_callable=view_and_upload_data,
    op_args=[task_clean_queries.output],
    op_kwargs={
        'bucket_name': 'promptly-chat',
        'destination_blob_name': 'data/preprocessed_user_data.csv'
    },
    provide_context=True,
    dag=dag,
)

# Push Data to DVC once Cleaned
push_data_to_DVC = PythonOperator(
    task_id='push_data_to_dvc',
    python_callable=push_to_dvc,
    op_args=[task_clean_queries.output, "/data/preprocessed_user_data.csv", False],
    provide_context = True,
    dag=dag,
)

send_success_email_dag = PythonOperator(
    task_id="send_success_email",
    python_callable=send_success_email,
    op_args=[task_view_and_upload_data.output,push_data_to_DVC.output],
    provide_context = True,
    dag=dag,
)

trigger_rag_dag = TriggerDagRunOperator(
    task_id='trigger_RAG_document_pipeline',
    trigger_dag_id='Document_Processing_Pipeline', 
    wait_for_completion=False,
    reset_dag_run=True,
    conf={"source": "Train_User_Queries"},
    dag=dag,
)

# Set task dependencies and Optimise Flow
fetch_user_queries >> task_validate_schema >> task_clean_queries
task_clean_queries >> task_view_and_upload_data 
task_clean_queries >> push_data_to_DVC
push_data_to_DVC >> send_success_email_dag
send_success_email_dag >> trigger_rag_dag

# Set up the failure callback
dag.on_failure_callback = handle_failure

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
