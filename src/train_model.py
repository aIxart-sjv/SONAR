import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from features import engineer_features

TRAIN_PATH = "../data/processed/train_benign.csv"
MODEL_PATH = "../models/isolation_forest.pkl"

def train():
    print("Loading training data...")
    df = pd.read_csv(TRAIN_PATH)
    df["label"] = df["label"].str.strip()

    X, selected_cols = engineer_features(df)

    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Training Isolation Forest...")
    model = IsolationForest(
        n_estimators=200,
        contamination=0.30,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_scaled)

    os.makedirs("../models", exist_ok=True)
    joblib.dump((model, scaler, selected_cols), MODEL_PATH)

    print("Model trained and saved.")

if __name__ == "__main__":
    train()