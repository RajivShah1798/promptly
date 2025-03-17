import os
from airflow.models import DagBag

# Define additional DAG directories
extra_dag_dirs = [
    "/home/kushal/model_dev_promptly/promptly/model_pipeline/dags"
]

print("🔍 Checking extra DAG directories...")

for dag_dir in extra_dag_dirs:
    if os.path.exists(dag_dir) and os.path.isdir(dag_dir):
        print(f"🔄 Scanning DAG directory: {dag_dir}")

        # Prevent Recursive Loop
        if dag_dir.endswith('__pycache__') or '.airflowignore' in dag_dir:
            print(f"⚠ Skipping ignored directory: {dag_dir}")
            continue  

        print(f"✅ Loading DAGs from: {dag_dir}")
        dag_bag = DagBag(dag_dir, include_examples=False)

        if not dag_bag.dags:
            print(f"⚠ No DAGs found in: {dag_dir}")

        for dag_id, dag in dag_bag.dags.items():
            globals()[dag_id] = dag
            print(f"✅ Loaded DAG: {dag_id}")

print("✅ Successfully loaded additional DAGs from model_pipeline!")
