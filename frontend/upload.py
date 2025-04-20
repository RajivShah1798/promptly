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

BACKEND_URL = "http://127.0.0.1:8000"
GCS_BUCKET_NAME = "promptly-chat"
GCS_UPLOAD_FOLDER = "data/"

def upload_file_to_gcs(file, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, rewind=True)
    return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"

def uploadUserConversationSessionDetails(title, description, uploaded_files, is_private):
    res = requests.post(f"{BACKEND_URL}/user_conversation_session", json={
        "email_id": st.session_state["user"]["user_email_id"],
        "title": title,
        "description": description
    })

    if res.status_code == 200 and res.json():
        conv_id = res.json()[0]["conversation_session_id"]
        doc_contents = read_document(uploaded_files)
        pii_results = check_for_pii(doc_contents)
        redacted = redact_pii(pii_results)
        chunks = chunk_text(redacted)
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

@st.dialog("📄 Upload Documents to Start Chat", width="large")
def upload_stream_dialog():
    if st.button("← Cancel and Go Back"):
        st.rerun()
    title = st.text_input("Title")
    description = st.text_area("Description (max 100 chars)", max_chars=100)
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=['pdf', 'txt'],
        accept_multiple_files=True
    )
    is_private = st.toggle("🔒 Make Chat Private")

    if st.button("Submit"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
        elif not title.strip():
            st.warning("Please provide a title.")
        else:
            st.session_state['stream_info'] = {
                'title': title,
                'description': description,
                'files': uploaded_files
            }
            uploadUserConversationSessionDetails(title, description, uploaded_files, is_private)
            if 'user_conversation_sessions' in st.session_state:
                del st.session_state['user_conversation_sessions']
            st.rerun()
