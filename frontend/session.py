import streamlit as st

def init_session_state():
    defaults = {
        "user": None,
        "isNewUser": False,
        "conversation_session_data": None,
        "conversation_session_id": None,
        "user_conversation_sessions": None,
        "conversation_session_documents": [],
        "conversation_session_document_ids": [],
        "conversations": [],
        "stream_info": {},
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
