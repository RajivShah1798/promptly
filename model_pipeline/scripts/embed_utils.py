import os
import sys
import logging
import nomic
from nomic import embed

# ✅ Ensure correct path for config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data_pipeline")))

import config  # Import after setting the correct path

# Initialize logging
logging.basicConfig(level=logging.INFO)

def generate_nomic_embeddings(text_list):
    """
    Generate embeddings using Nomic API.

    Args:
        text_list (list of str): List of input text strings.

    Returns:
        list: List of embeddings for each input text.
    """
    logging.info("🔄 Generating embeddings using Nomic...")

    try:
        # ✅ Ensure authentication is done inside the function (for Airflow task safety)
        nomic.login(token=config.NOMIC_API_KEY)

        # ✅ Corrected API Call (Direct List)
        output = embed.text(
            texts=text_list,  # ✅ Ensure the argument matches Nomic's API
            model=config.MODEL_NAME,
            task_type=config.TASK_TYPE
        )

        embeddings = output.get("embeddings")

        if not embeddings:
            raise ValueError("❌ No embeddings were generated!")

        logging.info(f"✅ Successfully generated {len(embeddings)} embeddings.")
        return embeddings

    except Exception as e:
        logging.error(f"❌ Embedding generation failed: {e}")
        raise RuntimeError("Embedding generation failed.") from e

# ✅ Run test case when executed directly
if __name__ == "__main__":
    sample_texts = ["What is Promptly?", "Explain Apache Airflow."]
    embeddings = generate_nomic_embeddings(sample_texts)
    print("Sample Embeddings:", embeddings)
