import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from features import engineer_features

TEST_PATH = "../data/processed/test_mixed.csv"
MODEL_PATH = "../models/isolation_forest.pkl"

def evaluate():
    print("Loading test data...")
    df = pd.read_csv(TEST_PATH)
    df["label"] = df["label"].str.strip()

    y_true = df["label"]

    model, scaler, selected_cols = joblib.load(MODEL_PATH)

    X, _ = engineer_features(df)
    X = X[selected_cols]

    print("Scaling test data...")
    X_scaled = scaler.transform(X)

    print("Generating predictions...")
    preds = model.predict(X_scaled)

    y_pred = np.where(preds == 1, "BENIGN", "ATTACK")
    y_true_binary = np.where(y_true == "BENIGN", "BENIGN", "ATTACK")

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true_binary, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_true_binary, y_pred))

if __name__ == "__main__":
    evaluate()