import os
import subprocess
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
from supabase import create_client
from drift_detection import run_drift_detection
from bias_detection import check_user_dominance_bias_live

# === Load Env ===
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0")

# === Step 1: Classifier Retraining ===
def retrain_classifier():
    logging.info("📊 Starting SBERT + kNN retraining...")
    subprocess.run(["python", "model_pipeline/scripts/train_model.py"], check=True)
    logging.info("✅ Classifier retraining complete.")

# === Step 2: LLM Finetuning Trigger ===
def retrain_llm():
    logging.info("🧠 Triggering LLM finetuning via Kaggle CLI...")
    try:
        subprocess.run(["kaggle", "kernels", "push", "-p", "model_pipeline/training"], check=True)
        logging.info("✅ LLM retraining triggered successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.warning(f"⚠️ Failed to trigger LLM finetuning: {e}")
        return False

# === Step 3: Supabase Logging ===
def log_to_supabase(triggered_by, drift_detected, bias_blocked, classifier_retrained, llm_retrained=False):
    try:
        record = {
            "triggered_at": datetime.now(timezone.utc).isoformat(),
            "source": triggered_by,
            "drift_detected": drift_detected,
            "bias_blocked": bias_blocked,
            "classifier_retrained": classifier_retrained,
            "llm_retrained": llm_retrained,
            "rouge_metrics": {},  # Placeholder for future metrics
            "model_version": MODEL_VERSION
        }
        supabase.table("retraining_logs").insert(record).execute()
        logging.info("📦 Retraining run logged to Supabase.")
    except Exception as e:
        logging.warning(f"⚠️ Failed to log retraining: {e}")

# === Step 4: Full Pipeline ===
def run_pipeline(triggered_by="manual"):
    logging.info("🚀 Retraining Triggered (Drift + Bias + Logging)")

    drift = run_drift_detection()
    if not drift:
        logging.info("✅ No drift detected. Skipping retraining.")
        log_to_supabase(triggered_by, drift_detected=False, bias_blocked=False, classifier_retrained=False)
        return

    bias_ok = check_user_dominance_bias_live()
    if not bias_ok:
        logging.warning("🚫 Bias detected. Skipping retraining.")
        log_to_supabase(triggered_by, drift_detected=True, bias_blocked=True, classifier_retrained=False)
        return

    retrain_classifier()
    llm_success = retrain_llm()

    log_to_supabase(
        triggered_by=triggered_by,
        drift_detected=True,
        bias_blocked=False,
        classifier_retrained=True,
        llm_retrained=llm_success
    )

# === CLI Entrypoint ===
if __name__ == "__main__":
    run_pipeline()
