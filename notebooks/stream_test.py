from src.engine.realtime_detector import RealTimeDetector
from src.data_pipeline.loader import load_dataset
from src.data_pipeline.preprocess import clean_labels, clean_data, remove_rare_classes

import time
import random


def main():
    print("[*] Loading dataset...")

    # Load and prepare dataset
    df = load_dataset("data/raw")
    df = clean_labels(df)
    df = clean_data(df)
    df = remove_rare_classes(df)

    # Extract features only
    X = df.drop(columns=['Label'])

    # Initialize detector
    detector = RealTimeDetector()

    print("\n[🚀] Starting simulated real-time detection...\n")

    # 🔥 Random sampling for realistic traffic
    num_samples = 20
    indices = random.sample(range(len(X)), num_samples)

    for i, idx in enumerate(indices):
        row = X.iloc[idx].to_dict()

        result = detector.predict(row)

        print(f"[{i}] Prediction: {result['prediction']}")

        time.sleep(0.5)  # simulate real-time delay


if __name__ == "__main__":
    main()