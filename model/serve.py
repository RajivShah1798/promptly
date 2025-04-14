from fastapi import FastAPI, Request
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# ----------------------------
# Load tokenizer and base model
# ----------------------------
base_model_id = "Qwen/Qwen2.5-0.5B-Instruct"
lora_model_id = "RevLash/promptly-tuned"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(base_model_id, trust_remote_code=True)
model = PeftModel.from_pretrained(base_model, lora_model_id)
model.eval().to(device)

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9

@app.get("/v1/endpoints/{endpoint_id}/deployedModels/{model_id}")
def health_check(endpoint_id: str, model_id: str):
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Vertex AI-compatible route
@app.post("/v1/projects/{project}/locations/{region}/endpoints/{endpoint}:predict")
async def vertex_predict(project: str, region: str, endpoint: str, request: Request):
    payload = await request.json()
    
    # Assume first item in "instances" list matches PromptRequest format
    instance = payload["instances"][0]
    prompt_request = PromptRequest(**instance)

    inputs = tokenizer(prompt_request.prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=prompt_request.max_new_tokens,
            temperature=prompt_request.temperature,
            top_p=prompt_request.top_p,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"predictions": [response]}


@app.post("/predict")
async def predict(request: Request):
    payload = await request.json()
    
    # Handle both single-instance and batch requests
    instances = payload.get("instances", [])
    if not instances:
        return {"error": "No instances provided in request"}
    
    instance = instances[0]
    prompt_request = PromptRequest(**instance)
    results = []

    # Access attributes directly, not with .get()
    prompt = prompt_request.prompt
    max_new_tokens = prompt_request.max_new_tokens
    temperature = prompt_request.temperature
    top_p = prompt_request.top_p
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    results.append(response)
    
    return {"predictions": results}