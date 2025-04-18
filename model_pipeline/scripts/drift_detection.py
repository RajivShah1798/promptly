import os
import logging
from datetime import datetime, timedelta
import numpy as np
from supabase import create_client
from scipy.spatial.distance import cosine
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# === Initialize Supabase ===
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Logging Setup ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Drift Detection Config ===
DRIFT_THRESHOLD = 0.2
HOURS_TO_LOOK_BACK = 1

def fetch_embeddings(table: str, since_timestamp: str):
    logging.info(f"📥 Fetching embeddings from `{table}` since {since_timestamp}")
    response = supabase.table(table).select("embedding").gte("created_at", since_timestamp).execute()
    if not response.data:
        logging.warning("⚠️ No embeddings found in the given timeframe.")
        return []
    return [np.array(e["embedding"]) for e in response.data if e.get("embedding")]

def calculate_average_embedding(embeddings):
    if not embeddings:
        raise ValueError("No embeddings provided for averaging.")
    return np.mean(embeddings, axis=0)

def detect_drift(reference_embeds, recent_embeds):
    ref_avg = calculate_average_embedding(reference_embeds)
    recent_avg = calculate_average_embedding(recent_embeds)
    drift_score = cosine(ref_avg, recent_avg)
    logging.info(f"📊 Cosine Distance between recent and historical: {drift_score:.4f}")
    return drift_score > DRIFT_THRESHOLD

def detect_data_drift():
    logging.info("🔍 Running Data Drift Detection")

    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=HOURS_TO_LOOK_BACK)
    since = one_hour_ago.isoformat()

    # Fetch all historical document embeddings
    historical_response = supabase.table("document_chunks").select("embedding").execute()
    historical_embeddings = [np.array(row["embedding"]) for row in historical_response.data if row.get("embedding")]

    if len(historical_embeddings) < 10:
        logging.warning("⚠️ Not enough historical data for drift detection.")
        return

    # Fetch recent embeddings from the past hour
    recent_embeddings = fetch_embeddings("document_chunks", since)

    if not recent_embeddings:
        logging.info("⏱️ No recent embeddings found in the past hour. Skipping drift check.")
        return

    # Compare embeddings
    drifted = detect_drift(historical_embeddings, recent_embeddings)

    if drifted:
        logging.warning("🚨 Drift Detected! Consider triggering retraining.")
    else:
        logging.info("✅ No significant drift detected.")

def main():
    detect_data_drift()

if __name__ == "__main__":
    main()
