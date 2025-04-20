from supabase import create_client
import config
from datetime import datetime

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def fetch_chat_history(session_id):
    """
    Fetch chat history from Supabase using the `fetch_conversation_history` RPC.
    Returns list of dicts like: {role: 'user'|'assistant', content: '...'}
    """
    try:
        res = supabase.rpc("fetch_conversation_history", {"p_session_id": session_id}).execute()
        if res.data:
            return [{"role": row["role"], "content": row["content"]} for row in res.data]
        return []
    except Exception as e:
        print(f"❌ Supabase RPC error: {e}")
        return []

def log_chat_to_supabase(session_id, user_email, query, response, is_private=True, model="zephyr-7b-beta"):
    """
    Save a user query + assistant response to the Supabase conversations table.
    """
    try:
        supabase.table("conversations").insert({
            "conversation_session_id": session_id,
            "user_email_id": user_email,
            "query": query,
            "response": response,
            "is_private": is_private,
            "fallback_model": model,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        print(f"❌ Failed to log chat: {e}")
