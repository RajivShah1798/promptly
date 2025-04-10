import streamlit as st
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

# --- Setup ---
st.set_page_config(page_title="Promptly Logs Dashboard", layout="wide")
st.title("📊 Promptly Logs Monitoring Dashboard")

# --- Load ENV ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Fetch logs from Supabase ---
@st.cache_data(ttl=60)  # Cache for 1 min to simulate near real-time
def fetch_logs(limit=1000):
    response = supabase.table("conversations").select("*").order("id", desc=True).limit(limit).execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()

df = fetch_logs()

if df.empty:
    st.warning("No logs found in Supabase.")
    st.stop()

# ✅ Use real timestamps instead of simulation
df["created_at"] = pd.to_datetime(df["created_at"])
df.sort_values("created_at", ascending=False, inplace=True)

# ✅ Add time range filter here
time_range = st.selectbox("📅 Filter logs by timeframe", ["All", "Last 15 min", "Last 1 hr", "Last 24 hrs"])
now = datetime.utcnow()

if time_range == "Last 15 min":
    df = df[df["created_at"] >= now - timedelta(minutes=15)]
elif time_range == "Last 1 hr":
    df = df[df["created_at"] >= now - timedelta(hours=1)]
elif time_range == "Last 24 hrs":
    df = df[df["created_at"] >= now - timedelta(hours=24)]

# --- Simulate timestamp ---
df["created_at"] = pd.to_datetime(df["created_at"])
df.sort_values("created_at", ascending=False, inplace=True)

# --- Metrics ---
total_queries = len(df)
dislikes = df["is_disliked"].sum()
dislike_ratio = round((dislikes / total_queries) * 100, 2) if total_queries else 0

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Queries (approx. last hour)", total_queries)
with col2:
    st.metric("Dislike Ratio", f"{dislike_ratio:.2f}%")
    st.progress(min(dislike_ratio / 100, 1.0))

# --- Query Volume over Time ---
st.subheader("📈 Query Volume Over Time")
df_volume = df.groupby(pd.Grouper(key="created_at", freq="1min")).size()
st.line_chart(df_volume)

# --- Top Disliked Queries ---
if "query" in df.columns and "is_disliked" in df.columns:
    st.subheader("😠 Most Disliked Queries")
    top_disliked = df[df["is_disliked"] == True]["query"].value_counts().head(5)
    st.table(top_disliked.reset_index().rename(columns={"index": "Query", "query": "Dislike Count"}))

# --- Fallback Model Usage ---
if "fallback_model" in df.columns:
    st.subheader("🧠 Fallback Model Usage")
    fallback_stats = df["fallback_model"].fillna("None").value_counts()
    st.bar_chart(fallback_stats)

# --- Debug Table (Optional) ---
with st.expander("🛠️ View Raw Logs Table (Debugging)"):
    st.dataframe(df)

# --- Dislike Ratio Trend Over Time ---
st.subheader("📉 Dislike Ratio Over Time")
df['minute'] = df["created_at"].dt.floor("min")
dislike_trend = df.groupby("minute")["is_disliked"].mean()
st.line_chart(dislike_trend)

# --- Evaluate retraining policy ---
from datetime import datetime, timedelta

st.subheader("🔁 Retraining Trigger Status (Last 1 Hour)")

# Step 1: Filter logs within the last 60 minutes
time_threshold = datetime.utcnow() - timedelta(minutes=60)
recent_logs = df[df["created_at"] >= time_threshold]
recent_dislikes = recent_logs["is_disliked"].sum()
recent_total = len(recent_logs)
recent_dislike_ratio = (recent_dislikes / recent_total) if recent_total else 0

# Step 2: Display status
if recent_total == 0:
    st.info("ℹ️ No queries in the last hour. Retraining not required.")
elif recent_dislike_ratio > 0.5:
    st.error(f"🚨 Retraining Required — Dislike Ratio = {recent_dislike_ratio:.2%}")
else:
    st.success(f"✅ Stable — Dislike Ratio = {recent_dislike_ratio:.2%}")

