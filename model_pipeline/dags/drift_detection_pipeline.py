from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
import sys
import os

# ✅ Add the scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from drift_detection import run_drift_detection

default_args = {
    'owner': 'Promptly',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'drift_detection_pipeline',
    default_args=default_args,
    description='Hourly drift detection on document_chunks embeddings.',
    schedule_interval='@hourly',
    catchup=False,
    tags=['drift', 'monitoring']
) as dag:

    detect_drift_task = PythonOperator(
        task_id="run_drift_check",
        python_callable=run_drift_detection,
        provide_context=True
    )

    detect_drift_task
