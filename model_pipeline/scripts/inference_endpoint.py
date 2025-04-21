import os
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
import google.auth.transport.requests

class VertexAIPredictor:
    def __init__(self):
        load_dotenv()

        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.project_id = os.getenv("PROJECT_ID", "45932739705")
        self.region = os.getenv("REGION", "us-central1")
        self.endpoint_id = os.getenv("ENDPOINT_ID", "8636519800157241344")

        self.scopes = ["https://www.googleapis.com/auth/cloud-platform"]

        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path, scopes=self.scopes
        )

        self._refresh_token()

        self.url = f"https://{self.region}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.region}/endpoints/{self.endpoint_id}:predict"

    def _refresh_token(self):
        auth_req = google.auth.transport.requests.Request()
        self.credentials.refresh(auth_req)
        self.access_token = self.credentials.token

    def predict(self, prompt: str):
        self._refresh_token()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "instances": [
                {"prompt": prompt}
            ]
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Prediction failed: {response.status_code} - {response.text}")
