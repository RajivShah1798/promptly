import os
import pandas as pd
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from itertools import chain

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

    return "Data Uploaded SuccessFully!"


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


def upload_docs_data_to_gcs(chunk_store: list, bucket_name: str, destination_blob_name: str) -> None:
    """
    View nested chunked data and uploads it to GCS.

    Args:
        chunk_store (list): List of lists of dictionaries containing chunk metadata.
        bucket_name (str): Name of the GCS bucket.
        destination_blob_name (str): Destination path in the GCS bucket.

    Returns:
        None
    """
    # Flatten the chunk_store (list of lists → list of dictionaries)
    flat_chunk_store = list(chain.from_iterable(chunk_store))

    # Preview first 10 chunks
    print("Previewing first 10 chunks:")
    for item in flat_chunk_store[:10]:
        print(f"Document ID: {item['document_id']}")
        print(f"Chunk Content: {item['chunk_content']}")
        print(f"Embedding: {item['embedding'][:5]}...")  # Print first 5 elements of the embedding for brevity
        print(f"Section Order: {item['section_order']}")
        print(f"Created At: {item['created_at']}")
        print("------" * 10)

    local_path = base_dir + "/data/preprocessed_docs_chunks.csv"

    # Create DataFrame from chunk_store
    df = pd.DataFrame(flat_chunk_store)

    # Save DataFrame to CSV
    df.to_csv(local_path, index=False)
    print(f"Data saved to {local_path}")

    # Upload to GCS
    print("Uploading to GCS using GCSHook...")
    upload_to_gcs_using_hook(local_path, bucket_name, destination_blob_name)