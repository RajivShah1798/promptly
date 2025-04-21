import streamlit as st
import requests
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
from dotenv import load_dotenv
from streamlit_connection_utils import read_document, embed_and_store_chunks, chunk_text
from auth import show_auth_page
load_dotenv()
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


BACKEND_URL = "http://127.0.0.1:8000/"
INFERENCE_API_URL = "http://127.0.0.1:8000/ask"
GCS_BUCKET_NAME = "promptly-chat"
GCS_UPLOAD_FOLDER = "data/"

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    st.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    st.stop()

def getUserConversationSessions():
    res = requests.get(f"{BACKEND_URL}/user_conversation_sessions", json={"email_id": st.session_state["user"]["user_email_id"]})
    if res.status_code == 200:
        res.raise_for_status()
        # print(res)
        print(res.json())
        if (res and len(res.json()) > 0):
            st.session_state['user_conversation_sessions'] = res.json()
            st.rerun()
        else:
            st.session_state['user_conversation_sessions'] = []
    else:
        st.error("Not able to fetch your conversations. Please Retry!")

def getUserConversationSession(conv_session_id):
    res = requests.get(f"{BACKEND_URL}/user_conversation_session", json={"conversation_session_id": conv_session_id})
    if res.status_code == 200:
        res.raise_for_status()
        # print(res)
        print(res.json())
        if (res and len(res.json()) > 0 and res.json()[0]["user_preference"]):
            return res.json()[0]["user_preference"]
        else:
            return "Descriptive Answers"
    else:
        return "Descriptive Answers"

def uploadUserConversationSessionDetails(title, description, uploaded_files, is_private):
    # print("=======================Uploading New Conversation Session====================================")
    res = requests.post(f"{BACKEND_URL}/user_conversation_session", json={"email_id": st.session_state["user"]["user_email_id"], "title": title, "description": description})
    if (res and len(res.json()) > 0 and res.json()[0]["conversation_session_id"]):
        document_contents = read_document(uploaded_files)
        # pii_results = check_for_pii(document_contents)
        # redacted_contents = redact_pii(pii_results)
        chunked_data = chunk_text(document_contents)
        # print("New Conv Session id: " + res.json()[0]["conversation_session_id"])
        embed_and_store_chunks(chunked_data, is_private, st.session_state["user"]["org_id"], st.session_state["user"]["user_email_id"], res.json()[0]["conversation_session_id"])
        st.session_state["conversation_session_id"] = res.json()[0]["conversation_session_id"]
    else:
        st.error("Please try again! Session not created.")

def fetch_conversation_session_documents():
    res = requests.get(f"{BACKEND_URL}/conversation_session_documents", json={"conversation_session_id": st.session_state["conversation_session_id"]})
    if (res and len(res.json()) > 0):
        st.session_state["conversation_session_documents"] = res.json()
    else:
        st.session_state["conversation_session_documents"] = []
        st.error("Please upload documents to get relevant solutions!")

def fetch_conversation_for_session():
    res = requests.get(f"{BACKEND_URL}/conversations_for_session", json={"conversation_session_id": st.session_state["conversation_session_id"]})
    if (res and len(res.json()) > 0):
        conversations = []
        for conversation in res.json():
            conversations.append({"role": "user", "content": conversation["query"]})
            conversations.append({"role": "assistant", "content": conversation["response"]})
        st.session_state["conversations"] = conversations
        return True
    else:
        st.session_state["conversations"] = []
        # st.error("Error occured while fetching conversations!")
    return False

def stream_response(query):
    preference = st.session_state["preference"] if st.session_state["preference"] != "Custom Preference" else st.session_state["custom_text"]

    with requests.post(INFERENCE_API_URL, stream=True, 
            json={"conversation_session_id": st.session_state["conversation_session_id"], 
                  "query": query,  
                  "user_email_id": st.session_state["user"]["user_email_id"], 
                  "preference": preference,
                  "conversational_history": ""}) as response:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk.decode('utf-8')

