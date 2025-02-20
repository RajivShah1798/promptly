# Import necessary libraries and modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.lab import load_data, data_preprocessing, build_save_model,load_model_elbow
from scripts.bigq.bigquery_utils import get_bq_data
from scripts.email_utils import send_success_email

from airflow import configuration as conf

# Enable pickle support for XCom, allowing data to be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

# Define default arguments for your DAG
default_args = {
    'owner': 'Fantastic Four',
    'start_date': datetime(2025, 1, 15),
    'retries': 0, # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5), # Delay before retries
}

# Create a DAG instance named 'Airflow_Lab1' with the defined default arguments
dag = DAG(
    'Train_User_Queries',
    default_args=default_args,
    description='Dag example for Lab 1 of Airflow series',
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

fetch_bq_queries = PythonOperator(
    task_id="fetch_queries_task",
    python_callable=get_bq_data,
    dag=dag,
)

send_success_email_dag = PythonOperator(
    task_id="send_success_email",
    python_callable=send_success_email,
    dag=dag,
)

# Task to perform data preprocessing, depends on 'load_data_task'
# data_preprocessing_task = PythonOperator(
#     task_id='data_preprocessing_task',
#     python_callable=data_preprocessing,
#     op_args=[load_data_task.output],
#     dag=dag,
# )
# Task to build and save a model, depends on 'data_preprocessing_task'
# build_save_model_task = PythonOperator(
#     task_id='build_save_model_task',
#     python_callable=build_save_model,
#     op_args=[data_preprocessing_task.output, "model.sav"],
#     provide_context=True,
#     dag=dag,
# )
# # Task to load a model using the 'load_model_elbow' function, depends on 'build_save_model_task'
# load_model_task = PythonOperator(
#     task_id='load_model_task',
#     python_callable=load_model_elbow,
#     op_args=["model.sav", build_save_model_task.output],
#     dag=dag,
# )



# Set task dependencies
# load_data_task >> fetch_bq_queries >> data_preprocessing_task
fetch_bq_queries >> send_success_email_dag

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
