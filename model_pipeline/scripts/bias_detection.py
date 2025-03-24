import os
import logging
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import json

# Load environment
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
USER_DOMINANCE_THRESHOLD = float(os.getenv("USER_BIAS_THRESHOLD", 50.0))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_and_join_chunk_user_data(supabase_client):
    logging.info("🔎 Fetching document_chunks from Supabase...")
    chunks_resp = supabase_client.table("document_chunks").select("id, document_id").execute()
    if not chunks_resp.data:
        logging.warning("⚠️ No document chunks found.")
        return pd.DataFrame()

    chunks_df = pd.DataFrame(chunks_resp.data)
    doc_ids = chunks_df['document_id'].unique().tolist()

    logging.info("🔎 Fetching documents for document_id-user_id mapping...")
    documents_resp = supabase_client.table("documents").select("id, upload_user_id").in_("id", doc_ids).execute()
    if not documents_resp.data:
        logging.warning("⚠️ No documents found for those document_ids.")
        return pd.DataFrame()

    documents_df = pd.DataFrame(documents_resp.data)

    logging.info("🔗 Joining chunks with documents...")
    merged_df = chunks_df.merge(documents_df, left_on="document_id", right_on="id", suffixes=('_chunk', '_document'))

    return merged_df

def check_user_dominance_bias_live() -> bool:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    merged_df = load_and_join_chunk_user_data(supabase)

    if merged_df.empty or 'upload_user_id' not in merged_df.columns:
        logging.warning("⚠️ No valid chunk-to-user mapping found. Skipping bias detection.")
        return True

    user_chunk_counts = merged_df['upload_user_id'].value_counts().reset_index()
    user_chunk_counts.columns = ["user_id", "chunk_count"]
    total_chunks = user_chunk_counts["chunk_count"].sum()
    user_chunk_counts["percentage"] = (user_chunk_counts["chunk_count"] / total_chunks) * 100

    logging.info(f"📊 User contribution breakdown:\n{user_chunk_counts}")
    violators = user_chunk_counts[user_chunk_counts["percentage"] > USER_DOMINANCE_THRESHOLD]

    if not violators.empty:
        logging.warning(f"🚨 Bias detected! Violators:\n{violators}")
        logging.warning(f"Threshold = {USER_DOMINANCE_THRESHOLD}%. Blocking retraining.")
        return False
    else:
        logging.info(f"✅ No bias detected. Threshold = {USER_DOMINANCE_THRESHOLD}%.")
        return True

# Optional: test with mock JSON
def check_user_dominance_bias_local(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    user_counts = df["upload_user_id"].value_counts().reset_index()
    user_counts.columns = ["user_id", "chunk_count"]
    total_chunks = user_counts["chunk_count"].sum()
    user_counts["percentage"] = (user_counts["chunk_count"] / total_chunks) * 100
    logging.info(f"📊 Mock User contribution breakdown:\n{user_counts}")
    violators = user_counts[user_counts["percentage"] > USER_DOMINANCE_THRESHOLD]

    if not violators.empty:
        logging.warning(f"🚨 Bias Detected! Violating users:\n{violators}")
        return False
    else:
        logging.info("✅ No bias detected in mock data.")
        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bias Detection Script")
    parser.add_argument("--local_json", type=str, help="Path to local JSON test file")
    args = parser.parse_args()

    if args.local_json:
        result = check_user_dominance_bias_local(args.local_json)
    else:
        result = check_user_dominance_bias_live()

    logging.info(f"✅ Bias detection result: {'PASSED — Retraining Allowed' if result else 'FAILED — Retraining Blocked'}")