@st.dialog("Upload Documents to Chat!", width="large")
def upload_stream_dialog():
    title = st.text_input("Title")
    description = st.text_area("Description (max 100 characters)", max_chars=100)
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=['pdf', 'txt'],
        accept_multiple_files=True
    )
    is_private = st.toggle("🔒 Private Chat", value=True)

    if not is_private:
        st.info("This chat and associated documents will be visible to all!")
    else:
        st.info("Private chats are only visible to you. Others can’t see or query this session.")
    is_submit_enabled = bool(title and description and uploaded_files)
    # print(uploaded_files)
    col1, col2 = st.columns([7, 1])
    with col1:
        if st.button("Submit", disabled=not is_submit_enabled):
            with st.spinner("Creating chat session for you..."):
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

def refreshConversationSessionState():
    conv_session_states = ['conversation_session_documents','conversations', 'conversation_session_document_ids']
    for conv_session_state in conv_session_states:
        if conv_session_state in st.session_state:
            del st.session_state[conv_session_state]
    st.session_state["rendered_initial_conversations"] = False

def siderbarUI():
    if st.session_state["page"] != "home":
        if st.sidebar.button("⬅️ Back"):
            st.session_state["page"] = "home"
            refreshConversationSessionState()
            st.rerun()
        st.sidebar.header("📁 Upload Your Documents")

        uploaded_files_chat = st.sidebar.file_uploader(
        "Upload PDF or TXT files",
        type=['pdf', 'txt'],
        accept_multiple_files=True,
        )

        if st.sidebar.button("Upload") and uploaded_files_chat:
            with st.spinner("Processing files..."):
                try:
                    document_contents = read_document(uploaded_files_chat)
                    chunked_data = chunk_text(document_contents)
                    embed_and_store_chunks(
                        chunked_data,
                        True,
                        st.session_state["user"]["org_id"],
                        st.session_state["user"]["user_email_id"],
                        st.session_state["conversation_session_id"]
                    )
                    fetch_conversation_session_documents()
                    st.success("Files uploaded and processed successfully!")
                    
                    st.rerun()

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        
        with st.sidebar.expander("View Uploaded Documents", expanded=False):
            for num, doc in enumerate(st.session_state["conversation_session_documents"]):
                st.markdown(f"**{num+1}.** {doc['location']}")
        
        if "custom_text" not in st.session_state:
            st.session_state["custom_text"] = ""
        
        with st.sidebar:
            st.header("Answer Preferences")

            # Radio button for selecting preference
            preference = st.radio(
                "Select answer type:",
                options=["Short Answers", "Descriptive Answers", "Custom Preference"],
                index=st.session_state["user_preference_index"],  # Default to "Descriptive Answers"
                key="preference"
            )

            # Determine if text area should be disabled
            is_disabled = preference != "Custom Preference"

            if not is_disabled:
                custom_text = st.text_area(
                    "Enter custom preference (max 100 characters):",
                    value=st.session_state["custom_text"],
                    max_chars=100,
                    disabled=is_disabled,
                    key="custom_text"
                )
            st.info("Current Preference: "+ st.session_state["preference"])

    
####################### UI Starts from here #############################################
if 'isNewUser' not in st.session_state:
    st.session_state['isNewUser'] = False
if 'user' not in st.session_state:
    show_auth_page()
