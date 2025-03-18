import os
import logging
import json
import pandas as pd
from huggingface_hub import InferenceClient
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from load_data import load_data

# Check environment
if not os.getenv("HUGGINGFACE_API_KEY"):
    raise EnvironmentError("❌ HUGGINGFACE_API_KEY environment variable not found. Please set it before running.")

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_DIR = os.path.join(BASE_DIR, "model/")
LLM_CONFIG_OUTPUT = os.path.join(MODEL_DIR, "llm_config.json")

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Fallback inference clients for stability and throughput
llm_clients = [
    InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=os.getenv("HUGGINGFACE_API_KEY")),
    InferenceClient(model="tiiuae/falcon-7b-instruct", token=os.getenv("HUGGINGFACE_API_KEY"))
]

logging.info(f"✅ Using fallback models in order: {[client.model for client in llm_clients]}")

# Load embeddings model once
logging.info("🔄 Loading Embeddings Model...")
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_store(df: pd.DataFrame):
    """Builds a FAISS vector store from document responses."""
    logging.info("🔄 Building FAISS Index...")
    if "response" not in df.columns:
        logging.error("❌ Column 'response' not found in dataframe! Check data preprocessing.")
        return None

    texts = df["response"].tolist()
    vector_store = FAISS.from_texts(texts, embeddings_model)
    vector_store.index.nprobe = 10  # Higher precision for search
    return vector_store

def classify_query(query: str, vector_store, max_retries=3, temperature=0.0, max_tokens=25):
    """Classifies a query into a category using retrieved context and fallback LLMs."""
    retrieved_docs = vector_store.similarity_search(query, k=3)
    context = "\n".join([getattr(doc, 'page_content', str(doc)) for doc in retrieved_docs])

    prompt = f"""
    Given the following document excerpts:
    {context}

    Classify the following query into a relevant category:
    Query: {query}

    Provide only the category as the response.

    Category:
    """

    for attempt in range(max_retries):
        for client in llm_clients:
            try:
                response = client.chat_completion(
                    messages=[
                        {"role": "system", "content": "You are an AI assistant that returns only concise category names."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                predicted_category = response.choices[0].message.content.strip().split("Category:")[-1].strip()
                return predicted_category
            except Exception as e:
                logging.error(f"❌ Error with model {client.model}: {e}")
                continue
        logging.info(f"⚠️ Retrying attempt ({attempt + 1}/{max_retries})...")

    return "Error: All LLM calls failed"

def main():
    """Main routine for running LLM-based classification with document retrieval."""
    logging.info("🔄 Loading training data...")
    _, _, df_docs = load_data()
    logging.info(f"✅ Sample data preview:\n{df_docs.head()}")

    if "response" not in df_docs.columns:
        logging.error("❌ Column 'response' not found in dataframe! Check data preprocessing.")
        return

    vector_store = build_vector_store(df_docs)
    if vector_store is None:
        return

    test_queries = [
        "How does FDA regulate medical devices?",
        "What are the clinical trial requirements?"
    ]

    results = []
    for query in test_queries:
        category = classify_query(query, vector_store)
        results.append((query, category))
        logging.info(f"✅ Query: {query} -> Predicted Category: {category}")

    # Save model config (not the client itself)
    llm_config = {"primary_model": llm_clients[0].model}
    with open(LLM_CONFIG_OUTPUT, "w") as f:
        json.dump(llm_config, f)
    logging.info(f"✅ LLM model config saved at {LLM_CONFIG_OUTPUT}")

if __name__ == "__main__":
    main()
