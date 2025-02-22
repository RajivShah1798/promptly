import logging
import os
import subprocess
import pandas as pd

from supabase import create_client
from airflow.models import Variable
from dotenv import load_dotenv
from airflow.operators.python import get_current_context

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")) # at Root 
# Load environment variables from .env file.
load_dotenv(base_dir + "/.env")

# Load Supabase credentials (replace with Airflow Variable or environment variable)
SUPABASE_URL = os.getenv("SUPABASE_URL") # Variable.get("SUPABASE_URL")  # Or
SUPABASE_KEY = os.getenv("SUPABASE_KEY") # Variable.get("SUPABASE_KEY")  # Or 

def get_supabase_data():
    """
    Retrieves data from Supabase user_queries table.
    """
    try: 
        # Initialize Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        response = supabase.table("conversations").select("*").execute()

        if response.data is None:
            return "stop_task"
            raise ValueError("No data returned from Supabase.")

        query_results = response.data  # List of dicts

        print(query_results)

    except Exception as e:
        raise RuntimeError("Failed to load user data from Supabase.") from e

    return query_results

'''
def perform_similarity_search(**context):
    """
    Perform similarity search between course-prof pairs and PDF content using a vector search model.

    This DAG task retrieves the initial queries from the previous task and generates new queries using the LLM.
    It then performs a vector search on the generated queries to find the closest matching courses in the
    BigQuery table specified by Variable.get('banner_table_name'). The results of the vector search are
    then processed and saved to the 'similarity_results' XCom key.

    Args:
        **context: Arbitrary keyword arguments. This can include Airflow context variables.

    Returns:
        str: "stop_task" if the target sample count has been reached, or "generate_samples" to continue
        with the DAG run.
    """
    task_status = context['ti'].xcom_pull(task_ids='check_sample_count', key='task_status')
    logging.info(f"Task status: {task_status}")
    if task_status == "stop_task":
        return "stop_task"
    queries = context['ti'].xcom_pull(task_ids='get_initial_queries', key='initial_queries')

    client = bigquery.Client()
    query_response = {}

    for query in queries:
        logging.info(f"Processing seed query: {query}")
        new_queries = generate_sample_queries(query)
        for new_query in new_queries:
            bq_query = """
                    WITH query_embedding AS (
                        SELECT ml_generate_embedding_result 
                        FROM ML.GENERATE_EMBEDDING(
                            MODEL `coursecompass.mlopsdataset.embeddings_model`,
                            (SELECT @new_query AS content)
                        )
                    ),
                    vector_search_results AS (
                        SELECT 
                            base.*,
                            distance as search_distance
                        FROM VECTOR_SEARCH(
                            (
                                SELECT *
                                FROM `coursecompass.mlopsdataset.banner_data_embeddings`
                                WHERE ARRAY_LENGTH(ml_generate_embedding_result) = 768
                            ),
                            'ml_generate_embedding_result',
                            TABLE query_embedding,
                            distance_type => 'COSINE',
                            top_k => 5,
                            options => '{"use_brute_force": true}'
                        )
                    ),
                    course_matches AS (
                        SELECT 
                            v.*,
                            c.crn AS course_crn
                        FROM vector_search_results v
                        JOIN `coursecompass.mlopsdataset.course_data_table` c
                            ON v.faculty_name = c.instructor
                    ),
                    review_data AS (
                        SELECT * EXCEPT(review_id)
                        FROM `coursecompass.mlopsdataset.review_data_table`
                    )
                    SELECT DISTINCT
                        cm.course_crn AS crn,
                        cm.content,
                        STRING_AGG(CONCAT(review.question, '\\n', review.response, '\\n'), '; ') AS concatenated_review_info,
                        cm.search_distance AS score,
                        CONCAT(
                            'Course Information:\\n',
                            cm.content,
                            '\\nReview Information:\\n',
                            STRING_AGG(CONCAT(review.question, '\\n', review.response, '\\n'), '; '),
                            '\\n'
                        ) AS full_info
                    FROM course_matches cm
                    JOIN review_data AS review
                        ON cm.course_crn = review.crn
                    GROUP BY
                        cm.course_crn,
                        cm.content,
                        cm.search_distance
                    """

            query_params = [
                bigquery.ScalarQueryParameter("new_query", "STRING", new_query),
            ]

            job_config = bigquery.QueryJobConfig(
                query_parameters=query_params
            )
            query_job = client.query(bq_query, job_config=job_config)

            results = query_job.result()

            result_crns = []
            result_content = []

            for row in results:
                result_crns.append(row.crn)
                result_content.append(remove_punctuation(row.full_info))
            query_response[new_query] = {
                'crns': result_crns,
                'final_content': '\n\n'.join(result_content)
            }

            # logging.info(f"Similarity search results for query '{new_query}': {','.join(result_crns)}")
   
    context['ti'].xcom_push(key='similarity_results', value=query_response)
    return "generate_samples"
'''

def push_to_dvc(cleaned_query_results):
    """
    Saves the updated data as a CSV file and pushes it to GCP via DVC.
    """
    # Disjunct
    user_queries, user_response = cleaned_query_results

    if not user_queries or not user_response:
        raise ValueError("No data found in XCom for DVC push.")

    # Create DataFrame and save as CSV
    dvc_data_path = base_dir + "/data/user_queries.csv"  # Ensure this is inside a DVC-tracked directory
    df = pd.DataFrame({'question': user_queries, 'response': user_response})
    df.to_csv(dvc_data_path, index=False)

    try:
        # DVC Add, Commit, and Push to GCP Bucket
        subprocess.run(["dvc", "add", dvc_data_path], check=True)
        subprocess.run(["dvc", "push", "-r", "gcs_remote"], check=True)  # Push to GCP Bucket
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"DVC push failed: {e}")

    return "DVC Push to GCS Succeeded!"