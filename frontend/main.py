import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model_pipeline/scripts")))

from session import init_session_state
from auth import show_auth_page
from dashboard import show_dashboard
from chat import show_chat_interface

# Page config
st.set_page_config(page_title="Promptly", layout="wide")

# Initialize session state
init_session_state()

# Route user
if not st.session_state.get("user"):
    show_auth_page()
elif not st.session_state.get("conversation_session_data"):
    show_dashboard()
else:
    show_chat_interface()
