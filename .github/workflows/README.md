# Run Kaggle Notebook with GitHub Actions

This repository contains a GitHub Actions workflow to automate the execution of a Kaggle notebook whenever changes are pushed to the `model-training` branch.

## 📌 Workflow Overview

This workflow:
1. **Checks out the repository** to access the required notebook file.
2. **Configures the Kaggle API** using stored secrets.
3. **Installs the Kaggle CLI** for interaction with Kaggle.
4. **Validates the Kaggle API key** to ensure authentication is set up correctly.
5. **Pushes the notebook to Kaggle** and triggers execution.
6. **Monitors the notebook status** and waits for the training to complete.

## 🚀 How to Use

### 1️⃣ Set Up Secrets
Before running this workflow, add the following secrets to your GitHub repository:
- `KAGGLE_USERNAME`: Your Kaggle username.
- `KAGGLE_KEY`: Your Kaggle API key (found in [Kaggle API settings](https://www.kaggle.com/account)).

### 2️⃣ Workflow Trigger
This workflow automatically runs when you push changes to the `model-training` branch.

Alternatively, you can manually trigger it in the **GitHub Actions** tab.

### 3️⃣ Workflow Execution
When triggered, the workflow:
- Uploads the notebook `model_pipeline/training/promptly-finetuning.ipynb` to Kaggle.
- Configures Kaggle metadata for execution.
- Pushes and runs the notebook on Kaggle with GPU enabled.
- Waits for the training process to complete.

### 4️⃣ Monitor Execution Status
You can monitor the status in the **GitHub Actions logs** or directly in Kaggle:

```sh
kaggle kernels status rajivshah8197/promptly-finetuning
```

## 🛠️ Troubleshooting

### ❌ Error: "Failed to fetch status. Check notebook slug."
- Ensure the notebook exists in your Kaggle account.
- Verify that the `NOTEBOOK_SLUG` is correct.

### ❌ Error: "Kaggle API key is missing!"
- Make sure the `KAGGLE_USERNAME` and `KAGGLE_KEY` secrets are properly set.

### ❌ Notebook execution failed
- Check the logs in the **GitHub Actions** tab.
- View the Kaggle notebook logs for more details.

## 📌 Notes
- The notebook runs with **GPU enabled**.
- The workflow automatically retries every 60 seconds until execution is complete.
- You can modify `kernel-metadata.json` to update Kaggle notebook settings.

---

💡 **Need help?** Open an issue or check the Kaggle API documentation:  
🔗 [Kaggle API Docs](https://www.kaggle.com/docs/api)
