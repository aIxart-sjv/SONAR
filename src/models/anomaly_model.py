from sklearn.ensemble import IsolationForest
import joblib


def train_anomaly_model(X):
    model = IsolationForest(
        n_estimators=100,
        contamination=0.005,  # % of anomalies expected
        random_state=42,
        n_jobs=-1
    )

    model.fit(X)
    joblib.dump(model, "models/anomaly_model.pkl")

    print("✅ Anomaly model saved")


def load_anomaly_model():
    return joblib.load("models/anomaly_model.pkl")