else:
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    if ('conversation_session_data' not in st.session_state) or st.session_state["page"] == "home":
        # Streamlit UI setup
        st.set_page_config(page_title="Promptly", layout="wide")
        st.markdown(f"""
        <div style="text-align:center; margin-top: 10px; margin-bottom: 30px;">
            <h2 style="color:#356AE6; margin-bottom: 0;">Welcome, {st.session_state['user']['first_name']} 👋</h2>
        </div>
        """, unsafe_allow_html=True)
        # left, middle, right = st.columns([4,1,1])
        # right.text("")
        # if right.button("Start New Chat", icon="😃", use_container_width=True):
        #     upload_stream_dialog()
        
        if ('user_conversation_sessions' not in st.session_state):
            getUserConversationSessions()
        
        if (not st.session_state['user_conversation_sessions'] or len(st.session_state['user_conversation_sessions']) < 1):
            st.text("")
            st.info("Click the button below to create new chat!")
        cols = st.columns(3)
        for i, item in enumerate(st.session_state['user_conversation_sessions']):
            col = cols[i % 3]
            with col:
                with st.container(height=210):
                    top = st.container(height=120, border=False)
                    with top:
                        st.markdown(f"#### 📝 {item['title']}")
                        st.caption(item["description"])
                    left, middle, right = st.columns(3)
                    # st.json(st.session_state['user_conversation_sessions'][i], expanded=False)
                    if left.button("Start Chat", key=f"start_chat_{i}", use_container_width=True):
                        st.session_state["conversation_session_data"] = st.session_state['user_conversation_sessions'][i]
                        st.session_state["conversation_session_id"] = st.session_state['user_conversation_sessions'][i]["id"]
                        conv_session_user_pref = getUserConversationSession(st.session_state["conversation_session_id"])
                        # print(conv_session_user_pref)
                        if (conv_session_user_pref == "Short Answers"):
                            st.session_state["user_preference_index"] = 0
                        elif (conv_session_user_pref == "Descriptive Answers"):
                            st.session_state["user_preference_index"] = 1
                        else:
                            st.session_state["user_preference_index"] = 2
                        
                        if st.session_state["user_preference_index"] == 2:
                            st.session_state["custom_text"] = conv_session_user_pref
                        st.session_state["page"] = "chat"
                        st.rerun()
                    if right.button("Delete Chat", key=f"delete_chat_{i}", use_container_width=True):
                        st.rerun()
        st.markdown("---")
        center = st.columns([1, 2, 1])[1]
        with center:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            if st.button("➕ Start New Chat", use_container_width=True):
                upload_stream_dialog()
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.set_page_config(page_title="Promptly - Smart Document QA", layout="wide")

        # Initialize required session variables
        if "last_rendered_session" not in st.session_state:
            st.session_state["last_rendered_session"] = ""
        if "rendered_initial_conversations" not in st.session_state:
            st.session_state["rendered_initial_conversations"] = False
        if "conversation_session_document_ids" not in st.session_state:
            st.session_state["conversation_session_document_ids"] = []
        if "conversations" not in st.session_state:
            with st.spinner("Fetching Conversations..."):
                fetch_conversation_for_session()
        if "conversation_session_documents" not in st.session_state:
            with st.spinner("Loading your documents..."):
                fetch_conversation_session_documents()

        # Detect session change and reset flags if necessary
        if st.session_state["last_rendered_session"] != st.session_state["conversation_session_id"]:
            st.session_state["last_rendered_session"] = st.session_state["conversation_session_id"]
            st.session_state["rendered_initial_conversations"] = False
            print("Reached mismatch")
            st.rerun() 

        # Display static header and sidebar
        siderbarUI()
        header = st.container()
        with header:
            st.markdown("## 🔎 Ask a Question about Your Project Documentation")

        for conversation in st.session_state.get("conversations", []):
            st.chat_message(conversation["role"]).markdown(conversation["content"])

        # Accept user input at the end
        if query := st.chat_input("What is up?"):
            # Append user message and render it
            st.chat_message("user").markdown(query)
            st.session_state["conversations"].append({"role": "user", "content": query})

            # Get assistant response and append it
            # with st.spinner("Processing your query..."):
            assistant_message = st.chat_message("assistant")
            full_response = st.write_stream(stream_response(query))
            st.session_state["conversations"].append({"role": "assistant", "content": full_response})
            st.rerun()

