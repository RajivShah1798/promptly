import os
import logging
import pandas as pd
import numpy as np
from huggingface_hub import InferenceClient
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from supabase import create_client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse

# ✅ Environment Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not HUGGINGFACE_API_KEY:
    raise EnvironmentError("❌ SUPABASE_URL, SUPABASE_KEY, or HUGGINGFACE_API_KEY not set.")

# ✅ Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/inference_events.log", mode="a")
    ]
)


# ✅ Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Load Hugging Face embeddings model
logging.info("🔄 Loading HuggingFace Embeddings Model...")
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ✅ Function to pull document chunks from Supabase
def load_document_chunks_from_supabase():
    logging.info("🔄 Fetching document chunks from Supabase...")
    response = supabase.table("document_chunks").select("document_id, section_order, chunk_content").execute()
    if response.data is None or len(response.data) == 0:
        raise ValueError("❌ No document chunks found in Supabase.")
    df_chunks = pd.DataFrame(response.data)
    logging.info(f"✅ Retrieved {len(df_chunks)} chunks.")
    return df_chunks

# ✅ Build FAISS Vector Store
def build_vector_store(df_chunks: pd.DataFrame):
    logging.info("🔄 Building FAISS index from document chunks...")
    texts = df_chunks["chunk_content"].tolist()
    vector_store = FAISS.from_texts(texts, embeddings_model)
    vector_store.index.nprobe = 10
    return vector_store

# ✅ Load chunks & build vector store on startup
df_chunks = load_document_chunks_from_supabase()
vector_store = build_vector_store(df_chunks)

# ✅ Setup fallback LLM inference clients
llm_clients = [
    InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HUGGINGFACE_API_KEY),
    InferenceClient(model="tiiuae/falcon-7b-instruct", token=HUGGINGFACE_API_KEY),
    InferenceClient(model="google/gemma-7b-it", token=HUGGINGFACE_API_KEY)
]
logging.info(f"✅ LLM fallback models configured: {[client.model for client in llm_clients]}")

# ✅ Answer synthesis from retrieved chunks
def synthesize_answer(query: str, retrieved_context: list, max_tokens=200, max_retries=3):
    formatted_context = "\n".join([
        f"Section {chunk['section']} from Document ID {chunk['document']}:\n{chunk['excerpt']}"
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
                    temperature=0.2,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logging.error(f"❌ Error with model {client.model}: {e}")
                continue

    return "Could not generate an answer at this time."

# ✅ Retrieve top-k chunks and metadata
def retrieve_relevant_chunks(query_embedding, top_k=3):
    docs = vector_store.similarity_search_by_vector(query_embedding, k=top_k)
    references = []
    for doc in docs:
        result = supabase.table("document_chunks").select("document_id, section_order, chunk_content").eq("chunk_content", doc.page_content).execute()
        if result.data:
            metadata = result.data[0]
            references.append({
                "document": metadata["document_id"],
                "section": metadata["section_order"],
                "excerpt": metadata["chunk_content"][:500]  # limit excerpt length
            })
    return references

# ✅ FastAPI Setup
app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/ask")
def ask_query(input_data: QueryInput):
    query = input_data.query
    query_embedding = embeddings_model.embed_query(query)

    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    # Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(query_embedding, top_k=3)
    if not relevant_chunks:
        log_entry = {
            "request_id": request_id,
            "timestamp": timestamp,
            "query": query,
            "answer": None,
            "disliked": False,
            "fallback_model": "zephyr-7b-beta",
            "references": [],
            "status": "No context found"
        }
        logging.info(f"[PROMPTLY_LOG] {log_entry}")
        return {"query": query, "answer": "No relevant information found.", "references": []}

    # Synthesize answer
    answer = synthesize_answer(query, relevant_chunks)

    # ✅ STRUCTURED LOGGING ENTRY
    log_entry = {
        "request_id": request_id,
        "timestamp": timestamp,
        "query": query,
        "answer_snippet": answer[:100],
        "disliked": False,
        "fallback_model": "zephyr-7b-beta",
        "references": [
            {"document": ref["document"], "section": ref["section"]} for ref in relevant_chunks
        ],
        "status": "Success"
    }

    # ✅ LOG to console and file
    logging.info(f"[PROMPTLY_LOG] {log_entry}")

    # ✅ Optional: Supabase insert (append created_at once column is ready)
    supabase.table("conversations").insert({
    "query": query,
    "response": answer,
    "user_id": 1,
    "is_private": False,
    "is_disliked": False,
    "fallback_model": "zephyr-7b-beta",
    "created_at": timestamp  # ISO UTC string from earlier
}).execute()

    return {
        "query": query,
        "answer": answer,
        "references": relevant_chunks,
        "confidence": "High" if answer else "Low"
    }

class FeedbackInput(BaseModel):
    conversation_id: int
    is_disliked: bool

@app.post("/feedback")
def update_feedback(feedback: FeedbackInput):
    try:
        response = supabase.table("conversations").update({
            "is_disliked": feedback.is_disliked
        }).eq("id", feedback.conversation_id).execute()

        if len(response.data) == 0:
            raise ValueError("Conversation ID not found")

        logging.info(f"[PROMPTLY_FEEDBACK] Updated feedback for conversation ID {feedback.conversation_id} → Disliked = {feedback.is_disliked}")
        return JSONResponse(content={"message": "Feedback updated successfully"}, status_code=200)

    except Exception as e:
        logging.error(f"❌ Failed to update feedback: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
