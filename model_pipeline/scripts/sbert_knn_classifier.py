import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import KNeighborsClassifier
import logging
import multiprocessing

# ✅ Fix: Set multiprocessing start method to "spawn" for CUDA compatibility
multiprocessing.set_start_method("spawn", force=True)

# Initialize logger
logging.basicConfig(level=logging.INFO)

# ✅ Fix: Move SBERT Model Initialization Outside Task Functions
device = "cuda" if torch.cuda.is_available() else "cpu"
sbert_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# ✅ Expanded labeled data for better classification
examples = [
    {"question": "What is FDA approval process?", "category": "Regulatory"},
    {"question": "How to classify a medical device?", "category": "Product Classification"},
    {"question": "How does post-market surveillance work?", "category": "Post-Market Monitoring"},
    {"question": "What are the steps for 510(k) submission?", "category": "Regulatory"},
    {"question": "When does a device require PMA approval?", "category": "Regulatory"},
    {"question": "What is the difference between Class I, II, and III devices?", "category": "Product Classification"},
    {"question": "What post-market monitoring steps are required?", "category": "Post-Market Monitoring"},
    {"question": "What documentation is needed for device registration?", "category": "Regulatory"},
    {"question": "How do I check if my product is a medical device?", "category": "Product Classification"},
    {"question": "What reporting obligations do manufacturers have?", "category": "Post-Market Monitoring"}
]

# ✅ Convert text to embeddings
X_train = np.array([sbert_model.encode(ex["question"]) for ex in examples])
y_train = np.array([ex["category"] for ex in examples])

# ✅ Train k-NN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=3)  # 🔹 Changed `n_neighbors=3` for better accuracy
knn_classifier.fit(X_train, y_train)

def classify_query(query):
    """
    Classify a query using SBERT embeddings and k-NN.
    """
    query_embedding = sbert_model.encode(query).reshape(1, -1)
    predicted_category = knn_classifier.predict(query_embedding)[0]
    return predicted_category

if __name__ == "__main__":
    test_queries = [
        "How does FDA approve medical devices?",
        "What are the clinical trial requirements?",
        "Explain post-market surveillance regulations.",
        "How to determine if a product is a medical device?"
    ]
    
    for query in test_queries:
        category = classify_query(query)
        print(f"Query: {query}\nPredicted Category: {category}\n")
