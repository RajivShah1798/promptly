import os
import json
import logging
import numpy as np
from datetime import datetime, timedelta, timezone
from supabase import create_client
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
from dateutil.parser import isoparse  # Better ISO 8601 support

# === Load Env ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Logger Setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Constants ===
DRIFT_THRESHOLD = 0.2
HOURS_TO_LOOK_BACK = 1
TABLE_NAME = "document_chunks"

def fetch_embeddings_since(since_timestamp: str):
    logging.info(f"📥 Fetching embeddings from `{TABLE_NAME}` since {since_timestamp}")
    response = supabase.table(TABLE_NAME).select("embedding, created_at").gte("created_at", since_timestamp).execute()
    
    if not response.data:
        logging.warning("⚠️ No embeddings found in the given timeframe.")
        return []

    embeddings = []
    for row in response.data:
        embedding_raw = row.get("embedding")
        if not embedding_raw:
            continue
        emb = json.loads(embedding_raw) if isinstance(embedding_raw, str) else embedding_raw
        embeddings.append(np.array(emb))
        logging.debug(f"📦 Found embedding created_at: {row.get('created_at')}")

    return embeddings

def fetch_all_historical_embeddings():
    logging.info("📦 Fetching ALL historical embeddings from Supabase...")
    response = supabase.table(TABLE_NAME).select("embedding").execute()

    if not response.data:
        logging.error("❌ No historical embeddings found.")
        return []

    embeddings = []
    for row in response.data:
        embedding_raw = row.get("embedding")
        if not embedding_raw:
            continue
        emb = json.loads(embedding_raw) if isinstance(embedding_raw, str) else embedding_raw
        embeddings.append(np.array(emb))
    
    logging.info(f"📈 Loaded {len(embeddings)} historical embeddings.")
    return embeddings

def calculate_average_embedding(embeddings):
    if not embeddings:
        raise ValueError("No embeddings provided for averaging.")
    return np.mean(embeddings, axis=0)

def detect_drift(reference_embeds, recent_embeds):
    ref_avg = calculate_average_embedding(reference_embeds)
    recent_avg = calculate_average_embedding(recent_embeds)
    drift_score = cosine(ref_avg, recent_avg)
    logging.info(f"📊 Cosine Distance between recent and historical: {drift_score:.4f}")
    return drift_score > DRIFT_THRESHOLD, drift_score

def log_latest_document():
    logging.info("🔎 Checking latest document chunk timestamp...")
    response = supabase.table(TABLE_NAME).select("created_at").order("created_at", desc=True).limit(1).execute()
    if response.data:
        latest_ts = response.data[0]['created_at']
        now_utc = datetime.now(timezone.utc)
        try:
            latest_dt = isoparse(latest_ts)
            delta = now_utc - latest_dt
            logging.info(f"📌 Most recent chunk: created_at = {latest_ts} (Age: {delta.total_seconds():.1f}s)")
        except Exception as e:
            logging.warning(f"⚠️ Failed to parse latest timestamp: {latest_ts} | Error: {e}")
    else:
        logging.warning("⚠️ No documents in the system yet.")

def run_drift_detection():
    logging.info("🔍 Running Data Drift Detection")

    now = datetime.now(timezone.utc)
    since = (now - timedelta(hours=HOURS_TO_LOOK_BACK)).replace(microsecond=0).isoformat()

    logging.info(f"🕒 UTC NOW: {now.isoformat()}")
    logging.info(f"🔁 Filtering since: {since}")
    log_latest_document()

    # Fetch all historical data
    historical_embeddings = fetch_all_historical_embeddings()

    if len(historical_embeddings) < 10:
        logging.warning("⚠️ Not enough historical data for drift detection.")
        return

    # Fetch only recent embeddings
    recent_embeddings = fetch_embeddings_since(since)

    if not recent_embeddings:
        logging.info("⏱️ No recent embeddings found. Skipping drift check.")
        return

    # Perform drift detection
    drifted, drift_score = detect_drift(historical_embeddings, recent_embeddings)

    if drifted:
        logging.warning(f"🚨 Drift Detected! Cosine Distance = {drift_score:.4f}")
        # TODO: trigger retraining pipeline here
    else:
        logging.info(f"✅ No significant drift detected. Cosine Distance = {drift_score:.4f}")

# === CLI Trigger ===
if __name__ == "__main__":
    run_drift_detection()
