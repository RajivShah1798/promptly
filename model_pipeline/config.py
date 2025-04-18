import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# API Keys
NOMIC_API_KEY = os.getenv("NOMIC_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# Default Settings
MAX_TOKENS = 500
MODEL_NAME = "nomic-embed-text-v1.5"
TASK_TYPE = "search_query"

# Database Tables
DOCUMENT_TABLE = "documents"
CHUNKS_TABLE = "document_chunks"

# Test data configurations - organization and test user id
IS_PRIVATE = False
ORG_ID = 1
UPLOAD_USER_ID = 1
UPLOAD_TIME = datetime.now().isoformat()

# RAG Documents Directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
DATA_FOLDER = base_dir+"/data/rag_documents"

# Model provider for conversation generation
CONVERSATION_MODEL_PROVIDER = "fireworks-ai"

# conversations documents chunks batch size and limits
DOCUMENT_CHUNK_SIZE = 50
DOCUMENT_CHUNK_LIMIT = 100