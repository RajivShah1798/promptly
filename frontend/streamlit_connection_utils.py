import os
import logging
import pymupdf4llm
from datetime import datetime
import nomic
from nomic import embed
from supabase import create_client
from semantic_text_splitter import MarkdownSplitter
from tokenizers import Tokenizer
from io import StringIO
from typing import List
import tempfile
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config

logging.basicConfig(level=logging.INFO)

# Initialize Supabase client
supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

# Load tokenizer
tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
markdown_splitter = MarkdownSplitter.from_huggingface_tokenizer(tokenizer, config.MAX_TOKENS)

def read_document(uploaded_files: List):
    """
    Reads the content of each uploaded file (PDF or TXT) and returns a dictionary with filenames as keys.
    """
    document_contents = []

    for uploaded_file in uploaded_files:
        filename = uploaded_file.name

        if filename.endswith(".txt"):
            # Read text content from file-like object
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            # document_contents[filename] = stringio.read()
            document_contents.append({
                filename: stringio.read()
            })
        
        elif filename.endswith(".pdf"):
            # Write to a temporary file since pymupdf expects a path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # document_contents[filename] = pymupdf4llm.to_markdown(tmp_path)
            document_contents.append({
                filename: pymupdf4llm.to_markdown(tmp_path)
            })
            os.remove(tmp_path)

    logging.info(f"Read {len(document_contents)} documents.")
    return document_contents


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


def embed_and_store_chunks(chunked_data, is_private, org_id, user_email_id, conversation_session_id):
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
            "is_private": is_private,
            "org_id": org_id,
            "content": "\n".join(chunks),
            "upload_user_id": user_email_id,
            "upload_time": datetime.now().isoformat(),
            "conversation_session_id": conversation_session_id
        }

        response = supabase.table(config.DOCUMENT_TABLE).insert(document_data).execute()
        if response.data:
            document_id = response.data[0]["id"]

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
