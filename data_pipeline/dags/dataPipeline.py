# Import necessary libraries and modules
import logging
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.supadb.supabase_utils import get_supabase_data, push_to_dvc
from scripts.email_utils import send_success_email
from scripts.data.data_utils import clean_text, check_xcom_data

from airflow import configuration as conf

# Enable pickle support for XCom, allowing data to be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

logging.basicConfig(level=logging.INFO)

# Define default arguments for your DAG
default_args = {
    'owner': 'Ronak',
    'start_date': datetime(2025, 1, 15),
    'retries': 0, # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5), # Delay before retries
}

# Create a DAG instance named 'Airflow_Lab1' with the defined default arguments
dag = DAG(
    'Train_User_Queries',
    default_args=default_args,
    description='Dag for processing User Queries stored in Supabase for Model Training',
    schedule_interval=None,  # Set the schedule interval or use None for manual triggering
    catchup=False,
)

# Define PythonOperators for each function

# Task to load data, calls the 'load_data' Python function
# load_data_task = PythonOperator(
#     task_id='load_data_task',
#     python_callable=load_data,
#     dag=dag,
# )

fetch_user_queries = PythonOperator(
    task_id="fetch_queries_task",
    python_callable=get_supabase_data,
    provide_context = True,
    dag=dag,
)

clean_queries = PythonOperator(
    task_id="clean_user_queries_task",
    python_callable=clean_text,
    op_args=[fetch_user_queries.output],
    provide_context = True,
    dag=dag,
)

send_success_email_dag = PythonOperator(
    task_id="send_success_email",
    python_callable=send_success_email,
    provide_context = True,
    dag=dag,
)

# Push Data to DVC once Cleaned
push_data_to_DVC = PythonOperator(
    task_id='push_data_to_dvc',
    python_callable=push_to_dvc,
    op_args=[clean_queries.output],
    provide_context = True,
    dag=dag,
)

# Set task dependencies
fetch_user_queries >> clean_queries >> push_data_to_DVC >> send_success_email_dag

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
