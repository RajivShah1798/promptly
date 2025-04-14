from google.cloud import aiplatform_v1

from google.cloud import aiplatform

PROJECT_ID="45932739705"
REGION = "us-central1"
ENDPOINT_ID="2218045906224152576"

aiplatform.init(project=PROJECT_ID, location="us-central1")

endpoint = aiplatform.Endpoint(
    endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
)

response = endpoint.predict([{"prompt": "Tell me a joke about AI"}])

# client = aiplatform_v1.PredictionServiceClient()

# endpoint = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"

# response = client.predict(
#     endpoint=endpoint,
#     instances=[{"prompt": "Tell me a joke about AI"}],
#     parameters={},  # Optional, based on your model
# )

print(response.predictions)