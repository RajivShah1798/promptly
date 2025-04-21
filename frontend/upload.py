import streamlit as st
import os, sys
import requests
from datetime import datetime
from google.cloud import storage
import certifi

# Fix certificate path
os.environ["SSL_CERT_FILE"] = certifi.where()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model_pipeline/scripts")))

from streamlit_ui_utils import read_document, chunk_text, embed_and_store_chunks
from dags.data_preprocessing.check_pii_data import check_for_pii, redact_pii

# -------------------- Config -------------------- #
BACKEND_URL = "http://127.0.0.1:8000"
GCS_BUCKET_NAME = "promptly-chat"
GCS_UPLOAD_FOLDER = "data/"

# -------------------- Upload to GCS -------------------- #
def upload_file_to_gcs(file, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, rewind=True)
    return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"

# -------------------- Upload Workflow -------------------- #
def uploadUserConversationSessionDetails(title, description, uploaded_files, is_private):
    res = requests.post(f"{BACKEND_URL}/user_conversation_session", json={
        "email_id": st.session_state["user"]["user_email_id"],
        "title": title,
        "description": description
    })

    if res.status_code == 200 and res.json():
        conv_id = res.json()[0]["conversation_session_id"]

        with st.spinner("🔍 Reading and processing documents..."):
            doc_contents = read_document(uploaded_files)
            pii_results = check_for_pii(doc_contents)
            redacted = redact_pii(pii_results)
            chunks = chunk_text(redacted)

        with st.spinner("📌 Uploading to vector store..."):
            embed_and_store_chunks(
                chunks,
                is_private,
                st.session_state["user"]["org_id"],
                st.session_state["user"]["user_email_id"],
                conv_id
            )

        st.session_state["conversation_session_id"] = conv_id

    else:
        st.error("❌ Could not create session. Please try again.")

# -------------------- Upload Modal -------------------- #
@st.dialog("📄 Upload Documents to Start Chat", width="large")
def upload_stream_dialog():
    st.markdown("<div style='margin-bottom: 1rem;'>Fill in details to start a new document-based conversation.</div>", unsafe_allow_html=True)

    title = st.text_input("📝 Conversation Title", placeholder="e.g. Q2 API Integration Plan")
    description = st.text_area("🗒️ Description (max 100 chars)", max_chars=100, placeholder="Brief description of this document set")

    uploaded_files = st.file_uploader(
        "📎 Upload your PDFs or Text Files",
        type=['pdf', 'txt'],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.markdown("✅ **Files Selected:**")
        for f in uploaded_files:
            st.markdown(f"- `{f.name}`")

    is_private = st.toggle("🔒 Make Chat Private", value=True)
    st.caption("Private chats are only visible to you. Others can’t see or query this session.")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🚀 Start Chat", use_container_width=True):
            if not uploaded_files:
                st.warning("⚠️ Please upload at least one document.")
            elif not title.strip():
                st.warning("⚠️ Please provide a conversation title.")
            else:
                st.session_state['stream_info'] = {
                    'title': title,
                    'description': description,
                    'files': uploaded_files
                }
                uploadUserConversationSessionDetails(title, description, uploaded_files, is_private)

                if 'user_conversation_sessions' in st.session_state:
                    del st.session_state['user_conversation_sessions']

                st.success("✅ Documents uploaded successfully. Launching chat...")
                st.rerun()

    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()
