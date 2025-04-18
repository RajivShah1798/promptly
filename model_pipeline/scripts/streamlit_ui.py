import streamlit as st
import requests
from google.cloud import storage
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
from datetime import datetime
from dotenv import load_dotenv
from streamlit_ui_utils import read_document, embed_and_store_chunks, chunk_text
load_dotenv()
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from dags.data_preprocessing.check_pii_data import check_for_pii, redact_pii


# Constants
BACKEND_URL = "http://127.0.0.1:8000/"
INFERENCE_API_URL = "http://127.0.0.1:8000/ask"
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

def login(email, password):
    res = requests.post(f"{BACKEND_URL}/login", json={"email_id": email, "password": password})
    if res.status_code == 200:
        res.raise_for_status()
        # print(res)
        # print(res.json())
        if (res and len(res.json()) > 0):
            st.session_state['user'] = res.json()[0]
            st.rerun()
        else:
            st.error("Incorrect Login Credentials")
    else:
        st.error("Login failed. Please Retry!")

def signup(email, password, firstname, lastname, organization_id):
    res = requests.post(f"{BACKEND_URL}/signup", json={"firstname": firstname, "lastname": lastname, "email_id": email, "password": password, "organization_id": organization_id})
    if res.status_code == 200:
        st.session_state['user'] = res.json()['user']
        st.success("Sign Up successful")
    else:
        st.error("Sign Up failed")

def getUserConversationSessions():
    res = requests.get(f"{BACKEND_URL}/user_conversation_session", json={"email_id": st.session_state["user"]["user_email_id"]})
    if res.status_code == 200:
        res.raise_for_status()
        # print(res)
        print(res.json())
        if (res and len(res.json()) > 0):
            st.session_state['user_conversation_sessions'] = res.json()
            st.rerun()
        else:
            st.text("Click the button below to get your answers Promptly!")
    else:
        st.error("Not able to fetch your conversations. Please Retry!")

def uploadUserConversationSessionDetails(title, description, uploaded_files, is_private):
    # print("=======================Uploading New Conversation Session====================================")
    res = requests.post(f"{BACKEND_URL}/user_conversation_session", json={"email_id": st.session_state["user"]["user_email_id"], "title": title, "description": description})
    if (res and len(res.json()) > 0 and res.json()[0]["conversation_session_id"]):
        document_contents = read_document(uploaded_files)
        pii_results = check_for_pii(document_contents)
        redacted_contents = redact_pii(pii_results)
        chunked_data = chunk_text(redacted_contents)
        # print("New Conv Session id: " + res.json()[0]["conversation_session_id"])
        embed_and_store_chunks(chunked_data, is_private, st.session_state["user"]["org_id"], st.session_state["user"]["user_email_id"], res.json()[0]["conversation_session_id"])
        st.session_state["conversation_session_id"] = res.json()[0]["conversation_session_id"]
    else:
        st.error("Please try again! Session not created.")

def logout():
    requests.post(f"{BACKEND_URL}/logout")
    st.session_state.pop('user', None)
    st.success("Logged out")

def check_user():
    try:
        res = requests.get(f"{BACKEND_URL}/user", cookies={"user": st.session_state.get('user', '')})
        return res.json()['user']
    except:
        return None

def signUp():
    st.title("Sign Up")
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    firstname = st.text_input("First Name")
    lastname = st.text_input("Last Name")
    organization_id = st.text_input("Organization ID")
    if st.button("Sign Up"):
        if not all([email.strip(), password.strip(), firstname.strip(), lastname.strip(), organization_id.strip()]):
            st.error("Please fill in all the fields.")
        else:
            signup(email, password, firstname, lastname, organization_id)


def signIn():
    st.title("Sign In")
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    if st.button("Sign in"):
        if not all([email.strip(), password.strip()]):
            st.error("Please fill in all the fields.")
        else:
            login(email, password)

def fetch_conversation_session_documents():
    res = requests.get(f"{BACKEND_URL}/conversation_session_documents", json={"conversation_session_id": st.session_state["conversation_session_id"]})
    if (res and len(res.json()) > 0):
        st.session_state["conversation_session_documents"] = res.json()
    else:
        st.error("Please upload documents to get relevant solutions!")

