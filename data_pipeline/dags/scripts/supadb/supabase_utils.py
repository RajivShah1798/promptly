import logging
import os
import subprocess
import pandas as pd

from supabase import create_client
from airflow.models import Variable
from dotenv import load_dotenv
from airflow.operators.python import get_current_context

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
import config

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")) # at Root 

def get_supabase_data():
    """
    Retrieves data from Supabase user_queries table.
    """
    try: 
        # Initialize Supabase client
        supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

        response = supabase.table("conversations").select("*").execute()

        if response.data is None:
            return "stop_task"
            raise ValueError("No data returned from Supabase.")

        query_results = response.data  # List of dicts

        if query_results:
            print(query_results[0])

    except Exception as e:
        raise RuntimeError("Failed to load user data from Supabase.") from e

    return query_results


def push_to_dvc(cleaned_query_results, file_path, RAG_docs=False):
    """
    Saves the updated data as a CSV file and pushes it to DVC.
    """
    # Disjunct
    if not RAG_docs:
        user_queries, user_response = cleaned_query_results

        if not user_queries or not user_response:
            raise ValueError("Key Data not found for DVC push.")

    try:
        # DVC Add, Commit, and Push to GCP Bucket
        print('File Path -> ', base_dir + file_path)
        subprocess.run(["git", "init"])

        subprocess.run(["dvc", "init"], check=True)

        subprocess.run(["dvc", "add", base_dir + file_path], check=True)

        subprocess.run(["dvc", "push", "-v"], check=True)

        # subprocess.run(["dvc", "push", "-r", "gcs_remote"], check=True)  # DVC save to gcpbucket

        # # Delete data.json.dvc
        os.remove(base_dir + file_path + ".dvc")
    except subprocess.CalledProcessError as e:
        print(f"Error during DVC operations: {e}")
        # raise RuntimeError(f"DVC push failed: {e}")

    return "DVC Push to Succeeded!"