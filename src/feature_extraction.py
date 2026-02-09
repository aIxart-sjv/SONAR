import pandas as pd

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract relevant flow-level features for anomaly detection.
    """
    features = df[[
        "flow_duration",
        "packet_count",
        "byte_count",
        "protocol"
    ]].copy()

    return features