import os
import logging
from huggingface_hub import InferenceClient
from supabase import create_client
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import nomic
from nomic import embed
import sys
from dotenv import load_dotenv
from typing import List

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import config

# ✅ Environment Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not HUGGINGFACE_API_KEY:
    raise EnvironmentError("❌ SUPABASE_URL, SUPABASE_KEY, or HUGGINGFACE_API_KEY not set.")

# ✅ Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Load embeddings model
logging.info("🔄 Loading HuggingFace Embeddings Model...")
nomic.login(token=config.NOMIC_API_KEY)

# ✅ Setup fallback LLM inference clients
llm_clients = [
    InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HUGGINGFACE_API_KEY),
    # InferenceClient(model="tiiuae/falcon-7b-instruct", token=HUGGINGFACE_API_KEY),
    # InferenceClient(model="google/gemma-7b-it", token=HUGGINGFACE_API_KEY)
]
logging.info(f"✅ LLM fallback models configured: {[client.model for client in llm_clients]}")

# ✅ Answer synthesis from retrieved chunks
def synthesize_answer(query: str, retrieved_context: list, max_tokens=200, max_retries=3):
    formatted_context = "\n".join([
        f"Section {chunk['section_order']} from Document ID {chunk['document_id']}:\n{chunk['chunk_content']}"
        for chunk in retrieved_context
    ])

    prompt = f"""
    Given the following document excerpts:
    {formatted_context}

    Please answer the following question:
    Query: {query}

    Provide a clear, concise, and factual answer.

    Answer:
    """

    for attempt in range(max_retries):
        for client in llm_clients:
            try:
                response = client.chat_completion(
                    messages=[
                        {"role": "system", "content": "You are an AI assistant providing answers from provided documentation."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logging.error(f"❌ Error with model {client.model}: {e}")
                continue

    return "Could not generate an answer at this time."

def fetch_top_k_chunks(query_embedding: list, conversation_session_id: str, top_k: int = 5):
    print("============= Query Response ==============")
    print("conversation_session_id", conversation_session_id, type(conversation_session_id))
    response = supabase.rpc('fetch_top_k_chunks', {
        'match_threshold': 0.6,
        'query_embedding': query_embedding,
        'top_k': top_k,
        'conversation_session_id': conversation_session_id
    }).execute()
    # print(response)
    return response.data
# print(sign_in_user("wrong", "wrong"))
# ✅ FastAPI Setup
app = FastAPI()

class QueryInput(BaseModel):
    query: str
    conversation_session_id: str
@app.post("/ask")
def ask_query(input_data: QueryInput):
    query = input_data.query
    print("Reached here")
    query_embedding_response = embed.text(
        texts=[query],
        model=config.MODEL_NAME,
        task_type=config.TASK_TYPE,
    )
    # print(type(query_embedding_response))
    query_embedding = query_embedding_response["embeddings"][0]
    # Retrieve relevant chunks
    print("Reached here too")
    relevant_chunks = fetch_top_k_chunks(query_embedding, input_data.conversation_session_id, 3)
    if not relevant_chunks:
        return {"query": query, "answer": "No relevant information found.", "references": []}

    # Synthesize LLM answer
    answer = synthesize_answer(query, relevant_chunks)

    return {
        "query": query,
        "answer": answer,
        "references": relevant_chunks,
        "confidence": "High" if answer else "Low"
    }

class QueryInput(BaseModel):
    query: str
@app.post("/signup")
def sign_up_user(first_name: str, last_name: str, org_id: str, email_id: str, password: str):
    response = supabase.rpc('sign_up_user', {
        'first_name': first_name,
        'last_name': last_name,
        'org_id': org_id,
        'email_id': email_id,
        'password': password
    }).execute()
    print("========================SignUp===========================")
    print(response)
    return response.data

class LoginInput(BaseModel):
    email_id: str
    password: str

@app.post("/login")
def sign_in_user(user_details: LoginInput):
    # print("========================Login===========================")
    response = supabase.rpc('sign_in_user', {
        'email_id': user_details.email_id,
        'password': user_details.password
    }).execute()
    # print(response)
    return response.data

class ConversationSessionGetInput(BaseModel):
    email_id: str

@app.get("/user_conversation_session")
def get_user_conversation_session(user_details: ConversationSessionGetInput):
    # print("========================Login===========================")
    response = supabase.rpc('fetch_conversation_sessions', {
        'p_user_email_id': user_details.email_id
    }).execute()
    # print(response)
    return response.data

class ConversationSessionCreateInput(BaseModel):
    email_id: str
    title:str
    description: str
@app.post("/user_conversation_session")
def create_user_conversation_session(conv_session_details: ConversationSessionCreateInput):
    # print("========================Creating User Conv Session===========================")
    response = supabase.rpc('create_conversation_session', {
        'user_email_id': conv_session_details.email_id,
        'title': conv_session_details.title,
        'description': conv_session_details.description
    }).execute()
    # print(response)
    return response.data

class ConversationSessionDocumentsInput(BaseModel):
    conversation_session_id: str
@app.get("/conversation_session_documents")
def fetch_conversation_session_documents(conv_session_details: ConversationSessionDocumentsInput):
    print("========================Get Conversation Session Documents===========================")
    response = supabase.rpc('fetch_conv_session_documents', {
        'p_conversation_session_id': conv_session_details.conversation_session_id
    }).execute()
    print(response)
    return response.data


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
