import os
from dotenv import load_dotenv
import requests
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Define the required scopes
scopes = ["https://www.googleapis.com/auth/cloud-platform"]

# Create credentials with scopes
credentials = service_account.Credentials.from_service_account_file(
    credentials_path, scopes=scopes
)

# Refresh to get access token
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
access_token = credentials.token

# Replace these with your actual values
PROJECT_ID="45932739705"
REGION = "us-central1"
ENDPOINT_ID="8636519800157241344"

url = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}:predict"

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
