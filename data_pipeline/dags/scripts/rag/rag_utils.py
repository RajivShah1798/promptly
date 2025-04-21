import os
import logging
import pymupdf4llm
from datetime import datetime
import nomic
from nomic import embed
from supabase import create_client
from semantic_text_splitter import MarkdownSplitter
from tokenizers import Tokenizer
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
import config

logging.basicConfig(level=logging.INFO)

# Initialize Supabase client
supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

# Load tokenizer
tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
markdown_splitter = MarkdownSplitter.from_huggingface_tokenizer(tokenizer, config.MAX_TOKENS)

def get_documents_from_folder(folder_path):
    """
    Retrieves all PDF and TXT files from the specified folder.
    """
    document_paths = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf") or file.endswith(".txt"):
            document_paths.append(os.path.join(folder_path, file))
    
    logging.info(f"Found {len(document_paths)} documents in {folder_path}.")
    return document_paths  # Returns a list of file paths

def read_document(document_paths):
    """
    Reads the content of each document (PDF or TXT) and returns a dictionary with filenames as keys.
    """
    document_contents = {}

    for path in document_paths:
        filename = os.path.basename(path)

        if path.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as file:
                document_contents[filename] = file.read()
        elif path.endswith(".pdf"):
            document_contents[filename] = pymupdf4llm.to_markdown(path)  # Extract text from PDF
            
    logging.info(f"Read {len(document_contents)} documents.")
    return document_contents  # Returns a dictionary {filename: text_content}


def chunk_text(document_contents):
    """
    Splits text into chunks using MarkdownSplitter.

    Args:
        document_contents (list of dict): Each dictionary contains {filename: redacted_text}.

    Returns:
        dict: {filename: list of chunks} for each document.
    """
    chunked_data = {}

    for doc in document_contents:
        for filename, text in doc.items():
            chunks = markdown_splitter.chunks(text)
            chunked_data[filename] = chunks  # Store chunks per document

    logging.info(f"Chunked {len(document_contents)} documents into {sum(len(chunks) for chunks in chunked_data.values())} chunks.")
    return chunked_data


def embed_and_store_chunks(chunked_data):
    """
    Generates embeddings for document chunks and stores them in Supabase.
    """
    nomic.login(token=config.NOMIC_API_KEY)
 
    chunks_store = []
 
    for filename, chunks in chunked_data.items():
        try:
            output = embed.text(
                texts=chunks,
                model=config.MODEL_NAME,
                task_type=config.TASK_TYPE,
            )
 
            embeddings = output.get("embeddings")
        except Exception as e:
            logging.error(f"Error while embedding chunks: {e}")
            continue
 
        # Prepare document metadata
        document_data = {
            "location": filename,
            "is_private": config.IS_PRIVATE,
            "org_id": config.ORG_ID,
            "content": "\n".join(chunks),
            "upload_user_id": config.UPLOAD_USER_ID,
            "upload_time": datetime.now().isoformat(),
            "conversation_session_id": None
        }
 
        response = supabase.table(config.DOCUMENT_TABLE).insert(document_data).execute()
        if response.data:
            document_id = response.data[0]["id"]
 
            # Insert chunk embeddings
            chunk_data = [
                {
                    "document_id": document_id,
                    "chunk_content": chunk,
                    "embedding": embeddings[idx],
                    "section_order": idx,
                    "created_at": datetime.now().isoformat(),
                }
                for idx, chunk in enumerate(chunks)
            ]
 
            chunk_response = supabase.table(config.CHUNKS_TABLE).insert(chunk_data).execute()
            if chunk_response.data:
                chunks_store.append(chunk_response.data)
                logging.info(f"Inserted document {filename} and its chunks into Supabase.")
            else:
                logging.error(f"Error inserting chunks for {filename}: {chunk_response}")
        else:
            logging.error(f"Error inserting document {filename}: {response}")
 
    return chunks_store