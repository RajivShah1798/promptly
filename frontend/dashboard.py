import streamlit as st
import requests
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model_pipeline/scripts")))

from upload import upload_stream_dialog

BACKEND_URL = "http://127.0.0.1:8000"

def get_user_conversation_sessions():
    try:
        res = requests.get(f"{BACKEND_URL}/user_conversation_session", json={
            "email_id": st.session_state["user"]["user_email_id"]
        })
        if res.status_code == 200:
            st.session_state["user_conversation_sessions"] = res.json() or []
        else:
            st.session_state["user_conversation_sessions"] = []
            st.warning("No sessions found.")
    except Exception as e:
        st.session_state["user_conversation_sessions"] = []
        st.error(f"❌ Could not load sessions: {e}")

def show_dashboard():
    st.title(f"📂 Welcome, {st.session_state['user']['first_name']}!")

    if "user_conversation_sessions" not in st.session_state or st.session_state["user_conversation_sessions"] is None:
        get_user_conversation_sessions()

    sessions = st.session_state.get("user_conversation_sessions") or []

    if not sessions:
        st.info("You don't have any chat sessions yet. Upload a document to start.")

    cols = st.columns(3)
    for i, session in enumerate(sessions):
        col = cols[i % 3]
        with col:
            with st.container(height=210):
                st.subheader(session["title"])
                st.caption(session["description"])
                if st.button("Start Chat", key=f"start_chat_{i}"):
                    st.session_state["conversation_session_data"] = session
                    st.session_state["conversation_session_id"] = session["id"]
                    st.session_state["conversation_session_documents"] = []  # ✅ RESET here
                    st.session_state["conversations"] = []
                    st.rerun()

    st.markdown("---")
    center = st.columns([1, 3, 1])[1]
    with center:
        if st.button("➕ Start New Chat", use_container_width=True):
            upload_stream_dialog()
