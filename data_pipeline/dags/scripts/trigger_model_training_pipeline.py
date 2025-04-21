import requests
import os
import config

def trigger_model_training(prefil_input):
    github_token = config.GITHUB_TOKEN
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set.")

    repo_owner = "RajivShah1798"
    repo_name = "promptly"
    workflow_filename = "train-model.yaml"
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_filename}/dispatches"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "ref": "main"
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"GitHub notification status: {response.status_code}")
    print(f"Response: {response.text}")
