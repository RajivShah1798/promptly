import os
import pandas as pd
import numpy as np
from ast import literal_eval
import logging

# Define correct file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
USER_EMBEDDING_FILE = os.path.join(BASE_DIR, "data/user_queries_with_embeddings.csv")
USER_QUERY_FILE = os.path.join(BASE_DIR, "data/preprocessed_user_data.csv")  # ✅ Old data source for backup

def load_data():
    """
    Loads user queries with embeddings for model training.
    If "response" is missing, attempts to recover it from preprocessed data.
    
    Returns:
        - X (NumPy Array): Features (embeddings).
        - y (Series): Target variable (response).
        - user_queries (DataFrame): Original questions + embeddings.
    """
    logging.info("🔄 Loading user queries with embeddings...")

    # Ensure file exists
    if not os.path.exists(USER_EMBEDDING_FILE):
        raise FileNotFoundError(f"❌ File not found: {USER_EMBEDDING_FILE}")

    # Load CSV file
    df = pd.read_csv(USER_EMBEDDING_FILE)

    # ✅ Ensure required columns exist
    required_columns = {"question", "response", "embedding"}
    missing_columns = required_columns - set(df.columns)

    if "response" in missing_columns:
        logging.warning("⚠️ 'response' column missing! Attempting to recover from preprocessed data...")

        if os.path.exists(USER_QUERY_FILE):
            # ✅ Recover "response" from old preprocessed data
            preprocessed_df = pd.read_csv(USER_QUERY_FILE)
            df = df.merge(preprocessed_df[["question", "response"]], on="question", how="left")

            # If still missing, set default response
            df["response"].fillna("Unknown", inplace=True)
            logging.info("✅ 'response' column successfully recovered.")
        else:
            logging.error("❌ 'response' column is missing and no backup data is available.")
            raise ValueError("❌ Critical Error: 'response' column missing and cannot be recovered!")

    # ✅ Convert embeddings from string format to NumPy arrays
    df["embedding"] = df["embedding"].apply(lambda x: np.array(literal_eval(x)))

    # Prepare input features (X) and labels (y)
    X = np.vstack(df["embedding"].values)
    y = df["response"]

    if X.shape[0] != len(y):
        raise ValueError(f"❌ Mismatch: X has {X.shape[0]} samples, y has {len(y)} samples.")

    logging.info(f"✅ Loaded {len(df)} samples. X shape: {X.shape}, y shape: {y.shape}")
    return X, y, df  # ✅ Returns DataFrame as well

# Run standalone test
if __name__ == "__main__":
    try:
        X, y, df = load_data()
        print(f"✅ User Queries Loaded: {len(y)}")
        print("✅ Sample Embeddings:\n", X[:2])
    except Exception as e:
        logging.error(f"❌ Error loading data: {e}")
