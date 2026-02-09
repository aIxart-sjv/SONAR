import pandas as pd

def engineer_features(df):
    df = df.copy()
    df.columns = df.columns.str.strip()

    payload_cols = [col for col in df.columns if col.startswith("payload_byte_")]

    df["payload_mean"] = df[payload_cols].mean(axis=1)
    df["payload_std"] = df[payload_cols].std(axis=1)
    df["payload_max"] = df[payload_cols].max(axis=1)
    df["payload_min"] = df[payload_cols].min(axis=1)

    selected_cols = [
        "ttl",
        "total_len",
        "t_delta",
        "protocol",
        "payload_mean",
        "payload_std",
        "payload_max",
        "payload_min"
    ]

    X = df[selected_cols].copy()

    if X["protocol"].dtype == "object":
        X["protocol"] = X["protocol"].astype("category").cat.codes

    return X, selected_cols