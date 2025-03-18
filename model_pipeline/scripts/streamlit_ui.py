import streamlit as st
import requests
from google.cloud import storage
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
from datetime import datetime

# Constants
INFERENCE_API_URL = "http://0.0.0.0:8000/ask"
GCS_BUCKET_NAME = "promptly-chat"
GCS_UPLOAD_FOLDER = "data/"

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    st.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    st.stop()

# Function to upload file to GCS
def upload_file_to_gcs(file, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, rewind=True)
    return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"

# Streamlit UI setup
st.set_page_config(page_title="Promptly - Smart Document QA", layout="wide")
st.title("📄 Promptly - Document-Based Q&A Assistant")

st.sidebar.header("📁 Upload Your Documents")

uploaded_file = st.sidebar.file_uploader("Upload a PDF Document", type=["pdf"])
if uploaded_file:
    # Upload to GCS
    try:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        destination_blob_name = f"{GCS_UPLOAD_FOLDER}{timestamp}_{uploaded_file.name}"
        gcs_path = upload_file_to_gcs(uploaded_file, destination_blob_name)
        st.sidebar.success(f"Uploaded to GCS: {gcs_path}")
        st.sidebar.info("Document ingestion trigger will be automated soon.")

    except Exception as e:
        st.sidebar.error(f"❌ GCS Upload failed: {e}")

st.markdown("## 🔎 Ask a Question about Your Project Documentation")

query = st.text_input("Enter your query:", "How does FDA regulate medical devices?")

if st.button("Ask Promptly") and query:
    with st.spinner("Processing your query..."):
        try:
            response = requests.post(INFERENCE_API_URL, json={"query": query}, timeout=120)
            response.raise_for_status()
            answer = response.json().get("answer", "No response received.")

            st.success("✅ Promptly Response")
            st.write(f"**Query:** {query}")
            st.write(f"**Answer:** {answer}")

            # Optional: show references
            references = response.json().get("references", [])
            if references:
                st.markdown("### Referenced Documents & Sections")
                for ref in references:
                    st.write(f"- **Document:** {ref['document']}, Section: {ref['section']}")
                    st.write(f"  Excerpt: *{ref['excerpt'][:300]}...*")

        except Exception as e:
            st.error(f"❌ Query failed: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Ensure the inference service is running at `http://0.0.0.0:8000`. ")
st.sidebar.write("This UI will connect to `/ask` endpoint for contextual answers.")
