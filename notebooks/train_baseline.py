from src.data_pipeline.loader import load_dataset
from src.data_pipeline.preprocess import (
    clean_labels,
    clean_data,
    remove_rare_classes
)
from src.data_pipeline.prepare import (
    split_features_labels,
    encode_labels
)
from src.localization.attack_mapper import map_attack_context

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from src.models.save_model import save_artifacts

def main():
    print("\n[1] Loading dataset...")
    df = load_dataset("data/raw")

    print("[2] Cleaning labels...")
    df = clean_labels(df)

    print("[3] Cleaning data (NaN, Inf, duplicates)...")
    df = clean_data(df)

    print("[4] Removing rare classes...")
    df = remove_rare_classes(df)

    print("[5] Splitting features and labels...")
    X, y = split_features_labels(df)

    print("[6] Encoding labels...")
    y_encoded, encoder = encode_labels(y)

    print("[7] Train/Test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    print("[8] Scaling features (NO DATA LEAKAGE)...")
    scaler = StandardScaler()

    # IMPORTANT: Keep X_train/X_test as DataFrames until mapping
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("[9] Training model with custom class weights...")
    class_weight = {
        0: 1,   # Benign
        1: 5,   # Bot
        2: 2,   # Brute Force
        3: 2,   # DDoS
        4: 2,   # DoS
        5: 2,   # PortScan
        6: 3    # Web Attack
    }

    model = RandomForestClassifier(
        n_estimators=100,
        n_jobs=-1,
        random_state=42,
        class_weight=class_weight
    )

    model.fit(X_train_scaled, y_train)
    save_artifacts(model, scaler, encoder)

    print("[10] Evaluating model...")
    y_pred = model.predict(X_test_scaled)

    print("\n=== Classification Report ===\n")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_))

    print("\n[11] Generating attack insights...")
    
    # Use original (unscaled) X_test with indices preserved
    attack_insights = map_attack_context(X_test, y_pred, encoder)

    print("\n=== Sample Attack Insights ===\n")
    print(attack_insights.head(10))


if __name__ == "__main__":
    main()