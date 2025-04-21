import streamlit as st
import requests
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model_pipeline/scripts")))

from upload import upload_stream_dialog

BACKEND_URL = "http://127.0.0.1:8000"

# -------------------- DATA FETCHING -------------------- #

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

# -------------------- MAIN DASHBOARD VIEW -------------------- #

def show_dashboard():
    # Branding Header
    st.markdown(f"""
        <div style="text-align:center; margin-top: 10px; margin-bottom: 30px;">
            <h2 style="color:#356AE6; margin-bottom: 0;">Welcome, {st.session_state['user']['first_name']} 👋</h2>
            <p style="font-size: 1.1em; color: #CED6E0;">Here are your active document sessions. Click any to continue chatting.</p>
        </div>
    """, unsafe_allow_html=True)

    # Fetch sessions if needed
    if "user_conversation_sessions" not in st.session_state or st.session_state["user_conversation_sessions"] is None:
        get_user_conversation_sessions()

    sessions = st.session_state.get("user_conversation_sessions") or []

    if not sessions:
        st.info("🗃️ You don’t have any chat sessions yet. Upload a document to get started.")

    # 3-column responsive layout
    cols = st.columns(3)
    for i, session in enumerate(sessions):
        col = cols[i % 3]
        with col:
            with st.container(border=True):
                st.markdown(f"#### 📁 {session['title']}")
                st.caption(f"📝 {session['description']}")
                st.markdown(
                    f"<span style='font-size: 12px; color: #AAA;'>🆔 {session['id'][:8]}...</span>",
                    unsafe_allow_html=True
                )
                st.markdown("---")
                if st.button("💬 Start Chat", key=f"start_chat_{i}"):
                    st.session_state["conversation_session_data"] = session
                    st.session_state["conversation_session_id"] = session["id"]
                    st.session_state["conversation_session_documents"] = []  # Reset
                    st.session_state["conversations"] = []
                    st.rerun()

    st.markdown("---")

    # Centered CTA for Upload
    center = st.columns([1, 2, 1])[1]
    with center:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("➕ Start New Chat", use_container_width=True):
            upload_stream_dialog()
        st.markdown("</div>", unsafe_allow_html=True)
