# Model Directory

This directory contains all the necessary files and scripts for serving, testing, and deploying the machine learning model used in the `promptly` project. The model is fine-tuned for text generation tasks and is served using FastAPI.

## Directory Structure
```
/model
├── deploy_server.py   # Script to deploy the model to Google Cloud Vertex AI
├── Dockerfile         # Docker configuration for containerizing the model server
├── requirements.txt   # Python dependencies for the model
├── serve.py           # FastAPI server for serving the model
├── tests/             # Unit tests for the model and APIs
│   ├── api_test.py    # Test script for the REST API
│   └── sdk_test.py    # Test script for SDK integration
```

## Key Components

### 1. `serve.py`
- **Purpose**: Implements a FastAPI server to serve the model for inference.
- **Endpoints**:
  - `POST /predict`: Accepts a JSON payload with a prompt and returns generated text.
  - `GET /health`: Returns the health status of the server.
  - `GET /v1/endpoints/{endpoint_id}/deployedModels/{model_id}`: Endpoint for health checks with model and endpoint IDs.
- **Model Details**:
  - Base model: `Qwen/Qwen2.5-0.5B-Instruct`
  - Fine-tuned model: `RevLash/promptly-tuned`
  - Frameworks: PyTorch, Transformers, PEFT

### 2. `deploy_server.py`
- **Purpose**: Deploys the model to Google Cloud Vertex AI.
- **Key Features**:
  - Uploads the model to Vertex AI with a custom serving container.
  - Configures the serving container to use the `/predict` route for inference.

### 3. `Dockerfile`
- **Purpose**: Defines the Docker image for the model server.
- **Key Features**:
  - Uses a lightweight Python 3.10 base image.
  - Installs dependencies from `requirements.txt`.
  - Exposes port `8080` for the FastAPI server.

### 4. `requirements.txt`
- **Purpose**: Lists the Python dependencies required for the model server.
- **Dependencies**:
  - `torch`: PyTorch for model inference.
  - `transformers`: Hugging Face Transformers for tokenization and model loading.
  - `peft`: Parameter-efficient fine-tuning library.
  - `fastapi`: Web framework for serving the model.
  - `uvicorn`: ASGI server for running the FastAPI app.

### 5. `tests/`
- **Purpose**: Contains test scripts for validating the model and API functionality.
- **Files**:
  - `api_test.py`: Sends a sample request to the `/predict` endpoint and validates the response.
  - `sdk_test.py`: Placeholder for SDK integration tests.

## Usage

### Running the Model Server Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn serve:app --host 0.0.0.0 --port 8080
   ```
3. Test the server:
   - Health check: `GET http://localhost:8080/health`
   - Prediction: `POST http://localhost:8080/predict` with a JSON payload.

### Deploying the Model
1. Build the Docker image:
   ```bash
   docker build -t promptly-model-server .
   ```
2. Run the container:
   ```bash
   docker run -p 8080:8080 promptly-model-server
   ```
3. Deploy to Google Cloud Vertex AI using `deploy_server.py`.

### GitHub Actions for Build and Deployment

A GitHub Action workflow has been created to automate the build and deployment of the model to Google Cloud Vertex AI. This workflow is triggered upon the completion of model training and performs the following steps:

1. **Build the Docker Image**:
    - Packages the model server into a Docker container.

2. **Push to Container Registry**:
    - Uploads the Docker image to Google Container Registry (GCR).

3. **Deploy to Vertex AI**:
    - Uploads the latest promptly finetuned model from GCR to Vertex AI Model Registry.
    - Deploys the containerized model to Vertex AI for serving using endpoints.

### Testing the API
Run the test script:
```bash
python api_test.py
```

## Example Payload for `/predict`
```json
{
  "instances": [
    {
      "prompt": "Write a short poem about the future of AI",
      "max_new_tokens": 128,
      "temperature": 0.7,
      "top_p": 0.9
    }
  ]
}
```

## Notes
- Ensure that the model artifacts are properly loaded in `serve.py` before running the server.
- Update the `deploy_server.py` script with your Google Cloud project details before deploying.

## Contact
For any issues or questions, please contact the member of the team ~ Ronak(ronak.vadhaiya@somaiya.edu).
```