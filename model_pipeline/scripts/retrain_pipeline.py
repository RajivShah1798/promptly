import os
import subprocess
import logging
from drift_detection import run_drift_detection

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def retrain_classifier():
    logging.info("📊 Starting SBERT + kNN retraining...")
    subprocess.run(["python", "model_pipeline/scripts/train_model.py"], check=True)
    logging.info("✅ Classifier retraining complete.")

def run_pipeline():
    logging.info("🚀 Lightweight Retraining Triggered")

    drift = run_drift_detection()
    if not drift:
        logging.info("✅ No drift detected. Skipping retraining.")
        return

    retrain_classifier()

if __name__ == "__main__":
    run_pipeline()