@st.dialog("Upload Documents to Chat!", width="large")
def upload_stream_dialog():
    title = st.text_input("Title")
    description = st.text_area("Description (max 100 characters)", max_chars=100)
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=['pdf', 'txt'],
        accept_multiple_files=True
    )
    is_private = st.toggle("Private Chat")

    if not is_private:
        st.info("This chat and associated documents will be visible to all!")
    else:
        st.info("This chat is private!")
    
    print(uploaded_files)
    col1, col2 = st.columns([7, 1])
    with col1:
        if st.button("Submit"):
            st.session_state['stream_info'] = {
                'title': title,
                'description': description,
                'files': uploaded_files
            }
            uploadUserConversationSessionDetails(title, description, uploaded_files, is_private)
            if 'user_conversation_sessions' in st.session_state:
                del st.session_state['user_conversation_sessions']
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.rerun()

if 'isNewUser' not in st.session_state:
    st.session_state['isNewUser'] = False

if 'user' not in st.session_state:
    if st.session_state['isNewUser']:
        signUp()
        if st.button("Already have an account? Sign In"):
            st.session_state['isNewUser'] = False
            st.rerun()
    else:
        signIn()
        if st.button("New User? Sign Up"):
            st.session_state['isNewUser'] = True
            st.rerun()
else:
    if ('conversation_session_data' not in st.session_state):
        # Streamlit UI setup
        st.set_page_config(page_title="Promptly", layout="wide")
        st.title("Welcome "+st.session_state["user"]["first_name"] + "!")
        st.text("")
        if ('user_conversation_sessions' not in st.session_state):
            getUserConversationSessions()
        
        cols = st.columns(3)
        for i, item in enumerate(st.session_state['user_conversation_sessions']):
            col = cols[i % 3]
            with col:
                with st.container(height=210):
                    top = st.container(height=120, border=False)
                    with top:
                        st.subheader(item["title"])
                        st.caption(item["description"])
                    
                    if st.button("Start Chat", key=f"start_chat_{i}"):
                        st.session_state["conversation_session_data"] = st.session_state['user_conversation_sessions'][i]
                        st.session_state["conversation_session_id"] = st.session_state['user_conversation_sessions'][i]["id"]
                        st.rerun()
        st.text("")
        left, middle, right = st.columns(3)
        if middle.button("New Chat", icon="😃", use_container_width=True):
            upload_stream_dialog()
    else:
        st.set_page_config(page_title="Promptly - Smart Document QA", layout="wide")
        # st.title("📄 Promptly - Document-Based Q&A Assistant")

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

        if "conversations" not in st.session_state:
            st.session_state["conversations"] = []
        
        # st.json(st.session_state["conversations"])
        for conversation in st.session_state["conversations"]:
            st.chat_message(conversation["role"]).write(conversation["content"])
        # query = st.text_input("Enter your query:", "How does FDA regulate medical devices?")

        with st.spinner("Loading you documents", show_time=True):
            if "conversation_session_documents" not in st.session_state:
                fetch_conversation_session_documents()

        if "conversation_session_document_ids" not in st.session_state:
            st.session_state["conversation_session_document_ids"] = []
        with st.sidebar.expander("View Documents", expanded=True):
            for num, doc in enumerate(st.session_state["conversation_session_documents"]):
                st.markdown(f"**{num+1}.** {doc['location']}")
        
        if query := st.chat_input("What is up?"):
        # if st.button("Ask Promptly") and query:
            st.chat_message("user").markdown(query)
            st.session_state["conversations"].append({"role": "user", "content": query})
            with st.spinner("Processing your query..."):
                try:
                    response = requests.post(INFERENCE_API_URL, json={"query": query, "conversation_session_id": st.session_state["conversation_session_id"]}, timeout=120)
                    response.raise_for_status()
                    answer = response.json().get("answer", "No response received.")

                    st.chat_message("assistant").markdown(answer)
                    st.session_state["conversations"].append({"role": "assistant", "content": answer})
                    # references = response.json().get("references", [])
                    # if references:
                    #     st.markdown("### Referenced Documents & Sections")
                    #     for ref in references:
                    #         st.write(f"- **Document:** {ref['document']}, Section: {ref['section']}")
                    #         st.write(f"  Excerpt: *{ref['excerpt'][:300]}...*")
                    # st.rerun()
                except Exception as e:
                    st.error(f"❌ Query failed: {e}")

        # st.sidebar.markdown("---")
        # st.sidebar.write("Ensure the inference service is running at " + BACKEND_URL)
        # st.sidebar.write("This UI will connect to `/ask` endpoint for contextual answers.")
