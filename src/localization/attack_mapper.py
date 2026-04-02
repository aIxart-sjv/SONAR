import pandas as pd


# 🔥 EXISTING — KEEP THIS (for offline analysis / training)
def map_attack_context(df: pd.DataFrame, predictions, encoder) -> pd.DataFrame:
    """
    Batch mapping (USED ONLY IN TRAINING / NOTEBOOKS)
    """

    df = df.copy()
    df['Predicted_Label'] = encoder.inverse_transform(predictions)

    attacks = df[df['Predicted_Label'] != 'Benign']

    context_columns = [
        'Predicted_Label',
        'Destination Port',
        'Flow Duration',
        'Total Fwd Packets',
        'Total Backward Packets'
    ]

    context_columns = [col for col in context_columns if col in attacks.columns]

    return attacks[context_columns]


# 🔥 NEW — REALTIME MAPPER (THIS IS WHAT YOU USE IN ENGINE)
def map_realtime_context(features: dict, prediction: str) -> dict:
    port = features.get("Destination Port", 0)

    # 🔥 Service + Layer mapping
    if port == 80:
        service = "HTTP"
        layer = "L7 (Application)"
    elif port == 443:
        service = "HTTPS"
        layer = "L7 (Application)"
    elif port == 53:
        service = "DNS"
        layer = "L7 (Application)"
    elif port == 22:
        service = "SSH"
        layer = "L7 (Application)"
    elif port == 21:
        service = "FTP"
        layer = "L7 (Application)"
    else:
        service = "Unknown"
        layer = "L4 (Transport)"

    return {
        "attack": prediction,
        "service": service,
        "layer": layer
    }