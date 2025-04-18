from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
from model_pipeline.scripts.drift_detection import detect_data_drift  # Refactor this function into your script

default_args = {
    'owner': 'Promptly Team',
    'start_date': datetime(2025, 4, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='drift_detection_pipeline',
    default_args=default_args,
    description='Periodic check for data drift using recent Supabase embeddings',
    schedule_interval='@hourly',  # or use '0 * * * *'
    catchup=False
)

drift_detection_task = PythonOperator(
    task_id='run_drift_detection',
    python_callable=detect_data_drift,
    dag=dag
)
