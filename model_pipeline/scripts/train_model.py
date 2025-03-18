import os
import logging
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from collections import Counter
from load_data import load_data  # Ensure correct data loading

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_DIR = os.path.join(BASE_DIR, "model/")
MODEL_OUTPUT = os.path.join(MODEL_DIR, "best_model.pkl")

# Logging
logging.basicConfig(level=logging.INFO)

def train_model():
    """
    Train a classification model using Leave-One-Out Cross-Validation.
    Avoids train-test split failures for extremely small datasets.
    """
    logging.info("🔄 Loading training data...")
    X, y = load_data()  # Ensure embeddings are properly loaded

    # Check dataset size
    if len(y) < 10:
        logging.warning("⚠️ Warning: Dataset is extremely small. Consider adding more samples.")

    # Encode categorical labels into numerical values
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Count class distribution
    class_counts = Counter(y)
    logging.info(f"📊 Class distribution before grouping: {class_counts}")

    # Ensure we have at least 2 unique classes
    unique_classes = np.unique(y)
    if len(unique_classes) < 2:
        logging.error("❌ Only one class left. Cannot train a classifier.")
        logging.info("⚠️ Using DummyClassifier")
        model = DummyClassifier(strategy="most_frequent")
        model.fit(X, y)

        # Save fallback model
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)

        joblib.dump(model, MODEL_OUTPUT)
        logging.info(f"✅ Dummy model saved at {MODEL_OUTPUT}")
        return

    # Use Leave-One-Out Cross-Validation
    loo = LeaveOneOut()

    # Define models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, solver="liblinear"),
        "SVM": SVC(),
        "k-NN": KNeighborsClassifier(n_neighbors=3)
    }

    best_model = None
    best_accuracy = 0

    for name, model in models.items():
        accuracies = []
        logging.info(f"🚀 Training {name} using Leave-One-Out Cross-Validation...")

        for train_index, test_index in loo.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            accuracies.append(accuracy)

        avg_accuracy = np.mean(accuracies)
        logging.info(f"📊 {name} Accuracy (LOO-CV Avg): {avg_accuracy:.4f}")

        # Save best model
        if avg_accuracy > best_accuracy:
            best_accuracy = avg_accuracy
            best_model = model

    # Ensure model directory exists
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # Save the best model
    joblib.dump(best_model, MODEL_OUTPUT)
    logging.info(f"✅ Best model saved at {MODEL_OUTPUT}")

if __name__ == "__main__":
    train_model()
