import requests
import google.auth
import google.auth.transport.requests

# Replace these with your actual values
PROJECT_ID="45932739705"
REGION = "us-central1"
ENDPOINT_ID="2218045906224152576"

# Vertex AI REST endpoint URL
url = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict"

# Auth - get an access token
credentials, _ = google.auth.default()
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
access_token = credentials.token

# Sample payload — change this to match your model's input format
payload = {
    "instances": [
        {
            "prompt": "Write a short poem about the future of AI"
        }
    ]
}

# Set headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Make the request
response = requests.post(url, headers=headers, json=payload)

# Output the response
print("Status code:", response.status_code)
print("Response:")
print(response.json())