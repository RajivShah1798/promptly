from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from transformers import AutoTokenizer
from peft import PeftModel
from transformers import AutoModelForCausalLM
import logging
from fastapi.responses import PlainTextResponse
import os
from google.cloud import logging as cloud_logging
from google.cloud.logging.handlers import CloudLoggingHandler

app = FastAPI()
# Get log file path from environment variable
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
logging_client = cloud_logging.Client.from_service_account_json(credentials_path)

# Create a Cloud Logging handler and attach it to the root logger
cloud_handler = CloudLoggingHandler(logging_client, name='fastapi-logs')
cloud_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, handlers=[cloud_handler])


prompt = """
    You are an AI agent tasked with answering technical questions for IT Software systems. Your target audience will 
    generally be developers and engineers but occasionally technical managers so answer questions accordingly.

    You will generally be provided with some context elements and your priority will be to answer questions based on the context provided.
    You are to avoid negative or speculative responses, and prioritize factual information over assumption.

    Answer the question as comprehensively as possible.
    """
class TextRequest(BaseModel):
    query: str
    context: str

@app.on_event("startup")
async def load_model():
    global model, tokenizer
    logging.info("Load base model")
    base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    logging.info("Base model loaded successfully.")
    logging.info("Load the model")
    model = PeftModel.from_pretrained(base_model, "rajiv8197/promptly-tuned", use_safetensors = True)
    logging.info("Model loaded successfully.")
    logging.info("Loading tokenizer.")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    logging.info("Tokenizer loaded successfully.")

@app.post("/generate_response")
async def generate_summary(request: TextRequest):
    logging.info(f"Query: {request.query}")
    logging.info(f"Relevant Context chunks: {request.context}")
    try:
        # creating the full prompt for response generation
        input_text = prompt + "\n Context: " + request.context + "\n Query: " + request.query
        inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
        output = model.generate(**inputs, max_new_tokens=500)
        generated_sequence = output[0]
        input_length = inputs['input_ids'].shape[1]
        new_tokens = generated_sequence[input_length:]

        response = tokenizer.decode(new_tokens, skip_special_tokens=True)
        logging.info(f"Generated Response: {response}")
        return {"status":200, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def stream_logs(response: Response):
    try:
        log_entries = list(logging_client.list_entries())
        log_stream = '\n'.join([entry.payload for entry in log_entries])

        # Set content type and return streamed logs
        response.headers["Content-Type"] = "text/plain"
        return PlainTextResponse(log_stream)
    except Exception as e:
        logging.error(f"An error occurred while streaming logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not stream logs from Cloud Logging.")