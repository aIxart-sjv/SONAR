import pandas as pd
from src.models.save_model import load_artifacts
from src.features.feature_config import FEATURE_COLUMNS
from src.models.anomaly_model import load_anomaly_model


class RealTimeDetector:
    def __init__(self):
        print("[*] Loading model artifacts...")
        self.model, self.scaler, self.encoder = load_artifacts()
        self.anomaly_model = load_anomaly_model()
        print("[✓] Model loaded successfully")

    def get_feature_order(self):
        """
        Exact feature order used during training (CICIDS format).
        """
        return FEATURE_COLUMNS

    def preprocess_input(self, data: dict) -> pd.DataFrame:
        """
        Convert incoming partial feature dict into full feature vector.
        Missing features are safely filled with 0.
        """

        df = pd.DataFrame([data])
        expected_features = self.get_feature_order()

        # Add missing features
        for col in expected_features:
            if col not in df.columns:
                df[col] = 0

        # Ensure correct order
        df = df[expected_features]

        return df

    def predict(self, data):
        import pandas as pd

        # Convert input to DataFrame
        df = pd.DataFrame([data])

        # Ensure correct feature order
        df = df[self.get_feature_order()]

        # Scale features
        X_scaled = self.scaler.transform(df)

        # 🔥 ML prediction
        pred = self.model.predict(X_scaled)
        label = self.encoder.inverse_transform(pred)[0]

        # 🔥 ANOMALY prediction (FIXED)
        score = self.anomaly_model.decision_function(X_scaled)[0]
        is_anomaly = score < -0.1
        
        return {
            "prediction": label,
            "anomaly": is_anomaly
        }