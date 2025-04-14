from google.cloud import aiplatform_v1

from google.cloud import aiplatform

PROJECT_ID="45932739705"
REGION = "us-central1"
ENDPOINT_ID="1552920536256872448"

aiplatform.init(project=PROJECT_ID, location="us-central1")

endpoints = aiplatform.Endpoint.list()
for ep in endpoints:
    print(f"Name: {ep.display_name}, ID: {ep.resource_name}")

endpoint = aiplatform.Endpoint(
    endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
)

response = endpoint.predict(instances=[{"prompt": "Tell me a joke about AI"}])

# client = aiplatform_v1.PredictionServiceClient()

# endpoint = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"

# response = client.predict(
#     endpoint=endpoint,
#     instances=[{"prompt": "Tell me a joke about AI"}],
#     parameters={},  # Optional, based on your model
# )

# print(response.predictions)