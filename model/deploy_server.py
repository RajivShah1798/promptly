from google.cloud import aiplatform

aiplatform.init(project="adroit-chemist-450622-c4", location="us-central1")

model = aiplatform.Model.upload(
    display_name="promptly-finetuned-qwen-model",
    serving_container_image_uri="us-central1-docker.pkg.dev/adroit-chemist-450622-c4/trained-model/promptly-tuned:latest",
    labels={"type": "qwen"},
)

# endpoint = model.deploy(
#     machine_type="n1-standard-8"
# )