import os
import pandas as pd
from airflow.providers.google.cloud.hooks.gcs import GCSHook

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")) # at Root 

def view_and_upload_data(data: list, bucket_name: str, destination_blob_name: str, **kwargs) -> None:
    """
    Prints the final cleaned data

    Args:
    data (list): List of dictionaries containing 'Query', 'Response', and 'Context' keys.

    Returns:
    None
    """
    user_queries, user_response, user_context = data

    for item in range(0,10):
        print("Query:-")
        print(user_queries[item])
        print("-"*100)
        print("Context:-")
        print(user_context[item])
        print("-"*100)
        print("Response:-")
        print(user_response[item])
        print("-"*100)
        print()
        print("-"*100)

    if not user_queries or not user_response or not user_context:
        raise ValueError("Key Data not found to process the operation.")

    # Create DataFrame and Save to a local CSV file
    local_path = base_dir + "/data/preprocessed_user_data.csv" 

    df = pd.DataFrame({'question': user_queries, 'context': user_context, 'response': user_response})

    df.to_csv(local_path, index=False)
    
    print("Uploading to GCS using GCSHook")

    upload_to_gcs_using_hook(local_path, bucket_name, destination_blob_name)


def upload_to_gcs_using_hook(local_path: str, bucket_name: str, destination_blob_name: str) -> None:
    """
    Uploads a file to a GCS bucket using GCSHook.

    Args:
    local_path (str): Path to the local file.
    bucket_name (str): Name of the GCS bucket.
    destination_blob_name (str): Destination path in the GCS bucket.

    Returns:
    None
    """
    # Initialize the GCSHook
    gcs_hook = GCSHook()
    
    # Upload the file to GCS
    gcs_hook.upload(bucket_name, destination_blob_name, local_path)
    
    print(f"File {local_path} uploaded to {destination_blob_name} in bucket {bucket_name}.")