import os
from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
from fastapi.responses import JSONResponse
import uvicorn

# --- Load ENV ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Init Supabase Client ---
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FastAPI App ---
app = FastAPI()

@app.get("/should_retrain")
def check_if_model_should_retrain():
    # 1. Query Supabase for logs in the last 1 hour
    one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat()

    try:
        response = supabase.table("conversations") \
            .select("id, is_disliked, created_at") \
            .gte("created_at", one_hour_ago) \
            .execute()
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

    records = response.data or []
    df = pd.DataFrame(records)

    if df.empty:
        return {"status": "no_data", "message": "No queries in the last hour."}

    total = len(df)
    dislikes = df["is_disliked"].sum()
    ratio = dislikes / total

    if ratio > 0.5:
        return {"status": "trigger", "dislike_ratio": ratio}
    else:
        return {"status": "skip", "dislike_ratio": ratio}

# --- Entry Point ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)
