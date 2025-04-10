import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client

# Load credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Parameters
DISLIKE_THRESHOLD = 0.5  # 50%
TIME_WINDOW_MINUTES = 60

def fetch_recent_logs():
    """
    Fetch conversations from Supabase created in the last TIME_WINDOW_MINUTES.
    """
    cutoff_time = (datetime.utcnow() - timedelta(minutes=TIME_WINDOW_MINUTES)).isoformat()
    print(f"⏱️ Checking logs since: {cutoff_time}")
    
    response = supabase.table("conversations") \
        .select("id, query, is_disliked, created_at") \
        .gte("created_at", cutoff_time) \
        .execute()

    data = response.data or []
    df = pd.DataFrame(data)
    return df

def evaluate_policy(df):
    """
    Returns True if dislike ratio exceeds threshold.
    """
    if df.empty:
        print("ℹ️ No logs found in the last hour.")
        return False
    
    dislike_ratio = df["is_disliked"].sum() / len(df)
    print(f"📊 Dislike ratio (last {TIME_WINDOW_MINUTES} min): {dislike_ratio:.2%}")
    
    if dislike_ratio > DISLIKE_THRESHOLD:
        print("🚨 Retraining should be triggered! (Dislike ratio exceeded)")
        return True
    else:
        print("✅ Dislike ratio below threshold — no retraining needed.")
        return False

if __name__ == "__main__":
    logs_df = fetch_recent_logs()
    trigger = evaluate_policy(logs_df)
