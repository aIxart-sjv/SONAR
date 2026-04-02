import os
import joblib


def save_artifacts(model, scaler, encoder, path="models"):
    """
    Save trained model, scaler, and encoder to disk.
    """

    os.makedirs(path, exist_ok=True)

    joblib.dump(model, os.path.join(path, "model.pkl"))
    joblib.dump(scaler, os.path.join(path, "scaler.pkl"))
    joblib.dump(encoder, os.path.join(path, "encoder.pkl"))

    print(f"\n✅ Model artifacts saved in '{path}/'")


def load_artifacts(path="models"):
    """
    Load trained model, scaler, and encoder from disk.
    """

    model = joblib.load(os.path.join(path, "model.pkl"))
    scaler = joblib.load(os.path.join(path, "scaler.pkl"))
    encoder = joblib.load(os.path.join(path, "encoder.pkl"))

    return model, scaler, encoder