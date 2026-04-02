import pandas as pd


def map_attack_context(df: pd.DataFrame, predictions, encoder) -> pd.DataFrame:
    """
    Attach model predictions and extract meaningful attack context.

    Parameters:
    - df: Original feature DataFrame (must retain original indices)
    - predictions: Model predictions (encoded)
    - encoder: LabelEncoder used for decoding

    Returns:
    - DataFrame containing only attack-related insights
    """

    # Copy to avoid modifying original data
    df = df.copy()

    # Decode predictions back to labels
    df['Predicted_Label'] = encoder.inverse_transform(predictions)

    # Filter only attack traffic (exclude benign)
    attacks = df[df['Predicted_Label'] != 'Benign']

    # Select meaningful context features
    context_columns = [
        'Predicted_Label',
        'Destination Port',
        'Flow Duration',
        'Total Fwd Packets',
        'Total Backward Packets'
    ]

    # Some columns may not exist if dataset changes — safe filtering
    context_columns = [col for col in context_columns if col in attacks.columns]

    result = attacks[context_columns]

    return result