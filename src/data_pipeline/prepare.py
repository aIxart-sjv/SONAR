import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


def split_features_labels(df: pd.DataFrame):
    X = df.drop(columns=['Label'])
    y = df['Label']
    return X, y


def encode_labels(y):
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    return y_encoded, encoder


def scale_features(X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler