import pandas as pd
import numpy as np
from src.models.save_model import load_artifacts


class RealTimeDetector:
    def __init__(self):
        print("[*] Loading model artifacts...")

        self.model, self.scaler, self.encoder = load_artifacts()

        print("[✓] Model loaded successfully")

    def preprocess_input(self, data: dict) -> pd.DataFrame:
        """
        Convert incoming data into DataFrame and match training format.
        """

        df = pd.DataFrame([data])

        # Ensure correct column order (VERY IMPORTANT)
        df = df[self.get_feature_order()]

        return df

    def get_feature_order(self):
        """
        Define feature order used during training.
        MUST match training dataset exactly.
        """

        return [
            'Destination Port', 'Flow Duration', 'Total Fwd Packets',
            'Total Backward Packets', 'Total Length of Fwd Packets',
            'Total Length of Bwd Packets', 'Fwd Packet Length Max',
            'Fwd Packet Length Min', 'Fwd Packet Length Mean',
            'Fwd Packet Length Std', 'Bwd Packet Length Max',
            'Bwd Packet Length Min', 'Bwd Packet Length Mean',
            'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s',
            'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
            'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max',
            'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std',
            'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags',
            'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length',
            'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
            'Min Packet Length', 'Max Packet Length', 'Packet Length Mean',
            'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count',
            'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count',
            'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count',
            'ECE Flag Count', 'Down/Up Ratio', 'Average Packet Size',
            'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
            'Fwd Header Length.1', 'Fwd Avg Bytes/Bulk',
            'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate',
            'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk',
            'Bwd Avg Bulk Rate', 'Subflow Fwd Packets',
            'Subflow Fwd Bytes', 'Subflow Bwd Packets',
            'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
            'Init_Win_bytes_backward', 'act_data_pkt_fwd',
            'min_seg_size_forward', 'Active Mean', 'Active Std',
            'Active Max', 'Active Min', 'Idle Mean', 'Idle Std',
            'Idle Max', 'Idle Min'
        ]

    def predict(self, data: dict):
        """
        Predict attack type from incoming flow data.
        """

        # Preprocess input
        df = self.preprocess_input(data)

        # Scale
        X_scaled = self.scaler.transform(df)

        # Predict
        pred = self.model.predict(X_scaled)

        # Decode label
        label = self.encoder.inverse_transform(pred)[0]

        return {
            "prediction": label
        }