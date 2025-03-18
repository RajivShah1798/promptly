import os
import pandas as pd
import logging
import nomic
from nomic import embed
from dotenv import load_dotenv

load_dotenv()

# Set API key
nomic.login(token=os.getenv("NOMIC_API_KEY"))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
USER_QUERY_FILE = os.path.join(BASE_DIR, "data/preprocessed_user_data.csv")
USER_EMBEDDING_FILE = os.path.join(BASE_DIR, "data/user_queries_embeddings.csv")

def generate_and_save_embeddings():
    # Load user queries
    df_queries = pd.read_csv(USER_QUERY_FILE)
    queries = df_queries['question'].tolist()

    logging.info("Generating embeddings for user queries...")

    # Generate embeddings
    try:
        embeddings_response = embed.text(
            texts=queries,
            model="nomic-embed-text-v1.5",
            task_type="search_query"
        )

        query_embeddings = embeddings_response["embeddings"]

    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        raise e

    # Save embeddings alongside original queries
    df_queries["embedding"] = query_embeddings
    df_queries.to_csv(USER_EMBEDDING_FILE, index=False)

    logging.info(f"Embeddings saved successfully at {USER_EMBEDDING_FILE}")

if __name__ == "__main__":
    generate_and_save_embeddings()
