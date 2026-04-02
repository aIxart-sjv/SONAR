import numpy as np
import pandas as pd


def clean_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix label encoding issues and normalize attack categories.
    """

    # Fix encoding issues
    df['Label'] = df['Label'].str.replace('ï¿½', '-', regex=False)

    # Normalize labels
    mapping = {
        'BENIGN': 'Benign',

        # DoS group
        'DoS Hulk': 'DoS',
        'DoS GoldenEye': 'DoS',
        'DoS slowloris': 'DoS',
        'DoS Slowhttptest': 'DoS',

        # DDoS
        'DDoS': 'DDoS',

        # Brute force
        'FTP-Patator': 'Brute Force',
        'SSH-Patator': 'Brute Force',

        # Port scanning
        'PortScan': 'PortScan',

        # Botnet
        'Bot': 'Bot',

        # Web attacks
        'Web Attack - Brute Force': 'Web Attack',
        'Web Attack - XSS': 'Web Attack',
        'Web Attack - Sql Injection': 'Web Attack',

        # Rare attacks → grouped
        'Infiltration': 'Other',
        'Heartbleed': 'Other'
    }

    df['Label'] = df['Label'].map(mapping)

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean numerical issues and remove bad data.
    """

    # Replace infinite values with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Drop rows with NaN
    df.dropna(inplace=True)

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    return df


def remove_rare_classes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove extremely small classes that break training.
    """

    df = df[df['Label'] != 'Other']

    return df