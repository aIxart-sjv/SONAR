import pandas as pd
import joblib
import sys
import numpy as np
from features import engineer_features

MODEL_PATH = "../models/isolation_forest.pkl"

def predict(file_path):
    model, scaler, selected_cols = joblib.load(MODEL_PATH)

    df = pd.read_csv(file_path)

    X, _ = engineer_features(df)
    X = X[selected_cols]

    X_scaled = scaler.transform(X)

    preds = model.predict(X_scaled)

    results = np.where(preds == 1, "BENIGN", "ATTACK")
    df["prediction"] = results

    print("\nPrediction Summary:")
    print(df["prediction"].value_counts())

    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <path_to_csv>")
        sys.exit(1)

    predict(sys.argv[1])