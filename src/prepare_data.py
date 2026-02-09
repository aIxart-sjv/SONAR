import pandas as pd
import os

RAW_PATH = "../data/raw/Payload_data_CICIDS2017.csv"
PROCESSED_DIR = "../data/processed"

def prepare_samples():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    df = pd.read_csv(RAW_PATH)
    df.columns = df.columns.str.strip()
    df["label"] = df["label"].str.strip()

    train_df = df[df["label"] == "BENIGN"].sample(50000, random_state=42)
    test_df = df.sample(50000, random_state=24)

    train_df.to_csv(f"{PROCESSED_DIR}/train_benign.csv", index=False)
    test_df.to_csv(f"{PROCESSED_DIR}/test_mixed.csv", index=False)

    print("Training and test datasets created.")

if __name__ == "__main__":
    prepare_samples()