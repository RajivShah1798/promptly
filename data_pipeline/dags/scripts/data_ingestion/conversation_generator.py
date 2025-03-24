import yaml
from jinja2 import Template
from huggingface_hub import InferenceClient
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import config
import logging
from supabase import create_client

logging.basicConfig(level=logging.INFO)

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def get_conversation_api(prompt):
    try:
        logging.info("Sending prompt to conversation API.")
        client = InferenceClient(
            provider= config.CONVERSATION_MODEL_PROVIDER,
            api_key= config.HUGGING_FACE_API_KEY,
        )

        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages= prompt,
            max_tokens=1000,
        )
        logging.info("Received response from conversation API.")
        return completion.choices[0].message
    except Exception as e:
        logging.error(f"Error calling conversation API: {e}")
        return json.dumps({"conversations": []})

def getPrompt(prompt_location, **kwargs):
    try:
        prompt_list = []
        with open (prompt_location, "r") as f:
            prompt:dict = yaml.safe_load(f)
            # print(prompt)
            prompt_list = prompt["prompt"]

        formatted_prompt = [
            {k: Template(v).render(**kwargs) if isinstance(v, str) else v for k, v in entry.items()}
            for entry in prompt_list
        ]
        return formatted_prompt
    except Exception as e:
        logging.error(f"Error loading or formatting prompt: {e}")
        return []

def fetch_document_chunks(batch_size=config.DOCUMENT_CHUNK_SIZE, limit=config.DOCUMENT_CHUNK_LIMIT):
    try:
        response = supabase.table("document_chunks") \
                        .select("id, chunk_content") \
                        .order("id") \
                        .limit(limit) \
                        .execute()

        all_chunks = response.data

        logging.info(f"Fetched {len(all_chunks)} document chunks.")

        for i in range(0, len(all_chunks), batch_size):
            yield all_chunks[i:i + batch_size]
    except Exception as e:
        logging.error(f"Error fetching document chunks: {e}")
        yield []

def process_batches():
    data = {"conversations": []}

    for batch in fetch_document_chunks():
        if not batch:
            logging.warning("No document chunks to process in batch.")
            continue
        
        logging.info(f"Processing batch of size {len(batch)}.")
        try:
            formatted_chunks = [
                {"document_chunk_text": chunk["chunk_content"], "document_chunk_id": chunk["id"]}
                for chunk in batch
            ]

            documents_chunks_json = json.dumps(formatted_chunks, indent=4)
            # with open("document_chunks.txt", "w") as file:
            #     file.write(documents_chunks_json)
            prompt = getPrompt("config/prompts/conversation_generator.yaml", 
                            documents_chunks=documents_chunks_json)

            conversation_response = get_conversation_api(prompt)
            conversation_data = json.loads(conversation_response)
            logging.info(f"Received {len(conversation_data.get('conversations', []))} conversations.")
            # Append new conversations to the data dictionary
            data["conversations"].extend(conversation_data.get("conversations", []))
        except Exception as e:
            logging.error(f"Error processing batch: {e}")

        ## Uncomment this
        upload_conversations(data)

def upload_conversations(data):
    # with open('data/rag_documents/conversations.json', 'r') as file:
    #     data = json.load(file)
    logging.info(f"Received total {len(data.get('conversations', []))} conversations for upload.")
    for conversation in data["conversations"]:
        query = conversation["query"]
        response = conversation["response"]
        document_chunk_ids = conversation["extracted_from_document_chunk_ids"]

        conversation_data = {
            "query": query,
            "response": response,
            "is_private": False,
            "is_disliked": False,
            "fallback_model": None,
            "user_id": 1 
        }
        
        conversation_result = supabase.table("conversations").insert(conversation_data).execute()
        conversation_id = conversation_result.data[0]['id']

        chunk_records = [
            {"conversation_id": conversation_id, "document_chunk_id": chunk_id}
            for chunk_id in document_chunk_ids
        ]
        if chunk_records:
            supabase.table("conversation_document_chunks").insert(chunk_records).execute()

    logging.info("Data successfully inserted!")

# Run the batch processing
process_batches()
