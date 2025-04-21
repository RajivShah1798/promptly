import streamlit as st
import requests
from utils import fetch_chat_history, log_chat_to_supabase

INFERENCE_API_URL = "http://127.0.0.1:8000/ask"
BACKEND_URL = "http://127.0.0.1:8000/conversation_session_documents"

# ------------------ Helper: Load Docs ------------------ #
def fetch_conversation_session_documents():
    try:
        res = requests.get(BACKEND_URL, json={
            "conversation_session_id": st.session_state["conversation_session_id"]
        })
        if res.status_code == 200:
            st.session_state["conversation_session_documents"] = res.json()
        else:
            st.session_state["conversation_session_documents"] = []
            st.warning("No documents found for this session.")
    except Exception as e:
        st.session_state["conversation_session_documents"] = []
        st.error(f"❌ Failed to fetch documents: {e}")

# ------------------ Main Chat Page ------------------ #
def show_chat_interface():
    st.title("💬 Ask Promptly")

    # Sidebar: logout
    with st.sidebar:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    # Back button
    if st.button("← Back to Dashboard"):
        del st.session_state["conversation_session_data"]
        del st.session_state["conversation_session_id"]
        st.rerun()

    # Always fetch current docs
    with st.spinner("📥 Loading documents..."):
        fetch_conversation_session_documents()

    # Load chat history (persisted)
    if "conversations" not in st.session_state or not st.session_state["conversations"]:
        st.session_state["conversations"] = fetch_chat_history(st.session_state["conversation_session_id"])

    # Session title
    st.subheader(f"🗂️ {st.session_state['conversation_session_data']['title']}")

    # Show uploaded document list
    with st.sidebar.expander("📚 Uploaded Documents", expanded=True):
        for i, doc in enumerate(st.session_state.get("conversation_session_documents", [])):
            st.markdown(f"**{i+1}.** {doc['location']}")

    # Render conversation
    for msg in st.session_state["conversations"]:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

        if msg["role"] == "assistant" and msg.get("references"):
            st.chat_message("assistant", avatar="🤖").markdown("#### 📎 Referenced Document Sections")
            for ref in msg["references"]:
                with st.chat_message("assistant", avatar="🤖"):
                    with st.expander(f"📄 `{ref.get('document_title', 'Unknown Document')}` — Section {ref.get('section_order', '?')}"):
                        chunk_text = ref.get('chunk_content', '').replace('\n', ' ')[:800]
                        st.markdown(
                            f"<span style='font-size: 13px; line-height: 1.5;'>{chunk_text}...</span>",
                            unsafe_allow_html=True
                        )

    # Handle new user query
    if query := st.chat_input("Ask a question about your documents..."):
        st.chat_message("user", avatar="👤").write(query)
        st.session_state["conversations"].append({"role": "user", "content": query})

        with st.spinner("🔎 Generating response..."):
            try:
                res = requests.post(INFERENCE_API_URL, json={
                    "query": query,
                    "conversation_session_id": st.session_state["conversation_session_id"]
                }, timeout=120)
                res.raise_for_status()
                answer = res.json().get("answer", "No response received.")
                references = res.json().get("references", [])

                # Render assistant response
                st.chat_message("assistant", avatar="🤖").write(answer)

                if references:
                    st.chat_message("assistant", avatar="🤖").markdown("#### 📎 Referenced Document Sections")
                    for ref in references:
                        with st.chat_message("assistant", avatar="🤖"):
                            with st.expander(f"📄 `{ref.get('document_title', 'Unknown Document')}` — Section {ref.get('section_order', '?')}"):
                                chunk_text = ref.get('chunk_content', '').replace('\n', ' ')[:800]
                                st.markdown(
                                    f"<span style='font-size: 13px; line-height: 1.5;'>{chunk_text}...</span>",
                                    unsafe_allow_html=True
                                )

                # Store full message object with references
                st.session_state["conversations"].append({
                    "role": "assistant",
                    "content": answer,
                    "references": references
                })

                # Log to Supabase
                log_chat_to_supabase(
                    st.session_state["conversation_session_id"],
                    st.session_state["user"]["user_email_id"],
                    query,
                    answer
                )

            except Exception as e:
                st.error(f"❌ Query failed: {e}")
