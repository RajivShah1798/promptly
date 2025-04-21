from supabase import create_client, Client
from typing import List, Dict
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

SUPABASE_URL = "https://eoukhlpitglbkhxtjuvh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvdWtobHBpdGdsYmtoeHRqdXZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAwNzQ3NTcsImV4cCI6MjA1NTY1MDc1N30.d2cCXyLTLUIevdhqEEt7uNiwZvBUx44n4cu-ItWqpKU"
FINETUNING_DATA_JSON_FP = './finetuning_03212025.json'
os.environ["NOMIC_API_KEY"] = "nk-QyapgWDalVQaJy2UsfDqX7Qz_6CHrb28OmsPW2Kuj1Q"

"""
Format for JSON:

{
    "query": "How to do task X using Y and Z?",
    "context": ["context1", "context2"],
    "response": "sample response"
}
"""

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_conversation_data(supabase: Client) -> List[Dict]:
    try:
        response = (
            supabase.table("conversations")
            .select("query, response, conversation_document_chunks(document_chunks(chunk_content))")
            .execute()
        )

        result = []
        for conversation in response.data:
            conversation_data = {
                "query": conversation["query"],
                "response": conversation["response"],
                "context": []
            }

            # Extract chunk_content from related document_chunks
            for cdc in conversation["conversation_document_chunks"]:
                if "document_chunks" in cdc and cdc["document_chunks"]:
                    conversation_data["context"].append(cdc["document_chunks"]["chunk_content"])

            result.append(conversation_data)

        return result

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

data_for_finetuning = fetch_conversation_data(supabase)
training_data = data_for_finetuning[:60]
test_data = data_for_finetuning[-9:]


model_name = "Qwen/Qwen2.5-1.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)