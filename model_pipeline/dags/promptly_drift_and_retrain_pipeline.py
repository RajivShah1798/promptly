from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add script paths to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

# Import your main drift detection + retraining functions
from drift_detection import run_drift_detection
from retrain_pipeline import run_pipeline

# Default configuration for Airflow DAG
DEFAULT_ARGS = {
    'owner': 'promptly-ai',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='promptly_drift_and_retrain_pipeline',
    default_args=DEFAULT_ARGS,
    description='Runs drift detection hourly and triggers retraining pipeline if needed.',
    schedule_interval='@hourly',
    catchup=False,
    tags=['promptly', 'drift', 'retraining']
) as dag:

    # Step 1: Just run and log drift detection
    drift_check = PythonOperator(
        task_id='run_drift_detection_only',
        python_callable=run_drift_detection
    )

    # Step 2: Run the full retraining pipeline (drift check again + bias detection + retraining + logging)
    full_retrain_pipeline = PythonOperator(
        task_id='run_full_retraining_pipeline',
        python_callable=run_pipeline
    )

    # DAG Flow: drift check always runs first, followed by retrain pipeline
    drift_check >> full_retrain_pipeline
